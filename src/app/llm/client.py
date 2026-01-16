import os
import logging
from dotenv import load_dotenv
from google import genai

from app.llm.tools.tool import enrich_prompt_with_tools
from app.logging_config import get_session_id, init_session_logging

load_dotenv()

logger = logging.getLogger(__name__)

_client = None

def _gemini_client():
    global _client
    if _client is None:
        _client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    return _client

def _call_llm_raw(prompt: str) -> str:
    provider = os.getenv("LLM_PROVIDER", "gemini").lower()
    logger.debug("LLM call start provider=%s prompt_len=%d", provider, len(prompt or ""))
    if provider == "gemini":
        client = _gemini_client()
        model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        logger.debug("LLM model selected=%s", model)
        resp = client.models.generate_content(model=model, contents=prompt)
        logger.debug("LLM response received text_len=%d", len(resp.text or ""))
        return resp.text or ""
    logger.warning("Unsupported LLM provider=%s", provider)
    return ""


def generate(prompt: str, user_input: str) -> str:
    """
    prompt - The full prompt to send to the LLM (with history, system instructions, etc.)
    user_input - The current user input
    """
    if get_session_id() is None:
        init_session_logging("llm_client")
    if not prompt or not str(prompt).strip():
        logger.info("Empty prompt received; returning guardrail response")
        return "I don’t have enough information to answer. Please provide a question or application id."
    logger.debug("Generate called prompt_len=%d", len(prompt))
    enriched = enrich_prompt_with_tools(prompt, user_input, llm_call=_call_llm_raw)
    if not enriched:
        logger.warning("Prompt enrichment returned empty content")
        return "I don’t have enough information to answer. Please provide a question or application id."
    logger.debug("Prompt enriched prompt_len=%d", len(enriched))
    return _call_llm_raw(enriched)
