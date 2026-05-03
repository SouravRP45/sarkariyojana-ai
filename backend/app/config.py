"""Application configuration using pydantic-settings."""
import os
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    APP_NAME: str = "SarkariYojana AI"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # LLM Configuration
    GEMINI_API_KEY: str = "AIzaSyB5QdNHTSScHBMgNDz3aU69P5evgskDfJk"
    LLM_MODEL: str = "gemini-2.0-flash"
    LLM_TEMPERATURE: float = 0.3
    LLM_MAX_TOKENS: int = 2048

    # Embedding Configuration
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"

    # ChromaDB Configuration
    CHROMA_PERSIST_DIR: str = "./chroma_db"
    CHROMA_COLLECTION_NAME: str = "government_schemes"

    # Data paths
    DATA_DIR: str = os.path.join(os.path.dirname(__file__), "data")

    # Frontend path
    FRONTEND_DIR: str = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
        "frontend"
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
