import pandas as pd
import pytest

from src import pipeline
from src.quality import REQUIRED, clean, quality_report, validate_required_columns


VALID_ROW = {
    "order_id": 1,
    "order_date": "2026-01-01",
    "city": "Bengaluru",
    "product": "Phone",
    "quantity": 1,
    "unit_price": 100,
    "revenue": 100,
}

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


@pytest.mark.parametrize("missing_column", REQUIRED)
def test_each_missing_required_column_is_rejected(missing_column):
    row = {key: value for key, value in VALID_ROW.items() if key != missing_column}

    with pytest.raises(ValueError) as exc_info:
        clean(pd.DataFrame([row]))

    assert str(exc_info.value) == f"Missing required columns: {missing_column}"


def test_multiple_missing_columns_are_reported_in_schema_order():
    row = {
        key: value
        for key, value in VALID_ROW.items()
        if key not in {"order_id", "city", "revenue"}
    }
    frame = pd.DataFrame([row])

    with pytest.raises(ValueError) as exc_info:
        validate_required_columns(frame)

    assert str(exc_info.value) == "Missing required columns: order_id, city, revenue"
    assert quality_report(frame)["missing_columns"] == ["order_id", "city", "revenue"]


def test_valid_input_reporting_and_cleaning_are_preserved():
    frame = pd.DataFrame([VALID_ROW])

    validate_required_columns(frame)
    report = quality_report(frame)
    cleaned = clean(frame)

    assert report["missing_columns"] == []
    assert report["rows"] == 1
    assert cleaned.to_dict(orient="records") == [
        {**VALID_ROW, "order_date": pd.Timestamp("2026-01-01")},
    ]


def test_pipeline_validation_has_no_output_or_database_side_effects(tmp_path, monkeypatch):
    source = tmp_path / "missing-city.csv"
    output = tmp_path / "results" / "clean.csv"
    row = {key: value for key, value in VALID_ROW.items() if key != "city"}
    pd.DataFrame([row]).to_csv(source, index=False)
    monkeypatch.setenv("DATABASE_URL", "postgresql://not-used")

    def unexpected_database_access(_url):
        raise AssertionError("database access occurred before schema validation")

    monkeypatch.setattr(pipeline, "create_engine", unexpected_database_access)

    with pytest.raises(ValueError) as exc_info:
        pipeline.run(str(source), str(output))

    assert str(exc_info.value) == "Missing required columns: city"
    assert not output.exists()
    assert not output.parent.exists()


def test_valid_pipeline_input_preserves_output_behavior(tmp_path, monkeypatch):
    source = tmp_path / "valid.csv"
    output = tmp_path / "results" / "clean.csv"
    pd.DataFrame([VALID_ROW]).to_csv(source, index=False)
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.setattr(pipeline, "load_dotenv", lambda: None)

    result = pipeline.run(str(source), str(output))

    assert output.exists()
    assert result == {
        "before": {
            "rows": 1,
            "duplicate_rows": 0,
            "missing_values": {},
            "missing_columns": [],
        },
        "after": {
            "rows": 1,
            "duplicate_rows": 0,
            "missing_values": {},
            "missing_columns": [],
        },
        "output": str(output),
    }
    assert pd.read_csv(output).to_dict(orient="records") == [VALID_ROW]


def test_validation_error_does_not_expose_row_content():
    frame = pd.DataFrame([{"order_id": "private-row-value"}])

    with pytest.raises(ValueError) as exc_info:
        validate_required_columns(frame)

    assert "private-row-value" not in str(exc_info.value)
