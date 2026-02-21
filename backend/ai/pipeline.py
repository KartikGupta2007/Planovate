"""
AI Pipeline Orchestrator – ties together vision, scoring, pricing, optimizer.
This is the single source of truth for the full analysis pipeline.
"""
from __future__ import annotations

import logging
import uuid
from pathlib import Path
from typing import Dict, Optional

from ai.vision import extract_features, DEFAULT_IDEAL_VECTOR
from ai.scoring import (
    compute_delta_vector,
    compute_damage_score,
    classify_damage,
    rank_tasks,
)
from config import settings
from services.pricing import get_adjusted_rates, estimate_total_cost
from services.optimizer import optimize_budget

logger = logging.getLogger(__name__)

# In-memory session store: session_id → {image_id → path}
_sessions: Dict[str, Dict[str, str]] = {}


def create_session() -> str:
    sid = str(uuid.uuid4())
    _sessions[sid] = {}
    return sid


def store_image(session_id: str, image_id: str, file_path: str) -> None:
    if session_id not in _sessions:
        _sessions[session_id] = {}
    _sessions[session_id][image_id] = file_path


def get_image_path(session_id: str, image_id: str) -> Optional[Path]:
    path_str = _sessions.get(session_id, {}).get(image_id)
    if path_str:
        return Path(path_str)
    return None


def analyze_image(session_id: str, image_id: str) -> Dict:
    path = get_image_path(session_id, image_id)
    if path is None or not path.exists():
        raise FileNotFoundError(f"Image not found: session={session_id}, id={image_id}")
    features = extract_features(path)
    return {
        "session_id": session_id,
        "image_id": image_id,
        "features": features,
        "debug": {"path": str(path), "extractor": "opencv_heuristic_v1"},
    }


def run_comparison(
    session_id: str,
    current_image_id: str,
    ideal_image_id: Optional[str],
    city: str,
    area_sqft: float,
) -> Dict:
    """Full CV→IV→DV→Score→Classify→Rank pipeline."""
    # CV
    cv_path = get_image_path(session_id, current_image_id)
    if cv_path is None:
        raise FileNotFoundError("Current image not found in session.")
    current_features = extract_features(cv_path)

    # IV
    if ideal_image_id:
        iv_path = get_image_path(session_id, ideal_image_id)
        if iv_path and iv_path.exists():
            ideal_features = extract_features(iv_path)
        else:
            logger.warning("Ideal image not found, using default IV.")
            ideal_features = dict(DEFAULT_IDEAL_VECTOR)
    else:
        ideal_features = dict(DEFAULT_IDEAL_VECTOR)

    # DV, score, classify, rank
    delta = compute_delta_vector(current_features, ideal_features)
    damage_score = compute_damage_score(delta)
    classification = classify_damage(damage_score)
    ranked = rank_tasks(delta)

    return {
        "current_vector": current_features,
        "ideal_vector": ideal_features,
        "delta_vector": delta,
        "damage_score": damage_score,
        "classification": classification,
        "ranked_tasks": ranked,
    }