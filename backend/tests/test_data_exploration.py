import pytest
from app.services.data_exploration.statistics import calculate_summary_statistics
from app.services.data_exploration.visualization_data import prepare_visualization_data

@pytest.fixture
def sample_data():
    return [
        {"age": 45, "systolic": 130, "diastolic": 85},
        {"age": 50, "systolic": 140, "diastolic": 90},
        {"age": 60, "systolic": 150, "diastolic": 95},
        {"age": 55, "systolic": 160, "diastolic": 100},
        {"age": 40, "systolic": 120, "diastolic": 80},
    ]

def test_calculate_summary_statistics(sample_data):
    stats = calculate_summary_statistics(sample_data)
    assert stats['mean_systolic'] == 140
    assert stats['mean_diastolic'] == 90
    assert stats['median_systolic'] == 140
    assert stats['median_diastolic'] == 90

def test_prepare_visualization_data(sample_data):
    visualization_data = prepare_visualization_data(sample_data)
    assert len(visualization_data) == 5
    assert 'age' in visualization_data[0]
    assert 'systolic' in visualization_data[0]
    assert 'diastolic' in visualization_data[0]


def test_dashboard_matches_columns_regardless_of_case(tmp_path):
    """The shipped sample uses 'Hypertension' and 'SystolicBP'; the risk score must not silently fall back to 0%."""
    import asyncio
    from app.api.endpoints.data_exploration import DatasetRequest, get_dashboard
    csv = tmp_path / "patients.csv"
    csv.write_text("PatientID,Age,SystolicBP,Hypertension\n1,50,150,1\n2,40,120,0\n3,60,160,1\n4,30,110,0\n")
    out = asyncio.run(get_dashboard(DatasetRequest(dataset_id=str(csv))))
    assert out["risk_score"] == 50.0 and out["total_patients"] == 4
    assert out["stats"]["systolic_bp"] == 135.0


def test_dashboard_falls_back_to_systolic_when_no_label_column(tmp_path):
    import asyncio
    from app.api.endpoints.data_exploration import DatasetRequest, get_dashboard
    csv = tmp_path / "bp.csv"
    csv.write_text("Systolic_BP\n150\n150\n")
    assert asyncio.run(get_dashboard(DatasetRequest(dataset_id=str(csv))))["risk_score"] == 50.0
