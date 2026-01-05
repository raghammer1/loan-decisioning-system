# Simplified Credit Decisioning Flow (Project Version)

This document describes a **reduced, practical version** of an enterprise personal-loan decisioning flow.

The flow is inspired by real-world banking systems but intentionally simplified to:
- remain implementable by a single engineer
- preserve modular separation of concerns
- demonstrate production-style decision orchestration

---

## 1. High-Level Flow Overview

The application progresses through a linear but gated sequence of decisioning modules:

1. Application Intake
2. Eligibility Checks
3. Bureau Risk Assessment
4. Servicing (Affordability) Assessment
5. Risk-Based Decisioning
6. Verification (Conditional)
7. Final Decision

Each module:
- produces an independent outcome
- emits structured facts and reason codes
- does not override other modules

The Decisioning module aggregates all results into a final outcome.

---

## 2. Flow Diagram (Logical)

Conceptual flow (not execution order):

Application Start  
→ Eligibility  
→ Bureau  
→ Servicing  
→ Decisioning  
→ (Optional) Verification  
→ Final Outcome

Modules may short-circuit the flow by producing a **DECLINE** or **REFER**, but execution state is always recorded.

---

## 3. Application Intake

### Purpose
Capture the minimum information required to begin automated assessment.

### Inputs
- Requested loan amount
- Loan purpose
- Applicant income
- Employment status
- Basic demographics (synthetic)

### Output
- Normalised application record
- Application ID
- Initial facts snapshot

No decisions occur at this stage.

---

## 4. Eligibility Module

### Purpose
Fail-fast rejection of applications that cannot be considered under any circumstance.

### Typical Checks
- Minimum income threshold
- Loan amount bounds
- Age or residency bounds (synthetic)

### Outcomes
- PASS → continue
- FAIL → DECLINE

### Notes
- No external data is used
- No ML involvement
- Lowest latency module

---

## 5. Bureau Module

### Purpose
Assess external credit risk using credit-bureau-style signals.

### Typical Checks
- Debt-to-income ratio
- Revolving utilisation
- Recent delinquencies
- Credit enquiries
- Credit history depth

### Outcomes
- PASS → acceptable bureau risk
- REFER → marginal or thin credit file
- FAIL → adverse bureau indicators

### Notes
- This module mirrors the “soft bureau” and “hard bureau” split conceptually
- All thresholds are explicit and versioned

---

## 6. Servicing Module

### Purpose
Evaluate affordability and repayment capacity.

This mirrors the servicing / HEM logic in real lending systems.

### Inputs
- Declared income
- Derived expenses (DTI / HEM-style proxy)
- Existing liabilities
- Requested loan repayment estimate

### Key Calculations
- Net monthly surplus
- Serviceability ratio
- Post-loan cash position

### Outcomes
- PASS → sufficient affordability
- REFER → marginal surplus
- FAIL → insufficient servicing capacity

---

## 7. Decisioning Module

### Purpose
Aggregate all module outcomes and produce a single decision.

### Inputs
- Eligibility outcome
- Bureau outcome
- Servicing outcome
- ML risk score (if available)

### Decision Rules
- Any FAIL → DECLINE
- Any REFER → REFER
- Else:
  - evaluate risk score
  - approve if below threshold

### Outputs
- Final decision (APPROVE / REFER / DECLINE)
- Primary reason code
- Supporting reason codes
- Full audit trace

---

## 8. Verification Module (Conditional)

### Purpose
Perform identity and document verification **only when required**.

### Trigger Conditions
- Decision = APPROVE or REFER
- Risk band not extreme
- Policy requires verification

### Typical Checks
- Document verification status
- Address consistency
- Synthetic fraud indicators

### Outcomes
- PASS → continue
- FAIL → DECLINE
- REFER → manual review

### Notes
Verification is **not in the critical path** for early declines.

---

## 9. Final Outcomes

### APPROVE
- All modules passed
- Risk score acceptable
- May be express or standard approval

### REFER
- One or more modules require human review
- Full context provided for manual assessment

### DECLINE
- At least one hard-fail rule triggered
- Clear, explainable reason codes produced

---

## 10. Auditability & Replay

Every application stores:
- module outputs
- facts used in decisions
- rule versions
- timestamps

This allows:
- full replay of decisions
- deterministic explanations
- safe integration with the chatbot layer

---

## 11. What This Flow Intentionally Omits

This project does NOT implement:
- pricing optimisation
- product switching
- multiple loan offers
- regulatory reporting
- fairness modelling

These are explicitly marked as future work.

---

## 12. Why This Flow Is Academically & Professionally Strong

- Mirrors real bank decisioning structure
- Clear module boundaries
- Deterministic + probabilistic reasoning
- Explainability-first design
- Fully implementable within 10–12 weeks

This is a **systems project**, not a toy pipeline.