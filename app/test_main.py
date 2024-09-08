from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .main import app
from . import models, database

# Setup test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
models.Base.metadata.create_all(bind=engine)

# Dependency override
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[database.get_db] = override_get_db

client = TestClient(app)

def test_create_message():
    response = client.post(
        "/messages",
        json={"user_message": "hello"}
    )
    assert response.status_code == 200
    assert response.json() == {"chat_response": "Hi there! How can I assist you today?"}

def test_get_all_messages():
    response = client.get("/messages")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0

def test_edit_message():
    # Assume the message with ID 1 exists
    response = client.put(
        "/messages/2",
        json={"user_message": "hi"}
    )
    assert response.status_code == 200
    assert response.json() == {"chat_response": "Hello! What can I help you with today?"}

def test_delete_message():
    response = client.delete("/messages/3")
    assert response.status_code == 200
    assert response.json() == {"status": "Message deleted successfully"}

def test_delete_non_existing_message():
    response = client.delete("/messages/9999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Message not found"}