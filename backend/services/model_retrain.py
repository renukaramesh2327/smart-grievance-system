"""
Model retraining service.
Supports manual trigger (admin) and scheduled retraining.
"""
import os
import subprocess
import sys
from datetime import datetime


def reload_classifier():
    """Reload the ML classifier with newly trained model (call after retrain)."""
    try:
        from backend.services.classifier import classifier
        classifier.load_model()
        return True
    except Exception:
        return False


def get_retrain_status():
    """Get last training metadata if available."""
    try:
        import json
        metadata_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            'ml', 'artifacts', 'train_metadata.json'
        )
        if os.path.exists(metadata_path):
            with open(metadata_path) as f:
                return json.load(f)
    except Exception:
        pass
    return None


def retrain_model():
    """
    Run model retraining. Returns (success: bool, message: str).
    """
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    train_script = os.path.join(project_root, 'ml', 'train.py')
    
    if not os.path.exists(train_script):
        return False, "Training script not found"
    
    try:
        result = subprocess.run(
            [sys.executable, train_script],
            cwd=project_root,
            capture_output=True,
            text=True,
            timeout=300  # 5 min max
        )
        
        if result.returncode == 0:
            reload_classifier()
            status = get_retrain_status()
            acc = status.get('accuracy', 0) * 100 if status else 0
            return True, f"Model retrained successfully. Accuracy: {acc:.2f}%"
        else:
            err = result.stderr or result.stdout or "Unknown error"
            return False, f"Training failed: {err[:500]}"
    except subprocess.TimeoutExpired:
        return False, "Training timed out (5 min)"
    except Exception as e:
        return False, str(e)
