from fastapi.testclient import TestClient
from urllib.parse import quote
from uuid import uuid4
from src import app as myapp

client = TestClient(myapp.app)


def test_get_activities():
    res = client.get("/activities")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, dict)
    assert "Basketball Team" in data


def test_signup_and_unregister_flow():
    activity = "Art Studio"
    email = f"test-{uuid4().hex[:8]}@example.com"

    # ensure not registered
    assert email not in myapp.activities[activity]["participants"]

    # signup
    r = client.post(f"/activities/{quote(activity)}/signup?email={email}")
    assert r.status_code == 200
    assert email in myapp.activities[activity]["participants"]

    # unregister
    r2 = client.delete(f"/activities/{quote(activity)}/participants/{quote(email)}")
    assert r2.status_code == 200
    assert email not in myapp.activities[activity]["participants"]


def test_double_signup_returns_400():
    activity = "Basketball Team"
    existing = myapp.activities[activity]["participants"][0]
    r = client.post(f"/activities/{quote(activity)}/signup?email={existing}")
    assert r.status_code == 400


def test_unregister_nonexistent_returns_404():
    activity = "Art Studio"
    email = f"nope-{uuid4().hex[:8]}@example.com"
    r = client.delete(f"/activities/{quote(activity)}/participants/{quote(email)}")
    assert r.status_code == 404
