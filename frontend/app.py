import os
import requests
import pandas as pd
import plotly.express as px
import streamlit as st

API = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")
st.set_page_config(page_title="NexusOps AI", page_icon="📊", layout="wide")
st.title("NexusOps AI")
st.caption("Enterprise Operations Intelligence — portfolio MVP")

def get(path, params=None):
    try:
        response = requests.get(f"{API}{path}", params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:
        st.error(f"API unavailable: {exc}. Start FastAPI at {API}.")
        return None

with st.sidebar:
    st.header("Controls")
    days = st.slider("Forecast horizon (days)", 1, 30, 7)
    if st.button("Refresh"): st.rerun()

overview, models, copilot, about = st.tabs(["Overview", "Anomalies & Forecast", "AI Copilot", "About"])
with overview:
    data = get("/kpis")
    if data:
        cols = st.columns(5)
        for col, label, key, fmt in zip(cols, ["Orders", "Revenue", "Avg. order value", "Units sold", "Completion rate"],
                                        ["orders", "revenue", "avg_order_value", "units_sold", "completion_rate"],
                                        ["{:,.0f}", "{:,.2f}", "{:,.2f}", "{:,.0f}", "{:.1f}%"]):
            val = data[key] * 1 if key != "completion_rate" else data[key]
            col.metric(label, fmt.format(val))
    series = get("/daily-revenue")
    if series and series["items"]:
        df = pd.DataFrame(series["items"])
        df["date"] = pd.to_datetime(df["date"])
        st.plotly_chart(px.line(df, x="date", y="revenue", markers=True, title="Daily revenue"), use_container_width=True)
        st.dataframe(df.sort_values("date", ascending=False), use_container_width=True)
    else:
        st.info("No data yet. Run `python scripts/seed_data.py`.")

with models:
    st.subheader("Potential revenue anomalies")
    result = get("/anomalies")
    if result and result["items"]: st.dataframe(pd.DataFrame(result["items"]), use_container_width=True)
    else: st.info("No flags found, or insufficient history.")
    st.subheader("Revenue forecast")
    result = get("/forecast", {"days": days})
    if result and result["items"]:
        fdf = pd.DataFrame(result["items"])
        st.caption("Baseline estimate only; validate before business use.")
        st.dataframe(fdf, use_container_width=True)
        st.plotly_chart(px.line(fdf, x="date", y="forecast_revenue", markers=True), use_container_width=True)

with copilot:
    question = st.text_input("Ask about operations", "Summarize business performance")
    if st.button("Run analysis", type="primary"):
        try:
            response = requests.post(f"{API}/copilot", json={"question": question}, timeout=30)
            response.raise_for_status()
            result = response.json()
            st.write(result["answer"])
            st.json(result["data"])
            st.markdown("**Tool execution trace**")
            st.dataframe(pd.DataFrame(result["trace"]), use_container_width=True)
        except requests.RequestException as exc:
            st.error(f"Copilot request failed: {exc}")

with about:
    st.markdown("""
    - API documentation: [Swagger UI](http://127.0.0.1:8000/docs)
    - Demo data is synthetic and stored in SQLite.
    - Agent routing is deterministic; this is not yet an autonomous LLM agent.
    - Forecasting and anomaly detection are baseline methods.
    - The local file-path ingestion endpoint must not be publicly exposed as-is.
    """)
