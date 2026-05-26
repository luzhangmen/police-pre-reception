# 测试资产全目录（陆宣辰维护）

## 数据文件总览

| 文件 | 数量 | 用途 |
|------|------|------|
| `demo_cases.json` | **64** | 单轮 ground-truth（每类 16） |
| `demo_cases_variants.json` | **24** | 错别字/口语/噪声变体 |
| `demo_cases_negative.json` | **12** | 非案件/拒识/模糊输入 |
| `demo_dialogues.json` | **20** | 多轮对话 + 消歧 + 情绪 |
| `field_labels_zh.json` | — | 字段中文标签 |
| `demo_cases.schema.json` | — | 单轮结构 Schema |

| `demo_transcripts_three_scenarios.json` | **72** | 诈骗/盗窃/打架 规范问答应笔录 |
| `demo_transcripts_three_scenarios_variants.json` | **288** | 笔录微差变体（每基础笔录 4 条） |

**合计**：64 + 24 + 12 + 20 + 72 + 288 = **480** 条可测输入（含笔录及变体）。

笔录专档说明：`docs/transcripts_fraud_theft_fight.md`

## 单轮标签统计（64 条）

| 标签 | 约数量 | 说明 |
|------|--------|------|
| demo_star | 9+ | 演示推荐 |
| boundary | 12+ | 易混淆分类 |
| high_risk | 14+ | 高风险 |
| sparse_input | 6+ | 极短输入 |
| slang / typo | 8+ | 口语与错别字 |
| noise_prefix | 2+ | 前置闲聊噪声 |
| multi_topic | 4+ | 多意图混合 |

## 变体类型（24 条）

`typo` `slang` `dialect` `sparse` `noise_prefix` `emoji` `oral` `code_mix` `verbose` …

每条通过 `parent_id` 关联主案例。

## 负例（12 条）

`neg-001`–`neg-012`：选课、食堂吐槽、代写、在吗、我出事了、乱码、政务咨询等。

## 多轮对话（20 组）

含：补证据、止损、三轮补全、消歧、负例转案件、情绪宣泄、武器图片 handoff 等。

## 自动化测试

```bash
cd backend
python -m pytest tests/ -q
```

| 测试文件 | 内容 |
|----------|------|
| `test_demo_cases.py` | 单轮结构与完整度 |
| `test_demo_dialogues.py` | 多轮结构 |
| `test_demo_variants.py` | 变体与 parent 关联 |
| `test_pipeline_fixtures.py` | Pipeline 中文关键词 E2E |

## 规则层增强（便于 E2E）

- `scenario_classifier.py`：中英关键词 + 消歧
- `risk_triage.py` / `emotion_detector.py`：中文信号

> 第一周仍以案例 ground-truth 为准；规则层用于 demo 可跑通，模型接入后逐步替代。

## 扩充脚本

```bash
python tests/scripts/expand_demo_cases.py          # batch-2
python tests/scripts/expand_demo_cases_batch3.py # batch-3
```

## 相关文档

- `docs/week1_demo_cases.md`
- `docs/scenario_disambiguation.md`
- `docs/week1_evaluation_matrix.md`
- `docs/demo_case_authoring_guide.md`
