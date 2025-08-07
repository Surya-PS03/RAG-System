
class LangchainWrapper:
    def __init__(self,llm_wrapper):
        self.llm_wrapper = llm_wrapper
    
    def __call__(self,input_text):
        return self.llm_wrapper(input_text)