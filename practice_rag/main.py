import os
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve()))

from lib.config_loader import load_config
from lib.vector_db import RAGDatabase
from lib.llm_wrapper import LLMWrapper
# from lib.engines.simple_rag import SimpleRAGEngine as SelectedEngine
from lib.engines.agentic_rag import AgenticRAGEngine as SelectedEngine


# from lib.config_loader import load_config
# from lib.vector_db import RAGDatabase
# from lib.llm_wrapper import LLMWrapper


# def main():
#     config = load_config()
#     db = RAGDatabase(config)
#     llm = LLMWrapper(config)
    
#     # contextファイル読み込み
#     with open(r'templates/rag_instruction.txt', "r", encoding="utf-8", errors="ignore") as f:
#         template = f.read()

#     # ---データの登録---
#     data_dir = Path("data")
#     if data_dir.exists():
#         for file_path in data_dir.glob("*.txt"):
#             print(f"Reading {file_path.name}...")
#             content = file_path.read_text(encoding="utf-8")
            
#             # ファイル名をIDにして登録
#             print({"source": file_path.name})
#             db.upsert_data(file_path.name, content, {"source": file_path.name})
#         print("Registration complete!")
#     else:
#         print("Data directory not found.")

#     # --- 質問の部分 ---
#     print("\nEnter your question")
#     while True:
#         user_input = input('\nType your question here (type "exit" to quit) > ')

#         if user_input.lower() in ["exit", "quit", "end", "終了"]:
#             print("Ending the session.")
#             break

#         if not user_input.strip():
#             continue

#         # クエリとしてDBへ問い合わせ
#         contexts, metadatas = db.query(user_input, n_results=3)  # 一旦ユーザーの入力をそのまま「クエリ」として使用

#         # プロンプトの組み立てと回答生成
#         with open(r'templates/rag_instruction.txt', "r", encoding="utf-8") as f:
#             template = f.read() 

#         print(f"--- {config['llm']['model_name']} is generating a response... ---")
#         # LLMには全コンテキストを結合して渡す TODO 評価してみて気に入らなければ要修正
#         combined_context = "\n---\n".join(contexts)
#         answer = llm.generate_answer(template, combined_context, user_input)
        
#         print(f"\nAnswer:\n{answer}")

#         print("\n[References]")
#         for meta in metadatas:
#             print(f"- {meta['source']}")




def main():
    config = load_config()
    db = RAGDatabase(config)
    llm = LLMWrapper(config)

    # エンジンの初期化（今はSimpleRAGを使用）
    engine = SelectedEngine(db, llm, config)

    print(f"=== RAG System Ready (Model: {config['llm']['model_name']}) ===")

    while True:
        user_input = input('\nType your question here (type "exit" to quit)> ')
        if user_input.lower() in ["exit", "quit", "終了"]:
            break

        # エンジンに丸投げして、回答と参照元をもらう
        answer, sources = engine.run(user_input)

        print(f"\nA> {answer}")
        print(f"\n[Sources]: {', '.join(set(sources))}")

if __name__ == "__main__":
    main()