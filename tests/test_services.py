import pandas as pd
from backend.services import validate

def test_valid_data():
    df = pd.DataFrame([{"order_id":"A1","order_date":"2025-01-01","region":"West","product":"Mouse","quantity":2,"unit_price":10,"revenue":20,"status":"completed"}])
    assert validate(df)["valid"]

def test_missing_columns_rejected():
    report = validate(pd.DataFrame([{"order_id":"A1"}]))
    assert not report["valid"]
    assert "Missing columns" in report["errors"][0]
