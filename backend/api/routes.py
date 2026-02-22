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
import tempfile
import os

from .schemas import RenovationResponse, HistoryResponse
from .dependencies import validate_image_file

router = APIRouter()

# Path to storage directory for user history
STORAGE_DIR = Path(__file__).parent.parent / "storage"
STORAGE_DIR.mkdir(exist_ok=True)


# ── Helper: Save image bytes to temp file ──
def _save_temp_image(image_bytes: bytes, suffix: str = ".jpg") -> str:
    """
    Save image bytes to a temporary file and return the file path.
    Member 4's pipeline expects FILE PATHS, not raw bytes.
    """
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    tmp.write(image_bytes)
    tmp.close()
    return tmp.name


# ── Helper: Calculate score from diff_vector ──
def _calculate_score(diff_vector: dict) -> float:
    """
    Calculate overall damage score from diff_vector.
    Weighted average matching Member 3's scoring weights.
    """
    weights = {
        "cracks": 0.25,
        "paint": 0.20,
        "lighting": 0.15,
        "floor": 0.25,
        "ceiling": 0.15,
    }
    score = sum(weights.get(k, 0) * v for k, v in diff_vector.items())
    return round(min(max(score, 0.0), 1.0), 4)


# ── Helper: Generate user-friendly explanation ──
def _generate_explanation(pipeline_result: dict, score: float) -> str:
    """
    Generate a comprehensive, user-friendly explanation for the renovation analysis.
    """
    plan_items = pipeline_result.get("plan_items", [])
    estimated_cost = pipeline_result.get("estimated_cost_total", 0)
    optimized = pipeline_result.get("optimized_for_budget", False)
    diff_vector = pipeline_result.get("diff_vector", {})
    
    # Opening statement based on overall score
    if score >= 0.66:
        condition = "significant renovation work"
    elif score >= 0.33:
        condition = "moderate renovation"
    else:
        condition = "minor updates"
    
    explanation_parts = [
        f"Based on our analysis of your room images, we've identified that {condition} is needed."
    ]
    
    # List main issues found
    if diff_vector:
        issues = []
        for key, value in diff_vector.items():
            if value >= 0.2:  # Significant difference
                issues.append(key.replace("_", " "))
        
        if issues:
            issues_text = ", ".join(issues[:-1]) + " and " + issues[-1] if len(issues) > 1 else issues[0]
            explanation_parts.append(f"The main areas requiring attention are {issues_text}.")
    
    # Describe the plan
    if plan_items:
        task_count = len(plan_items)
        high_priority = sum(1 for item in plan_items if item.get("priority") == "high")
        
        if high_priority > 0:
            explanation_parts.append(
                f"We've created a {task_count}-step renovation plan with {high_priority} high-priority task{'s' if high_priority > 1 else ''}."
            )
        else:
            explanation_parts.append(
                f"We've created a {task_count}-step renovation plan to transform your space."
            )
    
    # Budget information
    if optimized:
        explanation_parts.append(
            f"The plan has been optimized to fit within your budget while addressing the most critical improvements. "
            f"Total estimated cost: ₹{int(estimated_cost):,}."
        )
    else:
        explanation_parts.append(
            f"The total estimated cost for the complete renovation is ₹{int(estimated_cost):,}."
        )
    
    # Add a closing statement
    explanation_parts.append(
        "Each task in the plan includes detailed cost breakdowns and can be adjusted based on your priorities."
    )
    
    return " ".join(explanation_parts)


# ── Helper: Map pipeline output → API contract ──
def _map_pipeline_to_response(pipeline_result: dict) -> dict:
    """
    Map Member 4's pipeline output to our frozen API contract.

    Pipeline returns:
      { estimated_cost_total, optimized_for_budget, plan_items, diff_vector, notes }

    Our API contract expects:
      { score, estimated_cost, optimized, plan[], explanation }
    """
    diff_vector = pipeline_result.get("diff_vector", {})
    score = _calculate_score(diff_vector)

    # Map plan_items → plan (lowercase priority + rename 'why' → 'description')
    plan = []
    for item in pipeline_result.get("plan_items", []):
        plan.append({
            "task": item.get("task", ""),
            "priority": item.get("priority", "low").lower(),
            "cost": float(item.get("cost", 0)),
            "description": item.get("why", item.get("task", "")),
        })

    # Generate user-friendly explanation
    explanation = _generate_explanation(pipeline_result, score)

    return {
        "score": score,
        "estimated_cost": pipeline_result.get("estimated_cost_total", 0),
        "optimized": pipeline_result.get("optimized_for_budget", False),
        "currency": "INR",
        "plan": plan,
        "explanation": explanation,
    }


@router.post("/analyze", response_model=RenovationResponse)
async def analyze_renovation(
    old_image: UploadFile = File(..., description="Current room image"),
    new_image: UploadFile = File(..., description="Ideal room image"),
    budget: Optional[float] = Form(None, description="Budget in INR (optional)"),
    location: Optional[str] = Form(None, description="City/location for price adjustment"),
    room_area: Optional[float] = Form(None, description="Room area in sqft (auto-estimated if not given)"),
    llm_provider: Optional[str] = Form(None, description="LLM provider: gemini, openai, ollama"),
    llm_api_key: Optional[str] = Form(None, description="Your LLM API key"),
    llm_model: Optional[str] = Form(None, description="LLM model name (e.g. gemini-2.0-flash)"),
    user_id: Optional[str] = Form(None, description="User ID for saving to history"),
):
    """
    Main endpoint: Compare old room vs ideal room and generate renovation plan.

    Users can pass their own LLM API key + model to enable AI-powered
    location pricing and explanations. If not provided, falls back to .env config.
    """

    # ── Step 1: Validate both images ──
    await validate_image_file(old_image, label="old_image")
    await validate_image_file(new_image, label="new_image")

    # ── Step 2: Validate budget and room_area if provided ──
    if budget is not None and budget < 0:
        raise HTTPException(status_code=400, detail="Budget cannot be negative.")
    if room_area is not None and room_area <= 0:
        raise HTTPException(status_code=400, detail="Room area must be positive.")

    # ── Step 3: Build LLM config from user-provided values ──
    llm_config = None
    if llm_provider or llm_api_key or llm_model:
        llm_config = {
            "provider": llm_provider or "",
            "api_key": llm_api_key or "",
            "model": llm_model or "",
        }

    # ── Step 4: Read image bytes ──
    old_image_bytes = await old_image.read()
    new_image_bytes = await new_image.read()

    # ── Step 5: Save to temp files (Member 4's pipeline takes file paths) ──
    old_tmp_path = _save_temp_image(old_image_bytes)
    new_tmp_path = _save_temp_image(new_image_bytes)

    try:
        # ── Step 6: Call AI pipeline ──
        from services.pipeline import run_pipeline

        pipeline_result = run_pipeline(
            old_image_path=old_tmp_path,
            new_image_path=new_tmp_path,
            budget=budget,
            location=location,
            user_context={"room_area_sqft": room_area} if room_area else None,
            llm_config=llm_config,
        )

        # ── Step 6: Map pipeline output to our API contract ──
        response_data = _map_pipeline_to_response(pipeline_result)

        # ── Step 7: Save to history if user_id provided ──
        if user_id:
            save_to_history(user_id, response_data)

        return RenovationResponse(**response_data)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pipeline error: {str(e)}")

    finally:
        # ── Cleanup: Remove temp files ──
        os.unlink(old_tmp_path)
        os.unlink(new_tmp_path)


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
