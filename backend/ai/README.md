# Smart RenovAI Planner – Backend / AI

FastAPI backend with full AI pipeline: Computer Vision → Scoring → LLM Pricing → Budget Optimizer.

## Folder Structure

```
backend/
├── main.py                  # FastAPI app entry point
├── conftest.py              # pytest path setup
├── requirements.txt
├── .env.example
├── config/
│   ├── __init__.py          # Settings + data loaders
│   └── weights.json         # Feature weights, thresholds, buffer %
├── data/
│   ├── base_rates.json      # National avg rates per service
│   ├── materials_catalog.json
│   ├── steps_templates.json
│   └── pricing_cache.json   # Auto-populated cache
├── storage/                 # Uploaded images (gitignored)
├── ai/
│   ├── __init__.py
│   ├── vision.py            # OpenCV heuristic feature extractor
│   └── scoring.py           # DV, damage score, classification, ranking
├── services/
│   ├── __init__.py
│   ├── pipeline.py          # Orchestrator
│   ├── llm_client.py        # LLM wrapper with fallback
│   ├── pricing.py           # Cost engine + adjusted rates
│   ├── optimizer.py         # Greedy budget optimizer
│   └── cache.py             # In-memory + JSON cache with TTL
├── api/
│   ├── __init__.py
│   ├── routes.py            # All endpoints
│   └── schemas.py           # Pydantic v2 models
└── tests/
    └── test_scoring.py
```

## Local Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env          # Edit with your LLM key
python main.py                # or: uvicorn main:app --reload
```

API docs available at: http://localhost:8000/docs

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `LLM_PROVIDER` | `openai` | `openai`, `mistral`, or `other` |
| `LLM_API_KEY` | _(empty)_ | API key; if blank, uses base rates |
| `LLM_BASE_URL` | _(empty)_ | Custom endpoint (e.g. Ollama) |
| `LLM_MODEL` | `gpt-3.5-turbo` | Model name |
| `LLM_TIMEOUT_SECONDS` | `15` | LLM call timeout |
| `FRONTEND_ORIGIN` | `*` | CORS origin |

## Running Tests

```bash
cd backend
pytest tests/ -v
```

## curl Examples

### Health check
```bash
curl http://localhost:8000/api/health
```

### Upload image
```bash
curl -X POST http://localhost:8000/api/upload-image \
  -F "file=@/path/to/room.jpg"
# Returns: {"image_id": "...", "session_id": "...", "filename": "room.jpg"}
```

### Upload second image (same session)
```bash
curl -X POST "http://localhost:8000/api/upload-image?session_id=SESSION_ID" \
  -F "file=@/path/to/ideal.jpg"
```

### Analyze a single image
```bash
curl -X POST http://localhost:8000/api/analyze-room \
  -H "Content-Type: application/json" \
  -d '{"session_id": "SESSION_ID", "image_id": "IMAGE_ID", "image_role": "current"}'
```

### Compare rooms (full pipeline)
```bash
curl -X POST http://localhost:8000/api/compare-rooms \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "SESSION_ID",
    "current_image_id": "CURRENT_IMG_ID",
    "ideal_image_id": "IDEAL_IMG_ID",
    "city": "Bangalore",
    "area_sqft": 250
  }'
```

### Get local prices
```bash
curl -X POST http://localhost:8000/api/get-local-prices \
  -H "Content-Type: application/json" \
  -d '{"city": "Mumbai"}'
```

### Optimize budget (with budget)
```bash
curl -X POST http://localhost:8000/api/optimize-budget \
  -H "Content-Type: application/json" \
  -d '{
    "city": "Delhi",
    "area_sqft": 300,
    "delta_vector": {"crack": 0.7, "paint": 0.5, "mold": 0.3, "lighting": 0.4, "floor": 0.6, "ceiling": 0.5},
    "budget": 5000
  }'
```

### Optimize budget (no budget → get recommendation)
```bash
curl -X POST http://localhost:8000/api/optimize-budget \
  -H "Content-Type: application/json" \
  -d '{
    "city": "Pune",
    "area_sqft": 200,
    "delta_vector": {"crack": 0.6, "paint": 0.4, "mold": 0.5, "lighting": 0.3, "floor": 0.7, "ceiling": 0.4}
  }'
```

## Deploy on Render

1. Push this repo to GitHub
2. Create a new **Web Service** on Render
3. Set **Build Command**: `pip install -r backend/requirements.txt`
4. Set **Start Command**: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add env vars from `.env.example` in Render's environment settings
6. Deploy!

## Deploy on Railway

1. Push to GitHub
2. New project → Deploy from GitHub repo
3. Set root directory to `/` (uses `Procfile`)
4. Add environment variables in Railway dashboard
5. Deploy!

## Architecture Notes

- **LLM is ONLY used** for city price multiplier adjustment and explanations — never for vision, scoring, or optimization.
- All LLM responses are validated; invalid/timeout → silent fallback to `multiplier=1.0`.
- Pricing cache TTL is 7 days (configurable in `config/weights.json`).
- Vision engine uses OpenCV heuristics and is designed to be swapped with a CNN by replacing `ai/vision.py::extract_features()`.