# NexusOps AI — End-to-End Operations Intelligence MVP

A runnable portfolio project combining data ingestion, validation, SQL analytics, anomaly detection, forecasting, FastAPI, Streamlit, and a bounded tool-using copilot.

## Requirements
Python 3.11 recommended. No API key is required; the demo uses synthetic data and SQLite.

## Run on Windows PowerShell
```powershell
cd NexusOps_AI
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python scripts\seed_data.py
uvicorn backend.main:app --reload
```
Open a second PowerShell terminal, activate the same environment, then:
```powershell
cd NexusOps_AI
.\.venv\Scripts\Activate.ps1
streamlit run frontend\app.py
```
API docs: http://127.0.0.1:8000/docs
Dashboard: http://localhost:8501

If activation is blocked:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## Run on macOS/Linux
```bash
cd NexusOps_AI
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/seed_data.py
uvicorn backend.main:app --reload
```
In a second terminal:
```bash
cd NexusOps_AI
source .venv/bin/activate
streamlit run frontend/app.py
```

## Docker
```bash
docker compose up --build
```
Dashboard: http://localhost:8501 · API docs: http://localhost:8000/docs

## Endpoints
- `GET /health`
- `GET /kpis`
- `GET /daily-revenue`
- `GET /anomalies`
- `GET /forecast?days=7` (1–30 days)
- `POST /copilot` with `{"question":"Show revenue anomalies"}`
- `POST /ingest` with `{"csv_path":"data/sample_orders.csv"}` for local demo use only

## Tests
```bash
pytest -q
```

## Example copilot questions
- Summarize business performance
- Show revenue anomalies
- Forecast revenue for the next 7 days
- Show the daily revenue trend

## Structure
```text
backend/       FastAPI, database, analytics, agent router
frontend/      Streamlit dashboard
scripts/       Synthetic data generator and loader
tests/         Basic unit and API tests
data/          Generated CSV and SQLite database
PROMPT_FOR_AI_CODING_ASSISTANT.md
```

## Important limitations
This is a local portfolio MVP, not a certified production system. It uses synthetic data, SQLite, a simple linear-trend forecast, statistical anomaly flags, and deterministic tool routing rather than a fully autonomous LLM. The `/ingest` endpoint accepts a server-local file path and must not be exposed publicly as-is. Before production use, add authentication/authorization, managed secrets, safer file upload, database migrations, robust monitoring, formal model/LLM evaluation, and privacy controls. Do not claim production deployment or model accuracy without evidence.
