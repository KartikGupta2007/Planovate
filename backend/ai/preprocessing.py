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
        raise ValueError("Failed to decode image")
    return image


def resize_image(image: np.ndarray, target_size: tuple = (512, 512)) -> np.ndarray:
    """Resize image to a standard size for consistent analysis."""
    return cv2.resize(image, target_size, interpolation=cv2.INTER_AREA)


def convert_to_grayscale(image: np.ndarray) -> np.ndarray:
    """Convert BGR image to grayscale."""
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def apply_gaussian_blur(image: np.ndarray, kernel_size: int = 5) -> np.ndarray:
    """Apply Gaussian blur to reduce noise."""
    return cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)


def preprocess_for_analysis(image_bytes: bytes) -> dict:
    """
    Full preprocessing pipeline.
    Returns dict with different processed versions of the image.
    """
    original = load_image_from_bytes(image_bytes)
    resized = resize_image(original)
    gray = convert_to_grayscale(resized)
    blurred = apply_gaussian_blur(gray)

    return {
        "original": original,
        "resized": resized,
        "gray": gray,
        "blurred": blurred,
    }
