from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
import joblib
import pandas as pd
import uuid
from typing import List, Dict, Tuple, Any, Optional
from app.services.data_exploration.statistics import load_dataframe

class ModelTrainer:
    def __init__(self, model, data, target_column):
        self.model = model
        self.data = data
        self.target_column = target_column
        self.X = self.data.drop(columns=[self.target_column])
        self.y = self.data[self.target_column]

    def train(self, test_size=0.2, random_state=42):
        X_train, X_test, y_train, y_test = train_test_split(self.X, self.y, test_size=test_size, random_state=random_state)
        self.model.fit(X_train, y_train)
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred)
        return accuracy, report

    def save_model(self, filename):
        joblib.dump(self.model, filename)

    def load_model(self, filename):
        self.model = joblib.load(filename)

    def evaluate(self, X_test, y_test):
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred)
        return accuracy, report


# Model registry
MODEL_REGISTRY: Dict[str, Any] = {}


def _get_model_class(model_type: str):
    """Get the model class based on model type string."""
    models = {
        'random_forest': RandomForestClassifier,
        'gradient_boosting': GradientBoostingClassifier,
        'logistic_regression': LogisticRegression,
        'xgboost': XGBClassifier
    }
    if model_type not in models:
        raise ValueError(f"Unknown model type: {model_type}")
    return models[model_type]


def train_model(model_type_or_X=None, features_or_y=None, target=None, hyperparameters=None):
    """Train a model. Accepts either (X_train, y_train) or (model_type, features, target, hyperparameters)."""
    if isinstance(model_type_or_X, (list, __import__('numpy').ndarray)):
        model = RandomForestClassifier(random_state=42)
        model.fit(model_type_or_X, features_or_y)
        return model

    model_type = model_type_or_X
    features = features_or_y


def _train_model_api(
    model_type: str,
    features: List[str],
    target: str,
    hyperparameters: Dict[str, float]
) -> Tuple[str, Dict[str, float], Dict[str, float]]:
    """
    Train a model and return results.

    Args:
        model_type: Type of model (random_forest, gradient_boosting, etc.)
        features: List of feature column names
        target: Target column name
        hyperparameters: Dictionary of hyperparameters

    Returns:
        Tuple of (model_id, metrics, feature_importance)
    """
    # For now, return placeholder values
    # In production, this would load data and actually train
    model_id = str(uuid.uuid4())

    # Placeholder metrics
    metrics = {
        "accuracy": 0.0,
        "precision": 0.0,
        "recall": 0.0,
        "f1_score": 0.0
    }

    # Placeholder feature importance
    feature_importance = {f: 0.0 for f in features}

    return model_id, metrics, feature_importance


def train_model_on_dataset(
    dataset_id: str,
    model_type: str,
    target: str,
    features: Optional[List[str]] = None,
    hyperparameters: Optional[Dict] = None,
) -> Tuple[str, Dict[str, float], Dict[str, float]]:
    df = load_dataframe(dataset_id)

    if target not in df.columns:
        raise ValueError(f"Target column '{target}' not found in dataset")

    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    if features:
        feature_cols = [f for f in features if f in df.columns]
    else:
        feature_cols = [c for c in numeric_cols if c != target]

    if not feature_cols:
        raise ValueError("No usable feature columns found")

    X = df[feature_cols].dropna()
    y = df.loc[X.index, target]

    n_unique = y.nunique()
    if n_unique > 20 or n_unique == len(y):
        raise ValueError(
            f"Target column '{target}' has {n_unique} unique values — it looks continuous. "
            "Please choose a categorical column (e.g. hypertension, smoking, gender)."
        )

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model_class = _get_model_class(model_type)
    hp = {k: v for k, v in (hyperparameters or {}).items()}
    model = model_class(**hp, random_state=42) if model_type != 'logistic_regression' else LogisticRegression(**hp, max_iter=1000)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    avg = 'weighted'
    metrics = {
        "accuracy":  round(float(accuracy_score(y_test, y_pred)), 4),
        "precision": round(float(precision_score(y_test, y_pred, average=avg, zero_division=0)), 4),
        "recall":    round(float(recall_score(y_test, y_pred, average=avg, zero_division=0)), 4),
        "f1_score":  round(float(f1_score(y_test, y_pred, average=avg, zero_division=0)), 4),
    }

    if hasattr(model, 'feature_importances_'):
        importance = {c: round(float(v), 4) for c, v in zip(feature_cols, model.feature_importances_)}
    elif hasattr(model, 'coef_'):
        coefs = model.coef_[0] if model.coef_.ndim > 1 else model.coef_
        importance = {c: round(float(abs(v)), 4) for c, v in zip(feature_cols, coefs)}
    else:
        importance = {c: 0.0 for c in feature_cols}

    model_id = str(uuid.uuid4())
    joblib.dump(model, f"uploads/{model_id}.pkl")

    return model_id, metrics, importance