from fastapi.testclient import TestClient
from datetime import date
from panchanga_app.api.main import app

client = TestClient(app)

def test_compute_panchanga():
    response = client.post(
        "/panchanga",
        json={
            "latitude": 10.5276,
            "longitude": 76.2144,
            "local_date": "2024-01-01"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "sunrise_local" in data
    assert "tithi_index" in data
    assert "festivals" in data

def test_compute_panchanga_default_coordinates():
    response = client.post(
        "/panchanga",
        json={
            "local_date": "2024-01-01"
        }
    )
    assert response.status_code == 200 