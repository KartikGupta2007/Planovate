# ============================================
# OWNER: Member 4 – LLM + Optimization + Deployment
# FILE: Budget Optimizer
# ============================================


def optimize_for_budget(
    tasks_with_costs: list[dict], budget: float
) -> tuple[list[dict], bool]:
    """
    Optimize renovation plan to fit within user's budget.

    Strategy:
        - Sort tasks by priority (high > medium > low)
        - Allocate budget to high-priority tasks first
        - Skip or reduce low-priority tasks if over budget

    Input:
        - tasks_with_costs: list with cost field from pricing engine
        - budget: user's total budget

    Output:
        - (optimized_tasks, was_optimized)
        - optimized_tasks: filtered/adjusted list that fits budget
        - was_optimized: True if plan was modified to fit budget
    """
    total_cost = sum(task["cost"] for task in tasks_with_costs)

    # If within budget, no optimization needed
    if total_cost <= budget:
        return tasks_with_costs, False

    # Sort by priority: high first, then medium, then low
    priority_order = {"high": 0, "medium": 1, "low": 2}
    sorted_tasks = sorted(
        tasks_with_costs, key=lambda t: priority_order.get(t["priority"], 3)
    )

    # Greedily include tasks until budget is exhausted
    optimized = []
    remaining_budget = budget

    for task in sorted_tasks:
        if task["cost"] <= remaining_budget:
            optimized.append(task)
            remaining_budget -= task["cost"]
        else:
            # TODO: Optionally include partial task with reduced scope
            pass

    return optimized, True
