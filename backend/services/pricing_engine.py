# ============================================
# OWNER: Person 4 – Pricing Engine
# ============================================

from __future__ import annotations

from typing import Any

from . import constants
from .llm_service import get_llm_client


def _resolve_unit_cost(task: dict[str, Any]) -> float:
    task_key = task.get("task_key")
    if task_key == "crack_repair":
        return constants.CRACK_REPAIR_PER_SQFT
    if task_key == "paint_upgrade":
        material = (task.get("recommended_material") or "").lower()
        if "waterproof" in material:
            return constants.PAINT_WATERPROOF_PER_SQFT
        return constants.PAINT_MATTE_PER_SQFT
    if task_key == "lighting_upgrade":
        return constants.LIGHTING_BASIC_PER_UNIT
    if task_key == "flooring_change":
        return constants.FLOORING_TILE_PER_SQFT
    if task_key == "ceiling_work":
        return constants.CEILING_BASIC_PER_SQFT
    return 0.0


def _apply_multiplier(base_cost: float, multipliers: dict[str, float], category: str) -> float:
    multiplier = multipliers.get(category, 1.0)
    return base_cost * multiplier


def _compute_task_cost(unit_cost: float, qty: float, diff_value: float) -> float:
    # diff_value = severity of damage (0→1), NOT area percentage.
    # If a task is included, the WHOLE room needs work (you can't paint half a wall).
    # Map diff_value to a work factor: [0, 1] → [0.6, 1.0]
    #   - diff 0.1 → 0.64 (minor issue, but still full-room effort)
    #   - diff 0.5 → 0.80 (moderate work)
    #   - diff 1.0 → 1.00 (full renovation intensity)
    work_factor = constants.MIN_WORK_FACTOR + (max(diff_value, 0.0) * (1.0 - constants.MIN_WORK_FACTOR))
    base_cost = unit_cost * qty * work_factor
    cost_with_labor = base_cost * (1.0 + constants.LABOR_FACTOR)
    final_cost = cost_with_labor * (1.0 + constants.BUFFER_FACTOR)
    return round(final_cost, 2)


def price_tasks(
    tasks: list[dict[str, Any]],
    location: str | None = None,
    llm_config: dict[str, str] | None = None,
) -> tuple[list[dict[str, Any]], float, list[str]]:
    """
    Apply pricing to task list using base rates and optional LLM multipliers.

    Returns: (priced_tasks, total_cost, notes)
    """
    notes: list[str] = []
    multipliers: dict[str, float] = {key: 1.0 for key in constants.LLM_MULTIPLIER_KEYS}

    if location:
        llm_client = get_llm_client(llm_config)
        loc_multipliers, note = llm_client.get_location_multipliers(location)
        if loc_multipliers:
            multipliers.update(loc_multipliers)
        if note:
            notes.append(note)

    total_cost = 0.0
    priced_tasks: list[dict[str, Any]] = []

    for task in tasks:
        unit_cost = _resolve_unit_cost(task)
        category = task.get("category", "repair")
        unit_cost = _apply_multiplier(unit_cost, multipliers, category)
        qty = float(task.get("qty", 0))
        diff_value = float(task.get("diff_value", 0))
        cost = _compute_task_cost(unit_cost, qty, diff_value)

        task_out = dict(task)
        task_out["unit_cost"] = round(unit_cost, 2)
        task_out["cost"] = cost
        priced_tasks.append(task_out)
        total_cost += cost

    return priced_tasks, round(total_cost, 2), notes
