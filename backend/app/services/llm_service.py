import google.generativeai as genai
from app.config import get_settings
import logging

settings = get_settings()
logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        # We read the key from settings (.env file)
        self.api_key = settings.GEMINI_API_KEY
        
        # Only configure if the key looks like a real API key (longer than 10 characters)
        if self.api_key and len(self.api_key) > 10:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(settings.LLM_MODEL)
        else:
            logger.warning("GEMINI_API_KEY is missing or invalid. LLM features will fail.")

    def generate(self, prompt: str, temperature: float = None) -> str:
        if not self.api_key or len(self.api_key) < 10:
            return "Please configure the Gemini API key in the backend/.env file to use chat features."
            
        temp = temperature if temperature is not None else settings.LLM_TEMPERATURE
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=temp,
                    max_output_tokens=settings.LLM_MAX_TOKENS,
                )
            )
            return response.text
        except Exception as e:
            logger.error(f"Error calling Gemini API: {str(e)}")
            return f"Sorry, I encountered an error while processing your request: {str(e)}. Please try again later."

llm_service = LLMService()
