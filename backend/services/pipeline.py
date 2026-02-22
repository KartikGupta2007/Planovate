# ============================================
# OWNER: Person 4 – Pipeline Orchestrator
# ============================================

from __future__ import annotations

from typing import Any

from . import constants
from .llm_service import get_llm_client
from .optimizer import optimize_for_budget
from .pricing_engine import price_tasks


def run_pipeline(
    old_image_path: str,
    new_image_path: str,
    budget: float | None,
    location: str | None,
    user_context: dict | None = None,
    llm_config: dict[str, str] | None = None,
) -> dict:
    """Run the RenovAI pipeline and return an API-contract response."""
    notes: list[str] = []
    budget_value: float | None = None
    if budget is not None:
        try:
            budget_value = float(budget)
        except (TypeError, ValueError):
            notes.append("Invalid budget value; ignoring budget.")
    if budget_value is not None and budget_value < constants.MIN_BUDGET:
        notes.append("Budget below minimum; ignoring budget.")
        budget_value = None

    diff_vector, coverage_factor, dv_note = _get_diff_vector(old_image_path, new_image_path)
    if dv_note:
        notes.append(dv_note)

    # Estimate room area: user input > image-based estimation > default
    context = dict(user_context) if user_context else {}
    if not context.get("room_area_sqft"):
        estimated_area = _estimate_area_from_coverage(coverage_factor)
        context["room_area_sqft"] = estimated_area
        notes.append(
            f"Room coverage ~{int(coverage_factor * 100)}% detected; "
            f"estimated full room area: {estimated_area:.0f} sqft."
        )

    tasks = _build_tasks(diff_vector, context)
    priced_tasks, estimated_total, pricing_notes = price_tasks(tasks, location, llm_config)
    notes.extend(pricing_notes)

    plan_items = priced_tasks
    optimized_for_budget = False
    budget_used = estimated_total

    if budget_value is not None:
        optimized_items, budget_used, was_optimized = optimize_for_budget(
            priced_tasks, budget_value
        )
        if was_optimized:
            plan_items = optimized_items
            optimized_for_budget = True
        else:
            plan_items = priced_tasks
            optimized_for_budget = False

    llm_client = get_llm_client(llm_config)
    if llm_client.enabled():
        rewritten, note = llm_client.rewrite_explanations(plan_items, diff_vector)
        if rewritten:
            for item in plan_items:
                if item.get("task") in rewritten:
                    item["why"] = rewritten[item["task"]]
        if note:
            notes.append(note)
        elif not rewritten:
            notes.append("LLM unavailable; using deterministic explanations.")
    else:
        notes.append("LLM disabled; using deterministic explanations.")

    output_items = [_public_plan_item(item) for item in plan_items]
    
    # Calculate actual total from the plan items being returned
    # If optimized, this will be the optimized cost; otherwise the full cost
    actual_total = sum(item.get("cost", 0) for item in output_items)

    return {
        "estimated_cost_total": actual_total,
        "optimized_for_budget": optimized_for_budget,
        "budget_used": budget_used if budget_value is not None else actual_total,
        "plan_items": output_items,
        "diff_vector": diff_vector,
        "notes": notes,
    }


def _get_diff_vector(
    old_path: str, new_path: str
) -> tuple[dict[str, float], float, str | None]:
    """Returns (diff_vector, coverage_factor, note)."""
    dv = None
    coverage_factor = constants.DEFAULT_COVERAGE_FACTOR

    try:
        from ai.vision import extract_features  # type: ignore
        from ai.feature_vector import build_vectors  # type: ignore

        old_features = extract_features(old_path)
        new_features = extract_features(new_path)
        _, _, dv = build_vectors(old_features, new_features)
    except Exception:
        dv = None

    if dv is None:
        try:
            from ai.feature_vector import get_feature_comparison  # type: ignore

            old_bytes = _read_bytes(old_path)
            new_bytes = _read_bytes(new_path)
            comparison = get_feature_comparison(old_bytes, new_bytes)
            diff_list = comparison.get("difference_vector")
            if isinstance(diff_list, list) and len(diff_list) >= len(
                constants.FEATURE_KEYS
            ):
                dv = {
                    key: float(diff_list[i])
                    for i, key in enumerate(constants.FEATURE_KEYS)
                }
            elif isinstance(comparison.get("features"), dict):
                dv = {
                    key: float(comparison["features"][key].get("difference", 0))
                    for key in constants.FEATURE_KEYS
                }
        except Exception:
            dv = None

    # Estimate room coverage from the old (current) image
    try:
        from ai.vision import analyze_image  # type: ignore

        old_bytes = _read_bytes(old_path)
        analysis = analyze_image(old_bytes)
        coverage_info = analysis.get("coverage", {})
        if isinstance(coverage_info, dict) and "coverage_factor" in coverage_info:
            coverage_factor = float(coverage_info["coverage_factor"])
    except Exception:
        coverage_factor = constants.DEFAULT_COVERAGE_FACTOR

    if dv is None:
        return constants.DEFAULT_DIFF_VECTOR.copy(), coverage_factor, "Using fallback diff_vector."

    normalized = _normalize_vector(dv)
    if sum(normalized.values()) <= 0.001:
        return constants.DEFAULT_DIFF_VECTOR.copy(), coverage_factor, "Using fallback diff_vector."

    return normalized, coverage_factor, None


def _normalize_vector(dv: dict[str, Any]) -> dict[str, float]:
    normalized: dict[str, float] = {}
    for key in constants.FEATURE_KEYS:
        try:
            value = float(dv.get(key, 0))
        except (TypeError, ValueError):
            value = 0.0
        normalized[key] = min(max(value, 0.0), 1.0)
    return normalized


def _build_tasks(diff_vector: dict[str, float], user_context: dict[str, Any]) -> list[dict]:
    room_area = _get_room_area(user_context)
    lighting_units = _get_lighting_units(user_context)

    tasks: list[dict[str, Any]] = []

    tasks.append(
        _make_task(
            task_key="crack_repair",
            task="Crack repair",
            category=constants.CATEGORY_REPAIR,
            diff_value=diff_vector["cracks"],
            qty=room_area,
            unit="sqft",
            recommended_material="cement putty + primer",
            why=_why_text("cracks", diff_vector["cracks"]),
        )
    )

    tasks.append(
        _make_task(
            task_key="paint_upgrade",
            task="Paint upgrade",
            category=constants.CATEGORY_PAINT,
            diff_value=diff_vector["paint"],
            qty=room_area,
            unit="sqft",
            recommended_material=_paint_material(diff_vector),
            why=_why_text("paint", diff_vector["paint"]),
        )
    )

    tasks.append(
        _make_task(
            task_key="lighting_upgrade",
            task="Lighting upgrade",
            category=constants.CATEGORY_LIGHTING,
            diff_value=diff_vector["lighting"],
            qty=lighting_units,
            unit="unit",
            recommended_material="LED panel",
            why=_why_text("lighting", diff_vector["lighting"]),
        )
    )

    tasks.append(
        _make_task(
            task_key="flooring_change",
            task="Flooring change",
            category=constants.CATEGORY_FLOORING,
            diff_value=diff_vector["floor"],
            qty=room_area,
            unit="sqft",
            recommended_material="vitrified tiles",
            why=_why_text("floor", diff_vector["floor"]),
        )
    )

    tasks.append(
        _make_task(
            task_key="ceiling_work",
            task="Ceiling work",
            category=constants.CATEGORY_LABOR,
            diff_value=diff_vector["ceiling"],
            qty=room_area,
            unit="sqft",
            recommended_material="gypsum + primer",
            why=_why_text("ceiling", diff_vector["ceiling"]),
        )
    )

    return [task for task in tasks if task["diff_value"] >= constants.MIN_DIFF_FOR_TASK]


def _make_task(
    *,
    task_key: str,
    task: str,
    category: str,
    diff_value: float,
    qty: float,
    unit: str,
    recommended_material: str,
    why: str,
) -> dict[str, Any]:
    return {
        "task_key": task_key,
        "task": task,
        "priority": _priority_label(task_key, diff_value),
        "recommended_material": recommended_material,
        "qty": qty,
        "unit": unit,
        "unit_cost": 0.0,
        "cost": 0.0,
        "why": why,
        "category": category,
        "diff_value": diff_value,
    }


def _priority_label(task_key: str, value: float) -> str:
    """
    Determine priority based on both task type and severity.
    
    Priority Rules (aligned with scoring.py):
    - crack_repair: Always HIGH (structural integrity)
    - ceiling_work: HIGH if value > 0.3, MEDIUM otherwise (safety)
    - flooring_work: HIGH if > 0.5, MEDIUM if > 0.3, LOW otherwise
    - painting: MEDIUM if > 0.4, LOW otherwise (cosmetic)
    - lighting_upgrade: MEDIUM if > 0.5, LOW otherwise (functional)
    """
    # Structural/Safety-critical tasks
    if task_key == "crack_repair":
        return "HIGH"  # Always high priority - structural integrity
    
    if task_key == "ceiling_work":
        return "HIGH" if value > 0.3 else "MEDIUM"  # Safety concern
    
    if task_key == "flooring_work":
        if value > 0.5:
            return "HIGH"
        elif value > 0.3:
            return "MEDIUM"
        else:
            return "LOW"
    
    # Functional tasks
    if task_key == "lighting_upgrade":
        return "MEDIUM" if value > 0.5 else "LOW"
    
    if task_key == "painting":
        return "MEDIUM" if value > 0.4 else "LOW"
    
    # Fallback to threshold-based priority
    if value >= constants.PRIORITY_HIGH_THRESHOLD:
        return "HIGH"
    if value >= constants.PRIORITY_MEDIUM_THRESHOLD:
        return "MEDIUM"
    return "LOW"


def _paint_material(diff_vector: dict[str, float]) -> str:
    if diff_vector.get("paint", 0) > 0.6 or diff_vector.get("cracks", 0) > 0.6:
        return "waterproof paint"
    return "matte paint"


def _why_text(feature: str, diff_value: float) -> str:
    label = {
        "cracks": "crack density",
        "paint": "paint condition",
        "lighting": "lighting quality",
        "floor": "floor wear",
        "ceiling": "ceiling condition",
    }.get(feature, "condition")
    return (
        f"Detected {label} difference score {diff_value:.2f}, "
        "indicating renovation effort is needed."
    )


def _public_plan_item(task: dict[str, Any]) -> dict[str, Any]:
    return {
        "task": task.get("task"),
        "priority": task.get("priority"),
        "recommended_material": task.get("recommended_material"),
        "qty": float(task.get("qty", 0)),
        "unit": task.get("unit"),
        "unit_cost": float(task.get("unit_cost", 0)),
        "cost": float(task.get("cost", 0)),
        "why": task.get("why"),
    }


def _estimate_area_from_coverage(coverage_factor: float) -> float:
    """
    Estimate full room area based on image coverage.
    If image shows only 40% of room, scale up: full_area = default / coverage.
    Capped between DEFAULT and MAX to stay realistic.
    """
    cov = max(coverage_factor, 0.3)
    estimated = constants.DEFAULT_ROOM_AREA_SQFT / cov
    return min(estimated, constants.MAX_ROOM_AREA_SQFT)


def _get_room_area(user_context: dict[str, Any]) -> float:
    area = user_context.get("room_area_sqft")
    try:
        area_val = float(area)
    except (TypeError, ValueError):
        area_val = constants.DEFAULT_ROOM_AREA_SQFT
    return area_val


def _estimate_lighting_units(room_area: float) -> float:
    """Estimate lighting units based on room area (1 unit per 30 sqft)."""
    return max(round(room_area / 30.0), constants.DEFAULT_LIGHTING_UNITS)


def _get_lighting_units(user_context: dict[str, Any]) -> float:
    units = user_context.get("lighting_units")
    try:
        units_val = float(units)
    except (TypeError, ValueError):
        # Derive from room area if available
        area = user_context.get("room_area_sqft")
        try:
            area_val = float(area)
            units_val = _estimate_lighting_units(area_val)
        except (TypeError, ValueError):
            units_val = constants.DEFAULT_LIGHTING_UNITS
    return units_val


def _read_bytes(path: str) -> bytes:
    with open(path, "rb") as handle:
        return handle.read()
