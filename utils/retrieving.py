from langchain.prompts import PromptTemplate
from langchain.retrievers import MultiQueryRetriever
from langchain_ollama import ChatOllama
from utils.Wrapper.TogetherWrapper import TogetherWrapper
from utils.Wrapper.langchainWrapper import LangchainWrapper
def retrieve(db,question):

    llm = TogetherWrapper(model = "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",temperature = 0.0)

    template = """
    You are a retrieval-focused assistant designed to help extract relevant information from formal documents such as insurance policies, contracts, and official correspondence.

    You will be given a user's question. Generate 3-4 formal document-style search queries to retrieve relevant content from such documents.

    Instructions:
    - Use terms likely to appear in official documents.
    - Avoid natural language or conversational phrases.
    - Only generate queries. Do not answer the question.

    Question: {question}
    Output:
    - ...
    """

    template = PromptTemplate(input_variables=["question"],template = template)
    retriever = MultiQueryRetriever.from_llm(llm = LangchainWrapper(llm),prompt = template,retriever=db.as_retriever())
    retrieved = retriever.invoke(question)
    return [doc.page_content for doc in retrieved] 