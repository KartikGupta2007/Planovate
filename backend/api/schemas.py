# ============================================
# OWNER: Member 2 – Backend API (FastAPI)
# FILE: Pydantic Schemas (API Contracts)
# ============================================

from pydantic import BaseModel
from typing import Optional


class RenovationRequest(BaseModel):
    """Request body for renovation analysis."""

    old_image: str  # Image URL or base64
    new_image: str  # Image URL or base64
    budget: Optional[float] = None


class PlanStep(BaseModel):
    """Single step in the renovation plan."""

    task: str  # e.g., "Repair cracks", "Repaint walls"
    priority: str  # "high", "medium", "low"
    cost: float  # Estimated cost for this step
    description: str  # Detailed description


class RenovationResponse(BaseModel):
    """
    Response body for renovation analysis.
    FROZEN API CONTRACT – Do not change without team agreement.
    """

    score: float  # 0.0 to 1.0 damage/difference score
    estimated_cost: float  # Total estimated renovation cost
    optimized: bool  # Whether plan was optimized for budget
    plan: list[PlanStep]  # Step-by-step renovation plan
    explanation: str  # LLM-generated explanation


class HistoryResponse(BaseModel):
    """Summary of a past renovation project."""

    project_id: str
    created_at: str
    score: float
    estimated_cost: float
    optimized: bool
