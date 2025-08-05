from langchain.prompts import PromptTemplate
from langchain.retrievers import MultiQueryRetriever
from langchain_ollama import ChatOllama

def retrieve(db,question):
    llm = ChatOllama(model = "mistral:7b-instruct-q4_K_M",temperature = 0)

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
    retriever = MultiQueryRetriever.from_llm(llm = llm,prompt = template,retriever=db.as_retriever())
    retrieved = retriever.invoke(question)
    return [doc.page_content for doc in retrieved]