"""Legacy per-reading trainer (kept for the pipeline UI). The staging model served to clinicians
is tested in test_abpm_service.py."""
import pytest

from app.services.modeling import model_trainer as mt
from scripts.synthetic_telemetry_generator import SyntheticTelemetryGenerator


@pytest.fixture(scope="module")
def telemetry_csv(tmp_path_factory):
    df = SyntheticTelemetryGenerator(num_patients=12, days_per_patient=2).generate_telemetry()
    path = tmp_path_factory.mktemp("telemetry") / "telemetry.csv"
    df.to_csv(path, index=False)
    return str(path), df


def test_legacy_trainer_splits_and_trains(telemetry_csv, tmp_path, monkeypatch):
    monkeypatch.setattr(mt, "MODEL_DIR", str(tmp_path))   # never overwrite the committed model
    path, _ = telemetry_csv
    trainer = mt.TelehealthModelTrainer(path)
    X_train, X_test, y_train, y_test = trainer.load_and_preprocess()
    assert len(X_train) + len(X_test) > 0 and list(X_train.columns) == trainer.feature_cols
    metrics, model = trainer.train_xgboost(X_train, X_test, y_train, y_test)
    assert {"accuracy", "precision", "recall"} <= set(metrics) and hasattr(model, "predict")
    assert (tmp_path / "xgboost_aha_model.pkl").exists()


def test_legacy_trainer_rejects_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        mt.TelehealthModelTrainer(str(tmp_path / "nope.csv")).load_and_preprocess()


def test_legacy_split_is_row_level_known_limitation(telemetry_csv):
    """Documents an audit finding: the legacy split is by reading, so one patient's readings can sit
    in both train and test. The ABPM staging model splits by patient (notebook section 4)."""
    path, df = telemetry_csv
    trainer = mt.TelehealthModelTrainer(path)
    X_train, X_test, _, _ = trainer.load_and_preprocess()
    pid = df.reset_index(drop=True)["patient_id"]
    shared = set(pid.loc[X_train.index]) & set(pid.loc[X_test.index])
    assert shared, "if this fails, the legacy split became patient-level; update the audit finding"
