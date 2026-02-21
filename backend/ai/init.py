import json
import os
from functools import lru_cache
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
CONFIG_DIR = BASE_DIR / "config"
STORAGE_DIR = BASE_DIR / "storage"
STORAGE_DIR.mkdir(exist_ok=True)


@lru_cache(maxsize=1)
def get_weights() -> dict:
    with open(CONFIG_DIR / "weights.json") as f:
        return json.load(f)


@lru_cache(maxsize=1)
def get_base_rates() -> dict:
    with open(DATA_DIR / "base_rates.json") as f:
        return json.load(f)


@lru_cache(maxsize=1)
def get_materials_catalog() -> dict:
    with open(DATA_DIR / "materials_catalog.json") as f:
        return json.load(f)


@lru_cache(maxsize=1)
def get_steps_templates() -> dict:
    with open(DATA_DIR / "steps_templates.json") as f:
        return json.load(f)


class Settings:
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "openai")
    LLM_API_KEY: str = os.getenv("LLM_API_KEY", "")
    LLM_BASE_URL: str = os.getenv("LLM_BASE_URL", "")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "gpt-3.5-turbo")
    LLM_TIMEOUT_SECONDS: int = int(os.getenv("LLM_TIMEOUT_SECONDS", "15"))
    FRONTEND_ORIGIN: str = os.getenv("FRONTEND_ORIGIN", "*")
    PRICING_CACHE_PATH: Path = DATA_DIR / "pricing_cache.json"
    STORAGE_DIR: Path = STORAGE_DIR


settings = Settings()