from app.services.data_loader import data_loader
from app.services.llm_service import llm_service
from app.models import UserProfile
import json

class RAGEngine:
    def __init__(self):
        self.collection = data_loader.collection
        self.embedding_model = data_loader.embedding_model

    def retrieve(self, query: str, top_k: int = 5) -> list[str]:
        query_embedding = self.embedding_model.encode(query).tolist()
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        
        if not results['documents'] or not results['documents'][0]:
            return []
            
        return results['documents'][0]

    def generate_response(self, user_query: str, user_profile: UserProfile = None, chat_history: list = None) -> str:
        # Retrieve context
        retrieved_chunks = self.retrieve(user_query, top_k=6)
        context = "\n".join(retrieved_chunks)

        profile_str = ""
        if user_profile:
            profile_dict = user_profile.model_dump(exclude_none=True)
            profile_str = json.dumps(profile_dict, indent=2)

        history_str = ""
        if chat_history:
            history_str = "Chat History:\n"
            for msg in chat_history[-4:]: # Keep last 4 messages
                history_str += f"{msg['role']}: {msg['content']}\n"

        system_prompt = f"""You are SarkariYojana AI, a friendly and knowledgeable assistant that helps Indian citizens discover and apply for government welfare schemes.

RULES:
1. Always be warm, respectful, and empathetic. Many users may be from rural areas or have limited digital literacy.
2. If the user's preferred language is Hindi or the user asks in Hindi, respond entirely in Hindi (Devanagari script). If English, use simple English.
3. ONLY reference schemes from the provided context. NEVER make up or hallucinate scheme names, benefits, or eligibility criteria.
4. When recommending schemes, always mention:
   - Scheme name
   - Key benefits
   - Basic eligibility match reasons
   - How to apply (simplified steps)
   - Required documents
5. If you don't know something or the information isn't in your context, say: "I don't have this information in my database. Please visit your nearest Common Service Centre (CSC) or call the scheme's helpline for accurate details."
6. Be proactive — if a user qualifies for related schemes they haven't asked about, mention them.
7. Provide helpline numbers and official URLs when available.
8. Never ask for sensitive personal information like Aadhaar number, bank details, or passwords.

USER PROFILE:
{profile_str if profile_str else "No profile provided."}

RELEVANT SCHEME INFORMATION:
{context}

{history_str}

USER QUESTION: {user_query}
"""
        return llm_service.generate(system_prompt)

rag_engine = RAGEngine()
