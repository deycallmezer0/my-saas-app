from fastapi import FastAPI
from backend.app.api.routes import router  # Use absolute import path
from backend.app.core.database import engine, Base
# Import all models to ensure they're registered
from backend.app.models.user import User

# Create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="User Authentication API",
    description="API for user authentication",
    version="0.1.0"
)

# Include your router
app.include_router(router)

@app.get("/", tags=["root"])
def read_root():
    return {"message": "Welcome to the API"}