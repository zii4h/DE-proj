from datetime import datetime, timezone
import pandas as pd
from sqlalchemy import inspect, create_engine, text


CATALOG_TABLE = "_pipeline_catalog"


def update_catalog(engine, table_name: str, df: pd.DataFrame, pipeline_name: str) -> None:
    """Inspects the just-loaded table and records its schema + row count.
    This is the toy version of Zwiron's 'Catalog' feature: after a sync,
    know what tables/columns exist without opening the DB by hand.
    """
    inspector = inspect(engine)
    columns = inspector.get_columns(table_name)

    rows = []
    ts = datetime.now(timezone.utc).isoformat()
    for col in columns:
        rows.append({
            "pipeline": pipeline_name,
            "table_name": table_name,
            "column_name": col["name"],
            "column_type": str(col["type"]),
            "row_count": len(df),
            "cataloged_at": ts,
        })

    catalog_df = pd.DataFrame(rows)
    catalog_df.to_sql(CATALOG_TABLE, engine, if_exists="append", index=False)
    print(f"[catalog] recorded {len(columns)} columns for '{table_name}' "
          f"({len(df)} rows) into '{CATALOG_TABLE}'")


def show_catalog(db_path: str) -> pd.DataFrame:
    """Convenience helper to peek at what's been cataloged so far."""
    engine = create_engine(f"sqlite:///{db_path}")
    with engine.connect() as conn:
        return pd.read_sql(text(f"SELECT * FROM {CATALOG_TABLE}"), conn)
