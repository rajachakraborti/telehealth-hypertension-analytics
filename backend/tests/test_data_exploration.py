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