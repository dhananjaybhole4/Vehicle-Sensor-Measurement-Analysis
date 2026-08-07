from anomaly_detector import AnomalyDetector
import pandas as pd
from pathlib import Path

import pytest

@pytest.fixture(scope = "module")
def anomaly_detector():
    return AnomalyDetector()

def test_csv_extractor(anomaly_detector):
    path = Path.cwd()/Path("dataset/10.35097-1130/data/dataset/OBD-II-Dataset/2017-07-26_Seat_Leon_S_KA_Normal.csv")
    df = anomaly_detector.csv_extractor(path)

    assert not df.empty
    assert isinstance(df, pd.DataFrame)

def test_anomaly_detector(anomaly_detector):
    path = Path.cwd()/Path("dataset/10.35097-1130/data/dataset/OBD-II-Dataset/2017-07-26_Seat_Leon_S_KA_Normal.csv")
    anomalies = anomaly_detector.anomaly_detector(path)

    assert isinstance(anomalies, pd.DataFrame)
    assert "anomaly" in anomalies.columns
    assert (anomalies["anomaly"] == -1).all()
