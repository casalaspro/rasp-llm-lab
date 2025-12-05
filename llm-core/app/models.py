"""
Pydantic models for API requests and responses.
"""

from pydantic import BaseModel, Field
from typing import Optional


class GenerateRequest(BaseModel):
    """Request model for text generation endpoint."""
    
    prompt: str = Field(
        ..., 
        description="The input prompt for text generation",
        min_length=1,
        max_length=10000
    )
    max_tokens: Optional[int] = Field(
        default=None,
        description="Maximum number of tokens to generate",
        ge=1,
        le=4000
    )
    temperature: Optional[float] = Field(
        default=None,
        description="Sampling temperature (0.0 to 2.0)",
        ge=0.0,
        le=2.0
    )


class GenerateResponse(BaseModel):
    """Response model for text generation endpoint."""
    
    completion: str = Field(
        ...,
        description="The generated text completion"
    )
    tokens_used: Optional[int] = Field(
        default=None,
        description="Number of tokens used in generation"
    )


class HealthResponse(BaseModel):
    """Response model for health check endpoint."""
    
    status: str = Field(..., description="Service status")
    service: str = Field(..., description="Service name")
    version: str = Field(..., description="Service version")
    environment: str = Field(..., description="Current environment")
    host: str = Field(..., description="Server host")
    port: int = Field(..., description="Server port")


class ErrorResponse(BaseModel):
    """Response model for error cases."""
    
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(default=None, description="Detailed error information")