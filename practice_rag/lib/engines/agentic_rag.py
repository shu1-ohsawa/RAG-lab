class AgenticRAGEngine:
    def __init__(self, db, llm, config):
        self.db = db
        self.llm = llm
        self.config = config

    def run(self, user_input):
        print(f"[*] エージェントが思考中...")
        
        optimized_query = self._generate_search_query(user_input)
        print(f"[*] 最適化されたクエリ: {optimized_query}")

        contexts, metadatas = self.db.query(optimized_query, n_results=3)

        if not contexts or not metadatas:
            return "すみません、関連する情報が見つかりませんでした。", []

        combined_context = "\n---\n".join(contexts)

        # ここで呼び出しているので、下の関数定義が有効である必要があります
        prompt = self._build_agent_prompt(combined_context, user_input)
        #answer = self.llm.generate_answer("", "", prompt)
        answer = self.llm.generate_answer(template="{user_input}", context="", user_input=prompt)

        sources = [meta['source'] for meta in metadatas if meta and 'source' in meta]
        return answer, sources

    def _generate_search_query(self, user_input):
        instruction = (
            "ユーザーの質問から、検索用の単語のみを抽出してください。\n\n"
            "質問: RAGのメリットは何？\n単語: RAG メリット 特徴\n\n"
            "質問: エージェントRAGとGraphRAGの違い\n単語: エージェントRAG GraphRAG 比較\n\n"
            f"質問: {user_input}\n単語:"
        )
        query = self.llm.generate_answer("", "", instruction)
        result = query.strip().split('\n')[0]
        
        if "provide" in result.lower() or not result:
            return user_input
        return result

    def _build_agent_prompt(self, context, user_input):
            """制約を少し緩め、回答のきっかけ（書き出し）を与えます"""
            return f"""あなたは親切なAIアシスタントです。
    提供された資料の内容を参考にして、ユーザーの質問に日本語で詳しく答えてください。

    【資料】
    {context}

    【ユーザーの質問】
    {user_input}

    【回答のヒント】
    資料に基づくと、"""