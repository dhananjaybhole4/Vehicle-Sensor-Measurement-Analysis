import pandas as pd
from pathlib import Path

import logging

logger = logging.getLogger(__name__)

class DataLoader():
    def __init__(self):
        pass

    # extracting data from csv file
    def csv_extractor(self, path: Path) -> pd.DataFrame:
        try:
            df = pd.read_csv(path)

            # logging
            logger.debug("columns: %s, shape: %s", df.columns.tolist(), df.shape)
            logger.info("data successfully loaded with %s rows", df.shape[0])

            if df.empty:
                logger.warning("csv is empty")
            elif df.isna().any().any():
                logger.warning("%s data points are missing in csv", df.isna().sum().sum())

            return df
        except FileNotFoundError:
            logger.error("given csv file doesnt exist")
            raise FileNotFoundError("csv file doesnt exist")
        except pd.errors.ParserError:
            logger.error("given csv is corrupt")
            raise ValueError("csv is corrupt")