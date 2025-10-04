## Testing Guide

This project ships two complementary test suites:

- Python tests (pytest) for the MCP server and tools
- Playwright end-to-end (E2E) tests for the frontend demo flows

Both suites can run locally. Integration tests that call OpenAI require an API key in a local `.env` file.

---

### Prerequisites

- Python 3.12+
- Node.js 18+ and npm
- Docker (optional, recommended for running the server)

Create a `.env` file at the project root for integration/E2E tests:

```
OPENAI_API_KEY=sk-...
# Optional override for Playwright base URL
# BASE_URL=http://localhost:8000
```

---

### Backend Tests (pytest)

Install dependencies:

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Run all tests:

```
pytest tests/
```

Coverage report:

```
pytest --cov=server --cov-report=term-missing tests/
```

Targeted subsets:

```
# Unit tests only (no OpenAI calls)
pytest tests/test_logging.py

# Integration tests (call OpenAI; require OPENAI_API_KEY)
pytest tests/test_tools.py
```

Notes:

- Integration tests are skipped automatically if `OPENAI_API_KEY` is not set
- See `tests/README.md` for additional details

---

### Run the Server for E2E

You can run the server either with Docker or locally:

```
# Docker (recommended)
docker compose up -d

# OR local Python
python server.py
```

Health check:

```
curl http://localhost:8000/health
```

---

### Frontend E2E Tests (Playwright)

Install Node dependencies and Playwright browsers:

```
npm install
npx playwright install --with-deps
```

Ensure the server is running on `http://localhost:8000` (default base URL). You can override with `BASE_URL` in `.env`.

Run the tests:

```
# Headless run
npx playwright test

# Headed / UI modes
npx playwright test --headed
npx playwright test --ui
```

What the tests cover:

- `phone_a_friend` demo flow: fills API key, question (and optional context), expects a non-empty answer
- `review_plan` demo flow: fills API key and plan content, expects structured JSON-like feedback

Implementation files:

- Playwright config: `playwright.config.ts` (loads `.env`, sets `baseURL`)
- Tests: `tests-e2e/home.spec.ts`

---

### Troubleshooting

- Missing API key: set `OPENAI_API_KEY` in `.env`
- Server not reachable: ensure it is running (`docker compose logs -f`, or `python server.py`) and responding at `/health`
- Playwright dependencies: re-run `npx playwright install --with-deps`
- Rate limits or model errors: re-run later or switch models in server if applicable

---

### Useful Commands (summary)

```
# Python tests
pytest tests/
pytest --cov=server --cov-report=term-missing tests/

# Playwright tests
npm install && npx playwright install --with-deps
npx playwright test
```


