import pandas as pd
from sqlalchemy import create_engine


# EXTRACT
df = pd.read_csv("data/customers.csv")

print("Extracted data:")
print(df)


# TRANSFORM
df["country"] = df["country"].str.upper()

print("\nTransformed data:")
print(df)


# LOAD
engine = create_engine("sqlite:///data/warehouse.db")

df.to_sql(
    "customers",
    engine,
    if_exists="replace",
    index=False
)

print("\nData loaded successfully.")