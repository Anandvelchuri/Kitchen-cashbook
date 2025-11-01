from fastapi.testclient import TestClient
import os
import tempfile

from backend.app import app
from backend import db


def setup_function():
    # use a temp DB for tests
    fd, path = tempfile.mkstemp(prefix="ck_test_")
    os.close(fd)
    os.environ["CK_DB_PATH"] = path
    db.init_db()


def teardown_function():
    path = os.environ.get("CK_DB_PATH")
    if path and os.path.exists(path):
        os.remove(path)


def test_create_and_summary():
    client = TestClient(app)
    r = client.post("/entries", json={
        "type": "income",
        "amount": 100.0,
        "category": "delivery",
        "date": "2025-10-01",
        "note": "test",
    })
    assert r.status_code == 200
    j = r.json()
    assert j["type"] == "income"

    r2 = client.post("/entries", json={
        "type": "expense",
        "amount": 30.0,
        "category": "supplies",
        "date": "2025-10-02",
    })
    assert r2.status_code == 200

    s = client.get("/summary", params={"month": "2025-10"})
    assert s.status_code == 200
    data = s.json()
    assert data["total_income"] == 100.0
    assert data["total_expense"] == 30.0
    assert data["balance"] == 70.0
