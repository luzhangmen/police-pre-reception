# API Contract

Base URL for local development:

```text
http://127.0.0.1:8000
```

Interactive docs:

```text
http://127.0.0.1:8000/docs
```

## GET /

Returns basic service links.

```json
{
  "name": "Police Pre-Reception API",
  "docs": "/docs",
  "health": "/health",
  "reason_endpoint": "/api/v1/reason"
}
```

## GET /health

Health check.

```json
{
  "status": "ok"
}
```

## POST /api/v1/reason

Runs the complete pre-reception pipeline for one user message.

### Request

```json
{
  "case_id": "case-001",
  "text": "我在闲鱼买演唱会门票，被对方骗了500元，是微信转账的，我还有聊天记录和转账截图。"
}
```

`case_id` is optional. `text` is required and cannot be empty.

### Response

```json
{
  "case_id": "case-001",
  "user_text": "我在闲鱼买演唱会门票，被对方骗了500元，是微信转账的，我还有聊天记录和转账截图。",
  "scenario": "telecom_fraud",
  "intent": "unknown",
  "emotion": "neutral",
  "risk_level": "medium",
  "completeness_score": 0.58,
  "slots": {
    "fraud_method": "票务交易诈骗",
    "loss_amount": 500,
    "transfer_channel": "微信",
    "platform": "闲鱼",
    "evidence": ["聊天记录", "转账截图"]
  },
  "missing_fields": ["reporter_name", "reporter_contact"],
  "evidence_checklist": [],
  "key_facts": ["损失金额：500元", "转账渠道：微信"],
  "knowledge_snippets": [
    "先停止继续转账或付款，保留聊天记录、转账凭证、平台订单、对方账号和拉黑记录。"
  ],
  "next_action": "ask_followup",
  "next_question": "请问你的姓名或登记称呼是什么？",
  "police_summary": "学生疑似遭遇票务交易诈骗，已通过微信转账500元，保留聊天记录和转账截图。仍需补充报警人联系方式、收款账户等信息。",
  "suggested_next_steps": ["保存聊天记录和转账凭证", "补充收款账号和联系方式"],
  "extracted_addresses": ["一食堂二楼就餐区"],
  "map_locations": [
    {
      "query": "某某大学 一食堂二楼就餐区",
      "display_name": "University Canteen, Example City",
      "lat": 31.2304,
      "lng": 121.4737,
      "source": "nominatim",
      "map_url": "https://www.google.com/maps/search/?api=1&query=..."
    }
  ]
}
```

### Enum Values

`scenario`:

- `telecom_fraud`
- `property_loss`
- `dorm_conflict`
- `personal_safety_threat`
- `unknown`

`risk_level`:

- `low`
- `medium`
- `high`

`next_action`:

- `ask_followup`: continue asking for missing key information
- `give_guidance`: required information is mostly complete; provide guidance and summary
- `handoff_human`: high risk; human or emergency handling recommended

### Pipeline Notes

The endpoint combines LLM modules and local rules:

1. Kimi classifies the scenario.
2. Local rules detect emotion.
3. Kimi extracts fields according to `case_schemas.yaml`.
4. Local rules compute missing fields and completeness.
5. Local rules triage risk.
6. Local KB retrieval returns `knowledge_snippets`.
7. Kimi generates a follow-up question, with rule-based fallback.
8. Kimi generates police summary payload, with KB snippets as fallback next steps.

The full request may call the LLM multiple times, so it requires `.env` with `LLM_API_KEY`.

After summary generation, the pipeline also:

9. Extracts physical location phrases into `extracted_addresses`.
10. Geocodes up to two addresses into `map_locations` (skipped when `MAP_GEOCODING_ENABLED=false`).

## GET /api/v1/map/config

Returns map-related configuration for the UI.

```json
{
  "geocoding_enabled": true,
  "default_region": "某某大学",
  "map_provider": "google",
  "has_google_maps_key": true,
  "nearby_radius_meters": 250
}
```

## POST /api/v1/map/geocode

Geocode addresses from free text and optional slots without running the full LLM pipeline.

### Request

```json
{
  "text": "今天下午在一食堂二楼手机被偷了",
  "slots": { "lost_location": "一食堂二楼" },
  "max_results": 2
}
```

### Response

```json
{
  "extracted_addresses": ["一食堂二楼", "一食堂二楼就餐区"],
  "map_locations": [],
  "map_provider": "nominatim"
}
```

`map_locations` may be empty when geocoding fails or only online channels are mentioned.

## Voice Input (Browser)

Speech-to-text is handled in `frontend/public/app.js` using the Web Speech API (`zh-CN`). The backend still receives plain text via `POST /api/v1/reason`.
