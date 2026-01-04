# Reason Code Taxonomy (v0.1)

Each reason has:
- a **stable machine code** (used in systems, logs, APIs)
- a **human-readable identifier** (used in documentation)

---

## Eligibility

- **D1001 — ELIG_INCOME_TOO_LOW**  
  Applicant income does not meet minimum eligibility threshold.

- **D1002 — ELIG_AMOUNT_OUT_OF_RANGE**  
  Requested loan amount is outside supported bounds.

- **D1003 — ELIG_AGE_OUT_OF_RANGE**  
  Applicant age does not fall within eligible range.

---

## Verification

- **D2001 — VERIF_DOCUMENT_FAILED**  
  Required identity or income documents could not be verified.

- **R2002 — VERIF_ADDRESS_MISMATCH**  
  Address information mismatch requires manual review.

- **D2003 — VERIF_HIGH_FRAUD_RISK**  
  Fraud risk indicators exceed acceptable thresholds.

---

## Bureau

- **D3001 — BUR_DTI_TOO_HIGH**  
  Debt-to-income ratio exceeds policy threshold.

- **D3002 — BUR_REVOL_UTIL_TOO_HIGH**  
  Revolving credit utilisation is above acceptable levels.

- **D3003 — BUR_RECENT_DELINQUENCY**  
  Recent delinquency detected within restricted lookback window.

- **R3004 — BUR_TOO_MANY_ENQUIRIES**  
  Excessive recent credit enquiries require review.

- **R3005 — BUR_CREDIT_HISTORY_THIN**  
  Credit history length is insufficient for automated decisioning.

---

## Servicing

- **D4001 — SRV_NET_CASH_POSITION_NEGATIVE**  
  Estimated net monthly cash position is negative after expenses and liabilities.

- **D4002 — SRV_EXPENSES_TOO_HIGH**  
  Living expenses exceed acceptable affordability limits.

- **D4003 — SRV_LIABILITIES_TOO_HIGH**  
  Existing liabilities materially reduce repayment capacity.

- **R4004 — SRV_SERVICEABILITY_RATIO_LOW**  
  Serviceability ratio falls below automatic approval threshold.

---

## Decisioning

- **D5001 — DEC_RISK_SCORE_TOO_HIGH**  
  Modelled probability of default exceeds policy threshold.

- **R5002 — DEC_REFER_MANUAL_REVIEW**  
  Aggregated signals require manual assessment.

- **A5003 — DEC_APPROVED**  
  Application satisfies all automated decision criteria.
