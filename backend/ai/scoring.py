# ============================================
# OWNER: Member 3 – AI / Computer Vision
# FILE: Damage Scoring & Priority Analysis
# ============================================

import numpy as np
from .feature_vector import FEATURE_NAMES

# Weights for each feature in overall score calculation
FEATURE_WEIGHTS = {
    "cracks": 0.25,
    "paint": 0.20,
    "lighting": 0.15,
    "floor": 0.25,
    "ceiling": 0.15,
}


def calculate_damage_score(difference_vector: list[float]) -> float:
    """
    Calculate weighted damage score from difference vector.
    Score = sum(weight_i * diff_i) for each feature.
    Returns: float between 0.0 and 1.0.
    """
    score = 0.0
    for i, name in enumerate(FEATURE_NAMES):
        score += FEATURE_WEIGHTS[name] * difference_vector[i]
    return round(min(score, 1.0), 4)


def get_priority_tasks(difference_vector: list[float]) -> list[dict]:
    """
    Determine renovation priorities based on difference vector.
    Returns sorted list of tasks by priority (highest difference first).

    This output feeds into Member 4's cost estimation and optimization.
    """
    tasks = []
    task_labels = {
        "cracks": "Repair cracks and structural damage",
        "paint": "Repaint walls and surfaces",
        "lighting": "Upgrade lighting fixtures",
        "floor": "Repair or replace flooring",
        "ceiling": "Fix ceiling issues",
    }

    for i, name in enumerate(FEATURE_NAMES):
        diff = difference_vector[i]
        if diff > 0.1:  # Only include tasks with meaningful differences
            priority = "high" if diff > 0.6 else "medium" if diff > 0.3 else "low"
            tasks.append(
                {
                    "feature": name,
                    "task": task_labels[name],
                    "difference": round(diff, 4),
                    "priority": priority,
                    "weight": FEATURE_WEIGHTS[name],
                }
            )

    # Sort by difference (highest first)
    tasks.sort(key=lambda x: x["difference"], reverse=True)
    return tasks
