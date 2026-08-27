from src.anomaly_detector import AnomalyDetector
from src.ingest import DataLoader
from src.anomaly_report import AnomalyReport

from pathlib import Path
import argparse
import logging

# path variables
path = Path.cwd()/"dataset/10.35097-1130/data/dataset/OBD-II-Dataset"

logging_dict = {"debug": logging.DEBUG,
                "info": logging.INFO,
                "warning": logging.WARNING,
                "error": logging.ERROR,
                "fatal": logging.FATAL}

def main(path):

    parser = argparse.ArgumentParser()
    parser.add_argument("file_name")
    parser.add_argument("save_file_name")
    parser.add_argument("--logging", default = "warning")

    args = parser.parse_args()

    # logging
    logging.basicConfig(level = logging_dict[(args.logging).lower()], format = "%(asctime)s | %(levelname)s | %(name)s | %(message)s")

    # extract data from csv
    dataloader = DataLoader()
    df = dataloader.csv_extractor(path/args.file_name)

    # get anamomalies using the defined Anomaly Detector class
    anomaly_detector = AnomalyDetector()
    anomalies = anomaly_detector.detect(df)

    # get report
    anomaly_report = AnomalyReport()
    anomaly_report.report(df, anomalies, args.save_file_name)

if __name__ == "__main__":
    main(path)