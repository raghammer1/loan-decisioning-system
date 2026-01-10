import re

from app.llm.tools.application_record_lookup_tool import lookup_application_record
from app.llm.agents.tool_routing_agent import run_tool_routing_agent


def _extract_application_id(text: str) -> str | None:
    match = re.search(r"\bAPP_\d+\b", text or "")
    if match:
        return match.group(0)

    cleaned = (text or "").strip()
    if cleaned.startswith("APP_") and " " not in cleaned:
        return cleaned

    return None


def _detect_tool_from_prompt(prompt: str) -> str | None:
    app_id = _extract_application_id(prompt)
    if app_id:
        return app_id
    return None


def _agent_fallback_tool_check(prompt: str, llm_call) -> str | None:
    app_id = run_tool_routing_agent(prompt, llm_call)
    if isinstance(app_id, str) and _extract_application_id(app_id) == app_id:
        return app_id
    return None


def _apply_application_lookup(prompt: str, app_id: str) -> str:
    tool_context = lookup_application_record(app_id)
    lines = [
        "ToolResult(application_record_lookup):",
        tool_context,
        "",
        prompt,
    ]
    return "\n".join(lines)


def enrich_prompt_with_tools(prompt: str, llm_call=None) -> str:
    # TOOL 1 - Application Record Lookup
    app_id = _detect_tool_from_prompt(prompt)
    if app_id:
        return _apply_application_lookup(prompt, app_id)

    fallback_app_id = _agent_fallback_tool_check(prompt, llm_call)
    if fallback_app_id:
        return _apply_application_lookup(prompt, fallback_app_id)

    return prompt
