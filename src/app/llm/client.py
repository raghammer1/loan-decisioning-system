import os
from dotenv import load_dotenv
from google import genai

from app.llm.tools.tool import enrich_prompt_with_tools

load_dotenv()


_client = None

def _gemini_client():
    global _client
    if _client is None:
        _client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    return _client

def _call_llm_raw(prompt: str) -> str:
    provider = os.getenv("LLM_PROVIDER", "gemini").lower()
    if provider == "gemini":
        client = _gemini_client()
        model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        resp = client.models.generate_content(model=model, contents=prompt)
        return resp.text or ""
    return ""


def generate(prompt: str) -> str:
    prompt = enrich_prompt_with_tools(prompt, llm_call=_call_llm_raw)
    return _call_llm_raw(prompt)
