# Architecture Notes

- Batch-first design ensures correctness and auditability
- Online API is a thin wrapper over the same engine
- ML scoring is advisory and failure-tolerant
- Chatbot is constrained by structured inputs
- All components are replaceable without rewriting the system
