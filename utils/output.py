from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from utils.Wrapper.TogetherWrapper import TogetherWrapper
from utils.Wrapper.langchainWrapper import LangchainWrapper
def responses(query_context_map):
    
    template = """You are an expert assistant designed to extract accurate, concise, and context-grounded answers from official documents like insurance policies, contracts, or legal agreements.

    For every query, use only the information present in the provided context to generate a reliable and factual response.
    
    Answer based on context: {context} and question/query: {question}

    Follow these rules:

    Do not guess or hallucinate any information that is not explicitly present in the context.

    If the query cannot be answered based on the given context, respond with: "The provided context does not contain enough information to answer this question."

    Justify your response using evidence or phrases from the context when applicable.

    Be clear and direct. Avoid unnecessary elaboration or repetition.

    The context you receive may vary per query — always assume that it is the only information available.

    Always aim for precision, factual consistency, and groundedness.

    Output response should be not more than two lines
    """
    prompt = ChatPromptTemplate.from_template(template)
    wrap = TogetherWrapper(model = "meta-llama/Llama-3.2-3B-Instruct-Turbo",temperature = 0)
    llm = LangchainWrapper(wrap)

    answers = []

    chain = (prompt| llm | StrOutputParser())
    for question,context in query_context_map.items():
        
        answers.append(chain.invoke({"question":question,"context":context}))
    
    return answers
