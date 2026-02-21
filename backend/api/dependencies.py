# ============================================
# OWNER: Member 2 – Backend API (FastAPI)
# FILE: Shared Dependencies & Utilities
# ============================================

from fastapi import UploadFile, HTTPException
from config import settings

ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png", "image/webp"]


async def validate_image(file: UploadFile) -> bytes:
    """Validate uploaded image file type and size."""

    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type: {file.content_type}. Allowed: {ALLOWED_IMAGE_TYPES}",
        )

    contents = await file.read()
    size_mb = len(contents) / (1024 * 1024)

    if size_mb > settings.MAX_IMAGE_SIZE_MB:
        raise HTTPException(
            status_code=400,
            detail=f"File too large: {size_mb:.1f}MB. Max: {settings.MAX_IMAGE_SIZE_MB}MB",
        )

    return contents
