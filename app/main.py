from fastapi import FastAPI
from app.database import engine, Base
from app.models import user, todo, post, product
from app.routers import auth
# Import all models so they get registered
from app.models import user, todo, post, product

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="DevBoard API", version="1.0.0")

# Include routers
app.include_router(auth.router)

# Root endpoint
@app.get("/")
def home():
    return {"message": "Welcome to DevBoard API 🚀"}

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "ok", "version": "1.0.0"}