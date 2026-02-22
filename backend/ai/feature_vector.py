# ============================================
# OWNER: Member 3 – AI / Computer Vision
# FILE: Feature Vector Generation & Comparison
# ============================================

import numpy as np
from .vision import analyze_image

# Feature order is fixed — all other files must respect this order
FEATURE_NAMES = ["cracks", "paint", "lighting", "floor", "ceiling"]

# Default ideal vector: target scores for a fully renovated room
# 0.0 = perfect condition for that feature
DEFAULT_IDEAL_VECTOR = np.array([0.0, 0.05, 0.10, 0.05, 0.05])


def extract_feature_vector(image_bytes: bytes) -> np.ndarray:
    """
    Extract feature vector from an image.

    Args:
        image_bytes: raw bytes of a JPEG/PNG image

    Returns:
        numpy array of shape (5,) with values in [0.0, 1.0]
        Order: [cracks, paint, lighting, floor, ceiling]
        0.0 = no issue, 1.0 = severe issue
    """
    analysis = analyze_image(image_bytes)
    vector = np.array([analysis[name] for name in FEATURE_NAMES], dtype=float)
    return np.clip(vector, 0.0, 1.0)


def compute_difference_vector(
    current_vector: np.ndarray,
    ideal_vector: np.ndarray,
) -> np.ndarray:
    """
    Compute the absolute difference between current and ideal room vectors.
    DV = |IV - CV| per feature, clamped to [0, 1].

    Args:
        current_vector: feature vector extracted from the current (old) room
        ideal_vector:   feature vector extracted from the ideal (target) room

    Returns:
        numpy array of shape (5,) — difference per feature in [0.0, 1.0]
    """
    return np.clip(np.abs(ideal_vector - current_vector), 0.0, 1.0)


def get_feature_comparison(old_image_bytes: bytes, new_image_bytes: bytes) -> dict:
    """
    Full comparison pipeline between old room and ideal/new room images.
    This is the primary function called by Member 4's pipeline.py.

    Args:
        old_image_bytes: raw bytes of the current (problem) room image
        new_image_bytes: raw bytes of the ideal (target) room image

    Returns:
        {
            "current_vector":    list[float]  – CV scores per feature
            "ideal_vector":      list[float]  – IV scores per feature
            "difference_vector": list[float]  – DV = |IV - CV| per feature
            "features": {
                "<feature_name>": {
                    "current":    float,
                    "ideal":      float,
                    "difference": float,
                }
            }
        }
    """
    current_vector = extract_feature_vector(old_image_bytes)
    ideal_vector   = extract_feature_vector(new_image_bytes)
    diff_vector    = compute_difference_vector(current_vector, ideal_vector)

    return {
        "current_vector":    current_vector.tolist(),
        "ideal_vector":      ideal_vector.tolist(),
        "difference_vector": diff_vector.tolist(),
        "features": {
            name: {
                "current":    round(float(current_vector[i]), 4),
                "ideal":      round(float(ideal_vector[i]), 4),
                "difference": round(float(diff_vector[i]), 4),
            }
            for i, name in enumerate(FEATURE_NAMES)
        },
    }


def get_feature_comparison_with_default_ideal(old_image_bytes: bytes) -> dict:
    """
    Comparison pipeline when no ideal image is provided.
    Uses DEFAULT_IDEAL_VECTOR as the target.
    Useful when Member 4 only has a single uploaded image.

    Args:
        old_image_bytes: raw bytes of the current room image

    Returns:
        Same structure as get_feature_comparison()
    """
    current_vector = extract_feature_vector(old_image_bytes)
    ideal_vector   = DEFAULT_IDEAL_VECTOR.copy()
    diff_vector    = compute_difference_vector(current_vector, ideal_vector)

    return {
        "current_vector":    current_vector.tolist(),
        "ideal_vector":      ideal_vector.tolist(),
        "difference_vector": diff_vector.tolist(),
        "features": {
            name: {
                "current":    round(float(current_vector[i]), 4),
                "ideal":      round(float(ideal_vector[i]), 4),
                "difference": round(float(diff_vector[i]), 4),
            }
            for i, name in enumerate(FEATURE_NAMES)
        },
    }