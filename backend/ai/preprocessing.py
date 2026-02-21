# ============================================
# OWNER: Member 3 – AI / Computer Vision
# FILE: Image Preprocessing
# ============================================

import cv2
import numpy as np


def load_image_from_bytes(image_bytes: bytes) -> np.ndarray:
    """Convert raw image bytes to OpenCV image (BGR)."""
    nparr = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError("Failed to decode image. Ensure valid JPEG/PNG bytes.")
    return image


def resize_image(image: np.ndarray, target_size: tuple = (512, 512)) -> np.ndarray:
    """Resize image to a standard size for consistent analysis."""
    return cv2.resize(image, target_size, interpolation=cv2.INTER_AREA)


def convert_to_grayscale(image: np.ndarray) -> np.ndarray:
    """Convert BGR image to grayscale."""
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def apply_gaussian_blur(image: np.ndarray, kernel_size: int = 5) -> np.ndarray:
    """Apply Gaussian blur to reduce noise. kernel_size must be odd."""
    if kernel_size % 2 == 0:
        kernel_size += 1
    return cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)


def convert_to_hsv(image: np.ndarray) -> np.ndarray:
    """Convert BGR image to HSV color space."""
    return cv2.cvtColor(image, cv2.COLOR_BGR2HSV)


def preprocess_for_analysis(image_bytes: bytes) -> dict:
    """
    Full preprocessing pipeline.
    Returns dict with all processed versions of the image
    ready for use by the vision.py detectors.

    Keys:
        original  - raw decoded BGR image (original resolution)
        resized   - BGR image resized to 512x512
        gray      - blurred grayscale of resized (for edge/line detection)
        gray_raw  - clean grayscale of resized (for brightness stats)
        blurred   - alias for gray
        hsv       - HSV of resized image (for color-based analysis)
    """
    original = load_image_from_bytes(image_bytes)
    resized = resize_image(original)
    gray_raw = convert_to_grayscale(resized)
    blurred = apply_gaussian_blur(gray_raw, kernel_size=5)
    hsv = convert_to_hsv(resized)

    return {
        "original": original,
        "resized":  resized,
        "gray":     blurred,    # pre-blurred for edge/line detection
        "gray_raw": gray_raw,   # clean grayscale for brightness stats
        "blurred":  blurred,    # explicit alias kept for compatibility
        "hsv":      hsv,        # for color-based analysis
    }