"""
LLM Core Service

A FastAPI-based service for text generation using Language Models.
Currently provides mock responses for testing pipeline integration.
"""

from fastapi import FastAPI
from app.config import settings
from app.routes import router

# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Language Model Core Service for text generation",
    debug=settings.debug
)

# Include API routes
app.include_router(router)


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level
    )