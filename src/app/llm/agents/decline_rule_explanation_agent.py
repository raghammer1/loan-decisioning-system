import csv
import json
import re

from app.globals import curr_dir


DATA_FILE = (
    curr_dir.parent.parent / "data" / "decline_rules_explained.csv"
)
_DECLINE_RULE_INDEX = None


def _load_decline_rule_index():
    global _DECLINE_RULE_INDEX
    if _DECLINE_RULE_INDEX is not None:
        return _DECLINE_RULE_INDEX

    index = {}
    with DATA_FILE.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            rule_id = (row.get("rule_id") or "").strip()
            if rule_id:
                index[rule_id] = row

    _DECLINE_RULE_INDEX = index
    return _DECLINE_RULE_INDEX


def _extract_rule_ids(text: str) -> list[str]:
    matches = re.findall(r"\bD\d{3,4}\b", text or "", flags=re.IGNORECASE)
    seen = set()
    ordered = []
    for match in matches:
        rule_id = match.upper()
        if rule_id not in seen:
            seen.add(rule_id)
            ordered.append(rule_id)
    return ordered


def should_call_decline_rule_explanation_agent(prompt: str) -> bool:
    if _extract_rule_ids(prompt):
        return True

    lower = (prompt or "").lower()
    keywords = [
        "decline rule",
        "decline code",
        "reason code",
        "rule code",
        "why was i declined",
        "why was it declined",
        "why was my application declined",
        "why declined",
        "why did it decline",
        "why did it get declined",
        "more about the decline",
        "explain the decline",
        "explain decline",
        "why was this declined",
        "why was my application rejected",
    ]
    return any(keyword in lower for keyword in keywords)


def _select_rules_for_prompt(user_prompt: str) -> tuple[list[str], list[dict]]:
    index = _load_decline_rule_index()
    requested_ids = _extract_rule_ids(user_prompt)
    if requested_ids:
        rules = [index[rule_id] for rule_id in requested_ids if rule_id in index]
        return requested_ids, rules

    return [], [index[rule_id] for rule_id in sorted(index.keys())]


def _insert_agent_context(prompt: str, context: str) -> str:
    marker = "\nAssistant:"
    idx = prompt.rfind(marker)
    if idx == -1:
        return "\n".join([context, prompt])
    return "".join([prompt[:idx], context, prompt[idx:]])


def apply_decline_rule_explanation_agent(prompt: str, user_prompt: str,llm_call) -> str:
    requested_rule_ids, rules = _select_rules_for_prompt(user_prompt)
    payload = {
        "mentionedRuleIds": requested_rule_ids,
        "rules": rules,
    }

    instructions = [
        "SYSTEM (Decline Rule Explanation Agent):",
        "You help explain decline rules using the provided decline rule data.",
        "When the user asks about a decline rule or reason code:",
        "1) Verify whether any user-mentioned rule_id matches the application's",
        "   primaryReasonCode or secondaryReasonCodes in ToolResult(application_record_lookup).",
        "2) If the mentioned rule_id does not match, say you can only explain the",
        "   triggered rule(s) and ask if they want that explanation.",
        "3) Use DECLINE_RULE_DATA to explain the rule and compare the rule requirement",
        "   to the applicant's actual values in the application record.",
        "4) Only use fields present in the application record; do not guess or infer.",
        "5) If required application data or rule data is missing, say you don't have",
        "   enough information to explain the rule.",
        "6) Imp: You must look through application data and find relevant fields to tell user there values were these whereas the rule required these values.",
        "DECLINE_RULE_DATA:",
        json.dumps(payload, ensure_ascii=True, indent=2),
        "",
    ]

    response = llm_call(instructions)
    if not response:
        return None

    try:
        data = json.loads(response)
    except json.JSONDecodeError:
        return None

    context = "\n".join(instructions)
    return _insert_agent_context(prompt, data)
