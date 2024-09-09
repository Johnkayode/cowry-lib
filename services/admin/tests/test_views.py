from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_book():
    """Test book creation in admin"""
    response = client.post("/api/books", json={
        "title": "New Book",
        "publisher": "Publisher",
        "category": "arts",
        "author": "Shakespeare"
    })
    assert response.status_code == 200
    assert response.json()["title"] == "New Book"

def test_get_enrolled_users():
    """Test fetching users enrolled in the library"""
    response = client.get("/api/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_unavailable_books():
    """Test retrieving books that are unavailable"""
    response = client.get("/api/books/unavailable")
    assert response.status_code == 200
    assert isinstance(response.json(), list)