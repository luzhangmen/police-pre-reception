from fastapi import FastAPI

from app.core.pipeline import run_pipeline
from app.core.state import UserMessage

app = FastAPI(title="Police Pre-Reception API")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/v1/reason")
def reason(message: UserMessage) -> dict:
    return run_pipeline(message).model_dump()

