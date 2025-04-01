from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_query_valid_data():
    # First, create some test data
    payload = {
        "sensor_id": "1",
        "temperature": 24.5,
        "humidity": 55,
        "windspeed": 10.2
    }
    post_response = client.post("/data", json=payload)
    assert post_response.status_code == 200

    # Now query the average temperature and humidity for the same sensor
    query_params = {
        "sensor_id": "1",
        "metrics": ["temperature", "humidity"],
        "statistics": ["average"],
        "days": 30
    }

    response = client.get("/query", params=query_params)
    assert response.status_code == 200

    data = response.json()
    assert "sensor_id" in data
    assert "results" in data
    assert "temperature" in data["results"]
    assert "humidity" in data["results"]
    assert "average" in data["results"]["temperature"]
    assert isinstance(data["results"]["temperature"]["average"], (float, int))

def test_query_latest_data_when_days_not_provided():
    response = client.get("/query", params={
        "sensor_id": "1",
        "metrics": ["temperature"],
        "statistics": ["average"]
    })
    assert response.status_code == 200
    assert "results" in response.json()
