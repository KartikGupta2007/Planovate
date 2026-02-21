# ============================================
# OWNER: Person 4 – Services Layer
# ============================================

# Deferred import — do not import pipeline at package level.
# It triggers AI/OpenCV imports that crash if not fully ready.
# Use directly: from services.pipeline import run_pipeline
__all__ = ["run_pipeline"]
