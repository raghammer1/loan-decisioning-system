> Design notes: this document may describe planned behavior. See the [current implementation status](../README.md) before treating any feature, test or performance target as delivered.

# Architecture Notes

- Batch-first design ensures correctness and auditability
- Online API is a thin wrapper over the same engine
- ML scoring is advisory and failure-tolerant
- Chatbot is constrained by structured inputs
- All components are replaceable without rewriting the system
