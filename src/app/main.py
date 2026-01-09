from fastapi import FastAPI
from app.llm.client import generate

app = FastAPI()

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/ask")
def ask(q: str):
    return {"q": q, "answer": generate(q)}
