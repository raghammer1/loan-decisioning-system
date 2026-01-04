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

---

## 10. Machine Learning (Risk Scoring Layer)

### Purpose

The Machine Learning (ML) layer provides a **probabilistic risk signal** to augment deterministic rules.

The ML model:
- **does not make approval decisions**
- **does not override hard rules**
- acts only as an **advisory risk score**

This ensures explainability, auditability, and safe degradation.

---

### Model Role in the System

The ML layer produces:
- `pd` — probability of default
- `risk_band` — discretised risk tier (e.g. LOW / MEDIUM / HIGH)

The Decisioning module uses this output as:
- a **decline gate** (e.g. `pd > threshold`)
- or a **refer trigger**
- or an **approval modifier**

If ML is unavailable, the system falls back to **rules-only decisioning**.

---

### Model Choice

Initial implementation uses a **simple, interpretable baseline model**:

- Logistic Regression **or**
- Gradient Boosted Trees (LightGBM)

Rationale:
- Fast inference
- Stable behaviour
- Easy evaluation
- Suitable for local execution

Model complexity is intentionally constrained.

---

### Features

Features are derived from **module-produced facts**, not raw inputs.

Examples:
- dti
- revolving_utilisation
- delinquency_count
- credit_history_length
- net_monthly_surplus
- serviceability_ratio

This reinforces modular ownership and prevents feature leakage.

---

### Evaluation Metrics

The model is evaluated offline using:
- AUC
- KS statistic
- score distribution analysis

Operational metrics tracked:
- inference latency
- score drift (simple PSI)
- decision impact analysis

---

### Failure Handling

- ML scoring failures return `None`
- Decisioning module detects missing score
- Rules-only path is executed
- Decision audit trace records ML unavailability

This guarantees system stability.

---

### Explicit Non-Goals

- No automated feature learning
- No deep neural networks
- No model explainability tooling (e.g. SHAP) in v1
- No online model retraining

Future work may explore these areas.

---

## 11. Explanation Chatbot

### Purpose

The Explanation Chatbot translates **structured decision outputs** into **clear, human-readable explanations**.

It exists solely to explain decisions — **not to make them**.

---

### Inputs

The chatbot receives:
- `decision_output` (canonical decision JSON)
- relevant policy snippets (markdown)
- user question

It does **not** receive:
- raw application data
- training datasets
- internal model parameters

---

### Output Scope

The chatbot may:
- explain why an application was approved, referred, or declined
- describe the primary and supporting reason codes
- provide **generic next steps** based on policy documentation

The chatbot must:
- stay grounded in provided data
- cite reason codes explicitly
- respond conservatively

---

### Guardrails

The chatbot **must not**:
- invent new reasons
- override decisions
- infer missing data
- provide legal or financial advice
- expose internal thresholds not already present in `reason_details`

If asked outside scope, it responds:
> “I don’t have access to that information.”

---

### Prompting Strategy

The system prompt enforces:
- strict grounding
- refusal on unknowns
- neutral, professional tone

Example instruction:
> “You may only use the supplied decision output and policy snippets.  
> Do not speculate or infer additional reasons.”

---

### Technology

- Local, open-source LLM (via Ollama)
- Lightweight orchestration (LangChain or equivalent)
- Retrieval over policy markdown only (RAG)

All components run **locally** and **without paid APIs**.

---

### Performance Considerations

- Chat latency is **not part of decision latency**
- Typical context size: < 3 KB
- One application per interaction

This ensures scalability and predictable behaviour.

---

### Failure Handling

- If decision data is missing → chatbot refuses
- If policy snippet not found → chatbot explains limitation
- LLM errors do not affect decisioning pipeline

---

### Explicit Non-Goals

- Conversational small talk
- Sentiment analysis
- Personalised financial advice
- Multi-application reasoning

The chatbot is intentionally narrow and controlled.
