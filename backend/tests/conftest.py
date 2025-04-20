import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.app.core.database import Base, get_db
from backend.app.models.user import User  # Import the User model
import os
from dotenv import load_dotenv
from backend.app.main import app
load_dotenv()
SQLALCHEMY_DATABASE_URL = os.getenv("TEST_DATABASE_URL")
if SQLALCHEMY_DATABASE_URL is None:
    raise ValueError(
        "TEST_DATABASE_URL environment variable is not set. Please set it to your test database URL."
    )

connect_args = {"check_same_thread": False} if SQLALCHEMY_DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args=connect_args)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# define a client fixture
@pytest.fixture(scope="module")
def client():
    # Create the database tables
    Base.metadata.create_all(bind=engine)
    
    # Create a new FastAPI TestClient instance
    with TestClient(app) as test_client:
        # Override the get_db dependency to use the testing session
        def override_get_db():
            db = TestingSessionLocal()
            try:
                yield db
            finally:
                db.close()

        app.dependency_overrides[get_db] = override_get_db
        yield test_client

    # Clean up the database after tests
    Base.metadata.drop_all(bind=engine)
    # Remove the dependency override
    app.dependency_overrides[get_db] = lambda: TestingSessionLocal()

# define db fixture
@pytest.fixture(scope="function")
def db():
    # Create a new database session for each test
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(autouse=True)
def reset_db():
    # Ensure all model classes are imported before creating tables
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)  # This should create all tables including 'users'