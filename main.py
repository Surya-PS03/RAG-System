from fastapi import HTTPException,FastAPI,Depends,status
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from pydantic import BaseModel
import requests
from typing import List
from dotenv import load_dotenv
import os
from urllib.parse import urlsplit
from utils import parsing,chunking,vectorizing,retrieving
app = FastAPI()

load_dotenv()

bearer_token = os.getenv("BEARER_TOKEN")

http_scheme = HTTPBearer()

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


@app.post("/hackrx/run")
def response(request: QueryRequest, token: str = Depends(authorize)):
    documents_url = request.documents
    root = "hackrx/files"
    os.makedirs(root,exist_ok = True)

    #sending get request to the document url
    try:
        resp = requests.get(documents_url)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Url is not working: {str(e)}")
    
    #extracting filename from url
    url_split = urlsplit(documents_url) 
    doc_path = url_split.path
    filename = os.path.basename(doc_path)

    #Creating a filepath and writing in it
    try:
        file_path = os.path.join(root,filename)

        with open(file_path,'wb') as f:
            f.write(resp.content)
    except:
        raise HTTPException(status_code=500,detail = "Can't extract the file content")

    questions = request.questions
    #RAG procedure
    parsed_doc = parsing.parser(file_path,filename)
    chunks = chunking.chunker(parsed_doc)
    db = vectorizing.vectorize(chunks)
    contexts = {question: retrieving.retrieve(db = db,question=question) for question in questions}
    return {"status": "success", "filename": filename,"context":contexts}



