"""
API routes for llm-core service.
"""

from fastapi import APIRouter, HTTPException
from app.models import GenerateRequest, GenerateResponse, HealthResponse
from app.config import settings

# Create router instance
router = APIRouter()


@router.get("/", response_model=HealthResponse, tags=["Health"])
def health_check():
    """
    Health check endpoint.
    Returns service information and current configuration.
    """
    return HealthResponse(
        status="ok",
        service=settings.app_name,
        version=settings.app_version,
        environment=settings.environment,
        host=settings.host,
        port=settings.port
    )


@router.get("/health", response_model=HealthResponse, tags=["Health"])
def detailed_health_check():
    """
    Detailed health check endpoint.
    Alias for the root endpoint with explicit health path.
    """
    return health_check()


@router.post("/generate", response_model=GenerateResponse, tags=["Generation"])
def generate_text(request: GenerateRequest):
    """
    Generate text completion from a prompt.
    
    Currently returns a mock response for testing purposes.
    This will be replaced with actual LLM integration in the future.
    """
    try:
        # Mock LLM response for testing
        mock_completion = f"[MOCK LLM] I received your prompt: {request.prompt}"
        
        # Add parameter info if provided
        if request.max_tokens:
            mock_completion += f" | Max tokens: {request.max_tokens}"
        if request.temperature:
            mock_completion += f" | Temperature: {request.temperature}"
        
        return GenerateResponse(
            completion=mock_completion,
            tokens_used=len(mock_completion.split())
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating text: {str(e)}"
        )