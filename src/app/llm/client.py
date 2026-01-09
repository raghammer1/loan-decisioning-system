import os
from dotenv import load_dotenv
from google import genai

load_dotenv()


_client = None

def _gemini_client():
    global _client
    if _client is None:
        _client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    return _client

def generate(prompt: str) -> str:
    provider = os.getenv("LLM_PROVIDER", "gemini").lower()

    if provider == "gemini":
        client = _gemini_client()
        model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        resp = client.models.generate_content(model=model, contents=prompt)
        return resp.text or ""
