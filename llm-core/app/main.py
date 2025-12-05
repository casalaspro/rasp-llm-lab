from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class GenerateRequest(BaseModel):
    prompt: str


class GenerateResponse(BaseModel):
    completion: str


@app.get("/")
def root():
    return {"status": "ok", "service": "llm-core"}


@app.post("/generate", response_model=GenerateResponse)
def generate(req: GenerateRequest):
    """
    Fake LLM: it returns just the fake message just
    to test pipeline between services.
    """
    fake_reply = f"[MOCK LLM] I received: {req.prompt}"
    return GenerateResponse(completion=fake_reply)