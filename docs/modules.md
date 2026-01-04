# Module Responsibilities

This document defines the responsibility and scope of each decisioning module.

Each module:
- owns one risk domain
- computes deterministic facts
- emits reason codes
- does not make the final decision

---

## Eligibility Module

**Purpose:**  
Determine whether an application can be considered at all.

**Typical checks:**
- Minimum income threshold
- Requested amount bounds
- Age / residency flags (synthetic)
- Product eligibility rules

**Outputs:**
- eligibility_passed
- income_band
- amount_band

**Behavior:**
- Fail-fast
- No ML usage

---

## Verification Module

**Purpose:**  
Establish identity and document trustworthiness.

**Checks:**
- Document verification status
- Identity mismatch flags
- Synthetic fraud risk score

**Outputs:**
- verification_status
- fraud_risk_band

---

## Bureau Module

**Purpose:**  
Evaluate external credit risk signals.

**Signals:**
- Debt-to-income ratio (DTI)
- Revolving utilization
- Recent delinquencies
- Credit enquiries
- Credit history depth

**Outputs:**
- bureau_risk_band
- dti
- revol_util
- delinquency_flags

---

## Servicing Module

**Purpose:**  
Evaluate **repayment capacity and affordability**.

This module focuses on:
- Income vs expenses
- Existing liabilities
- Household Expenditure Measure (HEM-style proxies)
- Post-loan surplus calculations

**Key concepts:**
- Net serviceability surplus
- Expense floors
- Liability buffers

**Outputs:**
- net_monthly_surplus
- serviceability_ratio
- servicing_risk_band

---

## Decisioning Module

**Purpose:**  
Aggregate module outputs into a final decision.

**Decision rules:**
- Any module returns `FAIL` → `DECLINE`
- Any module returns `REFER` → `REFER`
- Otherwise:
  - Evaluate ML risk score (if enabled)
  - Apply final decision thresholds

**Outputs:**
- final_decision
- primary_reason_code
- supporting_reason_codes
