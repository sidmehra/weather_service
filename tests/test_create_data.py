from fastapi.testclient import TestClient
from app.main import app 
import pytest

client = TestClient(app)

def test_create_sensor_data_valid():
    payload = {
        "sensor_id": "1",
        "temperature": 23.5,
        "humidity": 60.0,
        "windspeed": 15.2
    }

    response = client.post("/data", json=payload)
    assert response.status_code == 200
    assert response.json()["message"] == "Data added successfully"

def test_create_sensor_data_with_no_metrics():
    payload = {
        "sensor_id": "2"
    }

    response = client.post("/data", json=payload)
    assert response.status_code == 422 or response.status_code == 400


def test_create_sensor_data_with_invalid_sensor_id():
    payload = {
        "sensor_id": "abc",  # invalid
        "temperature": 20.0
    }

    response = client.post("/data", json=payload)
    assert response.status_code == 400


def test_create_sensor_data_partial_metrics():
    payload = {
        "sensor_id": "3",
        "temperature": 28.7
    }

    response = client.post("/data", json=payload)
    assert response.status_code == 200
    assert response.json()["message"] == "Data added successfully" 