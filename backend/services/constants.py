# ============================================
# OWNER: Person 4 – Services Constants
# ============================================

from __future__ import annotations

# Feature keys expected in diff_vector
FEATURE_KEYS = ["cracks", "paint", "lighting", "floor", "ceiling"]

# Default fallback diff vector if AI modules are missing or return zeros
DEFAULT_DIFF_VECTOR = {
    "cracks": 0.4,
    "paint": 0.5,
    "lighting": 0.3,
    "floor": 0.2,
    "ceiling": 0.2,
}

# Thresholds for priority labels
PRIORITY_HIGH_THRESHOLD = 0.66
PRIORITY_MEDIUM_THRESHOLD = 0.33

# Default quantities
DEFAULT_ROOM_AREA_SQFT = 120
DEFAULT_LIGHTING_UNITS = 4

# Base rates (INR) – realistic Indian market rates (2024-25)
CRACK_REPAIR_PER_SQFT = 200       # cement putty + primer + finish
PAINT_MATTE_PER_SQFT = 45         # primer + 2 coats matte paint
PAINT_WATERPROOF_PER_SQFT = 70    # waterproof primer + 2 coats
LIGHTING_BASIC_PER_UNIT = 2500    # LED panel light with wiring
FLOORING_TILE_PER_SQFT = 250      # vitrified tiles + laying + adhesive
CEILING_BASIC_PER_SQFT = 110      # gypsum board + framework + finishing

# Cost factors
LABOR_FACTOR = 0.35  # 35% labor surcharge (Indian market: 30-40%)
BUFFER_FACTOR = 0.1  # 10% contingency buffer
MIN_WORK_FACTOR = 0.6  # If a task is needed, price at least 60% of full room cost

# Budget buffer to preserve headroom in optimizer
BUDGET_BUFFER_FACTOR = 0.1

# Minimum allowed user budget (INR)
MIN_BUDGET = 15000

# Minimum diff required to include a task
MIN_DIFF_FOR_TASK = 0.01

# LLM categories for location multipliers
LLM_MULTIPLIER_KEYS = ["paint", "labor", "flooring", "lighting", "repair"]

# Pricing categories per task
CATEGORY_REPAIR = "repair"
CATEGORY_PAINT = "paint"
CATEGORY_LIGHTING = "lighting"
CATEGORY_FLOORING = "flooring"
CATEGORY_LABOR = "labor"
