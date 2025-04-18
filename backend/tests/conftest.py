import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.app.main import app
from backend.app.db import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./app/test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
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
def client(test_db):
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