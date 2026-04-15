import ollama

class LLMWrapper:
    def __init__(self, config):
        self.model_name = config["llm"]["model_name"]

    def generate_answer(self, template, context, user_input):
        # rag_system.txt 内の {context} と {query} に値を流し込む
        full_prompt = template.format(context=context, user_input=user_input)
        
        #デバッグ
        #print("DEBUG FULL PROMPT:", full_prompt) 

        response = ollama.generate(model=self.model_name, prompt=full_prompt)
        return response['response']