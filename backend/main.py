# ============================================
# OWNER: Member 2 – Backend API (FastAPI)
# FILE: Main Application Entry Point
# ============================================

import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from api.routes import router as api_router
from config import settings

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(name)s - %(message)s")

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


# ── Global Error Handler ──
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Catches any unhandled exception across ALL endpoints.
    Returns a clean JSON error instead of an ugly server traceback.
    """
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error. Please try again later.",
            "error": str(exc) if settings.DEBUG else "Something went wrong.",
        },
    )


# Run: uvicorn main:app --reload
