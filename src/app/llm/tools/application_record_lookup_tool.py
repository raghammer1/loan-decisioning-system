import csv
import json

from app.globals import curr_dir


DATA_FILE = curr_dir.parent.parent / "data" / "sample_application_outcomes_realistic_complete.csv"
_APPLICATION_INDEX = None


def _load_application_index():
    global _APPLICATION_INDEX
    if _APPLICATION_INDEX is not None:
        return _APPLICATION_INDEX

    index = {}
    with DATA_FILE.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            app_id = row.get("applicationId")
            if app_id:
                index[app_id] = row

    _APPLICATION_INDEX = index
    return _APPLICATION_INDEX


def lookup_application_record(app_id: str) -> str:
    index = _load_application_index()
    record = index.get(app_id)
    if not record:
        payload = {
            "tool": "application_record_lookup",
            "status": "not_found",
            "applicationId": app_id,
        }
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
    return json.dumps(payload, indent=2, ensure_ascii=True)
