import pandas as pd
from src.quality import clean, quality_report

def test_quality_report_detects_duplicate_and_missing():
    df = pd.DataFrame([
        {"order_id": 1, "order_date": "2026-01-01", "city": "Bengaluru", "product": "Phone", "quantity": 1, "unit_price": 100, "revenue": 100},
        {"order_id": 1, "order_date": "2026-01-01", "city": "Bengaluru", "product": "Phone", "quantity": 1, "unit_price": 100, "revenue": 100},
        {"order_id": 2, "order_date": "2026-01-02", "city": None, "product": "Mouse", "quantity": 1, "unit_price": 20, "revenue": 20},
    ])
    report = quality_report(df)
    assert report["duplicate_rows"] == 1
    assert report["missing_values"]["city"] == 1
    cleaned = clean(df)
    assert len(cleaned) == 1
