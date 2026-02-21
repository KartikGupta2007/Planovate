# RenovAI API Contract (Freeze)

## POST /analyze
Compares old vs ideal room images. Returns cost estimate and renovation plan.
Budget and location are optional.

### Request (multipart/form-data)
- old_image: file (required)
- new_image: file (required)
- budget: number (optional)
- location: string (optional)

### Response (application/json)
Fields are stable and must not change during hackathon.

- estimated_cost_total: number
- optimized_for_budget: boolean
- budget_used: number
- plan_items: array of plan item objects (always present)
- diff_vector: object with numeric fields
- notes: array of strings

#### PlanItem
- task: string
- priority: "HIGH" | "MEDIUM" | "LOW"
- recommended_material: string
- qty: number
- unit: string
- unit_cost: number
- cost: number
- why: string

#### DiffVector
- cracks: number (0..1)
- paint: number (0..1)
- lighting: number (0..1)
- floor: number (0..1)
- ceiling: number (0..1)

### Example Response
```json
{
  "estimated_cost_total": 72000,
  "optimized_for_budget": true,
  "budget_used": 50000,
  "plan_items": [
    {
      "task": "Crack repair",
      "priority": "HIGH",
      "recommended_material": "cement putty + primer",
      "qty": 120,
      "unit": "sqft",
      "unit_cost": 90,
      "cost": 10800,
      "why": "Visible crack density indicates structural finishing work is required before painting."
    }
  ],
  "diff_vector": { "cracks": 0.7, "paint": 0.6, "lighting": 0.4, "floor": 0.2, "ceiling": 0.1 },
  "notes": ["If LLM is unavailable, we fall back to deterministic explanations."]
}
```
