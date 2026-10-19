import os
import sqlite3
from pathlib import Path
from contextlib import contextmanager

ROOT = Path(__file__).resolve().parents[1]

def db_path():
    value = os.getenv("NEXUSOPS_DB_PATH", "data/nexusops.db")
    path = Path(value)
    if not path.is_absolute():
        path = ROOT / path
    path.parent.mkdir(parents=True, exist_ok=True)
    return path

@contextmanager
def connection():
    conn = sqlite3.connect(db_path(), timeout=15)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    with connection() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS orders (
          order_id TEXT PRIMARY KEY,
          order_date TEXT NOT NULL,
          region TEXT NOT NULL,
          product TEXT NOT NULL,
          quantity INTEGER NOT NULL,
          unit_price REAL NOT NULL,
          revenue REAL NOT NULL,
          status TEXT NOT NULL
        )""")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_orders_date ON orders(order_date)")
        conn.commit()
