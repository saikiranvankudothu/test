# services/document_service.py
import json
from ai_engine.docling_extractor import DoclingExtractor
from utils.logger import logger
from errors.exceptions import DocumentProcessingError


class DocumentService:
    def __init__(self):
        self.extractor = DoclingExtractor()

    def process_pdf(self, pdf_path: str) -> dict:
        """
        Returns:
            {
              text: str,
              json: dict
            }
        """
        try:
            result = self.extractor.extract(pdf_path)
        except Exception as e:
            logger.exception("Document extraction failed")
            raise DocumentProcessingError(str(e))


        with open(result["json_path"], "r", encoding="utf-8") as f:
            doc_json = json.load(f)

        return {
            "text": result["text"],
            "json": doc_json
        }
