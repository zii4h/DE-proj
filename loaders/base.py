from abc import ABC, abstractmethod
import pandas as pd
from sqlalchemy.engine import Engine


class BaseLoader(ABC):
    """Every loader writes a DataFrame to a target and exposes its engine
    so the catalog/quality steps can inspect what landed."""

    def __init__(self, config: dict):
        self.config = config

    @abstractmethod
    def load(self, df: pd.DataFrame) -> None:
        ...

    @abstractmethod
    def get_engine(self) -> Engine:
        ...
