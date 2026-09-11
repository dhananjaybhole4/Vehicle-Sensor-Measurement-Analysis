from src.anomaly_detector import AnomalyDetector
from src.ingest import DataLoader
from src.anomaly_report import AnomalyReport
from src.anomaly_explainer import AnomalyExplainer

from pathlib import Path
import argparse
import logging

# API calling
from dotenv import load_dotenv
import os

load_dotenv()

# path variables
dataset_path = Path(__file__).parent/"dataset/10.35097-1130/data/dataset/OBD-II-Dataset"

report_path = Path(__file__).parent/"report"

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
    df = dataloader.csv_extractor(path/(args.file_name+".csv"))

    # get anamomalies using the defined Anomaly Detector class
    anomaly_detector = AnomalyDetector()
    anomalies = anomaly_detector.detect(df)
    print(f"total anomalies capture:{anomalies["Time"].shape}")

    # get report
    anomaly_report = AnomalyReport()
    filtered_dataframe = anomaly_report.report(df, anomalies, report_path, args.save_file_name)

    # get a summary about the anomalies from AI
    api_key = os.environ["GEMINI_API_KEY"]
    anomaly_explainer = AnomalyExplainer(api_key)
    summary = anomaly_explainer.ai_explainer(filtered_dataframe, args.file_name)
    print(summary)

if __name__ == "__main__":
    main(dataset_path)