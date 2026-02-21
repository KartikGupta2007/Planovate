# ============================================
# OWNER: Member 2 – Backend API (FastAPI)
# FILE: Main Application Entry Point
# ============================================

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router as api_router
from config import settings

app = FastAPI(
    title="RenovAI API",
    description="Smart Room Renovation Planner Backend",
    version="1.0.0",
)

# CORS – Allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(api_router, prefix="/api")


@app.get("/")
def health_check():
    return {"status": "ok", "message": "RenovAI API is running"}


# Run: uvicorn main:app --reload
