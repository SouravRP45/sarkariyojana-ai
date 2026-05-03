import json
import os
import chromadb
from sentence_transformers import SentenceTransformer
from app.config import get_settings

settings = get_settings()

class DataLoader:
    def __init__(self):
        from chromadb.config import Settings
        self.chroma_client = chromadb.PersistentClient(
            path=settings.CHROMA_PERSIST_DIR,
            settings=Settings(anonymized_telemetry=False)
        )
        self.collection = self.chroma_client.get_or_create_collection(
            name=settings.CHROMA_COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"}
        )
        self.embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL)
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
                    
    def get_all_schemes(self):
        return self.all_schemes

    def get_scheme_by_id(self, scheme_id: str):
        for scheme in self.all_schemes:
            if scheme["id"] == scheme_id:
                return scheme
        return None

    def initialize_db(self):
        """Populate ChromaDB if it's empty."""
        count = self.collection.count()
        if count > 0:
            print(f"ChromaDB already initialized with {count} chunks.")
            return

        print("Initializing ChromaDB with scheme data...")
        documents = []
        metadatas = []
        ids = []

        for scheme in self.all_schemes:
            # Chunk 1: General info
            chunk1 = f"Scheme Name: {scheme['name']} ({scheme.get('name_hi', '')}). Description: {scheme['description']} Benefits: {scheme['benefits']}"
            documents.append(chunk1)
            metadatas.append({"scheme_id": scheme["id"], "type": "info", "category": scheme["category"]})
            ids.append(f"{scheme['id']}_info")

            # Chunk 2: Eligibility
            eligibility_text = []
            e = scheme["eligibility"]
            if e.get("min_age"): eligibility_text.append(f"Minimum age: {e['min_age']}.")
            if e.get("max_age"): eligibility_text.append(f"Maximum age: {e['max_age']}.")
            if e.get("gender") and e["gender"] != "all": eligibility_text.append(f"Gender: {e['gender']} only.")
            if e.get("income_limit"): eligibility_text.append(f"Income limit: strictly below {e['income_limit']}.")
            if e.get("states") and e["states"] != ["all"]: eligibility_text.append(f"Applicable only in states: {', '.join(e['states'])}.")
            
            chunk2 = f"Scheme Name: {scheme['name']}. Eligibility criteria: {' '.join(eligibility_text)}"
            documents.append(chunk2)
            metadatas.append({"scheme_id": scheme["id"], "type": "eligibility", "category": scheme["category"]})
            ids.append(f"{scheme['id']}_eligibility")

            # Chunk 3: Application process
            chunk3 = f"Scheme Name: {scheme['name']}. How to apply: {scheme['application_process']} Required documents: {', '.join(scheme.get('documents_required', []))}."
            documents.append(chunk3)
            metadatas.append({"scheme_id": scheme["id"], "type": "application", "category": scheme["category"]})
            ids.append(f"{scheme['id']}_application")

        # Generate embeddings
        print(f"Generating embeddings for {len(documents)} chunks...")
        embeddings = self.embedding_model.encode(documents).tolist()

        # Add to Chroma
        batch_size = 100
        for i in range(0, len(documents), batch_size):
            self.collection.add(
                documents=documents[i:i+batch_size],
                embeddings=embeddings[i:i+batch_size],
                metadatas=metadatas[i:i+batch_size],
                ids=ids[i:i+batch_size]
            )
        print("Database initialization complete.")

data_loader = DataLoader()