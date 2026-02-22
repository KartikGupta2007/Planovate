# Planovate – Smart Room Renovation Planner

AI-powered web app that compares your current room with your ideal room and generates a renovation plan with cost estimation.

## Quick Start

See [docs/SETUP.md](docs/SETUP.md) for full setup instructions.

## Project Structure

```
Planovate/
├── frontend/                  # Member 1 – React + Appwrite
│   ├── src/
│   │   ├── pages/             # Login, Register, Upload, Dashboard, History
│   │   ├── components/        # Navbar, ImageUploader, ResultCard, etc.
│   │   ├── appwrite/          # Auth, Storage config
│   │   ├── api/               # Backend API calls
│   │   └── context/           # Auth context
│   └── .env.example
│
├── backend/
│   ├── main.py                # Member 2 – FastAPI entry point
│   ├── config.py              # Member 2 – App configuration
│   ├── api/                   # Member 2 – Routes, schemas, deps
│   │   ├── routes.py
│   │   ├── schemas.py
│   │   └── dependencies.py
│   ├── ai/                    # Member 3 – Computer Vision
│   │   ├── vision.py          # Image analysis
│   │   ├── scoring.py         # Damage scoring
│   │   ├── feature_vector.py  # Feature extraction
│   │   └── preprocessing.py   # Image preprocessing
│   ├── services/              # Member 4 – LLM + Optimization
│   │   ├── pipeline.py        # Main orchestrator
│   │   ├── llm_service.py     # LLM integration
│   │   ├── pricing.py         # Cost estimation
│   │   └── optimizer.py       # Budget optimization
│   ├── storage/               # Uploaded files (gitignored)
│   ├── requirements.txt
│   └── .env.example
│
├── shared/
│   └── contracts.json         # Frozen API contracts
│
└── docs/
    └── SETUP.md               # Setup guide
```

## Team Ownership

| Member | Folder | Responsibility |
|--------|--------|----------------|
| 1 | `frontend/` | React UI, Appwrite auth, image upload |
| 2 | `backend/api/`, `main.py`, `config.py` | FastAPI routes, schemas, validation |
| 3 | `backend/ai/` | OpenCV, feature vectors, scoring |
| 4 | `backend/services/`, `requirements.txt` | LLM, pricing, optimizer, pipeline, deployment |

## API Contract

```
POST /api/analyze
  → { old_image, new_image, budget? }
  ← { score, estimated_cost, optimized, plan[], explanation }
```

See [shared/contracts.json](shared/contracts.json) for full contract details.
