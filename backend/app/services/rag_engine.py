from app.services.data_loader import data_loader
from app.services.llm_service import llm_service
from app.models import UserProfile
import json

class RAGEngine:
    def __init__(self):
        pass  # No heavy models needed - uses Gemini directly with keyword matching

    def retrieve(self, query: str, user_profile: UserProfile = None, top_k: int = 8) -> list[str]:
        """Lightweight retrieval: filter schemes by state and keyword matching."""
        all_schemes = data_loader.get_all_schemes()
        query_lower = query.lower()

        scored = []
        for scheme in all_schemes:
            score = 0
            # State match bonus
            if user_profile:
                states = scheme.get("eligibility", {}).get("states", ["all"])
                if "all" in states or user_profile.state in states:
                    score += 3
            # Keyword match in name/description/benefits/category
            text = f"{scheme.get('name','')} {scheme.get('description','')} {scheme.get('benefits','')} {scheme.get('category','')}".lower()
            for word in query_lower.split():
                if len(word) > 3 and word in text:
                    score += 1
            if score > 0:
                scored.append((score, scheme))

        scored.sort(key=lambda x: x[0], reverse=True)
        top_schemes = [s for _, s in scored[:top_k]]

        chunks = []
        for s in top_schemes:
            chunk = (
                f"Scheme: {s['name']} | Ministry: {s.get('ministry','N/A')} | "
                f"Benefits: {s.get('benefits','N/A')} | "
                f"Eligibility: Age {s.get('eligibility',{}).get('min_age','any')}-{s.get('eligibility',{}).get('max_age','any')}, "
                f"States: {', '.join(s.get('eligibility',{}).get('states',['All India']))} | "
                f"Apply: {s.get('application_process','N/A')} | "
                f"URL: {s.get('official_url','N/A')} | Helpline: {s.get('helpline','N/A')}"
            )
            chunks.append(chunk)
        return chunks

    def generate_response(self, user_query: str, user_profile: UserProfile = None, chat_history: list = None) -> str:
        retrieved_chunks = self.retrieve(user_query, user_profile=user_profile, top_k=8)
        context = "\n".join(retrieved_chunks) if retrieved_chunks else "No specific schemes found for this query."

        profile_str = ""
        if user_profile:
            profile_str = json.dumps(user_profile.model_dump(exclude_none=True), indent=2)

        history_str = ""
        if chat_history:
            history_str = "Chat History:\n"
            for msg in chat_history[-4:]:
                history_str += f"{msg['role']}: {msg['content']}\n"

        system_prompt = f"""You are SarkariYojana AI, a friendly assistant helping Indian citizens find government welfare schemes.

RULES:
1. Be warm, respectful, and empathetic.
2. If the user asks in Hindi, respond in Hindi (Devanagari script). Otherwise use simple English.
3. ONLY reference schemes from the provided context. Never hallucinate scheme names or benefits.
4. When recommending schemes, mention: name, benefits, eligibility, how to apply, required documents.
5. If unsure, say: "Please visit your nearest Common Service Centre (CSC) or call the scheme helpline."
6. Provide helpline numbers and official URLs when available.
7. Never ask for sensitive personal info like Aadhaar number or bank details.

USER PROFILE:
{profile_str if profile_str else "No profile provided."}

RELEVANT SCHEME INFORMATION:
{context}

{history_str}

USER QUESTION: {user_query}
"""
        return llm_service.generate(system_prompt)

rag_engine = RAGEngine()
