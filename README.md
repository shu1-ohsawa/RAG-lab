# RAG-Lab (Retrieval-Augmented Generation Laboratory)

このリポジトリは、生成AI（LLM）を用いた「検索拡張生成（RAG）」の基本構造から、自律型エージェント（Agentic RAG）までの実装と実験を目的としたラボラトリです。

## このリポジトリについて
RAG技術を単なる「外部知識の検索」としてだけでなく、実装の切り替えが可能なモジュール形式で開発しています。

- **Simple RAG**: ユーザーの質問から関連ドキュメントを検索し、そのまま回答を生成する基本構成。
- **Agentic RAG**: LLMが検索クエリを自律的に最適化し、思考プロセスを経て回答する構成。
- **Future Work**: GraphRAG（知識グラフを用いたRAG）の実装を予定。



## インストールの仕方

本プロジェクトはパッケージマネージャーとして `uv` を使用しています。

1. **リポジトリのクローン**
    ```bash
    git clone [https://github.com/あなたのユーザー名/RAG-lab.git](https://github.com/あなたのユーザー名/RAG-lab.git)
    cd RAG-lab
    ```

    ```bash
    uv venv
    .venv\Scripts\activate
    uv pip install -r requirements.txt
    ```


## 設定ファイルの準備
config.yaml.example を config.yaml にコピーし、使用するモデル名（Gemma2等）やDBパスを自身の環境に合わせて書き換えてください。

## データの配置
data/ ディレクトリに、検索対象としたいテキストファイル（.txt）を配置してください。

## 実行例
main.py を実行すると対話型インターフェースが起動します。

```
python practice_rag/main.py
```


## 実行ログのイメージ
Agentic RAGモードの場合

```
Type your question here > RAGのメリットを教えて
[*] エージェントが思考中...
[*] 最適化されたクエリ: RAG メリット 特徴

A> RAG（検索拡張生成）の主なメリットは、外部の最新知識を参照することで
ハルシネーション（嘘）を抑え、正確な回答ができる点にあります...


[Sources]: sample_knowledge_01.txt
```