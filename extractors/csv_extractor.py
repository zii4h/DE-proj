import pandas as pd
from extractors.base import BaseExtractor


class CSVExtractor(BaseExtractor):
    """Reads a local CSV file into a DataFrame."""

    def extract(self) -> pd.DataFrame:
        path = self.config["path"]
        df = pd.read_csv(path)
        print(f"[extract] read {len(df)} rows from {path}")
        return df
