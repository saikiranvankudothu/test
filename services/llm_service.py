# services/llm_service.py
from errors.exceptions import LLMServiceError
from utils.logger import logger

class LLMService:
    def __init__(self, groq_client):
        self.client = groq_client

    def answer_question(self, context: str, question: str) -> str:
        prompt = f"""
You are a Document QA Assistant. Use ONLY the context provided.

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
"""
        try:
            return self.client.complete(
                prompt=prompt,
                max_tokens=300,
                temperature=0.1
            )
        except Exception as e:
            logger.exception("LLM QA generation failed")
            raise LLMServiceError(str(e))

    def summarize(self, text: str) -> str:
        prompt = f"""
Summarize the following document into clear bullet points.
Keep it concise. No hallucinations.

TEXT:
{text}

SUMMARY:
"""
        try:
            return self.client.complete(
                prompt=prompt,
                max_tokens=400,
                temperature=0.2
            )
        except Exception as e:
            logger.exception("LLM summarization failed")
            raise LLMServiceError(str(e))

    def generate_mindmap(self, text: str) -> str:
        prompt = f"""
You MUST generate a valid Mermaid mindmap using Mermaid v11 syntax.

RULES:
- NO colons
- NO backticks
- NO quotes
- NO code fences
- Use ONLY this structure:
    mindmap
    Root
        Topic
            Subtopic

Text to convert:
{text}

Output ONLY the Mermaid mindmap code.
"""
        try:
            return self.client.complete(
                prompt=prompt,
                max_tokens=800,
                temperature=0.2
            )
        except Exception as e:
            logger.exception("LLM mindmap generation failed")
            raise LLMServiceError(str(e))
