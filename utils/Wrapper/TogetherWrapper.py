from together import Together
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("TOGETHER_API_KEY")

class TogetherWrapper:

    def __init__(self,model = "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",temperature = 0.0):
        self.client = Together(api_key = api_key)
        self.model = model
        self.temperature = temperature
    
    def __call__(self,input_text):

        try:
            input_text = input_text.to_string()
        except AttributeError:
            pass
        messages = [{"role":"user","content":input_text}]

        response = self.client.chat.completions.create(
            messages = messages,
            model = self.model,
            temperature = self.temperature
        )
        return response.choices[0].message.content