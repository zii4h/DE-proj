from abc import ABC, abstractmethod
import pandas as pd


class BaseExtractor(ABC):
    """Every extractor pulls data from a source and returns a DataFrame."""

    def __init__(self, config: dict):
        self.config = config

    @abstractmethod
    def extract(self) -> pd.DataFrame:
        ...
