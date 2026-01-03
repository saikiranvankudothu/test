# services/rag_service.py
from ai_engine.rag_engine import RAGEngine
from utils.logger import logger
from errors.exceptions import RAGIndexingError

class RAGService:
    def __init__(self):
        self.rag = RAGEngine()

    def index(self, doc_json: dict, doc_id: str):
        return self.rag.index_document(doc_json, doc_id)

    def get_context(self, question: str, k: int = 5) -> str:
        return self.rag.get_context_for_query(question, k)
    
    def index(self, doc_json: dict, doc_id: str):
        try:
            return self.rag.index_document(doc_json, doc_id)
        except Exception as e:
            logger.exception("RAG indexing failed")
            raise RAGIndexingError(str(e))
