"""
Modular Dewey Decimal Classification Engine (webddc)
Handles categorization and lookup across the 10 primary DDC classes.
"""

import json
import os
from typing import Dict, List, Optional

DEFAULT_MAIN_CLASSES = {
    "000": "Computer science, information & general works",
    "100": "Philosophy & psychology",
    "200": "Religion",
    "300": "Social sciences",
    "400": "Language",
    "500": "Science",
    "600": "Technology",
    "700": "Arts & recreation",
    "800": "Literature",
    "900": "History & geography"
}

class DDCCategorizer:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.main_classes = self._load_json("main_classes.json", DEFAULT_MAIN_CLASSES)
        self.relative_index = self._load_json("relative_index.json", {})

    def _load_json(self, filename: str, fallback: dict) -> dict:
        filepath = os.path.join(self.data_dir, filename)
        if os.path.exists(filepath):
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return fallback
        return fallback

    def get_class_info(self, code: str) -> Optional[Dict[str, str]]:
        """Lookup classification details by 3-digit code or prefix."""
        clean_code = code.strip()
        if len(clean_code) >= 3:
            prefix = clean_code[:3]
            main_key = f"{prefix[0]}00"
            return {
                "code": clean_code,
                "main_class": main_key,
                "discipline": self.main_classes.get(main_key, "Unknown Discipline")
            }
        return None

    def categorize_text(self, text: str) -> Dict[str, str]:
        """Categorizes input text based on keyword heuristics."""
        text_lower = text.lower()
        
        if any(w in text_lower for w in ["code", "python", "algorithm", "software", "computer", "data"]):
            code = "005"
        elif any(w in text_lower for w in ["mind", "philosophy", "psychology", "ethics", "think"]):
            code = "150"
        elif any(w in text_lower for w in ["religion", "god", "theology", "faith"]):
            code = "200"
        elif any(w in text_lower for w in ["society", "economics", "law", "politics", "government"]):
            code = "320"
        elif any(w in text_lower for w in ["language", "linguistics", "grammar", "english"]):
            code = "420"
        elif any(w in text_lower for w in ["science", "physics", "math", "biology", "chemistry"]):
            code = "500"
        elif any(w in text_lower for w in ["technology", "engineering", "medicine", "health", "construction"]):
            code = "600"
        elif any(w in text_lower for w in ["art", "music", "recreation", "sports", "painting"]):
            code = "700"
        elif any(w in text_lower for w in ["literature", "poetry", "drama", "novel", "prose"]):
            code = "810"
        else:
            code = "900"

        info = self.get_class_info(code)
        return {
            "query": text,
            "assigned_code": code,
            "discipline": info["discipline"] if info else "General Works",
            "main_class": info["main_class"] if info else "000"
        }
