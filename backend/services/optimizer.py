# ============================================
# OWNER: Person 4 – Budget Optimizer
# ============================================

from __future__ import annotations

from typing import Any

from . import constants


_PRIORITY_ORDER = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}


def _impact_per_cost(task: dict[str, Any]) -> float:
    cost = float(task.get("cost", 0))
    diff_value = float(task.get("diff_value", 0))
    if cost <= 0:
        return float("inf")
    return diff_value / cost


def optimize_for_budget(
    tasks: list[dict[str, Any]],
    budget: float,
) -> tuple[list[dict[str, Any]], float, bool]:
    """
    Greedy optimization based on priority, then impact per cost.

    Returns: (optimized_tasks, budget_used, optimized_flag)
    """
    if budget <= 0:
        return [], 0.0, True

    usable_budget = budget * (1.0 - constants.BUDGET_BUFFER_FACTOR)

    total_cost = sum(float(task.get("cost", 0)) for task in tasks)
    if total_cost <= usable_budget:
        return tasks, round(total_cost, 2), False

    sorted_tasks = sorted(
        tasks,
        key=lambda t: (
            _PRIORITY_ORDER.get(t.get("priority", "LOW"), 3),
            -_impact_per_cost(t),
        ),
    )

    optimized: list[dict[str, Any]] = []
    remaining = usable_budget

    for task in sorted_tasks:
        cost = float(task.get("cost", 0))
        if cost <= remaining:
            optimized.append(task)
            remaining -= cost
        elif cost == 0:
            optimized.append(task)

    budget_used = sum(float(task.get("cost", 0)) for task in optimized)
    return optimized, round(budget_used, 2), True
