# ============================================
# OWNER: Member 2 – Backend API (FastAPI)
# FILE: Main Application Entry Point
# ============================================

import logging
import time
import uuid
from typing import Callable

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from api.routes import router as api_router
from config import settings

# Configure logging
log_level = logging.DEBUG if settings.DEBUG else logging.INFO
logging.basicConfig(
    level=log_level,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Planovate API",
    description="Smart Room Renovation Planner Backend",
    version="1.0.0",
    docs_url="/docs" if settings.DEBUG else None,  # Disable docs in production
    redoc_url="/redoc" if settings.DEBUG else None,
)

# Security: Trusted Host Middleware (production only)
if not settings.DEBUG and settings.ALLOWED_HOSTS:
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=settings.ALLOWED_HOSTS
    )

# CORS – Allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    max_age=3600,  # Cache preflight requests for 1 hour
)


# Request ID and timing middleware
@app.middleware("http")
async def add_request_id_and_timing(request: Request, call_next: Callable):
    """
    Add unique request ID for tracking and measure request duration.
    """
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    
    start_time = time.time()
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    
    # Add custom headers
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = str(round(process_time, 3))
    
    # Security headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    
    # Log request
    logger.info(
        f"{request.method} {request.url.path} - Status: {response.status_code} - "
        f"Duration: {process_time:.3f}s - Request ID: {request_id}"
    )
    
    return response

# Register routes
app.include_router(api_router, prefix="/api")


@app.get("/")
def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "ok",
        "message": "Planovate API is running",
        "version": "1.0.0",
        "environment": "development" if settings.DEBUG else "production"
    }


@app.get("/api/health")
def api_health_check():
    """Detailed health check for API services."""
    return {
        "status": "healthy",
        "api_version": "1.0.0",
        "services": {
            "llm": "configured" if settings.LLM_PROVIDER else "not_configured",
            "vision": "ready",
        }
    }


# ── Global Error Handler ──
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Catches any unhandled exception across ALL endpoints.
    Returns a clean JSON error instead of an ugly server traceback.
    """
    request_id = getattr(request.state, "request_id", "unknown")
    
    # Log the error with request details
    logger.error(
        f"Unhandled exception - Request ID: {request_id} - "
        f"Path: {request.url.path} - Error: {str(exc)}",
        exc_info=settings.DEBUG  # Include traceback in debug mode
    )
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Internal server error. Please try again later.",
            "error": str(exc) if settings.DEBUG else "Something went wrong.",
            "request_id": request_id,
        },
    )


@app.on_event("startup")
async def startup_event():
    """Log startup information."""
    logger.info("="*60)
    logger.info("Planovate API Starting...")
    logger.info(f"Environment: {'Development' if settings.DEBUG else 'Production'}")
    logger.info(f"LLM Provider: {settings.LLM_PROVIDER}")
    logger.info(f"CORS Origins: {', '.join(settings.ALLOWED_ORIGINS)}")
    logger.info("="*60)


@app.on_event("shutdown")
async def shutdown_event():
    """Log shutdown information."""
    logger.info("Planovate API Shutting down...")


# Run: uvicorn main:app --reload
