import pytest

from pathlib import Path
import pandas as pd

from src.anomaly_detector import AnomalyDetector
from src.ingest import DataLoader

@pytest.fixture(scope = "module")
def anomaly_detector():
    return AnomalyDetector()

@pytest.fixture(scope = "module")
def dataloader():
    return DataLoader()

@pytest.fixture()
def path():
    return Path(__file__).parent/"fixtures"/"sample.csv"

def test_detect(anomaly_detector, dataloader, path):
    df = dataloader.csv_extractor(path)
    anomalies = anomaly_detector.detect(df)

    assert isinstance(anomalies, pd.DataFrame)
