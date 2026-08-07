import numpy as np
import pandas as pd

from sklearn.ensemble import IsolationForest

class AnomalyDetector():
    """Identifies anomaly from the data with the help of algorithm Isolation Forest
    """
    def __init__(self):
        None

    # extracting data from csv using pandas
    def csv_extractor(self, csv_path):
        df = pd.read_csv(csv_path)
        return df

    # finding anomalies with the help of Isolation Forest
    def anomaly_detector(self, csv_path):

        df = self.csv_extractor(csv_path)
        # removed the timeframe column
        df_new = df.iloc[:,1:]

        model = IsolationForest(contamination = 0.05, random_state = 42)
        model.fit(df_new)
        predictions = model.predict(df_new)

        # adding a new coloum of anomaly in the dataframe
        df["anomaly"] = predictions

        anomalies = df[df["anomaly"] == -1]
        return anomalies
    
