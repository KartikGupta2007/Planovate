# ============================================
# OWNER: Member 2 – Backend API (FastAPI)
# FILE: API Routes / Endpoints
# ============================================

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional
from .schemas import RenovationRequest, RenovationResponse, HistoryResponse

# TODO: Import pipeline when Member 4 completes it
# from services.pipeline import run_pipeline

router = APIRouter()


@router.post("/analyze", response_model=RenovationResponse)
async def analyze_renovation(
    old_image: UploadFile = File(...),
    new_image: UploadFile = File(...),
    budget: Optional[float] = Form(None),
):
    """
    Main endpoint: Compare old room vs ideal room.

    API Contract:
      Request:  old_image (file), new_image (file), budget (optional float)
      Response: { score, estimated_cost, optimized, plan, explanation }
    """
    # TODO: Validate file types and sizes
    # TODO: Read image bytes
    # TODO: Call AI pipeline
    # result = await run_pipeline(old_image_bytes, new_image_bytes, budget)
    # return result

    # Placeholder response
    return RenovationResponse(
        score=0.0,
        estimated_cost=0,
        optimized=False,
        plan=[],
        explanation="Pipeline not yet connected.",
    )


@router.get("/history/{user_id}", response_model=list[HistoryResponse])
async def get_user_history(user_id: str):
    """
    Get past renovation projects for a user.
    """
    # TODO: Fetch from storage/database
    return []


@router.get("/health")
async def health():
    return {"status": "ok"}
