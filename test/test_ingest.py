import pytest
from pathlib import Path
import pandas as pd

from src.ingest import DataLoader

@pytest.fixture(scope = "module")
def dataloader():
    return DataLoader()

@pytest.fixture()
def path():
    return Path.cwd()/"dataset/10.35097-1130/data/dataset/OBD-II-Dataset/2017-07-26_Seat_Leon_S_KA_Normal.csv"

def test_csv_extractor(dataloader, path):
    df = dataloader.csv_extractor(path)

    assert isinstance(df, pd.DataFrame)
    assert not df.empty
