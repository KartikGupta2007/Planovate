"""
Tests for DV computation, classification, budget optimizer, and cache.
"""
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest


# ---------------------------------------------------------------------------
# DV Computation
# ---------------------------------------------------------------------------


def test_delta_vector_basic():
    from ai.scoring import compute_delta_vector

    cv = {"crack": 0.8, "paint": 0.3, "mold": 0.1, "lighting": 0.5, "floor": 0.6, "ceiling": 0.4}
    iv = {"crack": 0.0, "paint": 0.9, "mold": 0.0, "lighting": 0.1, "floor": 0.9, "ceiling": 0.8}
    dv = compute_delta_vector(cv, iv)

    assert abs(dv["crack"] - 0.8) < 1e-6
    assert abs(dv["paint"] - 0.6) < 1e-6
    assert abs(dv["mold"] - 0.1) < 1e-6


def test_delta_vector_clamped():
    from ai.scoring import compute_delta_vector

    cv = {"crack": 0.0, "paint": 0.0, "mold": 0.0, "lighting": 0.0, "floor": 0.0, "ceiling": 0.0}
    iv = {"crack": 1.0, "paint": 1.0, "mold": 1.0, "lighting": 1.0, "floor": 1.0, "ceiling": 1.0}
    dv = compute_delta_vector(cv, iv)

    for v in dv.values():
        assert 0.0 <= v <= 1.0


def test_delta_vector_same():
    from ai.scoring import compute_delta_vector

    vec = {"crack": 0.5, "paint": 0.5, "mold": 0.5, "lighting": 0.5, "floor": 0.5, "ceiling": 0.5}
    dv = compute_delta_vector(vec, vec)
    for v in dv.values():
        assert v == 0.0


# ---------------------------------------------------------------------------
# Classification boundaries
# ---------------------------------------------------------------------------


def test_classify_low():
    from ai.scoring import classify_damage
    assert classify_damage(0.0) == "Low"
    assert classify_damage(0.29) == "Low"
    assert classify_damage(0.30) == "Low"


def test_classify_medium():
    from ai.scoring import classify_damage
    assert classify_damage(0.31) == "Medium"
    assert classify_damage(0.59) == "Medium"
    assert classify_damage(0.60) == "Medium"


def test_classify_high():
    from ai.scoring import classify_damage
    assert classify_damage(0.61) == "High"
    assert classify_damage(1.0) == "High"


# ---------------------------------------------------------------------------
# Damage score
# ---------------------------------------------------------------------------


def test_damage_score_zero_dv():
    from ai.scoring import compute_damage_score
    dv = {k: 0.0 for k in ["crack", "paint", "mold", "lighting", "floor", "ceiling"]}
    assert compute_damage_score(dv) == 0.0


def test_damage_score_full_dv():
    from ai.scoring import compute_damage_score
    dv = {k: 1.0 for k in ["crack", "paint", "mold", "lighting", "floor", "ceiling"]}
    score = compute_damage_score(dv)
    # Weights sum to 1, so full DV → score = 1.0
    assert abs(score - 1.0) < 1e-4


# ---------------------------------------------------------------------------
# Budget optimizer
# ---------------------------------------------------------------------------


def _dummy_rates():
    return [
        {"service": "crack_repair", "adjusted_rate": 3.50, "base_rate": 3.50, "multiplier": 1.0, "source": "base"},
        {"service": "painting", "adjusted_rate": 2.00, "base_rate": 2.00, "multiplier": 1.0, "source": "base"},
        {"service": "mold_treatment", "adjusted_rate": 5.00, "base_rate": 5.00, "multiplier": 1.0, "source": "base"},
        {"service": "lighting_upgrade", "adjusted_rate": 4.00, "base_rate": 4.00, "multiplier": 1.0, "source": "base"},
        {"service": "flooring", "adjusted_rate": 8.00, "base_rate": 8.00, "multiplier": 1.0, "source": "base"},
        {"service": "ceiling_repair", "adjusted_rate": 4.50, "base_rate": 4.50, "multiplier": 1.0, "source": "base"},
    ]


def test_optimizer_no_budget_recommends():
    from services.optimizer import optimize_budget

    delta = {"crack": 0.5, "paint": 0.4, "mold": 0.3, "lighting": 0.2, "floor": 0.6, "ceiling": 0.5}
    selected, skipped, buffer, total_cost, recommended = optimize_budget(
        delta=delta, area_sqft=200, adjusted_rates=_dummy_rates(), budget=None
    )
    assert recommended is not None
    assert recommended > total_cost  # buffer included
    assert len(skipped) == 0  # all tasks selected when no budget constraint


def test_optimizer_tight_budget():
    from services.optimizer import optimize_budget

    delta = {"crack": 0.8, "paint": 0.7, "mold": 0.9, "lighting": 0.5, "floor": 0.8, "ceiling": 0.6}
    # Very tight budget: $100 on 200 sqft → most tasks ~$400-1600, so most skip
    selected, skipped, buffer, total_cost, _ = optimize_budget(
        delta=delta, area_sqft=200, adjusted_rates=_dummy_rates(), budget=100.0
    )
    assert total_cost <= 100.0 * 0.9 + 0.01  # within spendable (budget - buffer)
    assert len(skipped) > 0


def test_optimizer_sufficient_budget():
    from services.optimizer import optimize_budget

    delta = {"crack": 0.5, "paint": 0.4, "mold": 0.3, "lighting": 0.2, "floor": 0.6, "ceiling": 0.5}
    # Large budget → all tasks should be selected
    selected, skipped, buffer, total_cost, _ = optimize_budget(
        delta=delta, area_sqft=200, adjusted_rates=_dummy_rates(), budget=100_000.0
    )
    assert len(skipped) == 0


def test_optimizer_buffer():
    from services.optimizer import optimize_budget
    from config import get_weights

    delta = {"crack": 0.5, "paint": 0.5, "mold": 0.5, "lighting": 0.5, "floor": 0.5, "ceiling": 0.5}
    budget = 5000.0
    _, _, buffer, _, _ = optimize_budget(
        delta=delta, area_sqft=200, adjusted_rates=_dummy_rates(), budget=budget
    )
    expected_buffer = budget * get_weights()["buffer_percent"]
    assert abs(buffer - expected_buffer) < 0.01


# ---------------------------------------------------------------------------
# Cache
# ---------------------------------------------------------------------------


def test_cache_write_read(tmp_path, monkeypatch):
    import services.cache as cache_module
    from services.cache import get_city_pricing, set_city_pricing

    # Patch cache path to temp dir
    monkeypatch.setattr(cache_module, "_memory_cache", {})
    monkeypatch.setattr("config.settings.PRICING_CACHE_PATH", tmp_path / "test_cache.json")

    data = {"rates": [], "source": "base", "notes": "", "confidence": 0.5}
    set_city_pricing("TestCity", data)

    result, status = get_city_pricing("TestCity")
    assert status == "hit"
    assert result == data


def test_cache_miss(monkeypatch):
    import services.cache as cache_module
    monkeypatch.setattr(cache_module, "_memory_cache", {})

    result, status = cache_module.get_city_pricing("NonExistentCity")
    assert status == "miss"
    assert result is None


def test_cache_expired(monkeypatch):
    import services.cache as cache_module
    from datetime import datetime, timedelta

    past = (datetime.utcnow() - timedelta(days=1)).isoformat()
    monkeypatch.setattr(cache_module, "_memory_cache", {
        "expiredcity": {"data": {}, "expires": past}
    })

    result, status = cache_module.get_city_pricing("ExpiredCity")
    assert status == "expired"
    assert result is None


# ---------------------------------------------------------------------------
# Vision extractor returns 0..1
# ---------------------------------------------------------------------------


def test_extractor_returns_normalized(tmp_path):
    """Test that vision extractor always returns 0..1 scores."""
    import numpy as np
    import cv2
    from ai.vision import extract_features

    # Create a synthetic test image
    img = np.random.randint(0, 256, (300, 400, 3), dtype=np.uint8)
    img_path = tmp_path / "test_img.jpg"
    cv2.imwrite(str(img_path), img)

    features = extract_features(img_path)
    assert set(features.keys()) == {"crack", "paint", "mold", "lighting", "floor", "ceiling"}
    for k, v in features.items():
        assert 0.0 <= v <= 1.0, f"Feature {k}={v} out of range"