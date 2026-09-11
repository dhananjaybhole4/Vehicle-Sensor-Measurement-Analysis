import pandas as pd
from pathlib import Path

from src.ingest import DataLoader
from src.anomaly_detector import AnomalyDetector
from src.anomaly_report import AnomalyReport

FIXTURE_PATH = Path(__file__).parent/"fixtures"/"sample.csv"

def test_full_pipeline_runs_end_to_end(tmp_path):

    report_path = Path(tmp_path)/"test_output.csv"

    # create object of the following classes
    loader = DataLoader()
    detector = AnomalyDetector()
    reporter = AnomalyReport()

    # Act
    df = loader.csv_extractor(FIXTURE_PATH)
    anomalies = detector.detect(df)
    _ = reporter.report(df, anomalies, Path(tmp_path), "test_output")

    # assert
    # check whether saved report exist
    assert report_path.exists()

    # check whether the report have analysis column
    report = pd.read_csv(report_path)
    assert "analysis" in report.columns

    # check whether rows in the report are in range of total rows in input csv file
    assert report.shape[0] > 0 and report.shape[0] <= df.shape[0] 

    # check if the calculation of |z| values are correct (we will check on point 1. [12,0] (|z| = 4.249), 
    #                                                                            2. [15,4] (|z| = 3.75), 
    #                                                                            3. [16,1] (|z| = 4.129) as we know this are anomalies.
    assert abs(float(report.loc[4,"analysis"].split(" ")[-1][:-1]) - 4.249) <= 0.1  
    assert abs(float(report.loc[5,"analysis"].split(" ")[-1][:-1]) - 3.75) <= 0.1
    assert abs(float(report.loc[6,"analysis"].split(" ")[-1][:-1]) - 4.129) <= 0.1
    