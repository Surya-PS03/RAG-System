from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from fastapi import HTTPException,status

def vectorize(chunks):
    embedding_model = HuggingFaceEmbeddings(model_name = "sentence-transformers/all-MiniLM-L6-v2",model_kwargs = {'device':'cpu'},encode_kwargs = {'batch_size':32})
    try:
        db = FAISS.from_documents(documents=chunks,embedding = embedding_model)
        return db
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail = f"Database issue: {str(e)}")
    
