# 第一周评测矩阵

配合 `demo_cases.json`（48 条）与 `demo_dialogues.json`（12 组）使用。

## 1. 单轮必测集（12 条）

| 优先级 | ID | 测什么 |
|--------|-----|--------|
| P0 | fraud-002 | 高风险 handoff + 仍在转账 |
| P0 | loss-003 | 证件风险 high |
| P0 | threat-001 | 即时危险 handoff |
| P0 | fraud-003 | 完整度 0 追问 |
| P1 | fraud-001 | 标准抽取 |
| P1 | loss-007 | 完整度 1 guidance |
| P1 | conflict-003 | 肢体冲突 |
| P1 | threat-009 | 武器图片威胁 |
| P1 | fraud-007 | 边界分类 |
| P2 | conflict-011 | 辱骂非威胁 |
| P2 | threat-010 | 校外跟踪 |
| P2 | fraud-009 | 冒充公检法 |

## 2. 多轮必测集（6 组）

| dialogue_id | 轮数 | 测什么 |
|-------------|------|--------|
| dlg-fraud-001 | 2 | 补证据后完整度 1.0 |
| dlg-loss-002 | 3 | 极短输入逐步补全 |
| dlg-threat-001 | 2 | 紧急→安全位置更新 |
| dlg-misclass-001 | 2 | 消歧到诈骗 |
| dlg-misclass-002 | 2 | 消歧到宿舍 |
| dlg-full-001 | 3 | 完整三轮诈骗 |

## 3. 打分表（每条 0–2 分）

| 维度 | 0 分 | 1 分 | 2 分 |
|------|------|------|------|
| 场景分类 | 错误且无备选 | 错但在 acceptable 内 | 完全正确 |
| 风险等级 | high 漏判 | 差一级 | 正确 |
| 完整度 | 误差 >0.5 | 误差 0.25–0.5 | 误差 ≤0.25 |
| 缺失字段 | Jaccard <0.3 | 0.3–0.6 | ≥0.6 |
| 追问质量 | 无关 | 相关但缺关键词 | 含 2+ 关键词 |
| 警方摘要 | 无输出 | 有但不完整 | 覆盖 summary_points |

**通过线（第一周）**：P0 全过；总分 ≥ 70%（满分按 12 单轮 × 6 维 × 2 分 ≈ 144 计）。

## 4. 自动化 vs 人工

| 项目 | 自动化 `pytest` | 人工 |
|------|-----------------|------|
| JSON 结构、完整度计算 | ✅ test_demo_cases | — |
| 多轮结构 | ✅ test_demo_dialogues | — |
| 模型分类/抽取 | — | 评测矩阵打分 |
| 追问自然度 | — | 人工 |
| 警方摘要 | — | 对照 summary_points |

## 5. 回归策略

每次改 Prompt / Schema / 规则后：

```bash
cd backend
python -m pytest tests/test_demo_cases.py tests/test_demo_dialogues.py -q
```

再跑 P0 单轮 + dlg-fraud-001 人工 spot check。
