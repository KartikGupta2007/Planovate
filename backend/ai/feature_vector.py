# ============================================
# OWNER: Member 3 – AI / Computer Vision
# FILE: Feature Vector Generation & Comparison
# ============================================

import numpy as np
from .vision import analyze_image

# Feature order: [crack, paint, lighting, floor, ceiling]
FEATURE_NAMES = ["cracks", "paint", "lighting", "floor", "ceiling"]


def extract_feature_vector(image_bytes: bytes) -> np.ndarray:
    """
    Extract feature vector from an image.
    Returns: numpy array [crack, paint, lighting, floor, ceiling]
    Each value is 0.0 to 1.0.
    """
    analysis = analyze_image(image_bytes)
    vector = np.array([analysis[name] for name in FEATURE_NAMES])
    return vector


def compute_difference_vector(
    current_vector: np.ndarray, ideal_vector: np.ndarray
) -> np.ndarray:
    """
    Compute the absolute difference between current and ideal room.
    Difference Vector (DV) = |IV - CV|
    """
    return np.abs(ideal_vector - current_vector)


def get_feature_comparison(old_image_bytes: bytes, new_image_bytes: bytes) -> dict:
    """
    Full comparison pipeline between old and new room images.
    Returns dict with vectors and per-feature differences.

    This is the main function that Member 4 (pipeline) will call.
    """
    current_vector = extract_feature_vector(old_image_bytes)
    ideal_vector = extract_feature_vector(new_image_bytes)
    diff_vector = compute_difference_vector(current_vector, ideal_vector)

    return {
        "current_vector": current_vector.tolist(),
        "ideal_vector": ideal_vector.tolist(),
        "difference_vector": diff_vector.tolist(),
        "features": {
            name: {
                "current": float(current_vector[i]),
                "ideal": float(ideal_vector[i]),
                "difference": float(diff_vector[i]),
            }
            for i, name in enumerate(FEATURE_NAMES)
        },
    }
