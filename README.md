# Police Pre-Reception

Text-first MVP for campus police pre-reception.

## Live Demo（GitHub Pages · 地图）

推送到 GitHub 并启用 Pages 后，队友可直接打开**在线地图演示**（无需安装后端）：

```text
https://luzhangmen.github.io/police-pre-reception/demo.html
```

配置步骤见 [docs/github_pages_demo.md](docs/github_pages_demo.md)。可选：在仓库 Actions Secrets 中设置 `AMAP_WEB_KEY` 以使用高德底图。 The backend accepts one messy user report and returns structured case information, risk level, missing fields, one follow-up question, local knowledge guidance, and a short police-side summary.

## Scenarios

- `telecom_fraud`: telecom or online fraud
- `property_loss`: lost property or suspected theft
- `dorm_conflict`: dormitory conflict
- `personal_safety_threat`: personal safety threat

## MVP Status

Current backend covers the Week 1 MVP:

- Kimi-based scenario classification
- Kimi-based schema extraction
- Rule-based emotion detection
- Rule-based missing-field and completeness scoring
- Rule-based risk triage
- Local KB retrieval
- Kimi-based follow-up question with rule fallback
- Kimi-based police summary payload
- Fixture library and validation tests

Known limits:

- Multi-turn state merge is represented in fixtures but not yet persisted by the API.
- Field extraction quality depends on the LLM response.
- Voice input uses the browser Web Speech API (no server-side ASR yet).
- Map geocoding accuracy depends on `MAP_DEFAULT_REGION` and optional `GOOGLE_MAPS_API_KEY`.

## Setup

Use Python 3.12.

```powershell
cd "D:\zsk\Junior\AI+Design system\police-pre-reception\backend"
conda create -n police-pre python=3.12 -y
conda activate police-pre
python -m pip install -r requirements.txt
```

Create `.env` in the project root, not inside `backend`:

```text
D:\zsk\Junior\AI+Design system\police-pre-reception\.env
```

Example:

```env
LLM_PROVIDER=moonshot
LLM_API_KEY=your_kimi_key
LLM_MODEL=kimi-k2.6
LLM_BASE_URL=https://api.moonshot.cn/v1
```

Do not commit `.env`. Use `.env.example` as the shareable template.

## Run

```powershell
cd "D:\zsk\Junior\AI+Design system\police-pre-reception\backend"
conda activate police-pre
python -m uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/
http://127.0.0.1:8000/docs
```

The home page provides voice/text intake and an incident map. **In China, use Amap (高德地图)** for best campus POI accuracy:

```env
MAP_DEFAULT_REGION=某某大学
AMAP_API_KEY=your_amap_web_service_key
AMAP_WEB_KEY=your_amap_js_key
```

Without Amap keys, the backend falls back to OpenStreetMap Nominatim (works offline in demos, weaker for Chinese addresses).

Try `POST /api/v1/reason` with:

```json
{
  "case_id": "case-001",
  "text": "我在闲鱼买演唱会门票，被对方骗了500元，是微信转账的，我还有聊天记录和转账截图。"
}
```

## Tests

Fixture and rule tests do not call Kimi:

```powershell
cd "D:\zsk\Junior\AI+Design system\police-pre-reception"
py -3.12 -m pytest backend/tests -q
```

The default test suite validates:

- Core rule modules
- Demo case fixture structure
- Dialogue fixtures
- Variant and negative fixtures
- Transcript fixtures

## Important Files

- `backend/app/main.py`: FastAPI entrypoint
- `backend/app/core/state.py`: request and response state models
- `backend/app/core/pipeline.py`: reasoning pipeline
- `backend/app/schemas/case_schemas.yaml`: required/optional/high-risk fields
- `backend/app/kb/`: scenario knowledge base
- `backend/app/prompts/`: LLM prompts
- `backend/tests/fixtures/`: demo and evaluation cases
- `docs/api_contract.md`: API contract
- `docs/week1_demo_flow.md`: demo script
