# API Contracts

## POST /decision
Input:
- application features
- customer_id

Output:
- decision object with module results

---

## GET /decision/{app_id}
Returns the stored decision record.

---

## POST /explain
Input:
- app_id
- user question

Output:
- grounded explanation
- cited reason codes

The explanation service cannot override decisions or invent reasons.
