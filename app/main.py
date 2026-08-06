from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.routers import auth, tasks, documents, search, analytics
from app.config import DATABASE_URL
from app.database import engine

app = FastAPI(
    title="AI-Powered Task & Knowledge Management System API",
    description="Backend API for managing tasks, documents, semantic searches, and analytics.",
    version="1.0.0"
)

# Allowed Origins
origins = [
    "http://localhost:5173",
    "https://ai-taskmanagement.vercel.app",
]

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router)
app.include_router(tasks.router)
app.include_router(documents.router)
app.include_router(search.router)
app.include_router(analytics.router)


@app.get("/")
def read_root():
    return {
        "status": "online",
        "message": "Welcome to the AI-Powered Task & Knowledge Management System API",
        "docs_url": "/docs"
    }


@app.get("/debug-db")
def debug_db():
    return {
        "DATABASE_URL": DATABASE_URL
    }


@app.get("/test-db")
def test_db():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            return {
                "status": "connected",
                "result": result.scalar()
            }
    except Exception as e:
        return {
            "status": "failed",
            "error": str(e)
        }