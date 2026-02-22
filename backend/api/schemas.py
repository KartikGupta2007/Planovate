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
    cost: float = Field(..., ge=0, example=15000.0, description="Cost in INR (₹)")
    description: str = Field(..., example="Fix wall cracks in bedroom")


class RenovationResponse(BaseModel):
    """
    Response body for renovation analysis.
    All costs are in Indian Rupees (INR / ₹).
    """

    score: float = Field(..., ge=0, le=1, example=0.65)
    estimated_cost: float = Field(..., ge=0, example=72000, description="Total cost in INR (₹)")
    optimized: bool = Field(..., example=True)
    currency: str = Field(default="INR", description="Currency code (always INR)")
    plan: list[PlanStep] = Field(default_factory=list)
    explanation: str = Field(..., example="Based on the analysis...")


class HistoryResponse(BaseModel):
    """Summary of a past renovation project."""

    project_id: str
    created_at: str
    score: float
    estimated_cost: float
    optimized: bool
