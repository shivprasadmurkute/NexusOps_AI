from backend.services import kpis, anomalies, forecast, daily

def run(question):
    q = question.lower()
    trace, data = [], {}
    if any(w in q for w in ["anomal", "unusual", "spike", "drop", "decline"]):
        data["anomalies"] = anomalies()
        trace.append({"tool": "detect_anomalies", "status": "success", "detail": f"{len(data['anomalies'])} potential flags"})
        answer = (f"Found {len(data['anomalies'])} potential anomaly point(s). These statistical flags do not establish the cause."
                  if data["anomalies"] else "No anomalies were flagged, or there is not enough history. This does not prove performance is normal.")
    elif "forecast" in q or "predict" in q:
        import re
        match = re.search(r"(\d{1,2})\s*days?", q)
        days = min(int(match.group(1)), 30) if match else 7
        data["forecast"] = forecast(days)
        trace.append({"tool": "forecast_revenue", "status": "success", "detail": f"{days}-day baseline forecast"})
        answer = f"Generated a {days}-day forecast using a simple baseline. Validate it before business use."
    elif "daily" in q or "trend" in q:
        data["daily_revenue"] = daily()
        trace.append({"tool": "daily_revenue", "status": "success", "detail": f"{len(data['daily_revenue'])} daily records"})
        answer = "Here is the daily revenue trend calculated from the database."
    else:
        data["kpis"] = kpis()
        trace.append({"tool": "get_kpis", "status": "success", "detail": "KPIs calculated from stored records"})
        x = data["kpis"]
        answer = f"Business snapshot: {x['orders']} orders, revenue {x['revenue']:.2f}, average order value {x['avg_order_value']:.2f}, {x['units_sold']} units sold, completion rate {x['completion_rate']:.1f}%."
    return {"answer": answer, "data": data, "trace": trace}
