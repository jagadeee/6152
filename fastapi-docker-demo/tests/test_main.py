from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_and_get_item():
    payload = {"name": "Book", "price": 9.99, "in_stock": True}
    response = client.post("/items/1", json=payload)
    assert response.status_code == 200
    assert response.json()["item"]["name"] == "Book"

    response = client.get("/items/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Book"


def test_delete_item():
    client.post("/items/2", json={"name": "Pen", "price": 1.5})
    response = client.delete("/items/2")
    assert response.status_code == 200
    assert response.json() == {"message": "Item deleted"}
