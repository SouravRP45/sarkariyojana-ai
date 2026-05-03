import json
import os
from app.config import get_settings

settings = get_settings()

class DataLoader:
    def __init__(self):
        self.all_schemes = []
        self._load_all_schemes()

    def _load_all_schemes(self):
        self.all_schemes = []
        for filename in ["central_schemes.json", "state_schemes.json"]:
            filepath = os.path.join(settings.DATA_DIR, filename)
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.all_schemes.extend(data.get("schemes", []))
        print(f"Loaded {len(self.all_schemes)} schemes from JSON files.")

    def get_all_schemes(self):
        return self.all_schemes

    def get_scheme_by_id(self, scheme_id: str):
        for scheme in self.all_schemes:
            if scheme["id"] == scheme_id:
                return scheme
        return None

    def initialize_db(self):
        """No-op: ChromaDB/embeddings removed. Using direct JSON matching instead."""
        print(f"Using lightweight JSON-based matching. {len(self.all_schemes)} schemes loaded and ready.")

data_loader = DataLoader()
