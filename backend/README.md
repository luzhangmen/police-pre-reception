# Backend

The backend owns the reasoning pipeline:

1. Classify scenario
2. Detect emotion
3. Extract schema fields
4. Check missing fields
5. Score completeness
6. Triage risk
7. Decide next action
8. Generate police-side summary

## Pre-acceptance document (Word v2.0)

Module owner: 陆宣辰  
**组内交接说明（给组长）**：[`docs/警务预受理文档模块说明_陆宣辰.md`](../docs/警务预受理文档模块说明_陆宣辰.md)

- Core: `app/modules/document_generator.py` (programmatic排版)
- Styling: `app/modules/document_styling.py`
- Content: `app/modules/document_content.py`
- Narrative polish: `app/modules/narrative_polish.py`
- L2 colloquial cases: `tests/fixtures/demo_cases_colloquial.json`
- API: `POST /api/v1/documents/pre-acceptance` (body = `CaseState`)
- Download: `GET /api/v1/documents/download/{filename}`

```bash
cd backend
pip install -r requirements.txt
python scripts/generate_all_showcase_documents.py
python scripts/generate_showcase_demo.py
pytest tests/test_document_generator.py tests/test_narrative_polish.py -q
```

答辩样例输出：`backend/generated/documents/showcase/`（4 类场景各一份）

