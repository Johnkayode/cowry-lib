from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app, get_db, Base


## Test DB config ##

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)



## TESTS ##

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

def test_delete_book():
    """Test deleting a book by UID"""
   
    create_response = client.post("/api/books", json={
        "title": "Book To Delete",
        "publisher": "Publisher",
        "category": "science",
        "author": "Darwin"
    })
    book_uid = create_response.json()["uid"]
    
    delete_response = client.delete(f"/api/books/{book_uid}")
    assert delete_response.status_code == 204