# ============================================
# OWNER: Member 2 – Backend API (FastAPI)
# FILE: Application Configuration
# ============================================

import os
from typing import List
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv()


def _parse_allowed_hosts(raw_hosts: str) -> List[str]:
    """Parse ALLOWED_HOSTS entries and normalize URL-style values to hostnames."""
    normalized_hosts: List[str] = []

    for raw_host in raw_hosts.split(","):
        host = raw_host.strip()
        if not host:
            continue

        if host == "*":
            normalized_hosts.append("*")
            continue

        # Accept full URLs like https://api.example.com and extract the hostname.
        if host.startswith("http://") or host.startswith("https://"):
            parsed = urlparse(host)
            candidate = parsed.hostname or ""
        else:
            # If users add a path by mistake, keep only the authority segment.
            candidate = host.split("/")[0]

        candidate = candidate.strip().lower()
        if candidate:
            normalized_hosts.append(candidate)

    # De-duplicate while preserving order.
    seen = set()
    unique_hosts: List[str] = []
    for host in normalized_hosts:
        if host not in seen:
            unique_hosts.append(host)
            seen.add(host)

    return unique_hosts


class Settings:
    """Application settings loaded from environment variables."""

    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"
    
    # Server
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # Security - Allowed hosts for production
    ALLOWED_HOSTS: List[str] = _parse_allowed_hosts(os.getenv("ALLOWED_HOSTS", ""))
    
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
