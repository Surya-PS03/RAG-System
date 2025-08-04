from langchain_community.document_loaders import UnstructuredPDFLoader,UnstructuredWordDocumentLoader,UnstructuredEmailLoader
from fastapi import HTTPException,status
def parser(file_path: str,filename: str):

    if filename.endswith(".pdf"):
        loader = UnstructuredPDFLoader(file_path)
    elif filename.endswith(".docx"):
        loader = UnstructuredWordDocumentLoader(file_path)
    elif filename.endswith(".eml"):
        loader = UnstructuredEmailLoader(file_path)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail = "Wrong file format")
    try:
        parsed_doc = loader.load()
        return parsed_doc
    except Exception as e:
        raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, detail = f"Cannot load the document: {str(e)}")