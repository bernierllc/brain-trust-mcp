# Release v0.4.0 - Metrics, Redaction, and DB-backed Counters

## Summary
- Prometheus `/metrics` endpoint and in-memory tallies
- Homepage metrics widget displaying per-tool success/error totals
- Optional Postgres-backed daily request counters (gated by `TRACK_METRICS_DB`), with auto table creation
- Sensitive log redaction and demo routes gated by `ENABLE_DEMOS`
- Tests: pytest for `/metrics` and `/api/metrics/summary`, Playwright E2E validates widget

## Changes
- `server.py`:
  - Add Prometheus counters and `/metrics`
  - Add in-memory tallies and `/api/metrics/summary`
  - Add `TRACK_METRICS_DB` gating; `DATABASE_URL`/`SUPABASE_DB_URL` support
  - Auto-create `public.request_counts` if missing
  - Redact sensitive request content and headers in logs
  - Gate demo routes with `ENABLE_DEMOS` (default on in dev, off in prod)
- `requirements.txt`/`pyproject.toml`: add `prometheus-client`, `psycopg[binary]`
- Frontend: `Metrics` widget component wired into homepage
- Tests:
  - `tests/test_metrics.py` for API endpoints
  - `tests-e2e/metrics.spec.ts` for UI widget

## Breaking Changes
- None

## Upgrade Notes
- To persist metrics, set in `.env`:

```
TRACK_METRICS_DB=true
DATABASE_URL=postgresql://user:pass@host:5432/dbname
# or SUPABASE_DB_URL=...
```

- In production, leave `ENABLE_DEMOS=false` (default). Locally, demos are enabled for easy traffic generation.

## PR
- Pull Request: #10
