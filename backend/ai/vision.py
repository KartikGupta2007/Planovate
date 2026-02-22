# ============================================
# OWNER: Member 3 – AI / Computer Vision
# FILE: Vision Analysis – Detect Room Conditions
# ============================================

import cv2
import numpy as np
from .preprocessing import preprocess_for_analysis


def detect_cracks(gray_image: np.ndarray) -> float:
    """
    Detect cracks using Canny edge detection + Hough line detection.
    Cracks appear as thin, elongated straight edges in the image.

    Args:
        gray_image: blurred grayscale image (512x512)

    Returns:
        float 0.0 (no cracks) to 1.0 (severe cracks)
    """
    edges = cv2.Canny(gray_image, threshold1=50, threshold2=150)

    lines = cv2.HoughLinesP(
        edges,
        rho=1,
        theta=np.pi / 180,
        threshold=80,
        minLineLength=30,
        maxLineGap=10,
    )

    line_count = len(lines) if lines is not None else 0
    edge_density = float(np.sum(edges > 0)) / edges.size

    line_score = min(line_count / 150.0, 1.0)
    edge_score = min(edge_density / 0.15, 1.0)

    score = line_score * 0.7 + edge_score * 0.3
    return round(float(np.clip(score, 0.0, 1.0)), 4)


def detect_paint_condition(image: np.ndarray) -> float:
    """
    Analyze paint/wall condition using HSV color analysis.
    Worn paint = low saturation (faded) + uneven brightness.

    Args:
        image: resized BGR image (512x512)

    Returns:
        float 0.0 (good condition) to 1.0 (needs repainting)
    """
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    saturation = hsv[:, :, 1].astype(float) / 255.0
    value = hsv[:, :, 2].astype(float) / 255.0

    mean_saturation = float(np.mean(saturation))
    brightness_std = float(np.std(value))

    fade_score = 1.0 - mean_saturation
    uneven_score = min(brightness_std / 0.3, 1.0)

    score = fade_score * 0.6 + uneven_score * 0.4
    return round(float(np.clip(score, 0.0, 1.0)), 4)


def detect_lighting(image: np.ndarray) -> float:
    """
    Analyze room lighting quality using mean brightness + shadow unevenness.
    Dark rooms score high (poor lighting). Bright rooms score low.

    Args:
        image: resized BGR image (512x512)

    Returns:
        float 0.0 (well lit) to 1.0 (poor/dark lighting)
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    mean_brightness = float(np.mean(gray)) / 255.0

    brightness_std = float(np.std(gray.astype(float) / 255.0))
    uneven_score = min(brightness_std / 0.35, 1.0)

    darkness_score = 1.0 - mean_brightness

    score = darkness_score * 0.75 + uneven_score * 0.25
    return round(float(np.clip(score, 0.0, 1.0)), 4)


def detect_floor_condition(image: np.ndarray) -> float:
    """
    Analyze floor condition from the bottom 30% of the image.
    Worn/dirty floors show low texture variance and dark stain patches.

    Args:
        image: resized BGR image (512x512)

    Returns:
        float 0.0 (good floor) to 1.0 (needs repair/replacement)
    """
    h = image.shape[0]
    floor_region = image[int(h * 0.70):, :]

    gray_floor = cv2.cvtColor(floor_region, cv2.COLOR_BGR2GRAY)
    hsv_floor = cv2.cvtColor(floor_region, cv2.COLOR_BGR2HSV)

    texture_std = float(np.std(gray_floor)) / 128.0
    texture_score = 1.0 - min(texture_std, 1.0)

    dark_mask = cv2.inRange(hsv_floor, (0, 0, 0), (180, 255, 60))
    dark_ratio = float(np.sum(dark_mask > 0)) / dark_mask.size
    stain_score = min(dark_ratio / 0.15, 1.0)

    score = texture_score * 0.55 + stain_score * 0.45
    return round(float(np.clip(score, 0.0, 1.0)), 4)


def detect_ceiling_condition(image: np.ndarray) -> float:
    """
    Analyze ceiling condition from the top 20% of the image.
    Detects yellow/brown water stains and dark mold patches.

    Args:
        image: resized BGR image (512x512)

    Returns:
        float 0.0 (good ceiling) to 1.0 (needs repair)
    """
    h = image.shape[0]
    ceiling_region = image[: int(h * 0.20), :]

    hsv_ceil = cv2.cvtColor(ceiling_region, cv2.COLOR_BGR2HSV)

    yellow_mask = cv2.inRange(hsv_ceil, (15, 40, 80), (35, 255, 255))
    yellow_ratio = float(np.sum(yellow_mask > 0)) / yellow_mask.size
    stain_score = min(yellow_ratio / 0.10, 1.0)

    dark_mask = cv2.inRange(hsv_ceil, (0, 0, 0), (180, 255, 55))
    dark_ratio = float(np.sum(dark_mask > 0)) / dark_mask.size
    mold_score = min(dark_ratio / 0.08, 1.0)

    gray_ceil = cv2.cvtColor(ceiling_region, cv2.COLOR_BGR2GRAY)
    brightness_std = float(np.std(gray_ceil)) / 128.0
    uneven_score = min(brightness_std, 1.0)

    score = stain_score * 0.45 + mold_score * 0.35 + uneven_score * 0.20
    return round(float(np.clip(score, 0.0, 1.0)), 4)


def analyze_image(image_bytes: bytes) -> dict:
    """
    Full image analysis pipeline. Entry point called by feature_vector.py.

    Args:
        image_bytes: raw bytes of a JPEG/PNG image

    Returns:
        dict with keys matching FEATURE_NAMES in feature_vector.py:
        {
            "cracks":   float 0.0-1.0,
            "paint":    float 0.0-1.0,
            "lighting": float 0.0-1.0,
            "floor":    float 0.0-1.0,
            "ceiling":  float 0.0-1.0,
        }
        All scores: 0.0 = no issue, 1.0 = severe issue.
    """
    processed = preprocess_for_analysis(image_bytes)

    return {
        "cracks":   detect_cracks(processed["gray"]),
        "paint":    detect_paint_condition(processed["resized"]),
        "lighting": detect_lighting(processed["resized"]),
        "floor":    detect_floor_condition(processed["resized"]),
        "ceiling":  detect_ceiling_condition(processed["resized"]),
    }