import pandas as pd

REQUIRED = ["order_id", "order_date", "city", "product", "quantity", "unit_price", "revenue"]

def quality_report(df: pd.DataFrame) -> dict:
    missing_columns = [c for c in REQUIRED if c not in df.columns]
    return {
        "rows": int(len(df)),
        "duplicate_rows": int(df.duplicated().sum()),
        "missing_values": {k: int(v) for k, v in df.isna().sum().items() if v},
        "missing_columns": missing_columns,
    }

def clean(df: pd.DataFrame) -> pd.DataFrame:
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
