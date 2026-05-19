# API Contract

## POST /api/v1/reason

Request:

```json
{
  "case_id": "demo-001",
  "text": "User message here"
}
```

Response:

```json
{
  "case_id": "demo-001",
  "scenario": "telecom_fraud",
  "emotion": "anxious",
  "risk_level": "medium",
  "completeness_score": 0.5,
  "slots": {},
  "missing_fields": [],
  "next_action": "ask_followup",
  "next_question": "",
  "police_summary": ""
}
```

