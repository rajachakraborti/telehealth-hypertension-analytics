import pytest
from app.services.modeling.model_trainer import train_model
from app.services.modeling.model_evaluator import evaluate_model
from app.services.modeling.hyperparameter_tuner import tune_hyperparameters

def test_train_model():
    # Sample data for testing
    X_train = [[0, 0], [1, 1]]
    y_train = [0, 1]
    
    model = train_model(X_train, y_train)
    
    assert model is not None
    assert hasattr(model, 'predict')

def test_evaluate_model():
    # Sample data for testing
    X_test = [[0, 0], [1, 1]]
    y_test = [0, 1]
    
    model = train_model(X_test, y_test)
    metrics = evaluate_model(model, X_test, y_test)
    
    assert metrics is not None
    assert 'accuracy' in metrics

def test_tune_hyperparameters():
    # Sample data for testing
    X_train = [[0, 0], [1, 1]]
    y_train = [0, 1]
    
    best_params = tune_hyperparameters(X_train, y_train)
    
    assert best_params is not None
    assert isinstance(best_params, dict)