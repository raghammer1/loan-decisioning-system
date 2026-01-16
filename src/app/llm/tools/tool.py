import logging

from app.llm.tools.application_record_lookup_tool import (
    apply_application_lookup,
    extract_application_id,
    should_call_application_lookup,
    get_last_application_context
)
from app.llm.agents.decline_rule_explanation_agent import (
    apply_decline_rule_explanation_agent,
    should_call_decline_rule_explanation_agent,
)
from app.llm.agents.tool_routing_agent import run_tool_routing_agent

logger = logging.getLogger(__name__)

def _agent_fallback_tool_check(prompt: str, llm_call) -> str | None:
    logger.debug("Running tool routing agent fallback")
    app_id = run_tool_routing_agent(prompt, llm_call)
    if isinstance(app_id, str) and extract_application_id(app_id) == app_id:
        logger.info("Tool routing agent detected applicationId=%s", app_id)
        return app_id
    logger.debug("Tool routing agent did not select applicationId")
    return None


def enrich_prompt_with_tools(prompt: str, user_input, llm_call=None) -> str:
    user_prompt = prompt
    enriched_prompt = prompt
    # TOOL 1 - Application Record Lookup
    app_id = should_call_application_lookup(user_prompt)
    if app_id:
        logger.info("Application lookup triggered applicationId=%s", app_id)
        enriched_prompt = apply_application_lookup(user_prompt, app_id)

    if not app_id:
        fallback_app_id = _agent_fallback_tool_check(user_prompt, llm_call)
        if fallback_app_id:
            logger.info("Application lookup via fallback applicationId=%s", fallback_app_id)
            enriched_prompt = apply_application_lookup(user_prompt, fallback_app_id)

    if should_call_decline_rule_explanation_agent(user_prompt):
        logger.info("Decline rule explanation agent triggered")
        application_data = get_last_application_context()
        enriched_prompt = apply_decline_rule_explanation_agent(
            enriched_prompt, user_prompt, llm_call, application_data, user_input
        )
    else:
        logger.debug("Decline rule explanation agent not triggered")

    return enriched_prompt
