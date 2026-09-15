import pandas as pd
from sqlalchemy import create_engine
from loaders.base import BaseLoader


class SQLiteLoader(BaseLoader):
    """Writes a DataFrame into a SQLite table. mode: 'replace' or 'append'."""

    def __init__(self, config: dict):
        super().__init__(config)
        self._engine = create_engine(f"sqlite:///{config['db']}")

    def get_engine(self):
        return self._engine

    def load(self, df: pd.DataFrame) -> None:
        table = self.config["table"]
        mode = self.config.get("mode", "replace")
        df.to_sql(table, self._engine, if_exists=mode, index=False)
        print(f"[load] wrote {len(df)} rows to '{table}' ({mode}) in {self.config['db']}")
