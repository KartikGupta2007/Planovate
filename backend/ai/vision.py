"""
Vision Engine – heuristic feature extractor using OpenCV.
Returns a FeatureVector with normalized 0..1 scores.
Designed to be swapped with a CNN later by replacing extract_features().
"""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Dict

import cv2
import numpy as np

logger = logging.getLogger(__name__)


def _load_image(image_path: str | Path) -> np.ndarray:
    img = cv2.imread(str(image_path))
    if img is None:
        raise ValueError(f"Cannot load image: {image_path}")
    return img


def _normalize(value: float, min_v: float = 0.0, max_v: float = 1.0) -> float:
    return float(np.clip((value - min_v) / (max_v - min_v + 1e-8), 0.0, 1.0))


# ---------------------------------------------------------------------------
# Individual feature extractors
# ---------------------------------------------------------------------------


def _detect_cracks(gray: np.ndarray) -> float:
    """Edge density proxy for cracks: high edge count in thin lines = cracks."""
    edges = cv2.Canny(gray, threshold1=50, threshold2=150)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=80,
                             minLineLength=30, maxLineGap=10)
    line_count = len(lines) if lines is not None else 0
    # Normalise: ~0 lines → 0, ~200+ lines → 1
    return _normalize(line_count, 0, 200)


def _detect_paint_wear(bgr: np.ndarray) -> float:
    """Paint wear = high color variance + low mean saturation."""
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    saturation = hsv[:, :, 1].astype(float) / 255.0
    value = hsv[:, :, 2].astype(float) / 255.0
    # Paint wear: low saturation AND high brightness variance
    sat_mean = float(np.mean(saturation))
    val_std = float(np.std(value))
    # Low sat → worn/faded (score near 1); combine with variance
    wear_score = (1.0 - sat_mean) * 0.6 + val_std * 0.4
    return float(np.clip(wear_score, 0.0, 1.0))


def _detect_mold(bgr: np.ndarray) -> float:
    """Dark greenish spots heuristic."""
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    # Greenish-black mold: hue 40-90, low value
    mask_green = cv2.inRange(hsv, (40, 20, 10), (90, 255, 100))
    # Very dark spots (near black regardless of hue)
    mask_dark = cv2.inRange(hsv, (0, 0, 0), (180, 255, 50))
    combined = cv2.bitwise_or(mask_green, mask_dark)
    ratio = float(np.sum(combined > 0)) / (bgr.shape[0] * bgr.shape[1])
    # ~5%+ pixel coverage = severe mold
    return _normalize(ratio, 0.0, 0.05)


def _detect_lighting(gray: np.ndarray) -> float:
    """
    Low average brightness → poor lighting.
    Returns score where 1 = bright (good), 0 = dark (bad).
    We INVERT so that score near 1 = bad lighting issue.
    """
    mean_brightness = float(np.mean(gray)) / 255.0
    # Invert: dark room = high issue score
    return float(np.clip(1.0 - mean_brightness, 0.0, 1.0))


def _detect_floor(bgr: np.ndarray) -> float:
    """Analyse bottom 25% of image for floor condition (texture variance)."""
    h = bgr.shape[0]
    floor_region = bgr[int(h * 0.75):, :]
    gray_floor = cv2.cvtColor(floor_region, cv2.COLOR_BGR2GRAY)
    # Low texture variance = worn/dirty floor
    std = float(np.std(gray_floor)) / 128.0  # normalised against mid-range std
    # High std = detail present = better floor; low std = uniform/worn
    return float(np.clip(1.0 - std, 0.0, 1.0))


def _detect_ceiling(bgr: np.ndarray) -> float:
    """Analyse top 20% of image for ceiling condition."""
    h = bgr.shape[0]
    ceiling_region = bgr[: int(h * 0.20), :]
    gray_ceil = cv2.cvtColor(ceiling_region, cv2.COLOR_BGR2GRAY)
    # Yellowing / staining proxy: high value in red channel vs blue
    b_mean = float(np.mean(ceiling_region[:, :, 0]))
    r_mean = float(np.mean(ceiling_region[:, :, 2]))
    # Yellow stain = high R, low B
    yellow_ratio = (r_mean - b_mean) / 255.0
    std_score = float(np.std(gray_ceil)) / 128.0
    score = yellow_ratio * 0.5 + (1.0 - std_score) * 0.5
    return float(np.clip(score, 0.0, 1.0))


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def extract_features(image_path: str | Path) -> Dict[str, float]:
    """
    Extract feature scores from an image file.
    Returns dict with keys: crack, paint, mold, lighting, floor, ceiling.
    All values are normalised 0..1 (0 = no issue, 1 = severe issue).
    """
    try:
        bgr = _load_image(image_path)
        gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
        # Apply mild denoise for more stable scores
        gray = cv2.GaussianBlur(gray, (3, 3), 0)

        features = {
            "crack": _detect_cracks(gray),
            "paint": _detect_paint_wear(bgr),
            "mold": _detect_mold(bgr),
            "lighting": _detect_lighting(gray),
            "floor": _detect_floor(bgr),
            "ceiling": _detect_ceiling(bgr),
        }

        logger.info("Extracted features: %s", features)
        return features

    except Exception as exc:
        logger.error("Feature extraction failed: %s", exc)
        # Return neutral mid-scores so the pipeline can still proceed
        return {k: 0.5 for k in ["crack", "paint", "mold", "lighting", "floor", "ceiling"]}


DEFAULT_IDEAL_VECTOR: Dict[str, float] = {
    "crack": 0.0,
    "paint": 0.05,   # near perfect
    "mold": 0.0,
    "lighting": 0.1,  # well-lit
    "floor": 0.05,
    "ceiling": 0.05,
}