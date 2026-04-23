from fastapi import FastAPI , Depends
from app.database import engine, Base
from app.models import user, todo, post, product
from app.routers import auth, todo as todo_router , post as post_router , product as product_router
# Import all models so they get registered
#from app.models import user, todo, post, product
from app.oauth2 import get_current_user
from app.models.user import User

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="DevBoard API", version="1.0.0")

# Include routers
app.include_router(auth.router)
app.include_router(todo_router.router)
app.include_router(post_router.router)
app.include_router(product_router.router)


# Root endpoint
@app.get("/")
def home():
    return {"message": "Welcome to DevBoard API 🚀"}

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "ok", "version": "1.0.0"}

# Protected route — only logged in users can access!
@app.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email
    }