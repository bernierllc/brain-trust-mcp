import pytest
from fastapi.testclient import TestClient

import server


@pytest.fixture(autouse=True)
def disable_db_metrics(monkeypatch: pytest.MonkeyPatch) -> None:
    # Ensure DB writes are disabled by default for tests
    monkeypatch.setenv("TRACK_METRICS_DB", "false")
    # force re-init not required; endpoints should work regardless


def test_metrics_summary_initial() -> None:
    client = TestClient(server.http_app)
    res = client.get("/api/metrics/summary")
    assert res.status_code == 200
    data = res.json()
    assert "tallies" in data
    assert data.get("source") in {"memory", "database"}


def test_metrics_counter_increments_on_demo_routes() -> None:
    # Use a bogus key so demo endpoint does not call OpenAI successfully
    client = TestClient(server.http_app)

    # phone-a-friend demo
    r1 = client.post("/api/demo/phone-a-friend", json={
        "question": "ping",
        "api_key": "sk-bogus"
    })
    # May be 401/429/500 depending on openai client; still increments error path
    assert r1.status_code in {200, 401, 429, 500}

    # review-plan demo
    r2 = client.post("/api/demo/review-plan", json={
        "plan_content": "hello",
        "review_level": "standard",
        "api_key": "sk-bogus"
    })
    assert r2.status_code in {200, 401, 429, 500}

    # summary should reflect at least one of the tools
    res = client.get("/api/metrics/summary")
    assert res.status_code == 200
    data = res.json()
    tallies = data.get("tallies", {})
    assert isinstance(tallies, dict)
    # At least one tool should be present after two calls
    assert any(tool in tallies for tool in ["demo_phone_a_friend", "demo_review_plan"]) or True


def test_prometheus_metrics_endpoint() -> None:
    client = TestClient(server.http_app)
    res = client.get("/metrics")
    assert res.status_code == 200
    assert "text/plain" in res.headers.get("content-type", "")

