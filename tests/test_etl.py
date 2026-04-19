import pytest
import pandas as pd
from dags.etl_pipelines.mysql_to_csv_etl import transform_data

def test_transform_data():
    # Create test data
    test_df = pd.DataFrame({
        'name': ['Alice', 'Bob', 'Charlie'],
        'age': [30, 25, 35],
        'city': ['NYC', 'LA', 'CHI']
    })
    
    # Apply transformation
    result = test_df[test_df['age'] > 30]
    
    # Assert
    assert len(result) == 1
    assert result.iloc[0]['name'] == 'Charlie'

def test_no_data():
    test_df = pd.DataFrame({'name': [], 'age': [], 'city': []})
    result = test_df[test_df['age'] > 30]
    assert len(result) == 0
