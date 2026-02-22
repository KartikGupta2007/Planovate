# ============================================
# OWNER: Person 4 – Cache Layer
# ============================================

from __future__ import annotations

import json
import os
import time
from typing import Any

_CACHE: dict[str, dict[str, Any]] = {}
_LOADED = False

CACHE_FILE = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "data", "cache.json"
)


def _now() -> float:
    return time.time()


def _ensure_loaded() -> None:
    global _LOADED
    if _LOADED:
        return
    load()
    _LOADED = True


def load() -> None:
    """Load cache entries from disk if present."""
    if not os.path.exists(CACHE_FILE):
        return
    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as handle:
            raw = json.load(handle)
        if isinstance(raw, dict):
            for key, entry in raw.items():
                if not isinstance(entry, dict):
                    continue
                _CACHE[key] = entry
    except (OSError, json.JSONDecodeError):
        return


def flush() -> None:
    """Persist cache entries to disk."""
    os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
    try:
        with open(CACHE_FILE, "w", encoding="utf-8") as handle:
            json.dump(_CACHE, handle, indent=2)
    except OSError:
        return


def get(key: str) -> Any | None:
    _ensure_loaded()
    entry = _CACHE.get(key)
    if not entry:
        return None
    expires_at = entry.get("expires_at")
    if expires_at is not None and _now() > float(expires_at):
        _CACHE.pop(key, None)
        return None
    return entry.get("value")


def set(key: str, value: Any, ttl_seconds: int | None = None) -> None:
    _ensure_loaded()
    expires_at = None
    if ttl_seconds is not None:
        expires_at = _now() + ttl_seconds
    _CACHE[key] = {"value": value, "expires_at": expires_at}
