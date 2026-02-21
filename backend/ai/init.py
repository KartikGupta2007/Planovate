# ============================================
# OWNER: Member 3 – AI / Computer Vision
# ============================================

from .vision import analyze_image
from .scoring import (
    calculate_damage_score,
    get_damage_classification,
    get_priority_tasks,
    get_full_score_report,
)
from .feature_vector import (
    extract_feature_vector,
    compute_difference_vector,
    get_feature_comparison,
    get_feature_comparison_with_default_ideal,
    FEATURE_NAMES,
    DEFAULT_IDEAL_VECTOR,
)

__all__ = [
    # Vision
    "analyze_image",
    # Scoring
    "calculate_damage_score",
    "get_damage_classification",
    "get_priority_tasks",
    "get_full_score_report",
    # Feature Vector
    "extract_feature_vector",
    "compute_difference_vector",
    "get_feature_comparison",
    "get_feature_comparison_with_default_ideal",
    "FEATURE_NAMES",
    "DEFAULT_IDEAL_VECTOR",
]