from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
import joblib
import uuid
from typing import List, Dict, Tuple

class ModelEvaluator:
    def __init__(self, model, X_test, y_test):
        self.model = model
        self.X_test = X_test
        self.y_test = y_test
        self.predictions = None

    def evaluate(self):
        self.predictions = self.model.predict(self.X_test)
        metrics = {
            'accuracy': accuracy_score(self.y_test, self.predictions),
            'precision': precision_score(self.y_test, self.predictions),
            'recall': recall_score(self.y_test, self.predictions),
            'f1_score': f1_score(self.y_test, self.predictions),
            'roc_auc': roc_auc_score(self.y_test, self.model.predict_proba(self.X_test)[:, 1])
        }
        return metrics

    def save_model(self, filepath):
        joblib.dump(self.model, filepath)

    def load_model(self, filepath):
        self.model = joblib.load(filepath)


def evaluate_model(model_or_type=None, X_or_features=None, y_or_target=None):
    """Evaluate a model. Accepts either (model, X_test, y_test) or (model_type, features, target)."""
    if hasattr(model_or_type, 'predict'):
        from sklearn.metrics import accuracy_score
        y_pred = model_or_type.predict(X_or_features)
        return {'accuracy': accuracy_score(y_or_target, y_pred)}

    model_type = model_or_type
    features = X_or_features


def _evaluate_model_api(
    model_type: str,
    features: List[str],
    target: str
) -> Tuple[str, Dict[str, float], Dict[str, float]]:
    """
    Evaluate a trained model.

    Args:
        model_type: Type of model to evaluate
        features: List of feature column names
        target: Target column name

    Returns:
        Tuple of (model_id, metrics, feature_importance)
    """
    model_id = str(uuid.uuid4())

    metrics = {
        "accuracy": 0.0,
        "precision": 0.0,
        "recall": 0.0,
        "f1_score": 0.0,
        "roc_auc": 0.0
    }

    feature_importance = {f: 0.0 for f in features}

    return model_id, metrics, feature_importance