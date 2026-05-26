# Demo Cases & Dialogues Fixtures

## 文件一览

| 文件 | 数量 | 说明 |
|------|------|------|
| `demo_cases.json` | **64** | 单轮 ground-truth（每类 16 条） |
| `demo_cases_variants.json` | **24** | 错别字/口语/emoji 等变体 |
| `demo_cases_negative.json` | **12** | 非案件与拒识 |
| `demo_dialogues.json` | **20** | 多轮对话（含消歧、补全、紧急） |
| `demo_cases.schema.json` | — | 单轮 JSON Schema |
| `field_labels_zh.json` | — | 场景/字段/风险中文标签 |
| `demo_transcripts_three_scenarios.json` | **72** | 诈骗/盗窃/打架 基础笔录（每类 24） |
| `demo_transcripts_three_scenarios_variants.json` | **288** | 每条基础笔录 4 个微差变体 |

## 校验命令

```bash
cd backend
python -m pytest tests/test_demo_cases.py tests/test_demo_dialogues.py -v
```

当前约 **505+** 项自动化断言（含 pipeline E2E）。

完整目录见 `docs/fixtures_catalog.md`。

## 单轮案例扩展字段

除交付清单 7 项外，每条还包含：

- `tags`、`difficulty`
- `expected_completeness`、`expected_next_action`、`expected_emotion`
- `expected_high_risk_flags`、`expected_next_question_keywords`
- `acceptable_alternate_scenarios`、`boundary_notes`、`evaluator_notes`（按需）

## 多轮对话结构

```json
{
  "dialogue_id": "dlg-fraud-001",
  "scenario": "telecom_fraud",
  "turns": [
    { "turn": 1, "user": "...", "expected_completeness": 0.75 },
    { "turn": 2, "user": "...", "expected_slots_delta": { "evidence": "..." } }
  ],
  "final_expected_police_summary_points": ["...", "..."]
}
```

## 相关文档

- `docs/week1_demo_cases.md` — 全量索引与演示脚本
- `docs/scenario_disambiguation.md` — 四类消歧
- `docs/week1_evaluation_matrix.md` — 评测打分表
- `docs/demo_case_authoring_guide.md` — 编写规范
- `backend/app/kb/` — 知识库与摘要模板

## 批量扩充脚本

```bash
# 单轮口语案例
python tests/scripts/expand_demo_cases.py

# 三类笔录（含 batch-2 013–024）+ 微差变体
python tests/scripts/build_transcripts_three_scenarios.py
python tests/scripts/build_transcript_variants.py
```

batch-2 笔录定义见 `tests/scripts/transcripts_batch2.py`。

维护：陆宣辰
