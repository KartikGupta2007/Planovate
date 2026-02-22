# ============================================
# OWNER: Member 3 – AI / Computer Vision
# FILE: Damage Scoring & Priority Analysis
# ============================================

import numpy as np
from .feature_vector import FEATURE_NAMES

# Weights for each feature in the overall damage score.
# Must sum to 1.0.
FEATURE_WEIGHTS = {
    "cracks":   0.25,
    "paint":    0.20,
    "lighting": 0.15,
    "floor":    0.25,
    "ceiling":  0.15,
}

# Human-readable task labels for each feature
TASK_LABELS = {
    "cracks":   "Repair cracks and structural damage",
    "paint":    "Repaint walls and surfaces",
    "lighting": "Upgrade lighting fixtures",
    "floor":    "Repair or replace flooring",
    "ceiling":  "Fix ceiling issues",
}


def calculate_damage_score(difference_vector: list[float]) -> float:
    """
    Calculate weighted damage score from difference vector.
    Score = sum(weight_i * diff_i) for each feature, clamped to [0, 1].

    Args:
        difference_vector: list of 5 floats in [0.0, 1.0],
                           matching FEATURE_NAMES order.

    Returns:
        float between 0.0 (no damage) and 1.0 (severe damage)
    """
    score = sum(
        FEATURE_WEIGHTS[name] * difference_vector[i]
        for i, name in enumerate(FEATURE_NAMES)
    )
    return round(float(np.clip(score, 0.0, 1.0)), 4)


def get_damage_classification(score: float) -> str:
    """
    Classify damage score into a human-readable severity level.

    Args:
        score: float from calculate_damage_score()

    Returns:
        "Low" | "Medium" | "High"
    """
    if score <= 0.30:
        return "Low"
    if score <= 0.60:
        return "Medium"
    return "High"


def _determine_priority(feature: str, difference: float) -> str:
    """
    Determine priority based on both task type and severity.
    
    Priority Rules:
    - CRACKS: Always HIGH (structural integrity and safety)
    - CEILING: HIGH if diff > 0.3, MEDIUM otherwise (safety concern)
    - FLOOR: HIGH if diff > 0.5, MEDIUM if > 0.3, LOW otherwise
    - PAINT: MEDIUM if diff > 0.4, LOW otherwise (cosmetic)
    - LIGHTING: MEDIUM if diff > 0.5, LOW otherwise (functional upgrade)
    
    Args:
        feature: Feature name (cracks, paint, lighting, floor, ceiling)
        difference: Difference value [0.0, 1.0]
    
    Returns:
        "high" | "medium" | "low"
    """
    # Structural/Safety-critical tasks
    if feature == "cracks":
        # Cracks are always high priority (structural integrity)
        return "high"
    
    if feature == "ceiling":
        # Ceiling issues are safety concerns
        return "high" if difference > 0.3 else "medium"
    
    if feature == "floor":
        # Flooring is high-traffic, prioritize if significant damage
        if difference > 0.5:
            return "high"
        elif difference > 0.3:
            return "medium"
        else:
            return "low"
    
    # Functional tasks
    if feature == "lighting":
        # Lighting affects usability
        return "medium" if difference > 0.5 else "low"
    
    if feature == "paint":
        # Paint is mostly cosmetic, but important for appearance
        return "medium" if difference > 0.4 else "low"
    
    # Fallback to difference-based priority
    return "high" if difference > 0.6 else "medium" if difference > 0.3 else "low"


def get_priority_tasks(difference_vector: list[float]) -> list[dict]:
    """
    Determine renovation priorities from the difference vector.
    Filters out negligible differences and sorts by urgency.
    This output feeds directly into Member 4's cost estimation and optimizer.

    Args:
        difference_vector: list of 5 floats in [0.0, 1.0],
                           matching FEATURE_NAMES order.

    Returns:
        List of task dicts sorted by priority then difference descending:
        [
            {
                "feature":    str,
                "task":       str,   # human-readable label
                "difference": float, # how much improvement is needed
                "priority":   str,   # "high" | "medium" | "low"
                "weight":     float, # feature's importance weight
            },
            ...
        ]
        Only includes features with difference > 0.1 (meaningful gap).
    """
    tasks = []
    for i, name in enumerate(FEATURE_NAMES):
        diff = difference_vector[i]
        if diff <= 0.1:
            continue  # skip negligible differences

        priority = _determine_priority(name, diff)
        tasks.append(
            {
                "feature":    name,
                "task":       TASK_LABELS[name],
                "difference": round(float(diff), 4),
                "priority":   priority,
                "weight":     FEATURE_WEIGHTS[name],
            }
        )

    # Sort by priority (high > medium > low), then by difference
    priority_order = {"high": 0, "medium": 1, "low": 2}
    tasks.sort(key=lambda x: (priority_order.get(x["priority"], 3), -x["difference"]))
    return tasks


def get_full_score_report(difference_vector: list[float]) -> dict:
    """
    Convenience function that combines score + classification + tasks.
    Member 4 can call this as a single entry point for all scoring output.

    Args:
        difference_vector: list of 5 floats in [0.0, 1.0]

    Returns:
        {
            "damage_score":      float,
            "classification":    str,   ("Low" | "Medium" | "High")
            "priority_tasks":    list[dict],
        }
    """
    score = calculate_damage_score(difference_vector)
    return {
        "damage_score":   score,
        "classification": get_damage_classification(score),
        "priority_tasks": get_priority_tasks(difference_vector),
    }