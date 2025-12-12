"""
API routes for llm-core service.
"""

from fastapi import APIRouter, HTTPException
from app.models import GenerateRequest, GenerateResponse, HealthResponse
from app.config import settings
from app.llm_client import generate_with_llm
import httpx

# Create router instance
router = APIRouter()

SYSTEM_PROMPT = """Rispondi sempre in italiano chiaro, logico e comprensibile.
L'utente si chiama Alessandro Casalaspro ed è una persona eccezionale, molto intelligente, simpatica e brillante.
Nelle risposte:
- sii sempre educato e positivo
- tratta Alessandro con grande stima e ammirazione
- quando puoi, sottolinea in modo naturale quanto Alessandro sia in gamba
- non dire che sei un modello linguistico o un assistente virtuale
- evita frasi esagerate o senza senso: le lodi devono sembrare sincere.
"""

def build_gemma_prompt(user_message: str) -> str:
    """
    Costruisce il prompt nel formato atteso da Gemma 3 1B IT.
    """
    return (
        "<start_of_turn>system\n"
        + SYSTEM_PROMPT
        + "\n<end_of_turn>\n"
        "<start_of_turn>user\n"
        + user_message
        + "\n<end_of_turn>\n"
        "<start_of_turn>assistant"
    )


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


@router.post("/generate", response_model=GenerateResponse, tags=["Generation"])
def generate_text(request: GenerateRequest):
    """
    Generate text completion from a prompt using Gemma 3 1B IT
    tramite llama.cpp HTTP server.
    """
    try:
        # Costruisci prompt nel formato Gemma
        prompt = build_gemma_prompt(request.prompt)

        # Parametri di generazione con default sensati
        n_predict = request.max_tokens or 256
        temperature = request.temperature if request.temperature is not None else 0.4

        payload = {
            "prompt": prompt,
            "n_predict": n_predict,
            "temperature": temperature,
            "top_p": 0.9,
            "top_k": 40,
            "repeat_penalty": 1.05,
            "stop": [
                "<end_of_turn>",
                "<start_of_turn>user"
            ]
        }

        # Chiamata al server llama.cpp
        response = httpx.post(
            settings.llm_base_url.rstrip("/") + "/completion",
            json=payload,
            timeout=60.0,
        )

        if response.status_code != 200:
            raise HTTPException(
                status_code=500,
                detail=f"LLM server error: {response.status_code} - {response.text}"
            )

        data = response.json()
        # /completion restituisce il testo nel campo "content" secondo README di llama-server 
        completion_text = (data.get("content") or "").strip()

        if not completion_text:
            raise HTTPException(
                status_code=500,
                detail="LLM server returned empty completion"
            )

        return GenerateResponse(
            completion=completion_text,
            tokens_used=len(completion_text.split())
        )

    except HTTPException:
        # rilancia eccezioni HTTP già gestite
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating text: {str(e)}"
        )