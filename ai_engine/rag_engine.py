# ai_engine/rag_engine.py
import uuid
from ai_engine.chunker import prepare_chunks_from_docling
from ai_engine.embedder import GTEEmbedder
from ai_engine.vector_store import ChromaStore

class RAGEngine:
    def __init__(self, embed_model_name="thenlper/gte-base", persist_dir="chroma_db"):
        self.embedder = GTEEmbedder(model_name=embed_model_name)
        self.store = ChromaStore(persist_dir=persist_dir)
        self.store.create_collection("docs")

    def index_document(self, doc_json: dict, doc_id: str = None):
        doc_id = doc_id or str(uuid.uuid4())
        chunks = prepare_chunks_from_docling(doc_json)
        texts = [c["text"] for c in chunks]
        ids = [f"{doc_id}_{i}" for i in range(len(texts))]
        embeddings = self.embedder.embed_texts(texts)
        metadatas = [{"source_doc": doc_id, "chunk_id": ids[i]} for i in range(len(ids))]
        self.store.add_documents(ids, texts, embeddings, metadatas)
        return {"doc_id": doc_id, "n_chunks": len(texts)}

    def retrieve(self, query: str, k: int = 5):
        # embed query
        q_embed = self.embedder.embed_texts([query])[0]
        res = self.store.query(q_embed, n_results=k)
        docs = []
        # chroma returns nested lists: documents, distances, ids
        for doc_text, dist, mid in zip(res.get("documents", [])[0], res.get("distances", [])[0], res.get("ids", [])[0]):
            docs.append({"text": doc_text, "distance": dist, "id": mid})
        return docs

    def get_context_for_query(self, query: str, k: int = 5) -> str:
        docs = self.retrieve(query, k=k)
        cleaned = []
        for d in docs:
            t = d["text"]
            if isinstance(t, str) and len(t) > 5:
                cleaned.append(t)
        return "\n\n".join(cleaned)
