# ============================================
# OWNER: Member 2 – Backend API (FastAPI)
# FILE: Application Configuration
# ============================================

import os
from typing import List
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""

    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"
    
    # Server
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # Security - Allowed hosts for production
    ALLOWED_HOSTS: List[str] = [
        host.strip() 
        for host in os.getenv("ALLOWED_HOSTS", "").split(",") 
        if host.strip()
    ]
    
    # CORS - Allowed origins
    ALLOWED_ORIGINS: List[str] = [
        origin.strip() 
        for origin in os.getenv(
            "ALLOWED_ORIGINS", 
            "http://localhost:5173,http://localhost:5174,http://localhost:3000"
        ).split(",")
        if origin.strip()
    ]

    # LLM Configuration
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "")
    LLM_TIMEOUT: int = int(os.getenv("LLM_TIMEOUT", "12"))
    
    # Gemini
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
    
    # OpenAI
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    
    # Ollama
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama3.1")

    # File upload limits
    MAX_IMAGE_SIZE_MB: int = int(os.getenv("MAX_IMAGE_SIZE_MB", "10"))
    MAX_IMAGE_SIZE_BYTES: int = MAX_IMAGE_SIZE_MB * 1024 * 1024
    
    # Request timeouts
    REQUEST_TIMEOUT: int = int(os.getenv("REQUEST_TIMEOUT", "30"))
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO" if not DEBUG else "DEBUG")
    
    @property
    def is_production(self) -> bool:
        """Check if running in production mode."""
        return self.ENVIRONMENT == "production" or not self.DEBUG


settings = Settings()
