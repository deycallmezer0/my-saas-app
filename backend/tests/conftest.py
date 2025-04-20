import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.app.models import user  # ✅ Ensures User model is registered
from backend.app.main import app
from backend.app.db import Base, get_db
from backend.app.models.user import User
import os
from dotenv import load_dotenv
import os

load_dotenv()  # this will look for a .env file and load it
SQLALCHEMY_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL")
if SQLALCHEMY_DATABASE_URL is None:
    raise ValueError(
        "TEST_DATABASE_URL environment variable is not set. Please set it to your test database URL."
    )

from sqlalchemy import text


connect_args = {"check_same_thread": False} if SQLALCHEMY_DATABASE_URL.startswith("sqlite") else {}


engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Drop and recreate DB tables before each test function
@pytest.fixture(autouse=True)
def reset_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

@pytest.fixture
def test_db():
    """Return a test database session for use in tests"""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client(test_db, reset_db):
    def override_get_db():
        try:
            yield test_db
        finally:
            pass  # The test_db fixture handles closing

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        # Add the db as an attribute to the client for convenient access in tests
        c.db = test_db
        yield c
    
    app.dependency_overrides.clear()