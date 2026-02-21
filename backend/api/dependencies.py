# ============================================
# OWNER: Member 2 – Backend API (FastAPI)
# FILE: Shared Dependencies & Utilities
# ============================================

from fastapi import UploadFile, HTTPException
from config import settings

ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png", "image/webp"]
ALLOWED_EXTENSIONS = [".jpg", ".jpeg", ".png", ".webp"]


async def validate_image_file(file: UploadFile, label: str = "image") -> None:
    """
    Validate uploaded image file:
      1. Check MIME type (image/jpeg, image/png, image/webp)
      2. Check file extension (.jpg, .png, .webp)
      3. Check file is not empty
      4. Check file size (max from settings)

    Raises HTTPException(400) if any check fails.
    Resets file pointer after reading so routes.py can read() again.
    """

    # ── Check 1: MIME type ──
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"{label}: Invalid file type '{file.content_type}'. Allowed: JPEG, PNG, WebP.",
        )

    # ── Check 2: File extension ──
    filename = file.filename or ""
    extension = filename[filename.rfind("."):].lower() if "." in filename else ""
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"{label}: Invalid file extension '{extension}'. Allowed: {ALLOWED_EXTENSIONS}",
        )

    # ── Check 3 & 4: Read file to check empty + size ──
    contents = await file.read()
    await file.seek(0)  # Reset pointer so routes.py can read() again

    if len(contents) == 0:
        raise HTTPException(
            status_code=400,
            detail=f"{label}: File is empty.",
        )

    size_mb = len(contents) / (1024 * 1024)
    if size_mb > settings.MAX_IMAGE_SIZE_MB:
        raise HTTPException(
            status_code=400,
            detail=f"{label}: File too large ({size_mb:.1f}MB). Max allowed: {settings.MAX_IMAGE_SIZE_MB}MB.",
        )
