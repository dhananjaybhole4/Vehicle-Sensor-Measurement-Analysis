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
    return Path.cwd()/"dataset/10.35097-1130/data/dataset/OBD-II-Dataset/2017-07-26_Seat_Leon_S_KA_Normal.csv"

def test_detect(anomaly_detector, dataloader, path):
    df = dataloader.csv_extractor(path)
    anomalies = anomaly_detector.detect(df)

    assert isinstance(anomalies, pd.DataFrame)
    assert (anomalies["anomaly"] == -1).all()