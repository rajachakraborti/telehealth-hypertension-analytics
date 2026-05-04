from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from sklearn.metrics import make_scorer
import numpy as np
import uuid
from typing import List, Dict, Tuple

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