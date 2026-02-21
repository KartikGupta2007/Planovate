"""
Smart RenovAI Planner – FastAPI Backend
Entry point: main.py
"""
from __future__ import annotations

import logging
import sys
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Ensure backend root is on path (for relative imports in workers)
sys.path.insert(0, str(Path(__file__).parent))

from api.routes import router
from config import settings
from services.cache import load_cache

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Smart RenovAI Planner API",
    description="AI-powered room renovation planning backend",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS
origins = ["*"] if settings.FRONTEND_ORIGIN == "*" else [settings.FRONTEND_ORIGIN]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api")


@app.on_event("startup")
async def startup_event():
    logger.info("Starting Smart RenovAI Planner API...")
    load_cache()
    logger.info("Pricing cache loaded.")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down...")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)