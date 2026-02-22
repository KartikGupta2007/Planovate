# ============================================
# OWNER: Member 4 – LLM + Optimization + Deployment
# FILE: LLM Integration – Explanation & Price Adjustment
# ============================================

# TODO: Choose and import LLM library (openai, google-generativeai, etc.)
# import openai
# from config import settings


async def generate_explanation(
    score: float,
    priority_tasks: list[dict],
    estimated_cost: float,
    budget: float | None = None,
) -> str:
    """
    Use LLM to generate a human-readable renovation explanation.

    Input:
        - score: overall damage score (0-1)
        - priority_tasks: list from Member 3's scoring module
        - estimated_cost: total cost from pricing engine
        - budget: user's budget (optional)

    Output:
        - String explanation with reasoning, suggestions, and step-by-step plan
    """
    # TODO: Build prompt and call LLM API
    # prompt = f"""
    # You are a renovation expert. Based on the following analysis:
    # - Overall damage score: {score}
    # - Priority tasks: {priority_tasks}
    # - Estimated cost: ₹{estimated_cost}
    # - User budget: ₹{budget if budget else 'Not specified'}
    #
    # Provide:
    # 1. A brief summary of the room's condition
    # 2. Why each task is recommended
    # 3. A step-by-step renovation plan
    # 4. Budget advice (if budget was provided)
    # """
    #
    # response = await openai.ChatCompletion.acreate(
    #     model=settings.LLM_MODEL,
    #     messages=[{"role": "user", "content": prompt}],
    # )
    # return response.choices[0].message.content

    return "LLM explanation not yet implemented."


async def adjust_prices_with_llm(
    tasks: list[dict], location: str = "default"
) -> list[dict]:
    """
    Use LLM to adjust base prices based on location and market conditions.

    Input: list of tasks with base costs
    Output: same list with adjusted costs
    """
    # TODO: Call LLM to adjust pricing based on location
    return tasks
