from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_health():
    result = client.get("/health")
    assert result.status_code == 200
    assert result.json()["status"] == "ok"

def test_forecast_horizon_validation():
    assert client.get("/forecast?days=100").status_code == 400

def test_copilot_shape():
    result = client.post("/copilot", json={"question":"Summarize business performance"})
    assert result.status_code == 200
    assert "answer" in result.json()
    assert "trace" in result.json()
