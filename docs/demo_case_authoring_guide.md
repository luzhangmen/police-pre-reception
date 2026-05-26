# 测试案例编写指南

供陆宣辰及全组维护 `demo_cases.json`（48 条）与 `demo_dialogues.json`（12 组）时使用。

## 1. 编写原则

1. **像学生说话**：短句、口语、可有情绪词，避免公文腔。
2. **Ground truth 只写确定的**：`expected_slots` 仅包含从原话能明确推断的字段，不要猜测。
3. **缺失字段只对 required**：与 `completeness.py` / `case_schemas.yaml` 的 `required` 一致；可选字段缺失不写进 `expected_missing_fields`。
4. **边界案例要标注**：使用 `tags: ["boundary"]` 和 `acceptable_alternate_scenarios`。
5. **追问只问一件事**：`expected_next_question` 一句话，并用 `expected_next_question_keywords` 约束核心词。

## 2. 完整度计算

```
completeness = 已填 required 字段数 / required 总数
```

四类 required 均为 4 个字段（见 `case_schemas.yaml`）。

## 3. 风险与 next_action

| expected_risk | 建议 expected_next_action |
|---------------|---------------------------|
| high | handoff_human |
| medium/low 且有 missing | ask_followup |
| medium/low 且无 missing | give_guidance |

## 4. 标签（tags）

| 标签 | 含义 |
|------|------|
| `demo_star` | 周末演示推荐 |
| `sparse_input` | 极短输入，测追问 |
| `rich_slots` | 信息较全 |
| `high_risk` | 命中 high_risk 信号 |
| `boundary` | 易混淆场景 |
| `handoff` | 应转人工 |
| `emotion_heavy` | 情绪明显 |
| `regression` | 回归测试保留 |

## 5. 新增案例检查清单

- [ ] `id` 唯一，命名 `fraud|loss|conflict|threat-NNN`
- [ ] 跑 `pytest tests/test_demo_cases.py`
- [ ] 同步更新 `docs/week1_demo_cases.md` 索引表
- [ ] 若涉及新说法，在对应 `kb/*.md` 补一行映射

## 6. 多轮对话

- 文件：`backend/tests/fixtures/demo_dialogues.json`
- 每轮可写 `expected_slots_delta`，评测时合并到 slots
- 必须提供 `final_expected_police_summary_points`（2–6 条要点）
- 消歧对话使用 `acceptable_scenarios`（首轮）或 `expected_scenario`（澄清后）

## 7. 中文标签

字段展示用 `field_labels_zh.json`，勿在 JSON 案例里用中文作 field key。

## 8. 与分工接口

| 同学 | 如何使用 |
|------|----------|
| 何达煜 | Schema 变更时通知更新 required |
| 瞿逸凡 | 用案例调 Prompt，对比 slots / scenario |
| 陈誉 | 在 `test_pipeline.py` 引用 fixture 做端到端断言 |
| 张圣康 | 演示流选用 `demo_star` 案例 |
