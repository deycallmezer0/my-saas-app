# SQLAlchemy models
from sqlalchemy import Column, Integer, String
from backend.app.core.database import Base  # Import Base from database.py

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Integer, default=1)
    is_logged_in = Column(Integer, default=0)