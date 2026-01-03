# extensions.py
from services.document_service import DocumentService
from services.rag_service import RAGService
from services.llm_service import LLMService
from ai_engine.groq_llm import GroqClient


def init_services(app):
    """
    Initialize and wire all long-lived services to the Flask app.
    """

    # Create Groq client from validated app config
    groq_client = GroqClient(
        api_key=app.config["GROQ_API_KEY"],
        model=app.config["GROQ_MODEL"]
    )

    # Initialize services
    app.document_service = DocumentService()
    app.rag_service = RAGService()
    app.llm_service = LLMService(groq_client)
