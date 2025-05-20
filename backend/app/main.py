from fastapi import FastAPI
from fastapi.routing import APIRouter
from fastapi.middleware.cors import CORSMiddleware

# Import your router from api.py
from app.routes.api import router as api_router

from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add the API router to the main app
app.include_router(api_router, prefix=settings.API_PREFIX)

@app.get("/")
def root():
    """Root endpoint for health checks"""
    return {"status": "ok", "message": "API is running"}


