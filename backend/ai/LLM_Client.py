"""
LLM Client – thin wrapper for OpenAI-compatible / Mistral APIs.
Enforces strict JSON output for pricing adjustments.
Falls back to base rates on any failure.
"""
from __future__ import annotations

import json
import logging
from typing import Any, Dict, Optional

import httpx

from config import settings

logger = logging.getLogger(__name__)

# Multiplier validity bounds
MULTIPLIER_MIN = 0.7
MULTIPLIER_MAX = 1.8

PRICING_SCHEMA_EXAMPLE = """{
  "city": "<city>",
  "multipliers": {
    "painting": 1.00,
    "flooring": 1.00,
    "mold_treatment": 1.00,
    "ceiling_repair": 1.00,
    "lighting_upgrade": 1.00,
    "crack_repair": 1.00
  },
  "notes": "brief note",
  "confidence": 0.85
}"""

PRICING_SYSTEM_PROMPT = (
    "You are a construction cost analyst. "
    "Respond with ONLY valid JSON. No markdown, no extra text. "
    f"Your output MUST match this schema exactly:\n{PRICING_SCHEMA_EXAMPLE}"
)


def _build_pricing_user_prompt(city: str, base_rates: Dict) -> str:
    rate_lines = "\n".join(
        f"  {k}: ${v['rate']:.2f} per sqft" for k, v in base_rates.items()
    )
    return (
        f"Adjust the following US national average renovation rates for the city of {city}. "
        f"Provide a cost multiplier (0.7–1.8) for each service reflecting local labor, "
        f"material costs, and demand.\n\nBase national rates:\n{rate_lines}\n\n"
        f"Respond ONLY with JSON."
    )


def _get_api_url() -> str:
    if settings.LLM_BASE_URL:
        return settings.LLM_BASE_URL.rstrip("/") + "/v1/chat/completions"
    provider_defaults = {
        "openai": "https://api.openai.com/v1/chat/completions",
        "mistral": "https://api.mistral.ai/v1/chat/completions",
    }
    return provider_defaults.get(settings.LLM_PROVIDER, "https://api.openai.com/v1/chat/completions")


def _call_llm(system: str, user: str) -> Optional[str]:
    if not settings.LLM_API_KEY:
        logger.warning("LLM_API_KEY not set, skipping LLM call.")
        return None

    headers = {
        "Authorization": f"Bearer {settings.LLM_API_KEY}",
        "Content-Type": "application/json",
    }
    payload: Dict[str, Any] = {
        "model": settings.LLM_MODEL,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "temperature": 0.1,
        "max_tokens": 400,
    }

    for attempt in range(2):  # 1 retry
        try:
            with httpx.Client(timeout=settings.LLM_TIMEOUT_SECONDS) as client:
                resp = client.post(_get_api_url(), json=payload, headers=headers)
                resp.raise_for_status()
                data = resp.json()
                return data["choices"][0]["message"]["content"]
        except Exception as exc:
            logger.warning("LLM call attempt %d failed: %s", attempt + 1, exc)

    return None


def _validate_multipliers(multipliers: Dict) -> Dict[str, float]:
    """Clamp and validate multipliers to allowed range."""
    valid = {}
    for k, v in multipliers.items():
        try:
            val = float(v)
            valid[k] = max(MULTIPLIER_MIN, min(MULTIPLIER_MAX, val))
        except (TypeError, ValueError):
            valid[k] = 1.0
    return valid


def get_city_price_multipliers(city: str, base_rates: Dict) -> Dict:
    """
    Ask LLM for city-specific price multipliers.
    Returns dict with keys: multipliers, notes, confidence, source.
    Falls back to multiplier=1.0 for all services if anything fails.
    """
    default = {
        "multipliers": {k: 1.0 for k in base_rates},
        "notes": "Using base national rates (LLM unavailable).",
        "confidence": 0.0,
        "source": "base",
    }

    raw = _call_llm(PRICING_SYSTEM_PROMPT, _build_pricing_user_prompt(city, base_rates))
    if not raw:
        return default

    try:
        parsed = json.loads(raw.strip())
        mults = parsed.get("multipliers", {})
        # Ensure all services have a multiplier
        final_mults = {}
        for k in base_rates:
            final_mults[k] = float(mults.get(k, 1.0))
        final_mults = _validate_multipliers(final_mults)

        confidence = float(parsed.get("confidence", 0.5))
        confidence = max(0.0, min(1.0, confidence))

        return {
            "multipliers": final_mults,
            "notes": str(parsed.get("notes", ""))[:300],
            "confidence": confidence,
            "source": "llm",
        }
    except Exception as exc:
        logger.error("LLM response parse failed: %s | raw: %s", exc, raw[:200])
        return default