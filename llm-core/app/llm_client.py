from typing import Optional
import requests
from app.config import settings


def generate_with_llm(
    prompt: str,
    max_tokens: Optional[int] = None,
    temperature: Optional[float] = None,
) -> str:
    """
    Send the prompt to the llama.cpp server and return the generated text.
    
    Here we assume the /completion endpoint of llama-server.
    If you use a different endpoint (e.g., /v1/chat/completions) 
    you just need to adapt the payload and the response reading.
    """

    url = settings.llm_base_url.rstrip("/") + "/completion"

    # Payload according to the classic llama.cpp API
    # (if your version uses different fields, we can adapt them)
    payload = {
        "prompt": prompt,
    }

    if max_tokens is not None:
        # llama.cpp usually uses n_predict as "number of tokens to generate"
        payload["n_predict"] = max_tokens

    if temperature is not None:
        payload["temperature"] = temperature

    try:
        response = requests.post(url, json=payload, timeout=60)
        response.raise_for_status()
    except requests.RequestException as e:
        # Propagate the error to FastAPI, which will convert it to HTTP 5xx
        raise RuntimeError(f"Error calling llama-server: {e}")

    data = response.json()

    # Recent versions of llama.cpp usually return a "content" field
    # that contains the generated text.
    completion = data.get("content")
    if not completion:
        # If the format is different, you can print data and see what it looks like
        raise RuntimeError(f"Unexpected response from LLM server: {data}")

    return completion
