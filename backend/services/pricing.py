# ============================================
# OWNER: Member 4 – LLM + Optimization + Deployment
# FILE: Pricing Engine – Cost Estimation
# ============================================

# Base renovation rates (INR) – adjust per region
BASE_RATES = {
    "cracks": 2000,     # Crack repair base cost
    "paint": 3000,      # Full room repaint
    "lighting": 1500,   # Lighting fixture upgrade
    "floor": 5000,      # Flooring repair/replacement
    "ceiling": 2500,    # Ceiling repair
}

# Additional cost multipliers
LABOR_MULTIPLIER = 1.3    # 30% labor cost on top
BUFFER_MULTIPLIER = 1.1   # 10% contingency buffer


def estimate_task_cost(feature: str, difference: float) -> float:
    """
    Estimate cost for a single renovation task.
    Cost = base_rate * difference_score * labor * buffer
    """
    base = BASE_RATES.get(feature, 0)
    cost = base * difference * LABOR_MULTIPLIER * BUFFER_MULTIPLIER
    return round(cost, 2)


def estimate_total_cost(priority_tasks: list[dict]) -> list[dict]:
    """
    Add cost estimates to each priority task.

    Input: priority_tasks from Member 3's scoring module
        [{ feature, task, difference, priority, weight }]

    Output: same list with added 'cost' field
        [{ feature, task, difference, priority, weight, cost }]
    """
    for task in priority_tasks:
        task["cost"] = estimate_task_cost(task["feature"], task["difference"])
    return priority_tasks


def get_total_cost(tasks_with_costs: list[dict]) -> float:
    """Calculate total renovation cost from all tasks."""
    return round(sum(task["cost"] for task in tasks_with_costs), 2)
