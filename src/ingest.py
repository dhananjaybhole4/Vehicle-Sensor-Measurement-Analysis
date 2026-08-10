import pandas as pd
from pathlib import Path

class DataLoader():
    def __init__(self):
        pass

    # extracting data from csv file
    def csv_extractor(self, path: Path) -> pd.DataFrame:
        df = pd.read_csv(path)
        return df
            