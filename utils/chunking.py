from langchain_text_splitters import RecursiveCharacterTextSplitter
from fastapi import HTTPException,status

def chunker(parsed_doc):

    try:
        splitter = RecursiveCharacterTextSplitter(chunk_size = 400,chunk_overlap = 50)
        chunks = splitter.split_documents(parsed_doc)
        return chunks
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail = f"Cannot split document into valid chunks: {str(e)}")
    
    