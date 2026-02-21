# RenovAI – Setup Guide

## Prerequisites
- Node.js 18+
- Python 3.10+
- Git

---

## Frontend Setup (Member 1)

```bash
cd frontend
npm install
cp .env.example .env    # Fill in Appwrite credentials
npm run dev             # Starts at http://localhost:5173
```

## Backend Setup (Members 2, 3, 4)

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Linux/Mac
# venv\Scripts\activate         # Windows
pip install -r requirements.txt
cp .env.example .env            # Fill in API keys
uvicorn main:app --reload       # Starts at http://localhost:8000
```

---

## Git Workflow

1. Always work in your own folder only
2. Create feature branches: `git checkout -b feature/member1-login`
3. Pull before push: `git pull origin main`
4. Merge to main daily after testing

## Folder Ownership

| Member | Folder | Branch Prefix |
|--------|--------|---------------|
| Member 1 | `frontend/` | `feature/m1-` |
| Member 2 | `backend/api/`, `backend/main.py`, `backend/config.py` | `feature/m2-` |
| Member 3 | `backend/ai/` | `feature/m3-` |
| Member 4 | `backend/services/`, `backend/requirements.txt` | `feature/m4-` |
