import pytest
from backend.app.models.user import User

def test_signup(client):
    response = client.post("/signup", json={
        "email": "test@example.com",
        "password": "testpassword"
    })
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"
    assert "message" in response.json()
    assert "user_id" in response.json()
    
    # check to see if the user was created in the database
    db_user = client.db.query(User).filter(User.email == "test@example.com").first()
    assert db_user is not None
    assert db_user.is_active == 1
    assert db_user.is_logged_in == 0

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