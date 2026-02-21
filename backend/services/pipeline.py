# ============================================
# OWNER: Member 4 – LLM + Optimization + Deployment
# FILE: Main AI Pipeline Orchestrator
# ============================================

from ai.feature_vector import get_feature_comparison
from ai.scoring import calculate_damage_score, get_priority_tasks
from .pricing import estimate_total_cost, get_total_cost
from .optimizer import optimize_for_budget
from .llm_service import generate_explanation


async def run_pipeline(
    old_image_bytes: bytes,
    new_image_bytes: bytes,
    budget: float | None = None,
) -> dict:
    """
    Main orchestrator – runs the full AI pipeline.

    Flow:
        1. Feature extraction (Member 3: ai/)
        2. Scoring (Member 3: ai/)
        3. Cost estimation (Member 4: services/pricing)
        4. Budget optimization (Member 4: services/optimizer)
        5. LLM explanation (Member 4: services/llm_service)

    Input:
        - old_image_bytes: raw bytes of old/current room image
        - new_image_bytes: raw bytes of ideal room image
        - budget: optional user budget

    Output: dict matching API contract
        {
            score: float,
            estimated_cost: float,
            optimized: bool,
            plan: list[PlanStep],
            explanation: str
        }
    """
    # Step 1: Compare images → feature vectors
    comparison = get_feature_comparison(old_image_bytes, new_image_bytes)

    # Step 2: Calculate damage score
    score = calculate_damage_score(comparison["difference_vector"])

    # Step 3: Get priority tasks
    priority_tasks = get_priority_tasks(comparison["difference_vector"])

    # Step 4: Estimate costs
    tasks_with_costs = estimate_total_cost(priority_tasks)
    total_cost = get_total_cost(tasks_with_costs)

    # Step 5: Optimize for budget (if provided)
    optimized = False
    final_tasks = tasks_with_costs
    if budget is not None and budget > 0:
        final_tasks, optimized = optimize_for_budget(tasks_with_costs, budget)
        total_cost = get_total_cost(final_tasks)

    # Step 6: Generate LLM explanation
    explanation = await generate_explanation(score, final_tasks, total_cost, budget)

    # Step 7: Format plan for API response
    plan = [
        {
            "task": task["task"],
            "priority": task["priority"],
            "cost": task["cost"],
            "description": f"{task['task']} (difference: {task['difference']:.0%})",
        }
        for task in final_tasks
    ]

    return {
        "score": score,
        "estimated_cost": total_cost,
        "optimized": optimized,
        "plan": plan,
        "explanation": explanation,
    }
