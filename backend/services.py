import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from backend.database import connection, init_db

COLUMNS = ["order_id", "order_date", "region", "product", "quantity", "unit_price", "revenue", "status"]

def validate(df):
    missing = [c for c in COLUMNS if c not in df.columns]
    if missing:
        return {"valid": False, "rows": len(df), "errors": ["Missing columns: " + ", ".join(missing)]}
    errors = []
    if df["order_id"].isna().any(): errors.append("order_id has missing values")
    if df["order_id"].duplicated().any(): errors.append("order_id has duplicates")
    for col in ["order_date", "region", "product", "status"]:
        if df[col].isna().any(): errors.append(f"{col} has missing values")
    if pd.to_datetime(df["order_date"], errors="coerce").isna().any(): errors.append("order_date has invalid dates")
    for col in ["quantity", "unit_price", "revenue"]:
        values = pd.to_numeric(df[col], errors="coerce")
        if values.isna().any(): errors.append(f"{col} has non-numeric values")
        elif (values < 0).any(): errors.append(f"{col} has negative values")
    return {"valid": not errors, "rows": int(len(df)), "errors": errors}

def ingest(df, replace=False):
    report = validate(df)
    if not report["valid"]: return report
    data = df[COLUMNS].copy()
    data["order_date"] = pd.to_datetime(data["order_date"]).dt.strftime("%Y-%m-%d")
    data["quantity"] = pd.to_numeric(data["quantity"]).astype(int)
    for col in ["unit_price", "revenue"]: data[col] = pd.to_numeric(data[col]).astype(float)
    init_db()
    with connection() as conn:
        if replace: conn.execute("DELETE FROM orders")
        before = conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
        conn.executemany("INSERT OR IGNORE INTO orders VALUES (?, ?, ?, ?, ?, ?, ?, ?)", data[COLUMNS].itertuples(index=False, name=None))
        conn.commit()
        after = conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
    return {"valid": True, "rows": len(df), "inserted": int(after-before), "total_rows": int(after), "errors": []}

def orders():
    init_db()
    with connection() as conn:
        return pd.read_sql_query("SELECT * FROM orders ORDER BY order_date", conn)

def kpis():
    df = orders()
    if df.empty:
        return {"orders": 0, "revenue": 0.0, "avg_order_value": 0.0, "units_sold": 0, "completion_rate": 0.0, "regions": 0}
    total = float(df.revenue.sum())
    return {"orders": int(df.order_id.nunique()), "revenue": round(total, 2),
            "avg_order_value": round(total/max(df.order_id.nunique(), 1), 2),
            "units_sold": int(df.quantity.sum()),
            "completion_rate": round(float(df.status.str.lower().eq("completed").mean()*100), 2),
            "regions": int(df.region.nunique())}

def daily():
    df = orders()
    if df.empty: return []
    result = df.groupby("order_date", as_index=False).revenue.sum().sort_values("order_date")
    return [{"date": str(r.order_date), "revenue": round(float(r.revenue), 2)} for r in result.itertuples(index=False)]

def anomalies():
    rows = daily()
    if len(rows) < 7: return []
    df = pd.DataFrame(rows)
    df["baseline"] = df.revenue.rolling(7, min_periods=4).mean().shift(1)
    df["std"] = df.revenue.rolling(7, min_periods=4).std().shift(1)
    df["z_score"] = (df.revenue-df.baseline)/df["std"].replace(0, np.nan)
    result = df[df.z_score.abs() >= 2]
    return [{"date": str(r.date), "revenue": round(float(r.revenue), 2),
             "baseline": None if pd.isna(r.baseline) else round(float(r.baseline), 2),
             "z_score": None if pd.isna(r.z_score) else round(float(r.z_score), 2)}
            for r in result.itertuples(index=False)]

def forecast(days=7):
    days = max(1, min(int(days), 30))
    rows = daily()
    if not rows: return []
    df = pd.DataFrame(rows)
    df["date"] = pd.to_datetime(df.date)
    df = df.groupby("date", as_index=False).revenue.sum().sort_values("date")
    last_date = df.date.max()
    if len(df) < 3:
        values = [float(df.revenue.mean())] * days
        method = "mean baseline"
    else:
        df["t"] = (df.date-df.date.min()).dt.days
        model = LinearRegression().fit(df[["t"]], df.revenue)
        values = np.maximum(model.predict(pd.DataFrame({"t": range(int(df.t.max())+1, int(df.t.max())+days+1)})), 0)
        method = "linear trend baseline"
    return [{"date": (last_date+pd.Timedelta(days=i)).strftime("%Y-%m-%d"),
             "forecast_revenue": round(float(value), 2), "method": method}
            for i, value in enumerate(values, start=1)]
