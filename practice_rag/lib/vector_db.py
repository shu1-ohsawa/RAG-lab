import chromadb
from sentence_transformers import SentenceTransformer

class RAGDatabase:
    def __init__(self, config):
        self.embed_model = SentenceTransformer(config["embedding"]["model_name"])
        self.client = chromadb.PersistentClient(path=config["paths"]["db_path"])
        self.collection = self.client.get_or_create_collection(name="my_rag_collection")

    def upsert_data(self, doc_id, text, metadata):
        embedding = self.embed_model.encode(text).tolist()
        # 何のファイルを参照にしたか追跡できるよう、metadataに {"source": "sample_knowledge_03.txt"} などを入れる
        self.collection.upsert(
            documents=[text], 
            ids=[doc_id], 
            embeddings=[embedding],
            metadatas=[metadata] 
        )

    def query(self, question, n_results=2): # 念のため2〜3件取るように修正
        query_embedding = self.embed_model.encode(question).tolist()
        results = self.collection.query(query_embeddings=[query_embedding], n_results=n_results)
        
        return results['documents'][0], results['metadatas'][0] # 本文とメタデータをセットで返すように変更

    def split_text(self, text, chunk_size=300, overlap=50):
        """文章を一定の長さで分割する(overlapを導入して文脈が切れにくくする)"""
        chunks = []
        for i in range(0, len(text), chunk_size - overlap):
            chunk = text[i:i + chunk_size]
            chunks.append(chunk)
        return chunks

    # def upsert_data(self, file_name, text):
        
    #     chunks = self.split_text(text) # チャンクに分割
        
    #     # 各チャンクを登録
    #     documents = []
    #     metadatas = []
    #     ids = []
        
    #     for i, chunk in enumerate(chunks):
    #         documents.append(chunk)
    #         metadatas.append({"source": file_name, "chunk_no": i})
    #         ids.append(f"{file_name}_{i}")
        
    #     # まとめて登録（embeddingはChromaDB側で自動化していない場合はここで行う）
    #     embeddings = [self.embed_model.encode(c).tolist() for c in documents]
    #     self.collection.upsert(
    #         documents=documents,
    #         metadatas=metadatas,
    #         ids=ids,
    #         embeddings=embeddings
    #     )