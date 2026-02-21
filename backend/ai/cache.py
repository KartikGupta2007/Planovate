"""
Pricing cache: in-memory dict + persisted JSON.
Thread-safe for single-instance deployment.
"""
from __future__ import annotations

import json
import logging
import threading
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

from config import settings, get_weights

logger = logging.getLogger(__name__)

_lock = threading.Lock()
_memory_cache: Dict[str, Any] = {}


def _ttl_days() -> int:
    return get_weights().get("pricing_cache_ttl_days", 7)


def _cache_path() -> Path:
    return settings.PRICING_CACHE_PATH


def load_cache() -> Dict[str, Any]:
    """Load persisted cache from JSON file into memory."""
    global _memory_cache
    path = _cache_path()
    if path.exists():
        try:
            with open(path) as f:
                data = json.load(f)
            with _lock:
                _memory_cache = data
            logger.info("Loaded pricing cache from %s (%d entries)", path, len(data))
        except Exception as exc:
            logger.warning("Failed to load pricing cache: %s", exc)
            _memory_cache = {}
    return _memory_cache


def save_cache() -> None:
    """Persist in-memory cache to JSON file."""
    path = _cache_path()
    try:
        with _lock:
            data = dict(_memory_cache)
        with open(path, "w") as f:
            json.dump(data, f, indent=2, default=str)
    except Exception as exc:
        logger.error("Failed to save pricing cache: %s", exc)


def _is_expired(entry: Dict) -> bool:
    expires_str = entry.get("expires")
    if not expires_str:
        return True
    try:
        expires = datetime.fromisoformat(expires_str)
        return datetime.utcnow() > expires
    except Exception:
        return True


def get_city_pricing(city: str) -> Tuple[Optional[Dict], str]:
    """
    Returns (data, cache_status) where cache_status is 'hit', 'miss', or 'expired'.
    """
    key = city.lower()
    with _lock:
        entry = _memory_cache.get(key)
    if entry is None:
        return None, "miss"
    if _is_expired(entry):
        return None, "expired"
    return entry["data"], "hit"


def set_city_pricing(city: str, data: Dict) -> None:
    """Store pricing data for city with TTL."""
    key = city.lower()
    expires = (datetime.utcnow() + timedelta(days=_ttl_days())).isoformat()
    entry = {"data": data, "expires": expires}
    with _lock:
        _memory_cache[key] = entry
    save_cache()
    logger.info("Cached pricing for city=%s, expires=%s", city, expires)