import numpy as np
import pandas as pd

from sklearn.ensemble import IsolationForest

class AnomalyDetector():
    """Identifies anomaly from the data with the help of algorithm Isolation Forest
    """
    def __init__(self, contamination = 0.05 ,random_state = 42):
        self.contamination = contamination
        self.randome_state = random_state

    # finding anomalies with the help of Isolation Forest
    def detect(self, df: pd.DataFrame) -> pd.DataFrame:

        # removed the timeframe column
        df_new = df.iloc[:,1:]

        model = IsolationForest(contamination = self.contamination, random_state = self.randome_state)
        model.fit(df_new)
        predictions = model.predict(df_new)

        # adding a new coloum of anomaly in the dataframe
        df["anomaly"] = predictions

        anomalies = df[df["anomaly"] == -1]
        return anomalies
    
