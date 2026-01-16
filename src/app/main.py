import logging
from fastapi import FastAPI
from app.llm.client import generate
from app.logging_config import init_session_logging


init_session_logging("fastapi")
logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/health")
def health():
    logger.info("Health check requested")
    return {"ok": True}

@app.get("/ask")
def ask(q: str):
    logger.info("Ask endpoint called q_len=%d", len(q or ""))
    return {"q": q, "answer": generate(q)}
