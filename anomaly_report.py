import pandas as pd
from pathlib import Path
from datetime import datetime

class AnomalyReport():
    def __init__(self):
        pass
    
    def report(self, df: pd.DataFrame, anomalies: pd.DataFrame, save_file_name: str):
        # removed the first time coloumn and last anomalies coloumn
        feature_column = df.columns[1:-1]

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
        anomalies["analysis"] = z_values["analysis"]

        # create csv from dataframe
        report_directory = Path.cwd()/"report"
        report_directory.mkdir(exist_ok = True)
        anomalies.to_csv(path_or_buf = report_directory/(save_file_name + ".csv"))
