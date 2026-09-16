import sys
import os
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.services.modeling.explainability import DualLayerExplainer

explainer = DualLayerExplainer()
test_data = {
    "systolic": 140.0,
    "diastolic": 90.0,
    "map": 106.6,
    "pulse_pressure": 50.0,
    "is_night": 0,
    "is_dipper": 1
}

res = explainer.explain_prediction(test_data)
print(json.dumps(res, indent=2))
