import os,sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import HTTPException,FastAPI,Depends,status
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from pydantic import BaseModel
import requests
from typing import List
from dotenv import load_dotenv
from urllib.parse import urlsplit
import uvicorn
from utils import parsing,chunking,vectorizing,retrieving,output

load_dotenv()

bearer_token = os.getenv("BEARER_TOKEN")

http_scheme = HTTPBearer()

app = FastAPI()

#User authorization from bearer token
def authorize(token: HTTPAuthorizationCredentials = Depends(http_scheme)):
    if bearer_token != token.credentials:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
                            detail = "Unauthorized User",
                            headers={"WWW-Authenticate":"Bearer"})
    else:
        return bearer_token

#API model
class QueryRequest(BaseModel):
    documents: str
    questions: List[str]

def download_file_streaming(url, file_path):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

@app.post("/hackrx/run")
async def response(request: QueryRequest, token: str = Depends(authorize)):
    documents_url = request.documents
    root = "hackrx/files"
    os.makedirs(root,exist_ok = True)

    #extracting filename from url
    url_split = urlsplit(documents_url) 
    doc_path = url_split.path
    filename = os.path.basename(doc_path)



        #Creating a filepath and writing in it
    try:
        file_path = os.path.join(root,filename)
        download_file_streaming(documents_url,file_path)
    except:
        raise HTTPException(status_code=500,detail = "Can't extract the file content")

    questions = request.questions
    #RAG procedure
    parsed_doc = await parsing.parser(file_path,filename)
    chunks = chunking.chunker(parsed_doc)
    db = vectorizing.vectorize(chunks)
    contexts = {question: retrieving.retrieve(db = db,question=question) for question in questions}
    answers = output.responses(contexts)
    return {"answers":answers}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)




