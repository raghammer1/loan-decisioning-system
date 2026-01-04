# Modular Loan Decisioning Platform with Explainable Outcomes

## Overview
This project implements a **modular, production-style credit decisioning system** inspired by real-world financial institutions.

Unlike toy rule engines or notebook-based ML demos, this system is structured as a **multi-stage decision pipeline** with explicit domain ownership:

- Eligibility
- Verification
- Bureau
- Servicing
- Decisioning

Each module produces **deterministic outcomes, reason codes, and structured evidence**, which are then consumed by an **explanation chatbot** that translates decisions into human-readable explanations — without ever making decisions itself.

The goal is to demonstrate **engineering maturity**, not business correctness.

---

## Why This Project Exists
Real credit systems are not a single ruleset or ML model.  
They are **pipelines of independently-owned modules**, each responsible for a specific risk domain, operating under strict governance, explainability, and performance constraints.

This project exists to show:
- how such systems are architected
- how explainability is preserved end-to-end
- how ML can be integrated safely
- how decisions can be audited and replayed

---

## Key Principles
- **Modules compute facts; decisioning aggregates facts**
- **Rules are deterministic; ML is advisory**
- **Explainability is a first-class output**
- **Chatbot explains decisions; it never creates them**

---

## System Flow (High Level)

Application Intake  
→ Eligibility  
→ Verification  
→ Bureau  
→ Servicing  
→ Decisioning  
→ Decision Output + Explanation Object  
→ Chat Explanation Layer

---

## What This System Is NOT
- A replica of any bank’s internal policies
- A regulatory-compliant product
- A personalized financial advisor
- A UI-heavy loan application platform

---

## Technology Stack
- Python 3.11+
- Polars (batch processing)
- FastAPI (online decision API)
- DuckDB / Parquet (local persistence)
- scikit-learn / LightGBM (ML scoring)
- Ollama + open-source LLM (explanations only)

All components run **locally and free**.

---

## Deliverables
- Deterministic decision engine with tests
- Modular domain separation
- ML risk scoring (optional layer)
- Structured explanation objects
- Chat-based explanation service
- Design documentation + diagrams

See `docs/design.md` for full details.
