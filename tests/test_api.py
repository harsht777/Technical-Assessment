import pytest
import json
from app.main import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"API is running" in response.data

def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert b"UP" in response.data

def test_get_items(client):
    response = client.get("/api/v1/items")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["count"] >= 2

def test_post_item(client):
    payload = {"name": "Test Item"}
    response = client.post("/api/v1/items", json=payload)
    assert response.status_code == 201
    
def test_metrics(client):
    response = client.get("/metrics")
    assert response.status_code == 200
    assert b"http_requests_total" in response.data
