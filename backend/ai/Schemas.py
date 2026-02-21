from __future__ import annotations

from typing import Annotated, Dict, List, Optional
from pydantic import BaseModel, Field, field_validator

# ---------------------------------------------------------------------------
# Core data models
# ---------------------------------------------------------------------------

FeatureScore = Annotated[float, Field(ge=0.0, le=1.0)]

FEATURE_KEYS = ["crack", "paint", "mold", "lighting", "floor", "ceiling"]


class FeatureVector(BaseModel):
    crack: FeatureScore = 0.0
    paint: FeatureScore = 0.0
    mold: FeatureScore = 0.0
    lighting: FeatureScore = 0.0
    floor: FeatureScore = 0.0
    ceiling: FeatureScore = 0.0

    def to_dict(self) -> Dict[str, float]:
        return self.model_dump()


class Task(BaseModel):
    id: str
    name: str
    priority: int  # 1 = highest
    dv_component: float = Field(ge=0.0, le=1.0)
    impact_score: float
    estimated_cost: float
    materials: List[str]
    steps: List[str]
    service_key: str


class PricingRates(BaseModel):
    service: str
    base_rate: float
    multiplier: float
    adjusted_rate: float
    source: str  # "llm" | "base"
    ttl_expires: Optional[str] = None


class BudgetPlan(BaseModel):
    selected_tasks: List[Task]
    skipped_tasks: List[Task]
    buffer_amount: float
    total_cost: float
    total_budget: float
    utilization_pct: float


# ---------------------------------------------------------------------------
# Request / Response schemas
# ---------------------------------------------------------------------------


class UploadImageResponse(BaseModel):
    image_id: str
    session_id: str
    filename: str


class AnalyzeRoomRequest(BaseModel):
    session_id: str
    image_id: str
    image_role: str = "current"  # "current" | "ideal"


class AnalyzeRoomResponse(BaseModel):
    session_id: str
    image_id: str
    image_role: str
    feature_vector: FeatureVector
    debug_metadata: Dict


class CompareRoomsRequest(BaseModel):
    session_id: str
    current_image_id: str
    ideal_image_id: Optional[str] = None
    city: str = "national"
    area_sqft: float = Field(default=200.0, gt=0)

    @field_validator("city")
    @classmethod
    def clean_city(cls, v: str) -> str:
        return v.strip().title()


class RankedTask(BaseModel):
    id: str
    name: str
    priority: int
    dv_component: float
    impact_score: float
    service_key: str


class CompareRoomsResponse(BaseModel):
    session_id: str
    current_vector: FeatureVector
    ideal_vector: FeatureVector
    delta_vector: FeatureVector
    damage_score: float
    classification: str  # Low | Medium | High
    ranked_tasks: List[RankedTask]


class GetLocalPricesRequest(BaseModel):
    city: str

    @field_validator("city")
    @classmethod
    def clean_city(cls, v: str) -> str:
        return v.strip().title()


class GetLocalPricesResponse(BaseModel):
    city: str
    rates: List[PricingRates]
    cache_status: str  # "hit" | "miss" | "expired"
    source: str  # "llm" | "base"
    notes: Optional[str] = None
    confidence: Optional[float] = None


class OptimizeBudgetRequest(BaseModel):
    city: str = "national"
    area_sqft: float = Field(default=200.0, gt=0)
    delta_vector: Optional[Dict[str, float]] = None
    tasks: Optional[List[str]] = None  # override with explicit task ids
    budget: Optional[float] = None  # if omitted → recommend

    @field_validator("city")
    @classmethod
    def clean_city(cls, v: str) -> str:
        return v.strip().title()


class OptimizeBudgetResponse(BaseModel):
    city: str
    area_sqft: float
    recommended_budget: Optional[float] = None  # when no budget given
    budget_plan: BudgetPlan
    explanation: str