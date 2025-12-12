"""
Pydantic models for API requests and responses.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


# ============================
# REQUEST MODEL
# ============================
class GenerateRequest(BaseModel):
    """
    Request model for text generation endpoint.
    Compatible with llama.cpp /completion API.
    """
    
    prompt: str = Field(
        ..., 
        description="Input prompt (testo dell'utente in chiaro).",
        min_length=1,
        max_length=20000,
    )
    
    max_tokens: Optional[int] = Field(
        default=256,
        description="Numero massimo di token da generare.",
        ge=1,
        le=8192,
    )
    
    temperature: Optional[float] = Field(
        default=0.4,
        description="Temperature di campionamento (0 = deterministico, 2 = caotico).",
        ge=0.0,
        le=2.0,
    )
    
    top_p: Optional[float] = Field(
        default=0.9,
        description="Top-P nucleus sampling.",
        ge=0.0,
        le=1.0,
    )
    
    top_k: Optional[int] = Field(
        default=40,
        description="Top-K sampling.",
        ge=1,
        le=1000,
    )
    
    repeat_penalty: Optional[float] = Field(
        default=1.05,
        description="Penalità per evitare ripetizioni indesiderate.",
        ge=0.0,
        le=5.0,
    )


# ============================
# RESPONSE MODEL
# ============================
class GenerateResponse(BaseModel):
    """
    Response model for text generation endpoint.
    """
    
    completion: str = Field(
        ...,
        description="Il testo generato dal modello."
    )
    
    tokens_used: Optional[int] = Field(
        default=None,
        description="Conteggio totale dei token generati."
    )

    raw_response: Optional[dict] = Field(
        default=None,
        description="Risposta completa restituita da llama-server (per debug)."
    )


# ============================
# HEALTH MODEL
# ============================
class HealthResponse(BaseModel):
    """Response model for health check endpoint."""
    
    status: str = Field(..., description="Service status")
    service: str = Field(..., description="Service name")
    version: str = Field(..., description="Service version")
    environment: str = Field(..., description="Current environment")
    host: str = Field(..., description="Server host")
    port: int = Field(..., description="Server port")


# ============================
# ERROR MODEL
# ============================
class ErrorResponse(BaseModel):
    """Response model for error cases."""
    
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(default=None, description="Detailed error information")
