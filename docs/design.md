# Design Document — Modular Credit Decisioning System

## 1. Problem Statement
Credit decisioning in production environments is complex due to:
- tightly coupled business logic and engineering
- poor explainability when ML is introduced
- lack of deterministic audit trails
- difficulty evolving policies safely

This project builds a **modular decisioning platform** where each domain owns its logic, outputs structured facts, and participates in a transparent orchestration process.

---

## 2. Design Goals
- Clear separation of responsibility across domains
- Deterministic, replayable decisions
- Explicit reason codes with evidence
- Safe ML integration
- Human-readable explanations
- Realistic performance constraints

---

## 3. Non-Goals
- Regulatory certification
- Fairness / bias modelling
- Cloud-scale deployment
- UI-heavy frontends

---

## 4. Architecture Overview

### Core Concept
Each module:
- evaluates a specific risk domain
- emits outcomes and facts
- never overrides other modules

The Decisioning module:
- aggregates module outputs
- applies final policy orchestration
- produces the canonical decision object

---

## 5. Decision Context

All modules operate on a shared immutable context:

```json
{
  "app_id": "A123",
  "customer_id": "C456",
  "application": {...},
  "bureau": {...},
  "servicing": {...},
  "verification": {...},
  "facts": {}
}
```

## 6. Module Contract

Each decisioning module must implement the following **output contract**:

```json
{
  "module": "bureau",
  "outcome": "PASS | FAIL | REFER",
  "reason_codes": ["BUR_DTI_TOO_HIGH"],
  "facts": {
    "dti": 0.52,
    "dti_threshold": 0.40
  },
  "audit": {
    "version": "0.1.0",
    "timestamp": "2026-01-04T22:10:00+11:00"
  }
}
```

### Notes

- Modules **never override** other modules  
- Modules **only compute facts and domain-specific outcomes**  
- The **Decisioning module consumes module outputs**; it does **not recompute** them  

---

## 7. Performance Targets (Demo)

- **p95 online decision latency:** < 50 ms  
- **Batch processing:** 100k rows within seconds (local execution)  
- **Explanation latency:** measured separately (LLM is not in the decision path)  

---

## 8. Failure Handling

- Module execution failures result in **`REFER`**, not system crashes  
- ML scoring failures **degrade gracefully** to rules-only decisioning  
- All decisions are **fully replayable** using stored inputs and versioned rules  

---

## 9. Milestones

- **Weeks 1–4:** Core modules + orchestration  
- **Weeks 5–7:** ML scoring + evaluation  
- **Weeks 8–9:** Explanation chatbot  
- **Weeks 10–12:** Polish, documentation, demo  

