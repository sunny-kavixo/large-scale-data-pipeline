# Large-Scale Data Pipeline

A portfolio ETL project that demonstrates practical data-engineering fundamentals with **Python, Pandas, PostgreSQL, SQL, Git, data-quality checks, logging, and tests**.

## What it does

1. Generates 10,000 synthetic sales records plus controlled quality issues.
2. Reads raw CSV data with Pandas.
3. Detects duplicates, missing values, and schema problems.
4. Cleans and validates the dataset.
5. Writes a reproducible processed CSV.
6. Optionally loads the cleaned data into PostgreSQL.
7. Provides SQL queries for city, product, and monthly revenue analysis.
8. Includes automated tests for the quality layer.

> All data is synthetic. No production or employer data is used, and no performance claims are fabricated.

## Architecture

```text
Synthetic data
     |
     v
data/raw/sample_sales.csv
     |
     v
Python + Pandas ETL
     |
     +----> Data-quality report
     |
     +----> data/processed/clean_sales.csv
     |
     v
PostgreSQL
     |
     v
SQL analytics
```

## Tech stack

- Python
- Pandas
- PostgreSQL
- SQLAlchemy + psycopg
- SQL
- pytest
- Docker Compose

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python -m src.generate_data
python -m src.pipeline
pytest
```

The pipeline works without PostgreSQL and writes the cleaned CSV locally. To enable the database stage:

```bash
docker compose up -d
cp .env.example .env
python -m src.pipeline
```

Then run the queries in `sql/analytics.sql` against the `sales` table.

## Repository structure

```text
src/
  generate_data.py   # reproducible synthetic dataset
  quality.py         # validation and cleaning
  pipeline.py        # ETL orchestration + optional PostgreSQL load
sql/
  analytics.sql      # business-analysis queries
tests/
  test_quality.py    # automated quality tests
data/
  raw/               # generated locally
  processed/         # generated locally
```

## Why I built this

I built this project to practice the kind of data transformation, database, and reliability work used in data-heavy software systems. The focus is on readable code, reproducibility, honest metrics, and a pipeline that can be run locally rather than a screenshot-only portfolio project.

## Next improvements

- Batch/chunk processing for larger local datasets
- Incremental loads and idempotency
- PostgreSQL indexes and query-plan analysis
- CI with GitHub Actions
- Structured JSON logging and pipeline metrics
