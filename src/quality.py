import pandas as pd

REQUIRED = ["order_id", "order_date", "city", "product", "quantity", "unit_price", "revenue"]

def missing_required_columns(df: pd.DataFrame) -> list[str]:
    return [column for column in REQUIRED if column not in df.columns]

def validate_required_columns(df: pd.DataFrame) -> None:
    missing = missing_required_columns(df)
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")

def quality_report(df: pd.DataFrame) -> dict:
    return {
        "rows": int(len(df)),
        "duplicate_rows": int(df.duplicated().sum()),
        "missing_values": {k: int(v) for k, v in df.isna().sum().items() if v},
        "missing_columns": missing_required_columns(df),
    }

def clean(df: pd.DataFrame) -> pd.DataFrame:
    validate_required_columns(df)
    out = df.copy()
    out = out.drop_duplicates()
    out = out.dropna(subset=["order_id", "order_date", "city", "product"])
    out["order_date"] = pd.to_datetime(out["order_date"], errors="coerce")
    out = out.dropna(subset=["order_date"])
    for col in ["quantity", "unit_price", "revenue"]:
        out[col] = pd.to_numeric(out[col], errors="coerce")
    out = out.dropna(subset=["quantity", "unit_price", "revenue"])
    out = out[(out["quantity"] > 0) & (out["unit_price"] >= 0) & (out["revenue"] >= 0)]
    return out
