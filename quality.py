from datetime import datetime, timezone
import pandas as pd


QUALITY_TABLE = "_pipeline_quality_runs"


def run_checks(engine, table_name: str, df: pd.DataFrame, checks: list[dict], pipeline_name: str) -> list[dict]:
    """Runs simple post-load quality checks and logs pass/fail per check.
    This is the toy version of Zwiron's 'Quality' feature: catch obviously
    bad loads (empty tables, unexpected nulls) right after a run.
    """
    results = []
    ts = datetime.now(timezone.utc).isoformat()

    for check in checks or []:
        check_type = check["check"]

        if check_type == "not_empty":
            passed = len(df) > 0
            detail = f"{len(df)} rows"

        elif check_type == "no_nulls":
            col = check["column"]
            null_count = df[col].isna().sum()
            passed = null_count == 0
            detail = f"{null_count} nulls in '{col}'"

        else:
            raise ValueError(f"Unknown check type: {check_type}")

        results.append({
            "pipeline": pipeline_name,
            "table_name": table_name,
            "check": check_type,
            "passed": bool(passed),
            "detail": detail,
            "run_at": ts,
        })
        status = "PASS" if passed else "FAIL"
        print(f"[quality] {status} — {check_type} ({detail})")

    if results:
        pd.DataFrame(results).to_sql(QUALITY_TABLE, engine, if_exists="append", index=False)

    return results
