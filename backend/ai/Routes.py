"""
FastAPI routes – clean API contract for the React frontend.
"""
from __future__ import annotations

import uuid
from pathlib import Path
from typing import List

from fastapi import APIRouter, File, HTTPException, UploadFile

from api.schemas import (
    AnalyzeRoomRequest,
    AnalyzeRoomResponse,
    BudgetPlan,
    CompareRoomsRequest,
    CompareRoomsResponse,
    FeatureVector,
    GetLocalPricesRequest,
    GetLocalPricesResponse,
    OptimizeBudgetRequest,
    OptimizeBudgetResponse,
    PricingRates,
    RankedTask,
    Task,
    UploadImageResponse,
)
from config import settings
from services.pipeline import (
    analyze_image,
    create_session,
    run_comparison,
    store_image,
)
from services.pricing import get_adjusted_rates
from services.optimizer import optimize_budget

router = APIRouter()

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}


# ---------------------------------------------------------------------------
# Health
# ---------------------------------------------------------------------------


@router.get("/health")
async def health():
    return {"status": "ok", "service": "Smart RenovAI Planner"}


# ---------------------------------------------------------------------------
# 1. Upload Image
# ---------------------------------------------------------------------------


@router.post("/upload-image", response_model=UploadImageResponse)
async def upload_image(
    file: UploadFile = File(...),
    session_id: str = None,
):
    ext = Path(file.filename or "img.jpg").suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(400, f"Unsupported file type: {ext}")

    if not session_id:
        session_id = create_session()

    image_id = str(uuid.uuid4())
    save_path = settings.STORAGE_DIR / f"{session_id}_{image_id}{ext}"
    content = await file.read()
    save_path.write_bytes(content)

    store_image(session_id, image_id, str(save_path))

    return UploadImageResponse(
        image_id=image_id,
        session_id=session_id,
        filename=file.filename or "",
    )


# ---------------------------------------------------------------------------
# 2. Analyze Room
# ---------------------------------------------------------------------------


@router.post("/analyze-room", response_model=AnalyzeRoomResponse)
async def analyze_room(req: AnalyzeRoomRequest):
    try:
        result = analyze_image(req.session_id, req.image_id)
    except FileNotFoundError as e:
        raise HTTPException(404, str(e))
    except Exception as e:
        raise HTTPException(500, f"Analysis failed: {e}")

    features = result["features"]
    return AnalyzeRoomResponse(
        session_id=req.session_id,
        image_id=req.image_id,
        image_role=req.image_role,
        feature_vector=FeatureVector(**features),
        debug_metadata=result["debug"],
    )


# ---------------------------------------------------------------------------
# 3. Compare Rooms
# ---------------------------------------------------------------------------


@router.post("/compare-rooms", response_model=CompareRoomsResponse)
async def compare_rooms(req: CompareRoomsRequest):
    try:
        result = run_comparison(
            req.session_id,
            req.current_image_id,
            req.ideal_image_id,
            req.city,
            req.area_sqft,
        )
    except FileNotFoundError as e:
        raise HTTPException(404, str(e))
    except Exception as e:
        raise HTTPException(500, f"Comparison failed: {e}")

    ranked = [
        RankedTask(
            id=t["id"],
            name=t["name"],
            priority=t["priority"],
            dv_component=t["dv_component"],
            impact_score=t["impact_score"],
            service_key=t["service_key"],
        )
        for t in result["ranked_tasks"]
    ]

    return CompareRoomsResponse(
        session_id=req.session_id,
        current_vector=FeatureVector(**result["current_vector"]),
        ideal_vector=FeatureVector(**result["ideal_vector"]),
        delta_vector=FeatureVector(**result["delta_vector"]),
        damage_score=result["damage_score"],
        classification=result["classification"],
        ranked_tasks=ranked,
    )


# ---------------------------------------------------------------------------
# 4. Get Local Prices
# ---------------------------------------------------------------------------


@router.post("/get-local-prices", response_model=GetLocalPricesResponse)
async def get_local_prices(req: GetLocalPricesRequest):
    rates_list, cache_status, source, notes, confidence = get_adjusted_rates(req.city)

    rates = [
        PricingRates(
            service=r["service"],
            base_rate=r["base_rate"],
            multiplier=r["multiplier"],
            adjusted_rate=r["adjusted_rate"],
            source=r["source"],
        )
        for r in rates_list
    ]

    return GetLocalPricesResponse(
        city=req.city,
        rates=rates,
        cache_status=cache_status,
        source=source,
        notes=notes or None,
        confidence=confidence if confidence > 0 else None,
    )


# ---------------------------------------------------------------------------
# 5. Optimize Budget
# ---------------------------------------------------------------------------


@router.post("/optimize-budget", response_model=OptimizeBudgetResponse)
async def optimize_budget_endpoint(req: OptimizeBudgetRequest):
    # Build delta vector
    if req.delta_vector:
        delta = req.delta_vector
    else:
        # Default: moderate issues across all features
        delta = {k: 0.5 for k in ["crack", "paint", "mold", "lighting", "floor", "ceiling"]}

    # Get city pricing
    rates_list, _, _, _, _ = get_adjusted_rates(req.city)

    selected, skipped, buffer_amount, total_cost, recommended_budget = optimize_budget(
        delta=delta,
        area_sqft=req.area_sqft,
        adjusted_rates=rates_list,
        budget=req.budget,
    )

    def _to_task(t: dict) -> Task:
        return Task(
            id=t["id"],
            name=t["name"],
            priority=t["priority"],
            dv_component=t["dv_component"],
            impact_score=t["impact_score"],
            estimated_cost=t["estimated_cost"],
            materials=t["materials"],
            steps=t["steps"],
            service_key=t["service_key"],
        )

    total_budget = req.budget or recommended_budget or total_cost
    utilization = round((total_cost / total_budget * 100) if total_budget else 0, 1)

    plan = BudgetPlan(
        selected_tasks=[_to_task(t) for t in selected],
        skipped_tasks=[_to_task(t) for t in skipped],
        buffer_amount=buffer_amount,
        total_cost=total_cost,
        total_budget=total_budget,
        utilization_pct=utilization,
    )

    skipped_names = [t["name"] for t in skipped]
    if skipped_names:
        explanation = (
            f"Within your budget of ${total_budget:,.0f}, we can complete "
            f"{len(selected)} task(s) costing ${total_cost:,.0f} with a "
            f"${buffer_amount:,.0f} buffer reserved. "
            f"Skipped due to budget: {', '.join(skipped_names)}."
        )
    else:
        explanation = (
            f"All {len(selected)} renovation task(s) fit within the budget. "
            f"Total cost: ${total_cost:,.0f} with ${buffer_amount:,.0f} buffer reserved."
        )

    return OptimizeBudgetResponse(
        city=req.city,
        area_sqft=req.area_sqft,
        recommended_budget=recommended_budget,
        budget_plan=plan,
        explanation=explanation,
    )