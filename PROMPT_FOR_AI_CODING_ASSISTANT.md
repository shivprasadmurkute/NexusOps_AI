# Master Prompt — Build NexusOps AI End-to-End

Copy the prompt below into your AI coding assistant to extend or rebuild the project.

---

Act as a senior data engineer, analytics engineer, data scientist, ML engineer, GenAI engineer, backend engineer, QA engineer, and DevOps engineer. Build **NexusOps AI**, an end-to-end Enterprise Operations Intelligence Platform. Deliver a complete runnable repository, not just an architecture or code snippets.

## Business goal
Help operations teams investigate KPI changes, identify potential anomalies, forecast operational metrics, and ask natural-language questions over trusted data. Every numerical claim must be grounded in actual query/model output.

## Required modules
1. **Ingestion and data quality:** CSV and REST connector interfaces; validate schemas, types, dates, duplicates, nulls, and business rules; generate quality reports; implement idempotent ingestion.
2. **Storage and modeling:** SQLite local profile and PostgreSQL production profile; schema migrations, indexes, parameterized queries, least-privilege credentials.
3. **Analytics:** documented KPI definitions, revenue/order/fulfillment metrics, date/region/product breakdowns, chart-ready API responses and dashboards.
4. **Machine learning:** anomaly detection and forecasting baselines; temporal train/test split; MAE/RMSE/MAPE as appropriate; reproducible training, model metadata, versioning, and drift checks. Never claim accuracy without held-out evaluation.
5. **GenAI/RAG:** provider abstraction for local Ollama or hosted LLM; retrieve business definitions/SOPs with source metadata; ground answers in SQL results and retrieved passages; cite sources; say when evidence is insufficient; validate outputs with Pydantic.
6. **Agent orchestration:** use LangGraph or a bounded explicit state machine. Provide approved KPI, read-only SQL, anomaly, forecast, and document-retrieval tools. Persist task state, step status, tool outputs, errors, retries, and timestamps. Limit tool calls, execution time, and retries. Require human approval for consequential write actions.
7. **Backend/UI:** FastAPI with typed schemas and useful errors; dashboard for KPIs, trends, anomalies, forecasts, data quality, and copilot; health checks and empty-data states.
8. **Security/operations:** no hard-coded secrets; `.env.example`; add authentication/authorization before public deployment; restrict SQL to allowlisted tables, read-only credentials, query timeouts, and row limits; validate uploads and never accept arbitrary server paths on a public endpoint; structured logs and audit events without sensitive payloads.
9. **Evaluation/testing:** unit, integration, ingestion, SQL-guard, and agent tests. Create a fixed evaluation set with expected tools/results and grounding criteria. Track tool-selection accuracy, SQL success, retrieval relevance, groundedness, latency, cost, and regressions.
10. **DevOps/docs:** Docker, compose, CI, lint/test commands, architecture diagram, API examples, sample data, troubleshooting guide, and Windows/macOS/Linux setup.

## Engineering requirements
- Inspect the existing repo first and preserve working functionality.
- Use modular code, type hints, docstrings, and clear naming.
- Handle empty data and errors explicitly; do not silently swallow exceptions.
- Never invent benchmark results, accuracy, or production deployment claims.
- Add tests for each behavior and run tests when tools are available.
- Update docs to match the implementation.
- Final report must list implemented features, exact run commands, tests actually run and their results, limitations, and next steps.

Start by inspecting the repository and implementing the highest-priority gaps. Produce complete files and verify imports and tests before declaring success.
