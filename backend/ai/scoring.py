"""
Scoring Engine – deterministic DV computation, damage scoring,
classification, and priority ranking.
NO LLM usage here.
"""
from __future__ import annotations

from typing import Dict, List, Tuple

from config import get_weights


# ---------------------------------------------------------------------------
# Delta Vector
# ---------------------------------------------------------------------------


def compute_delta_vector(
    current: Dict[str, float], ideal: Dict[str, float]
) -> Dict[str, float]:
    """DV = abs(IV - CV) per component, clamped to [0,1]."""
    return {
        k: float(min(1.0, max(0.0, abs(ideal[k] - current[k]))))
        for k in current
    }


# ---------------------------------------------------------------------------
# Damage Score
# ---------------------------------------------------------------------------


def compute_damage_score(delta: Dict[str, float]) -> float:
    """Weighted sum of DV components using config weights."""
    weights = get_weights()["feature_weights"]
    score = sum(delta[k] * weights[k] for k in delta)
    return round(float(min(1.0, max(0.0, score))), 4)


# ---------------------------------------------------------------------------
# Classification
# ---------------------------------------------------------------------------


def classify_damage(score: float) -> str:
    thresholds = get_weights()["classification_thresholds"]
    if score <= thresholds["low"]:
        return "Low"
    if score <= thresholds["medium"]:
        return "Medium"
    return "High"


# ---------------------------------------------------------------------------
# Priority Ranking
# ---------------------------------------------------------------------------

# Map DV component key → (task name, service key)
TASK_META: Dict[str, Tuple[str, str]] = {
    "crack": ("Crack Repair", "crack_repair"),
    "paint": ("Interior Painting", "painting"),
    "mold": ("Mold Treatment", "mold_treatment"),
    "lighting": ("Lighting Upgrade", "lighting_upgrade"),
    "floor": ("Flooring Replacement", "flooring"),
    "ceiling": ("Ceiling Repair", "ceiling_repair"),
}


def rank_tasks(delta: Dict[str, float]) -> List[Dict]:
    """
    Rank tasks by: dv_component * weight * safety_modifier
    Returns list sorted by impact_score desc.
    """
    cfg = get_weights()
    weights = cfg["feature_weights"]
    safety = cfg["safety_modifiers"]

    scored = []
    for feature, dv_val in delta.items():
        if dv_val < 0.01:
            continue  # skip effectively-zero deltas
        task_name, service_key = TASK_META[feature]
        impact = dv_val * weights[feature] * safety[feature]
        scored.append(
            {
                "feature": feature,
                "name": task_name,
                "service_key": service_key,
                "dv_component": round(dv_val, 4),
                "impact_score": round(impact, 4),
            }
        )

    scored.sort(key=lambda x: x["impact_score"], reverse=True)
    for rank, item in enumerate(scored, start=1):
        item["priority"] = rank
        item["id"] = f"task_{item['service_key']}"

    return scored