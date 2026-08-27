import numpy as np
import pandas as pd
import logging

from sklearn.ensemble import IsolationForest

logger = logging.getLogger(__name__)

class AnomalyDetector():
    """Identifies anomaly from the data with the help of algorithm Isolation Forest
    """
    def __init__(self, contamination = 0.05 ,random_state = 42):
        self.contamination = contamination
        self.randome_state = random_state

    # finding anomalies with the help of Isolation Forest
    def detect(self, df: pd.DataFrame) -> pd.DataFrame:

        # removed the timeframe column
        df_new = df.drop("Time", axis = 1)

        model = IsolationForest(contamination = self.contamination, random_state = self.randome_state)
        model.fit(df_new)
        predictions = model.predict(df_new)

        # adding a new coloum of anomaly in the dataframe
        df_copy = df.copy()
        df_copy["anomaly"] = predictions

        anomalies = df[df_copy["anomaly"] == -1]

        # logging
        logger.info("anomalies found : %s", anomalies.shape[0])
        return anomalies
    
