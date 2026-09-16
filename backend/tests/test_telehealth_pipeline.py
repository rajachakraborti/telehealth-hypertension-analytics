import pytest
from fastapi.testclient import TestClient
import pandas as pd
import os
import sys

# Ensure backend is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import app
from scripts.synthetic_telemetry_generator import SyntheticTelemetryGenerator
from app.services.modeling.explainability import DualLayerExplainer

client = TestClient(app)

def test_synthetic_generator():
    """Test that the generator creates clinically bounded synthetic data."""
    generator = SyntheticTelemetryGenerator(num_patients=2, days_per_patient=1)
    df = generator.generate_telemetry()
    
    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0
    assert "systolic" in df.columns
    assert "map" in df.columns
    
    # Check physiological bounds (Prof Pollyn's feedback)
    assert df["map"].min() >= 70.0
    assert df["map"].max() <= 110.0

def test_api_rbac_rejection():
    """Test that the API correctly rejects unauthorized users (401/403)."""
    response = client.post("/api/modeling/explain", json={
        "systolic": 120.0,
        "diastolic": 80.0,
        "map": 93.3,
        "pulse_pressure": 40.0,
        "is_night": 0,
        "is_dipper": 1
    })
    # Should be 401 Unauthorized because no token was provided
    assert response.status_code == 401
