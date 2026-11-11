"""
Lookup and Categorization Router (webddc)
Provides route handlers for code lookups and text categorization requests.
"""

from typing import Dict, Any
from src.classifier import DDCCategorizer

class DDCRouter:
    def __init__(self, categorizer: DDCCategorizer = None):
        self.categorizer = categorizer or DDCCategorizer()

    def handle_lookup(self, code: str) -> Dict[str, Any]:
        """Handles requests to lookup specific DDC codes."""
        info = self.categorizer.get_class_info(code)
        if not info:
            return {"error": f"Invalid or missing classification code: {code}"}, 400
        return {"status": "success", "data": info}, 200

    def handle_categorization(self, text: str) -> Dict[str, Any]:
        """Handles requests to categorize raw text inputs."""
        if not text or not text.strip():
            return {"error": "Query text cannot be empty."}, 400
        result = self.categorizer.categorize_text(text)
        return {"status": "success", "data": result}, 200
