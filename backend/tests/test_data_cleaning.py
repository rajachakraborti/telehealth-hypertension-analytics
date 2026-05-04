import pytest
from app.services.data_cleaning.imputation import mean_imputation, median_imputation
from app.services.data_cleaning.outlier_detection import detect_outliers
import pandas as pd

# Sample data for testing
data = pd.DataFrame({
    'A': [1, 2, 3, None, 5],
    'B': [5, 6, None, 8, 10],
    'C': [1, 2, 3, 4, 100]  # Outlier in column C
})

def test_mean_imputation():
    result = mean_imputation(data, 'A')
    expected = pd.Series([1, 2, 3, 2.75, 5])
    pd.testing.assert_series_equal(result, expected, check_names=False)

def test_median_imputation():
    result = median_imputation(data, 'B')
    expected = pd.Series([5, 6, 7, 8, 10])
    pd.testing.assert_series_equal(result, expected, check_names=False, check_dtype=False)

def test_detect_outliers():
    outliers = detect_outliers(data, 'C')
    expected_outliers = [100]
    assert list(outliers) == expected_outliers

def test_no_outliers():
    no_outlier_data = pd.DataFrame({'D': [1, 2, 3, 4, 5]})
    outliers = detect_outliers(no_outlier_data, 'D')
    assert len(outliers) == 0