from fastapi import HTTPException,FastAPI,Depends,status
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from pydantic import BaseModel
import requests
from typing import List
from dotenv import load_dotenv
import os

app = FastAPI()

load_dotenv()

bearer_token = os.getenv("BEARER_TOKEN")

http_scheme = HTTPBearer()

def authorize(token: HTTPAuthorizationCredentials = Depends(http_scheme)):
    if bearer_token != token.credentials:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
                            detail = "Unauthorize User",
                            headers={"WWW-Authenticate":"Bearer"})
    else:
        return bearer_token

class QueryRequest(BaseModel):
    documents: str
    questions: List[str]


@app.post("/hackrx/run")
def response(request: QueryRequest, token: str = Depends(authorize)):
    documents = request.documents
    try:
        resp = requests.get(documents)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Url is not working: str{e}")
    
    questions = request.questions

