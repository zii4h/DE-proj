import pandas as pd

# Each transform op is a function: (series) -> series
TRANSFORM_OPS = {
    "upper": lambda s: s.str.upper(),
    "lower": lambda s: s.str.lower(),
    "strip": lambda s: s.str.strip(),
}


def apply_transforms(df: pd.DataFrame, steps: list[dict]) -> pd.DataFrame:
    for step in steps or []:
        col = step["column"]
        op = step["op"]
        fn = TRANSFORM_OPS.get(op)
        if fn is None:
            raise ValueError(f"Unknown transform op: {op}")
        df[col] = fn(df[col])
        print(f"[transform] applied '{op}' to column '{col}'")
    return df
