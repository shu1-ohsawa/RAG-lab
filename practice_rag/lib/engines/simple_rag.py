"""
simple_rag.py

"""
from pathlib import Path

class SimpleRAGEngine:
    def __init__(self, db, llm, config):
        self.db = db
        self.llm = llm
        self.config = config
        # プロンプトテンプレートの読み込み
        template_path = Path("templates/rag_instruction.txt")
        self.template = template_path.read_text(encoding="utf-8")

    def run(self, user_input):
        # 1. クエリとしてDBへ問い合わせ
        # 複数ヒットさせるために n_results=3 程度に
        contexts, metadatas = self.db.query(user_input, n_results=3)

        # 2. ヒットしたチャンクを合体
        combined_context = "\n---\n".join(contexts)

        # 3. 回答生成
        answer = self.llm.generate_answer(self.template, combined_context, user_input)
        #print("[DEBUG]",answer,metadatas)
        sources = []
        if metadatas:
            sources = [meta['source'] for meta in metadatas if meta is not None]
        
        return answer, sources