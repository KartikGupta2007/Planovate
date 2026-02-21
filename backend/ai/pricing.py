"""
Pricing service – computes adjusted rates for a city.
LLM used ONLY for multiplier adjustment, not core cost calculations.
"""
from __future__ import annotations

import logging
from typing import Dict, List, Tuple

from config import get_base_rates
from services.cache import get_city_pricing, set_city_pricing
from services.llm_client import get_city_price_multipliers

logger = logging.getLogger(__name__)


def get_adjusted_rates(city: str) -> Tuple[List[Dict], str, str, str, float]:
    """
    Returns (rates_list, cache_status, source, notes, confidence)
    rates_list: list of {service, base_rate, multiplier, adjusted_rate, source}
    """
    base_rates = get_base_rates()

    # Try cache first
    cached, cache_status = get_city_pricing(city)
    if cached:
        logger.info("Cache hit for city=%s", city)
        return cached["rates"], cache_status, cached["source"], cached.get("notes", ""), cached.get("confidence", 1.0)

    # Get LLM multipliers (or fallback)
    llm_result = get_city_price_multipliers(city, base_rates)
    multipliers = llm_result["multipliers"]
    source = llm_result["source"]
    notes = llm_result["notes"]
    confidence = llm_result["confidence"]

    rates_list = []
    for service_key, info in base_rates.items():
        base_rate = info["rate"]
        mult = multipliers.get(service_key, 1.0)
        adjusted = round(base_rate * mult, 2)
        rates_list.append(
            {
                "service": service_key,
                "base_rate": base_rate,
                "multiplier": mult,
                "adjusted_rate": adjusted,
                "source": source,
            }
        )

    payload = {
        "rates": rates_list,
        "source": source,
        "notes": notes,
        "confidence": confidence,
    }
    set_city_pricing(city, payload)

    return rates_list, cache_status, source, notes, confidence


def estimate_task_cost(service_key: str, area_sqft: float, adjusted_rates: List[Dict]) -> float:
    """Return estimated cost for a task given area and adjusted rates."""
    rate_map = {r["service"]: r["adjusted_rate"] for r in adjusted_rates}
    rate = rate_map.get(service_key, 0.0)
    return round(rate * area_sqft, 2)


def estimate_total_cost(tasks: List[Dict], area_sqft: float, adjusted_rates: List[Dict]) -> float:
    return round(sum(estimate_task_cost(t["service_key"], area_sqft, adjusted_rates) for t in tasks), 2)