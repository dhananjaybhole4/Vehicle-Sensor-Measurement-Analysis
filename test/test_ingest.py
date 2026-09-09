import pytest
from pathlib import Path
import pandas as pd

from src.ingest import DataLoader

@pytest.fixture(scope = "module")
def dataloader():
    return DataLoader()

@pytest.fixture()
def path():
    return Path(__file__).parent/"fixtures"/"sample.csv"

def test_csv_extractor(dataloader, path):
    df = dataloader.csv_extractor(path)

    assert isinstance(df, pd.DataFrame)
    assert not df.empty
