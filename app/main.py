from fastapi import FastAPI

app = FastAPI()

# Root endpoint
@app.get("/")
def home():
    return {"message": "Welcome to DevBoard API 🚀"}

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "ok", "version": "1.0.0"}