"""
Budget Optimizer – greedy allocation by impact score.
NO LLM usage. Pure deterministic logic.
"""
from __future__ import annotations

from typing import Dict, List, Optional, Tuple

from config import get_weights, get_materials_catalog, get_steps_templates
from ai.scoring import rank_tasks
from services.pricing import estimate_task_cost


def _build_full_tasks(ranked: List[Dict], area_sqft: float, adjusted_rates: List[Dict]) -> List[Dict]:
    catalog = get_materials_catalog()
    templates = get_steps_templates()
    rate_map = {r["service"]: r["adjusted_rate"] for r in adjusted_rates}

    full_tasks = []
    for t in ranked:
        sk = t["service_key"]
        cost = round(rate_map.get(sk, 0.0) * area_sqft, 2)
        full_tasks.append(
            {
                "id": t["id"],
                "name": t["name"],
                "priority": t["priority"],
                "dv_component": t["dv_component"],
                "impact_score": t["impact_score"],
                "service_key": sk,
                "estimated_cost": cost,
                "materials": catalog.get(sk, {}).get("materials", []),
                "steps": templates.get(sk, {}).get("steps", []),
            }
        )
    return full_tasks


def optimize_budget(
    delta: Dict[str, float],
    area_sqft: float,
    adjusted_rates: List[Dict],
    budget: Optional[float] = None,
) -> Tuple[List[Dict], List[Dict], float, float, Optional[float]]:
    """
    Returns (selected_tasks, skipped_tasks, buffer_amount, total_cost, recommended_budget)
    If budget is None, recommended_budget is computed and all tasks are selected.
    """
    cfg = get_weights()
    buffer_pct = cfg["buffer_percent"]

    ranked = rank_tasks(delta)
    full_tasks = _build_full_tasks(ranked, area_sqft, adjusted_rates)
    total_all = sum(t["estimated_cost"] for t in full_tasks)

    if budget is None:
        # Recommend budget = total cost + buffer
        buffer_amount = round(total_all * buffer_pct, 2)
        recommended = round(total_all + buffer_amount, 2)
        return full_tasks, [], buffer_amount, total_all, recommended

    # Greedy allocation
    buffer_amount = round(budget * buffer_pct, 2)
    spendable = budget - buffer_amount
    selected, skipped = [], []
    spent = 0.0

    for task in full_tasks:  # already sorted by impact_score desc
        if spent + task["estimated_cost"] <= spendable:
            selected.append(task)
            spent += task["estimated_cost"]
        else:
            skipped.append(task)

    total_cost = round(spent, 2)
    return selected, skipped, buffer_amount, total_cost, None