from pathlib import Path
import random
import pandas as pd

OUT = Path("data/raw/sample_sales.csv")

def generate(rows: int = 10_000, seed: int = 42) -> Path:
    random.seed(seed)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    cities = ["Bengaluru", "Hyderabad", "Chennai", "Pune", "Delhi"]
    products = ["Laptop", "Phone", "Monitor", "Keyboard", "Mouse"]
    records = []
    for i in range(1, rows + 1):
        qty = random.randint(1, 5)
        price = random.choice([499, 999, 4999, 19999, 59999])
        records.append({
            "order_id": i,
            "order_date": pd.Timestamp("2026-01-01") + pd.Timedelta(days=random.randint(0, 179)),
            "city": random.choice(cities),
            "product": random.choice(products),
            "quantity": qty,
            "unit_price": price,
            "revenue": qty * price,
        })
    df = pd.DataFrame(records)
    # Add controlled quality issues so the cleaning stage has real work to do.
    df.loc[10, "city"] = None
    df = pd.concat([df, df.iloc[[25]]], ignore_index=True)
    df.to_csv(OUT, index=False)
    return OUT

if __name__ == "__main__":
    print(generate())
