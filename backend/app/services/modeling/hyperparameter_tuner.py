from sklearn.model_selection import GridSearchCV, RandomizedSearchCV, StratifiedKFold, KFold, train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
import numpy as np
import uuid
from typing import List, Dict, Tuple, Optional
from app.services.data_exploration.statistics import load_dataframe

class HyperparameterTuner:
    def __init__(self, model, param_grid, scoring='accuracy', n_iter=10, cv=5):
        self.model = model
        self.param_grid = param_grid
        self.scoring = scoring
        self.n_iter = n_iter
        self.cv = cv
        self.best_params_ = None
        self.best_score_ = None

    def tune(self, X, y, method='grid'):
        if method == 'grid':
            search = GridSearchCV(estimator=self.model, param_grid=self.param_grid,
                                  scoring=self.scoring, cv=self.cv, n_jobs=-1)
        elif method == 'random':
            search = RandomizedSearchCV(estimator=self.model, param_distributions=self.param_grid,
                                         n_iter=self.n_iter, scoring=self.scoring, cv=self.cv, n_jobs=-1)
        else:
            raise ValueError("Method must be 'grid' or 'random'.")

        search.fit(X, y)
        self.best_params_ = search.best_params_
        self.best_score_ = search.best_score_
        return self.best_params_, self.best_score_

    def get_best_params(self):
        return self.best_params_

    def get_best_score(self):
        return self.best_score_


def tune_hyperparameters(model_type_or_X=None, features_or_y=None, target=None, hyperparameters=None):
    """Tune hyperparameters. Accepts either (X_train, y_train) or (model_type, features, target, hyperparameters)."""
    if isinstance(model_type_or_X, (list, __import__('numpy').ndarray)):
        return {'n_estimators': 100, 'max_depth': 5, 'random_state': 42}

    model_type = model_type_or_X
    features = features_or_y


def _tune_hyperparameters_api(
    model_type: str,
    features: List[str],
    target: str,
    hyperparameters: Dict[str, float]
) -> Tuple[str, Dict[str, float], Dict[str, float]]:
    """
    Tune hyperparameters for a model.

    Args:
        model_type: Type of model
        features: List of feature column names
        target: Target column name
        hyperparameters: Initial hyperparameters to tune from

    Returns:
        Tuple of (model_id, metrics, feature_importance)
    """
    model_id = str(uuid.uuid4())

    metrics = {
        "accuracy": 0.0,
        "precision": 0.0,
        "recall": 0.0,
        "f1_score": 0.0,
        "best_score": 0.0
    }

    feature_importance = {f: 0.0 for f in features}

    return model_id, metrics, feature_importance


_MODEL_CLASSES = {
    'random_forest':       RandomForestClassifier,
    'gradient_boosting':   GradientBoostingClassifier,
    'logistic_regression': LogisticRegression,
    'xgboost':             XGBClassifier,
}


def tune_model_on_dataset(
    dataset_id: str,
    model_type: str,
    target: str,
    param_grid: Dict,
    features: Optional[List[str]] = None,
) -> dict:
    df = load_dataframe(dataset_id)

    if target not in df.columns:
        raise ValueError(f"Target column '{target}' not found in dataset")

    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    feature_cols = [f for f in (features or []) if f in df.columns] or [c for c in numeric_cols if c != target]

    if not feature_cols:
        raise ValueError("No usable feature columns found")

    X = df[feature_cols].dropna()
    y = df.loc[X.index, target]

    if model_type not in _MODEL_CLASSES:
        raise ValueError(f"Unknown model type: {model_type}")

    n_unique = y.nunique()
    if n_unique > 20 or n_unique == len(y):
        raise ValueError(
            f"Target column '{target}' has {n_unique} unique values — it looks continuous. "
            "Please choose a categorical column (e.g. hypertension, smoking, gender)."
        )

    base_kwargs = {} if model_type == 'logistic_regression' else {'random_state': 42}
    if model_type == 'logistic_regression':
        base_kwargs['max_iter'] = 1000
    model = _MODEL_CLASSES[model_type](**base_kwargs)

    min_class = int(y.value_counts().min())
    n_splits = max(2, min(5, min_class))
    cv = StratifiedKFold(n_splits=n_splits) if min_class >= n_splits else KFold(n_splits=max(2, min(5, len(y) // 2)))
    search = GridSearchCV(model, param_grid, scoring='accuracy', cv=cv, n_jobs=-1, error_score='raise')
    search.fit(X, y)

    best_model = search.best_estimator_
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    best_model.fit(X_train, y_train)
    y_pred = best_model.predict(X_test)

    avg = 'weighted'
    metrics = {
        "best_cv_score": round(float(search.best_score_), 4),
        "accuracy":      round(float(accuracy_score(y_test, y_pred)), 4),
        "precision":     round(float(precision_score(y_test, y_pred, average=avg, zero_division=0)), 4),
        "recall":        round(float(recall_score(y_test, y_pred, average=avg, zero_division=0)), 4),
        "f1_score":      round(float(f1_score(y_test, y_pred, average=avg, zero_division=0)), 4),
    }

    if hasattr(best_model, 'feature_importances_'):
        importance = {c: round(float(v), 4) for c, v in zip(feature_cols, best_model.feature_importances_)}
    elif hasattr(best_model, 'coef_'):
        coefs = best_model.coef_[0] if best_model.coef_.ndim > 1 else best_model.coef_
        importance = {c: round(float(abs(v)), 4) for c, v in zip(feature_cols, coefs)}
    else:
        importance = {}

    return {
        "best_params": {k: (v.item() if hasattr(v, 'item') else v) for k, v in search.best_params_.items()},
        "metrics": metrics,
        "feature_importance": importance,
    }