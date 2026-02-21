# ============================================
# OWNER: Member 2 – Backend API (FastAPI)
# FILE: API Routes / Endpoints
# ============================================

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional
from pathlib import Path
from datetime import datetime
import json
import uuid

from .schemas import RenovationResponse, HistoryResponse
from .dependencies import validate_image_file

# TODO: Uncomment when Member 4 completes the pipeline
# from services.pipeline import run_pipeline

router = APIRouter()

# Path to storage directory for user history
STORAGE_DIR = Path(__file__).parent.parent / "storage"
STORAGE_DIR.mkdir(exist_ok=True)  # Create if it doesn't exist


@router.post("/analyze", response_model=RenovationResponse)
async def analyze_renovation(
    old_image: UploadFile = File(..., description="Current room image"),
    new_image: UploadFile = File(..., description="Ideal room image"),
    budget: Optional[float] = Form(None, description="Budget in USD (optional)"),
):
    """
    Main endpoint: Compare old room vs ideal room and generate renovation plan.

    Steps:
      1. Validate uploaded files (type + size)
      2. Read image bytes
      3. Call AI pipeline (Member 3 vision → Member 4 pipeline)
      4. Return structured renovation plan
    """

    # ── Step 1: Validate both images ──
    await validate_image_file(old_image, label="old_image")
    await validate_image_file(new_image, label="new_image")

    # ── Step 2: Validate budget if provided ──
    if budget is not None and budget < 0:
        raise HTTPException(status_code=400, detail="Budget cannot be negative.")

    # ── Step 3: Read image bytes into memory ──
    old_image_bytes = await old_image.read()
    new_image_bytes = await new_image.read()

    # ── Step 4: Call AI pipeline ──
    # TODO: Replace placeholder with real pipeline call when Member 4 is ready
    # result = await run_pipeline(old_image_bytes, new_image_bytes, budget)
    # return result

    # Placeholder response until pipeline is connected
    return RenovationResponse(
        score=0.0,
        estimated_cost=0,
        optimized=False,
        plan=[],
        explanation="Pipeline not yet connected. Images received successfully.",
    )


def save_to_history(user_id: str, result: dict) -> None:
    """
    Save a renovation result to user's history JSON file.
    Called after /analyze returns a result.

    File structure: backend/storage/{user_id}.json
    Contains: list of past project summaries
    """
    file_path = STORAGE_DIR / f"{user_id}.json"

    # Load existing history or start empty
    if file_path.exists():
        history = json.loads(file_path.read_text())
    else:
        history = []

    # Add new entry
    history.append({
        "project_id": str(uuid.uuid4()),
        "created_at": datetime.now().isoformat(),
        "score": result["score"],
        "estimated_cost": result["estimated_cost"],
        "optimized": result["optimized"],
    })

    # Save back to file
    file_path.write_text(json.dumps(history, indent=2))


@router.get("/history/{user_id}", response_model=list[HistoryResponse])
async def get_user_history(user_id: str):
    """
    Get past renovation projects for a user.
    Reads from backend/storage/{user_id}.json
    """
    file_path = STORAGE_DIR / f"{user_id}.json"

    if not file_path.exists():
        return []

    history = json.loads(file_path.read_text())
    return history


@router.get("/health")
async def health():
    return {"status": "ok"}
