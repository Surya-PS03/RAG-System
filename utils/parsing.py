from langchain_community.document_loaders import UnstructuredPDFLoader,UnstructuredWordDocumentLoader,UnstructuredEmailLoader
from fastapi import HTTPException,status
import asyncio

loader_map = {".pdf":UnstructuredPDFLoader,
              ".docx":UnstructuredWordDocumentLoader,
              ".eml":UnstructuredEmailLoader}
async def parser(file_path: str,filename: str):

    try:
        ext = '.' + filename.split('.')[-1]

        loader_cls = loader_map[ext]

        loader = loader_cls(file_path)

        try:
            docs = await asyncio.to_thread(loader.load)

            for doc in docs:
                doc.page_content = " ".join(doc.page_content.split())
            return docs
        except Exception as e:
            raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,detail = f"Cannot process the document {str(e)}")


    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail = f"Wrong file format {str(e)}")