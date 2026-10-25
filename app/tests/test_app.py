import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app import app  # noqa: E402


def client():
    app.testing = True
    return app.test_client()


def test_health_needs_no_database():
    r = client().get("/health")
    assert r.status_code == 200 and r.get_json()["status"] == "ok"


def test_info_reports_tier():
    assert client().get("/api/info").get_json()["tier"] == "app"


def test_empty_note_is_rejected_before_touching_the_database():
    r = client().post("/api/notes", json={"text": "   "})
    assert r.status_code == 400


def test_too_long_note_is_rejected():
    r = client().post("/api/notes", json={"text": "x" * 501})
    assert r.status_code == 400
