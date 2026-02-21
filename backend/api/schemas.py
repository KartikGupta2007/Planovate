# ============================================
# OWNER: Member 2 – Backend API (FastAPI)
# FILE: Pydantic Schemas (API Contracts)
# ============================================

from pydantic import BaseModel, Field
from typing import Optional, Literal


class RenovationRequest(BaseModel):
    """Request body for renovation analysis."""

    old_image: str  # Image URL or base64
    new_image: str  # Image URL or base64
    budget: Optional[float] = None


class PlanStep(BaseModel):
    """Single step in the renovation plan."""

    task: str = Field(..., example="Repair cracks")
    priority: Literal["high", "medium", "low"] = Field(..., example="high")
    cost: float = Field(..., ge=0, example=15000.0)
    description: str = Field(..., example="Fix wall cracks in bedroom")


class RenovationResponse(BaseModel):
    """
    Response body for renovation analysis.
    FROZEN API CONTRACT – Do not change without team agreement.
    """

    score: float = Field(..., ge=0, le=1, example=0.65)
    estimated_cost: float = Field(..., ge=0, example=72000)
    optimized: bool = Field(..., example=True)
    plan: list[PlanStep] = Field(default_factory=list)
    explanation: str = Field(..., example="Based on the analysis...")


class HistoryResponse(BaseModel):
    """Summary of a past renovation project."""

    project_id: str
    created_at: str
    score: float
    estimated_cost: float
    optimized: bool
