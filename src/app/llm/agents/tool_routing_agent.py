import json
import logging


logger = logging.getLogger(__name__)


def run_tool_routing_agent(prompt: str, llm_call):
    if llm_call is None:
        logger.warning("Tool routing agent invoked without llm_call")
        return None

    system_instructions = (
        "You decide whether a tool should be called. "
        "Tool available: application_record_lookup. "
        "Call it only when an explicit application id is present in the user prompt. "
        "Application id format: APP_ followed by digits (example APP_123). "
        "Return strict JSON only. "
        'If tool should be called: {"tool":"application_record_lookup","applicationId":"APP_123"} '
        'If no tool should be called: {"tool":null}.'
    )
    agent_prompt = "\n".join(
        [
            "SYSTEM:",
            system_instructions,
            "USER:",
            prompt or "",
        ]
    )

    response = llm_call(agent_prompt)
    if not response:
        logger.warning("Tool routing agent returned empty response")
        return None

    try:
        data = json.loads(response)
    except json.JSONDecodeError:
        logger.exception("Tool routing agent returned non-JSON response")
        return None

    if data.get("tool") != "application_record_lookup":
        logger.debug("Tool routing agent did not request application_record_lookup")
        return None

    app_id = data.get("applicationId")
    if isinstance(app_id, str):
        logger.info("Tool routing agent selected applicationId=%s", app_id)
        return app_id
    return None
