from app.llm.tools.application_record_lookup_tool import (
    apply_application_lookup,
    extract_application_id,
    should_call_application_lookup,
)
from app.llm.agents.decline_rule_explanation_agent import (
    apply_decline_rule_explanation_agent,
    should_call_decline_rule_explanation_agent,
)
from app.llm.agents.tool_routing_agent import run_tool_routing_agent


def _agent_fallback_tool_check(prompt: str, llm_call) -> str | None:
    app_id = run_tool_routing_agent(prompt, llm_call)
    if isinstance(app_id, str) and extract_application_id(app_id) == app_id:
        return app_id
    return None


def enrich_prompt_with_tools(prompt: str, llm_call=None) -> str:
    user_prompt = prompt
    enriched_prompt = prompt
    # TOOL 1 - Application Record Lookup
    app_id = should_call_application_lookup(user_prompt)
    if app_id:
        enriched_prompt = apply_application_lookup(user_prompt, app_id)

    if not app_id:
        fallback_app_id = _agent_fallback_tool_check(user_prompt, llm_call)
        if fallback_app_id:
            enriched_prompt = apply_application_lookup(user_prompt, fallback_app_id)

    if should_call_decline_rule_explanation_agent(user_prompt):
        enriched_prompt = apply_decline_rule_explanation_agent(
            enriched_prompt, user_prompt,llm_call
        )

    return enriched_prompt
