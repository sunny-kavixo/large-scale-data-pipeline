import logging
import os
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
from src.quality import clean, quality_report

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

def run(input_path: str = "data/raw/sample_sales.csv", output_path: str = "data/processed/clean_sales.csv") -> dict:
    load_dotenv()
    df = pd.read_csv(input_path)
    before = quality_report(df)
    clean_df = clean(df)
    after = quality_report(clean_df)

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    clean_df.to_csv(output, index=False)

    database_url = os.getenv("DATABASE_URL")
    if database_url:
        engine = create_engine(database_url)
        clean_df.to_sql("sales", engine, if_exists="replace", index=False, chunksize=1000, method="multi")
        log.info("Loaded %s rows into PostgreSQL table sales", len(clean_df))
    else:
        log.info("DATABASE_URL not set; PostgreSQL load skipped.")

    result = {"before": before, "after": after, "output": str(output)}
    log.info("Pipeline result: %s", result)
    return result

if __name__ == "__main__":
    run()
