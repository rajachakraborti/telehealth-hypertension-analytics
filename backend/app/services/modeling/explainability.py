import pandas as pd
import numpy as np
import joblib
import os
import shap
import xgboost as xgb

MODEL_DIR = os.path.join(os.path.dirname(__file__), "../../../models_saved")

class DualLayerExplainer:
    """
    Implements the Dual-Layer Explainable AI (XAI) as promised in the Topic 3 Blueprint.
    Layer 1: Mathematical SHAP Values.
    Layer 2: Plain-English Clinical Translation.
    """
    def __init__(self):
        self.xgb_model_path = os.path.join(MODEL_DIR, "xgboost_aha_model.pkl")
        self.model = None
        self.explainer = None
        
        self.label_mapping = {
            0: "Normal",
            1: "Elevated",
            2: "Stage 1 Hypertension",
            3: "Stage 2 Hypertension"
        }

    def _load_model(self):
        if not os.path.exists(self.xgb_model_path):
            raise FileNotFoundError("XGBoost model not found. Please run the model trainer first.")
        self.model = joblib.load(self.xgb_model_path)
        
        # Initialize SHAP explainer
        self.explainer = shap.TreeExplainer(self.model)

    def explain_prediction(self, patient_data: dict) -> dict:
        """
        Takes a single patient telemetry row and returns the prediction, SHAP values, 
        and a plain-English clinical summary.
        """
        if self.model is None:
            self._load_model()
            
        # Convert to DataFrame
        df_input = pd.DataFrame([patient_data])
        features = ["systolic", "diastolic", "map", "pulse_pressure", "is_night", "is_dipper"]
        
        # Predict
        pred_class_idx = int(self.model.predict(df_input[features])[0])
        pred_stage = self.label_mapping[pred_class_idx]
        
        # Calculate SHAP Values
        shap_values = self.explainer.shap_values(df_input[features])
        
        # In XGBoost multi-class, shap_values can be a 3D array or a list of 2D arrays.
        if isinstance(shap_values, list):
            class_shap_values = shap_values[pred_class_idx][0]
        else:
            # 3D array: (samples, features, classes) -> we want (features,)
            if len(shap_values.shape) == 3:
                class_shap_values = shap_values[0, :, pred_class_idx]
            else:
                class_shap_values = shap_values[0]
            
        # Map feature names to their SHAP impacts and convert numpy types to standard python floats for FastAPI
        feature_impacts = {k: float(v) for k, v in zip(features, class_shap_values)}
        
        # Sort features by absolute impact (highest first)
        sorted_impacts = sorted(feature_impacts.items(), key=lambda x: abs(x[1]), reverse=True)
        
        top_driver_1 = sorted_impacts[0]
        top_driver_2 = sorted_impacts[1]
        
        # Generate Plain-English Translation (Layer 2)
        narrative = (
            f"Patient Risk Rating: {pred_stage}. "
            f"Primary driver: {top_driver_1[0].replace('_', ' ').title()} "
            f"({'+' if top_driver_1[1] > 0 else ''}{round(top_driver_1[1], 3)} impact on risk score), "
            f"followed by {top_driver_2[0].replace('_', ' ').title()} "
            f"({'+' if top_driver_2[1] > 0 else ''}{round(top_driver_2[1], 3)} impact). "
        )
        
        if df_input["is_dipper"].iloc[0] == 0 and df_input["is_night"].iloc[0] == 1:
            narrative += "Anomaly alert: Absence of nocturnal systolic dipping detected."

        return {
            "prediction": pred_stage,
            "shap_attributions": feature_impacts,
            "clinical_summary": narrative
        }