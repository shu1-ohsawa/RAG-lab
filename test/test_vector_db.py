import pytest
from lib.vector_db import RAGDatabase

@pytest.fixture
def db():
    """テストごとにDBインスタンスを生成するフィクスチャ"""
    config = {
        "database": {"path": "./test_db"},
        "llm": {"embed_model": "all-MiniLM-L6-v2"}
    }
    return RAGDatabase(config)

def test_split_text(db):
    text = "あいうえおかきくけこさしすせそ"
    chunks = db.split_text(text, chunk_size=5, overlap=2)
    
    assert chunks[0] == "あいうえお"
    assert chunks[1].startswith("えお")
    assert len(chunks) > 1

def test_upsert_and_query(db):
    test_text = "RAGのテストデータです。"
    db.upsert_data("test_id", test_text)
    
    results, metadatas = db.query("テスト", n_results=1)
    assert "RAG" in results[0]
    assert metadatas[0]['source'] == "test_id"