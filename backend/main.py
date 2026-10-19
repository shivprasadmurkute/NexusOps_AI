from pathlib import Path
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from backend.database import init_db
from backend.services import kpis, daily, anomalies, forecast, ingest
from backend.agent import run

app = FastAPI(title="NexusOps AI API", version="0.1.0")

class CopilotRequest(BaseModel):
    question: str = Field(min_length=3, max_length=1000)
class IngestRequest(BaseModel):
    csv_path: str = Field(min_length=1, max_length=500)

@app.on_event("startup")
def startup():
    init_db()

@app.get("/health")
def health():
    return {"status": "ok", "service": "nexusops-ai"}

@app.get("/kpis")
def get_kpis():
    return kpis()

@app.get("/daily-revenue")
def get_daily():
    return {"items": daily()}

@app.get("/anomalies")
def get_anomalies():
    return {"items": anomalies()}

@app.get("/forecast")
def get_forecast(days: int = 7):
    if not 1 <= days <= 30: raise HTTPException(400, "days must be between 1 and 30")
    return {"items": forecast(days)}

@app.post("/copilot")
def copilot(body: CopilotRequest):
    return run(body.question)

@app.post("/ingest")
def ingest_csv(body: IngestRequest):
    # Local demo only. Do not expose publicly without authentication and file path restrictions.
    path = Path(body.csv_path).expanduser()
    if not path.is_file() or path.suffix.lower() != ".csv":
        raise HTTPException(400, "Provide an existing CSV file path on the API server.")
    try:
        result = ingest(pd.read_csv(path))
        if not result["valid"]: raise HTTPException(422, result)
        return result
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(400, f"CSV ingestion failed: {exc}")
