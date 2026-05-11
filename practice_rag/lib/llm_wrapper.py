"""_summary_
llm_wrapper.py

"""
import ollama

class LLMWrapper:
    def __init__(self, config):
        self.model_name = config["llm"]["model_name"]

    def generate_answer(self, template, context=None, user_input=None):
        # templateに中身があり、かつプレースホルダが含まれる場合のみformatを実行
        if template and ("{context}" in template or "{user_input}" in template):
            full_prompt = template.format(context=context or "", user_input=user_input or "")
        else:
            # そうでなければ、中身があるものをそのままプロンプトとして採用
            full_prompt = template or context or user_input or ""

        if not full_prompt:
            return "Error: Prompt is empty."

        # print("--- DEBUG: 最終的にOllamaに飛ぶプロンプト ---")
        # print(full_prompt)
        # print("---------------------------------------")

        response = ollama.generate(model=self.model_name, prompt=full_prompt)
        return response['response']