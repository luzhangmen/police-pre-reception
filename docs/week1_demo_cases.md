# 第一周演示与测试案例（完整版）

| 项目 | 说明 |
|------|------|
| 数据文件 | `backend/tests/fixtures/demo_cases.json` |
| Schema | `backend/tests/fixtures/demo_cases.schema.json` |
| 自动校验 | `backend/tests/test_demo_cases.py`（167 项） |
| 编写指南 | `docs/demo_case_authoring_guide.md` |
| 单轮案例 | **64**（四类各 **16**） |
| 变体 | **24**（`demo_cases_variants.json`） |
| 负例 | **12**（`demo_cases_negative.json`） |
| 多轮对话 | **20** 组（`demo_dialogues.json`） |
| 全目录 | `docs/fixtures_catalog.md` |
| **三类笔录** | `docs/transcripts_fraud_theft_fight.md`（诈骗/盗窃/打架各 24 份，含 288 微差变体） |
| 字段中文 | `field_labels_zh.json` |
| 消歧指南 | `docs/scenario_disambiguation.md` |
| 评测矩阵 | `docs/week1_evaluation_matrix.md` |
| 维护人 | 陆宣辰 |

---

## 1. 场景与字段

### 1.1 场景枚举

| `scenario` | 中文 | 案例前缀 |
|------------|------|----------|
| `telecom_fraud` | 电信/网络诈骗 | `fraud-` |
| `property_loss` | 财物遗失 | `loss-` |
| `dorm_conflict` | 宿舍冲突 | `conflict-` |
| `personal_safety_threat` | 人身安全威胁 | `threat-` |

### 1.2 必填字段（决定完整度与 missing_fields）

| 场景 | required 字段 |
|------|----------------|
| 诈骗 | `fraud_method`, `loss_amount`, `transfer_channel`, `evidence` |
| 遗失 | `lost_item`, `lost_time`, `lost_location`, `item_features` |
| 宿舍 | `parties`, `conflict_reason`, `time_location`, `expected_resolution` |
| 人身 | `threat_type`, `suspect_info`, `current_location`, `danger_level` |

### 1.3 风险等级

| 等级 | 典型触发 |
|------|----------|
| `low` | 信息较完整、无 high_risk 信号 |
| `medium` | 信息缺失或中等风险，无即时危险 |
| `high` | `still_transferring`、`account_or_id_risk`、`physical_conflict`、`threat`、`ongoing_threat`、`current_danger` 等 |

### 1.4 下一步动作

| `expected_next_action` | 含义 |
|------------------------|------|
| `ask_followup` | 继续追问缺失信息 |
| `give_guidance` | 必填已齐，给指引/摘要 |
| `handoff_human` | 高风险，建议人工/紧急处置 |

---

## 2. 周末演示脚本（★ 核心 8 条，另有 loss-002 可替换 loss-007）

按顺序演示，覆盖：抽取、缺项、完整度、高风险转人工。

| 顺序 | ID | 用户原话（摘要） | 演示要点 |
|------|-----|------------------|----------|
| 1 | fraud-001 ★ | 闲鱼买票微信 480 被拉黑 | 分类+抽取+完整度 0.75 |
| 2 | fraud-002 ★ | 刷单还在催继续打钱 | 高风险 handoff |
| 3 | loss-003 ★ | 图书馆丢包含身份证银行卡 | 证件风险 high |
| 4 | loss-007 ★ | 自习室丢 iPad 信息很全 | 完整度 1.0 + guidance |
| 5 | conflict-003 ★ | 宿舍打架推人受伤 | 肢体冲突 high |
| 6 | threat-001 ★ | 前男友楼下堵人 | 即时危险 handoff |
| 7 | conflict-008 ★ | 凌晨喝酒砸门摔杯子 | 高情绪+追问安全 |
| 8 | threat-008 ★ | 校外人员连续两晚滋扰 | 校外跟踪 high |

备用短句：`fraud-003`、`loss-004`、`threat-004`（测极短输入追问）。

---

## 3. 全量案例索引

### 3.1 电信/网络诈骗（8）

| ID | 难度 | 风险 | 完整度 | 标签 | 用户原话（摘要） |
|----|------|------|--------|------|------------------|
| fraud-001 | easy | medium | 0.75 | demo_star | 闲鱼买票微信 480 被拉黑 |
| fraud-002 | medium | high | 0.50 | demo_star, handoff | 刷单还在催继续打钱 |
| fraud-003 | hard | medium | 0.00 | sparse | 好像被网络诈骗了 |
| fraud-004 | easy | medium | 1.00 | rich | 冒充快递客服支付宝 1200 |
| fraud-005 | easy | medium | 0.75 | rich | QQ群买皮肤红包 300 |
| fraud-006 | medium | medium | 1.00 | regression | 冒充教务 QQ 交教材费 |
| fraud-007 | hard | medium | 0.50 | boundary | 二手群面交没收到货 |
| fraud-008 | medium | high | 0.75 | high_risk | 虚假投资 5 万仍催投 |

### 3.2 财物遗失（8）

| ID | 难度 | 风险 | 完整度 | 标签 | 用户原话（摘要） |
|----|------|------|--------|------|------------------|
| loss-001 | easy | low | 1.00 | rich | 宿舍楼道粉色 AirPods |
| loss-002 | easy | medium | 1.00 | demo_star | 一食堂手机被拿走 |
| loss-003 | medium | high | 1.00 | demo_star, handoff | 图书馆丢包含证件卡 |
| loss-004 | hard | low | 0.00 | sparse | 东西丢了挺急的 |
| loss-005 | medium | medium | 0.75 | rich | 体育馆更衣室钱包 |
| loss-006 | easy | low | 1.00 | rich | 教学楼北侧自行车 |
| loss-007 | easy | low | 1.00 | demo_star | 自习室丢 iPad 有监控 |
| loss-008 | hard | high | 0.75 | boundary, handoff | 宿舍丢手机怕被盗刷 |

### 3.3 宿舍冲突（8）

| ID | 难度 | 风险 | 完整度 | 标签 | 用户原话（摘要） |
|----|------|------|--------|------|------------------|
| conflict-001 | easy | low | 0.75 | rich | 室友打游戏外放吵架 |
| conflict-002 | medium | medium | 0.75 | rich | 空调吵一个月想换宿 |
| conflict-003 | medium | high | 1.00 | demo_star, handoff | 卫生分工打架推人 |
| conflict-004 | hard | low | 0.00 | sparse | 跟舍友合不来 |
| conflict-005 | medium | high | 0.75 | handoff | 举报打游戏要被揍 |
| conflict-006 | medium | medium | 0.75 | emotion | 小团体排挤两周 |
| conflict-007 | hard | low | 0.50 | boundary | 室友翻抽屉用充电宝 |
| conflict-008 | medium | medium | 0.75 | demo_star | 凌晨喝酒砸门摔杯 |

### 3.4 人身安全威胁（8）

| ID | 难度 | 风险 | 完整度 | 标签 | 用户原话（摘要） |
|----|------|------|--------|------|------------------|
| threat-001 | medium | high | 1.00 | demo_star, handoff | 前男友楼下堵人 |
| threat-002 | medium | medium | 0.75 | rich | 表白墙匿名威胁 |
| threat-003 | easy | low | 1.00 | rich | 网上骂要打我这周没事 |
| threat-004 | hard | medium | 0.00 | sparse | 有人威胁我怎么办 |
| threat-005 | medium | medium | 1.00 | regression | 同学跟踪有录音 |
| threat-006 | hard | high | 1.00 | handoff | 前男友极端言论害怕 |
| threat-007 | hard | high | 1.00 | boundary | 室友说要杀死我 |
| threat-008 | medium | high | 1.00 | demo_star, handoff | 校外人员翻围墙滋扰 |

---

## 4. 覆盖矩阵

| 维度 | 数量 | 案例 ID 示例 |
|------|------|----------------|
| 演示推荐 demo_star | 9 | 第 2 节用其中 8 条 |
| 高风险 high | 10 | fraud-002/008, loss-003/008, conflict-003/005, threat-001/006/007/008 |
| 极短输入 sparse | 4 | fraud-003, loss-004, conflict-004, threat-004 |
| 边界 boundary | 4 | fraud-007, loss-008, conflict-007, threat-007 |
| 完整度 = 0 | 4 | 同上 sparse |
| 完整度 = 1 | 12 | fraud-004/006, loss-001/002/003/006/007, conflict-003, threat-001/003/005/007/008 等 |

---

## 5. 边界案例说明

| ID | 主场景 | 可接受备选 | 说明 |
|----|--------|------------|------|
| fraud-007 | telecom_fraud | property_loss | 面交未交货，已转账失联 |
| loss-008 | property_loss | dorm_conflict | 发生在宿舍但核心是支付风险 |
| conflict-005 | dorm_conflict | personal_safety_threat | 宿舍内“要打你” |
| conflict-007 | dorm_conflict | property_loss | 涉及物品但是侵权冲突 |
| threat-007 | personal_safety_threat | dorm_conflict | 室友死亡威胁 |

---

## 6. 模型评测 rubric（建议）

对每条案例，pipeline 输出与 ground truth 对比：

| 维度 | 通过标准（第一周宽松） |
|------|------------------------|
| 场景分类 | 等于 `scenario` 或落在 `acceptable_alternate_scenarios` |
| 风险等级 | 与 `expected_risk` 一致，或 high 不漏判 |
| 完整度 | 与 `expected_completeness` 误差 ≤ 0.25 |
| 缺失字段 | 与 `expected_missing_fields`  Jaccard ≥ 0.5 |
| 追问 | 含 `expected_next_question_keywords` 中至少 2 个词 |
| 动作 | `expected_next_action` 一致（high 必须 handoff） |

**第一周目标**：主链路能跑、高风险不漏；不要求 slots 完全一致。

---

## 7. 团队成员使用方式

```bash
# 校验案例库
cd backend && python -m pytest tests/test_demo_cases.py -q

# 读取案例（Python）
import json
from pathlib import Path
cases = json.loads(Path("tests/fixtures/demo_cases.json").read_text(encoding="utf-8"))
star = [c for c in cases if "demo_star" in c.get("tags", [])]
```

| 成员 | 建议 |
|------|------|
| 张圣康 | 演示流用第 2 节 8 条 ★ |
| 何达煜 | Schema 变更时同步 required，并通知更新 fixture |
| 瞿逸凡 | 用 boundary + sparse 调 Prompt |
| 陈誉 | `test_pipeline.py` 参数化 `demo_cases.json` |
| 陆宣辰 | 维护 JSON、KB、`week1_demo_cases.md` |

---

## 8. 详细案例（★ 演示条全文）

### fraud-001 ★

- **原话**：我在闲鱼买演唱会票被骗了，微信转了480，对方把我拉黑了
- **场景**：`telecom_fraud` | **风险**：medium | **完整度**：0.75 | **动作**：ask_followup
- **slots**：platform=闲鱼, fraud_method=购票诈骗, loss_amount=480, transfer_channel=微信, still_contacting=false
- **仍缺**：evidence
- **追问**：你是否还保留了聊天记录、转账截图或对方收款账号？

### fraud-002 ★

- **原话**：刷单兼职对方让我先垫付2000，我又转了1500过去，现在还在催我继续打钱
- **场景**：`telecom_fraud` | **风险**：high | **完整度**：0.50 | **动作**：handoff_human
- **高风险标志**：still_transferring, still_contacting
- **追问**：请先停止一切转账。对方是通过什么方式收款的？有没有转账记录或对方账号？

### loss-003 ★

- **原话**：书包在图书馆丢了，里面有身份证和银行卡，昨晚丢的
- **场景**：`property_loss` | **风险**：high | **完整度**：1.00 | **动作**：handoff_human
- **高风险标志**：account_or_id_risk
- **追问**：请尽快挂失银行卡、冻结第三方支付，并确认身份证是否需要补办。是否怀疑被盗？

### threat-001 ★

- **原话**：前男友现在在宿舍楼下堵我，不让我走，我很害怕
- **场景**：`personal_safety_threat` | **风险**：high | **完整度**：1.00 | **动作**：handoff_human
- **高风险标志**：ongoing_threat, current_danger
- **追问**：你现在身边有没有同学或保安？能否先进入有人的地方并拨打110或校园报警电话？

> 其余 28 条完整字段见 `demo_cases.json`；每条含 `evaluator_notes` 供人工阅卷。

---

## 9. 知识库对应关系

| KB 文件 | 场景 |
|---------|------|
| `backend/app/kb/fraud.md` | telecom_fraud |
| `backend/app/kb/property_loss.md` | property_loss |
| `backend/app/kb/dorm_conflict.md` | dorm_conflict |
| `backend/app/kb/safety_threat.md` | personal_safety_threat |

知识库与案例 ID 交叉引用见各 KB 文末「推荐测试案例 ID」。

---

## 10. 新增批次（009–012）

每类新增 4 条，覆盖：冒充公检法、网恋、二次退款、小额诈骗；实验室显示器、快递被拆；抽烟/访客/调解无效；武器图片、网约车跟踪、亲属威胁等。

详见 `demo_cases.json` 中 `fraud-009`–`threat-012`。

## 11. 多轮对话（12 组）

| dialogue_id | 轮数 | 说明 |
|-------------|------|------|
| dlg-fraud-001 | 2 | 诈骗补证据 ★ |
| dlg-fraud-002 | 2 | 刷单止损 |
| dlg-loss-001 | 2 | 证件遗失挂失 |
| dlg-loss-002 | 3 | 极短三轮补全 |
| dlg-conflict-001 | 2 | 噪音→诉求 |
| dlg-conflict-002 | 2 | 威胁是否动手 |
| dlg-threat-001 | 2 | 楼下堵人 ★ |
| dlg-threat-002 | 2 | 匿名威胁截图 |
| dlg-misclass-001 | 2 | 消歧→诈骗 |
| dlg-misclass-002 | 2 | 消歧→宿舍 |
| dlg-full-001 | 3 | 诈骗全流程 |
| dlg-full-002 | 2 | 手机盗刷风险 |

## 12. 变更记录

| 版本 | 说明 |
|------|------|
| v1 | 20 条基础案例 |
| v2 | 32 条 + 元数据 + pytest |
| v3 | 48 单轮 + 12 多轮 + 消歧/评测/KB |
| v4 | **64** 单轮 + **24** 变体 + **12** 负例 + **20** 多轮 + pipeline E2E |
