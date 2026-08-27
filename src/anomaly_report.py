import pandas as pd
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class AnomalyReport():
    def __init__(self):
        pass
    
    def report(self, df: pd.DataFrame, anomalies: pd.DataFrame, save_file_name: str):
        # removed the first time coloumn
        feature_column = df.drop("Time", axis = 1).columns

        # calculate mean and std across feature columns
        means = df[feature_column].mean()
        stds = df[feature_column].std()

        # calculate z values for each value in anomalies
        z_values = abs((anomalies[feature_column] - means)/stds)
        for index, row in z_values.iterrows():
            analysis = []
            for column, value in row.items():
                if value > 3:
                    analysis.append(f"{column} (z = {value:.2f})")
            z_values.loc[index, "analysis"] = ",".join(analysis)

        # add a coloum of analysis in anomalies
        anomaly_report = anomalies.copy()
        anomaly_report["analysis"] = z_values["analysis"]

        # create csv from dataframe
        report_directory = Path.cwd()/"report"
        report_directory.mkdir(exist_ok = True)

        PATH = report_directory/(save_file_name + ".csv")
        try:
            anomaly_report.to_csv(path_or_buf = PATH)

            # logging
            if not PATH.exists():
                logger.warning("Anomaly report not made")        
            else:
                logger.debug("shape of anomaly report %s", anomalies.shape)
                logger.info("Anomaly report made successfully")
        except OSError:
            logger.error("failed in making a csv Anomaly report")
            raise OSError("failed in making a csv Anomaly report")