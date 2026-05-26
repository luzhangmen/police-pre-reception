# Week 1 Demo Flow

## Goal

Show that the backend can turn a messy student report into structured case information, risk level, next question, local guidance, and police-side output.

## Before Demo

Start the backend:

```powershell
cd "D:\zsk\Junior\AI+Design system\police-pre-reception\backend"
conda activate police-pre
python -m uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

Use `POST /api/v1/reason`.

## Suggested Demo Cases

### 1. Telecom Fraud

```json
{
  "case_id": "demo-fraud-001",
  "text": "我在闲鱼买演唱会门票，被对方骗了500元，是微信转账的，我还有聊天记录和转账截图。"
}
```

Expected highlights:

- `scenario`: `telecom_fraud`
- Extracted amount/channel/evidence
- Missing reporter and counterparty details
- Medium or high risk depending on extracted ongoing-contact signals
- Follow-up asks for one missing key field

### 2. Property Loss

```json
{
  "case_id": "demo-loss-001",
  "text": "我的黑色iPhone 13昨晚在图书馆不见了，手机里有银行卡和校园卡，可能需要挂失。"
}
```

Expected highlights:

- `scenario`: `property_loss`
- `account_or_id_risk` should raise risk
- KB guidance mentions freezing/reporting loss and protecting accounts

### 3. Dorm Conflict

```json
{
  "case_id": "demo-conflict-001",
  "text": "室友因为卫生问题跟我吵起来，今晚在寝室，还推了我一下，我希望辅导员或宿管介入。"
}
```

Expected highlights:

- `scenario`: `dorm_conflict`
- Risk rules catch physical conflict
- `next_action` should lean toward `handoff_human` when conflict is ongoing or physical

### 4. Personal Safety Threat

```json
{
  "case_id": "demo-threat-001",
  "text": "前男友现在在宿舍楼下堵我，不让我走，我很害怕，我在宿舍楼门口。"
}
```

Expected highlights:

- `scenario`: `personal_safety_threat`
- `emotion`: `fearful`
- `risk_level`: `high`
- `next_action`: `handoff_human`
- Follow-up prioritizes current safety and location

## What To Point Out

1. `slots`: structured fields extracted from free text.
2. `missing_fields`: required information still needed for police handling.
3. `completeness_score`: required-field completion ratio.
4. `risk_level`: local rule judgment, not only LLM output.
5. `knowledge_snippets`: local KB guidance for the scenario.
6. `next_question`: one concise follow-up question.
7. `police_summary`: short officer-facing summary.

## Test Data

The repository includes a larger fixture set for evaluation and prompt tuning:

- `backend/tests/fixtures/demo_cases.json`
- `backend/tests/fixtures/demo_cases_variants.json`
- `backend/tests/fixtures/demo_cases_negative.json`
- `backend/tests/fixtures/demo_dialogues.json`
- `backend/tests/fixtures/demo_transcripts_three_scenarios.json`

See `docs/week1_demo_cases.md` and `docs/fixtures_catalog.md` for the full catalog.
