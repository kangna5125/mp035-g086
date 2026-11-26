from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

VALID = {
    "pm25_today": 150.0,
    "wind_kmph": 12.0,
    "humidity_pct": 55.0,
    "temp_c": 25.0,
    "traffic_index": 60.0,
    "stubble_fires": 200.0,
    "day_type": "weekday",
    "station_zone": "Central",
}


def test_health_is_ok():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_predict_returns_a_number():
    r = client.post("/predict", json=VALID)
    assert r.status_code == 200
    assert isinstance(r.json()["prediction"], float)


def test_temp_above_70_is_rejected():
    r = client.post("/predict", json={**VALID, "temp_c": 71})
    assert r.status_code == 422


def test_negative_stubble_fires_is_rejected():
    r = client.post("/predict", json={**VALID, "stubble_fires": -1})
    assert r.status_code == 422
