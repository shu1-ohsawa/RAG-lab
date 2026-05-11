"""_summary_
multi_agent_rag.py
"""

class MultiAgentRAGEngine:
    def __init__(self, db, llm, config):
        self.db = db
        self.llm = llm
        self.config = config
        self.max_retries = 2  # 最大やり直し回数

    def run(self, user_input):
        combined_context = self._get_context(user_input)
        feedback = "初回回答を作成してください。" # 初回のフィードバックを定義
        
        for i in range(self.max_retries):
            print(f"--- ターン {i+1} ---")
            
            # 1. 調査員のプロンプト作成（feedbackを渡す）
            r_prompt = self._build_researcher_prompt(combined_context, user_input, feedback)
            
            # 2. 調査員の回答生成
            full_response = self.llm.generate_answer("", "", r_prompt)
            print(f"[full_response]",full_response)
            
            # --- ここに「受け皿（ハーネス）」を組み込む ---
            if "Answer:" in full_response:
                # ReAct形式から最終回答を抽出
                parts = full_response.split("Answer:")
                answer = parts[1].strip()
                thought = parts[0].replace("Thought:", "").strip()
                print(f"[*] 調査員の思考: {thought}")
            else:
                # 形式が崩れた場合のフォールバック
                answer = full_response
            # ------------------------------------------

            # 3. 検閲官のチェック
            is_ok, feedback = self._critic_check(user_input, answer, combined_context)
            
            if is_ok:
                return answer, ["sample_knowledge_02.txt", "sample_knowledge_03.txt"]
                
        return answer, ["sample_knowledge_02.txt", "sample_knowledge_03.txt"]

    def _get_context(self, user_input):
        """
        ユーザーの入力に基づき、関連するナレッジ（資料）を取得して結合するメソッド。
        今は練習用として、特定のファイルを読み込む実装にた。
        """
        # 本来はここでベクトル検索などを行いますが、
        # 今回は簡易的に sample_knowledge_03.txt を読み込む設定にします
        # try:
        #     with open("sample_knowledge_03.txt", "r", encoding="utf-8") as f:
        #         content = f.read()
        #     return content
        # except FileNotFoundError:
        #     return "資料が見つかりませんでした。"
        contents = []
        for filename in ["sample_knowledge_02.txt", "sample_knowledge_03.txt"]:
            try:
                with open(filename, "r", encoding="utf-8") as f:
                    contents.append(f"--- {filename} ---\n{f.read()}")
            except FileNotFoundError:
                continue
        return "\n\n".join(contents)

    def _generate_search_query(self, user_input):
        # 以前作った Few-shot プロンプトを利用
        instruction = (
            "質問から検索用単語を抽出してください。\n"
            f"質問: {user_input}"
        )
        query = self.llm.generate_answer("", "", instruction)
        return query.strip().split('\n')[0]

    def _build_researcher_prompt(self, context, user_input, feedback=""):
        return f"""資料から具体的な事実のみを抽出する調査員として回答してください。

### 回答例（この形式に従ってください）
Thought: 資料02に帳票解析の記述がある。
Answer: レイアウト解析とは、PDF内の複雑な構造を認識し、Markdown形式で出力する技術です。特に、セルが結合された複雑な帳票の解析に強みがあります。

---
【前回のフィードバック】: {feedback}
【資料】:
{context}

【質問】: {user_input}

Thought: (どの資料のどの言葉を引用するか書いてください)
Answer: (資料にある一文をそのまま引用して答えてください)
"""

    def _critic_check(self, user_input, answer, context):
        """検閲官のプロンプトを、より軽量モデルに優しく修正"""
        prompt = f"""あなたは採点官です。回答を100点満点で採点してください。
            判定は必ず以下の形式で、1行目にスコアを書いてください。

            スコア: (0〜100の数値)
            理由: (1行)

            【判定対象の回答】: {answer}
            【資料】: {context}
            """
        result = self.llm.generate_answer("", "", prompt)
        
        # --- 「数値ハーネス」のパース処理 ---
        score = 0
        feedback = "解析エラー"
        
        try:
            # 「スコア:」の後の数字を探す
            for line in result.split('\n'):
                if "スコア:" in line:
                    score_str = line.split("スコア:")[1].strip()
                    # 数字以外が含まれている場合を考慮して抽出
                    import re
                    match = re.search(r'\d+', score_str)
                    if match:
                        score = int(match.group())
                if "理由:" in line:
                    feedback = line.split("理由:")[1].strip()
        except Exception as e:
            print(f"[*] スコア解析失敗: {e}")

        
        is_ok = score >= 60 # ロジックとしてのハーネス：特定の点数以上ならOKとみなす
        return is_ok, f"({score}点) {feedback}"