from pathlib import Path
import sys
ROOT_FOR_IMPORT = Path(__file__).resolve().parents[1]
if str(ROOT_FOR_IMPORT) not in sys.path:
    sys.path.insert(0, str(ROOT_FOR_IMPORT))
import numpy as np
import pandas as pd
from backend.services import ingest

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "sample_orders.csv"

def main():
    rng = np.random.default_rng(42)
    dates = pd.date_range(end=pd.Timestamp.today().normalize(), periods=120, freq="D")
    products = {"Laptop Stand": 32, "USB Hub": 24, "Keyboard": 48, "Mouse": 18, "Monitor Arm": 72, "Webcam": 55}
    regions = ["West", "North", "South", "East"]
    rows, number = [], 1
    for date in dates:
        for _ in range(int(rng.integers(12, 28))):
            product = str(rng.choice(list(products)))
            qty = int(rng.integers(1, 5))
            price = round(products[product] * float(rng.normal(1, .08)), 2)
            if date == dates[-12] and rng.random() < .7: price *= .45
            rows.append({"order_id": f"ORD-{number:06d}", "order_date": date.strftime("%Y-%m-%d"),
                         "region": str(rng.choice(regions)), "product": product, "quantity": qty,
                         "unit_price": round(price, 2), "revenue": round(max(price, 0)*qty, 2),
                         "status": str(rng.choice(["completed", "pending", "cancelled"], p=[.82, .11, .07]))})
            number += 1
    df = pd.DataFrame(rows)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT, index=False)
    print("CSV:", OUT)
    print("Ingestion:", ingest(df, replace=True))

if __name__ == "__main__":
    main()
