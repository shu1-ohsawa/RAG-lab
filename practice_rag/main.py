import os
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve()))

from lib.config_loader import load_config
from lib.vector_db import RAGDatabase
from lib.llm_wrapper import LLMWrapper
#from lib.engines.simple_rag import SimpleRAGEngine as SelectedEngine
#from lib.engines.agentic_rag import AgenticRAGEngine as SelectedEngine
from lib.engines.multi_agent_rag import MultiAgentRAGEngine as SelectedEngine


def main():
    config = load_config()
    db = RAGDatabase(config)
    llm = LLMWrapper(config)

    # エンジンの初期化（今はSimpleRAGを使用）
    engine = SelectedEngine(db, llm, config)

    print(f"=== RAG System Ready (Model: {config['llm']['model_name']}) ===")

    while True:
        user_input = input('\nType your question here (type "exit" to quit)> ')
        if user_input.lower() in ["exit", "quit", "end", "終了"]:
            break

        # エンジンに丸投げして、回答と参照元をもらう
        answer, sources = engine.run(user_input)

        print(f"\nAnswer > {answer}")
        print(f"\n[Sources]: {', '.join(set(sources))}")

if __name__ == "__main__":
    main()