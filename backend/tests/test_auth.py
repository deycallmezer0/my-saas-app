import pytest
from backend.app.models.user import User

def test_signup(client, db):
    response = client.post("/signup", json={
        "email": "test@example.com",
        "password": "testpassword"
    })
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"
    assert "message" in response.json()
    assert "user_id" in response.json()

    # Use the injected db fixture
    db_user = db.query(User).filter(User.email == "test@example.com").first()
    assert db_user is not None

def test_login(client):
    # First, create a user
    client.post("/signup", json={
        "email": "test@example.com",
        "password": "testpassword"
    })
    
    # Now, try to log in
    response = client.post("/login", json={
        "email": "test@example.com",
        "password": "testpassword"
    })
    assert response.status_code == 200
    assert response.json()["message"] == "Login successful"
    assert "user_id" in response.json()

def test_login_invalid_credentials(client):
    # First, create a user
    client.post("/signup", json={
        "email": "test@example.com",
        "password": "testpassword"
    })
    # Now, try to log in with invalid credentials
    response = client.post("/login", json={
        "email": "test@example.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"

def test_logout(client):
    # First, create a user and log them in
    client.post("/signup", json={
        "email": "test@example.com",
        "password": "testpassword"
    })

    client.post("/login", json={
        "email": "test@example.com",
        "password": "testpassword"
    })

    # Now, log them out
    response = client.post("/logout", json={
        "email": "test@example.com"
    })
    assert response.status_code == 200
    assert response.json()["message"] == "Logout successful"
    assert "user_id" in response.json()
    