import csv
import json
import re
import logging

from app.globals import curr_dir


DATA_FILE = curr_dir.parent.parent / "data" / "sample_application_outcomes_realistic_complete.csv"
_APPLICATION_INDEX = None
_LAST_APPLICATION_CONTEXT = None
logger = logging.getLogger(__name__)


def _load_application_index():
    global _APPLICATION_INDEX
    if _APPLICATION_INDEX is not None:
        logger.debug("Application index cache hit size=%d", len(_APPLICATION_INDEX))
        return _APPLICATION_INDEX

    index = {}
    logger.info("Loading application index from %s", DATA_FILE)
    with DATA_FILE.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            app_id = row.get("applicationId")
            if app_id:
                index[app_id] = row

    _APPLICATION_INDEX = index
    logger.info("Application index loaded size=%d", len(_APPLICATION_INDEX))
    return _APPLICATION_INDEX


def extract_application_id(text: str) -> str | None:
    match = re.search(r"\bAPP_\d+\b", text or "")
    if match:
        logger.debug("Extracted applicationId via regex=%s", match.group(0))
        return match.group(0)

    cleaned = (text or "").strip()
    if cleaned.startswith("APP_") and " " not in cleaned:
        logger.debug("Extracted applicationId via cleaned prompt=%s", cleaned)
        return cleaned

    return None


def should_call_application_lookup(prompt: str) -> str | None:
    return extract_application_id(prompt)


def lookup_application_record(app_id: str) -> str:
    logger.info("Application lookup requested applicationId=%s", app_id)
    index = _load_application_index()
    record = index.get(app_id)
    if not record:
        logger.warning("Application record not found applicationId=%s", app_id)
        payload = {
            "tool": "application_record_lookup",
            "status": "not_found",
            "applicationId": app_id,
        }
        _set_last_application_context(payload)
        return json.dumps(payload, ensure_ascii=True)

    decision = {
        "finalDecision": record.get("finalDecision"),
        "decisionStage": record.get("decisionStage"),
        "decisionTimestamp": record.get("decisionTimestamp"),
    }
    reason_codes = {
        "primaryReasonCode": record.get("primaryReasonCode"),
        "secondaryReasonCodes": record.get("secondaryReasonCodes"),
        "customerFacingReasons": record.get("customerFacingReasons"),
    }
    facts = {
        "applicantAge": record.get("applicantAge"),
        "requestedLoanAmount": record.get("requestedLoanAmount"),
        "approvedLoanAmount": record.get("approvedLoanAmount"),
        "netMonthlyIncome": record.get("netMonthlyIncome"),
        "debtServiceRatio": record.get("debtServiceRatio"),
        "netSurplusMonthly": record.get("netSurplusMonthly"),
        "bureauScore": record.get("bureauScore"),
        "internalRiskScore": record.get("internalRiskScore"),
        "riskGrade": record.get("riskGrade"),
        "pd": record.get("pd"),
        "monthsRemainingOnVisa": record.get("monthsRemainingOnVisa"),
        "affordabilityPassFlag": record.get("affordabilityPassFlag"),
    }
    payload = {
        "tool": "application_record_lookup",
        "status": "ok",
        "applicationId": app_id,
        "record": record,
        # "decision": decision,
        # "reason_codes": reason_codes,
        # "facts": facts,
    }
    _set_last_application_context(payload)
    logger.info("Application record found applicationId=%s", app_id)
    return json.dumps(payload, indent=2, ensure_ascii=True)


def apply_application_lookup(prompt: str, app_id: str) -> str:
    logger.debug("Applying application lookup to prompt appId=%s prompt_len=%d", app_id, len(prompt or ""))
    tool_context = lookup_application_record(app_id)
    lines = [
        "ToolResult(application_record_lookup):",
        tool_context,
        "",
        prompt,
    ]
    return "\n".join(lines)


def _set_last_application_context(payload: dict) -> None:
    global _LAST_APPLICATION_CONTEXT
    _LAST_APPLICATION_CONTEXT = payload
    logger.debug("Last application context updated status=%s", payload.get("status"))


def get_last_application_context() -> dict | None:
    return _LAST_APPLICATION_CONTEXT
