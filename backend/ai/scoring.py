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


def get_priority_tasks(difference_vector: list[float]) -> list[dict]:
    """
    Determine renovation priorities from the difference vector.
    Filters out negligible differences and sorts by urgency.
    This output feeds directly into Member 4's cost estimation and optimizer.

    Args:
        difference_vector: list of 5 floats in [0.0, 1.0],
                           matching FEATURE_NAMES order.

    Returns:
        List of task dicts sorted by difference descending:
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

        priority = "high" if diff > 0.6 else "medium" if diff > 0.3 else "low"
        tasks.append(
            {
                "feature":    name,
                "task":       TASK_LABELS[name],
                "difference": round(float(diff), 4),
                "priority":   priority,
                "weight":     FEATURE_WEIGHTS[name],
            }
        )

    tasks.sort(key=lambda x: x["difference"], reverse=True)
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