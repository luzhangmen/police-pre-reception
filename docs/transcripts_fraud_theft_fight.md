# 诈骗 · 盗窃 · 打架 三类笔录样例库

> 数据文件：`backend/tests/fixtures/demo_transcripts_three_scenarios.json`  
> 维护：陆宣辰  
> 基础笔录 **72** 份（每类 **24** 份，含 batch-1 + batch-2）  
> 微差变体 **288** 份（每份基础笔录 **4** 个变体）→ 合计 **360** 条

## 1. 与系统场景的对应关系

| 口语类别 | 系统 `scenario` | 笔录中须体现的关键字段 |
|----------|-----------------|------------------------|
| **诈骗** | `telecom_fraud` | `fraud_method`、`loss_amount`、`transfer_channel`、`evidence` |
| **盗窃** | `property_loss` | 四要素 + **`suspected_theft: true`** |
| **打架** | `dorm_conflict` | 四要素 + **`physical_conflict: true`** |

盗窃、打架在预接待里分别挂在「财物遗失」「宿舍冲突」下，笔录里会写明「涉嫌盗窃」「发生肢体冲突」，便于模型与规则对齐。

## 2. 笔录体例说明

每条包含：

| 字段 | 说明 |
|------|------|
| `id` | 如 `transcript-fraud-001` |
| `title` | 笔录标题 |
| `record_type` | `victim_inquiry` 受害人询问 / `subject_inquiry` 行为人 / `witness_inquiry` 证人 |
| `subject` | 被询问人基本情况 |
| `body` | **问答正文**（`问：` / `答：`） |
| `plain_summary` | 一段式警方摘要（可直接测 `police_summary`） |
| `expected_slots` | 应从笔录中抽取的结构化字段 |
| `expected_missing_fields` | 相对必填项仍缺什么 |
| `expected_risk` | 低/中/高 |

## 3. 诈骗类 24 份索引

### 3.1 batch-1（001–012）

| ID | 标题 |
|----|------|
| transcript-fraud-001 | 闲鱼购票诈骗 |
| transcript-fraud-002 | 刷单（仍在催款） |
| transcript-fraud-003 | 冒充快递客服 |
| transcript-fraud-004 | 冒充公检法 |
| transcript-fraud-005 | 游戏装备交易 |
| transcript-fraud-006 | 冒充学校教务 |
| transcript-fraud-007 | 二手交易未交货 |
| transcript-fraud-008 | 虚假投资平台 |
| transcript-fraud-009 | 二次退款诈骗 |
| transcript-fraud-010 | 网恋交友诈骗 |
| transcript-fraud-011 | 钓鱼短信充值 |
| transcript-fraud-012 | 校园贷恐吓催收 |

### 3.2 batch-2（013–024）

| ID | 标题 |
|----|------|
| transcript-fraud-013 | 冒充辅导员活动保证金 |
| transcript-fraud-014 | 虚假招聘培训费 |
| transcript-fraud-015 | 游戏代练押金 |
| transcript-fraud-016 | 中奖缴纳税费 |
| transcript-fraud-017 | 兼职模特押金 |
| transcript-fraud-018 | 冒充外卖站长入职费 |
| transcript-fraud-019 | 虚假退款链接（网购） |
| transcript-fraud-020 | 数码租借押金 |
| transcript-fraud-021 | 贩卖考试答案 |
| transcript-fraud-022 | 冒充亲友紧急借钱 |
| transcript-fraud-023 | 虚假慈善募捐 |
| transcript-fraud-024 | AI换脸裸聊敲诈 |

## 4. 盗窃类 24 份索引

### 4.1 batch-1（001–012）

| ID | 标题 |
|----|------|
| transcript-theft-001 | 食堂手机被盗 |
| transcript-theft-002 | 图书馆书包（含证件） |
| transcript-theft-003 | 体育馆更衣室钱包 |
| transcript-theft-004 | 宿舍楼道耳机 |
| transcript-theft-005 | 教学楼自行车 |
| transcript-theft-006 | 实验室显示器 |
| transcript-theft-007 | 快递点拆包 |
| transcript-theft-008 | 自习室笔记本 |
| transcript-theft-009 | 洗澡间眼镜 |
| transcript-theft-010 | 机房 U 盘 |
| transcript-theft-011 | 手机丢失（支付风险） |
| transcript-theft-012 | 教室讲台钱包 |

### 4.2 batch-2（013–024）

| ID | 标题 |
|----|------|
| transcript-theft-013 | 电动车电瓶被盗 |
| transcript-theft-014 | 宿舍共享充电宝 |
| transcript-theft-015 | 操场看台外套 |
| transcript-theft-016 | 琴房小提琴 |
| transcript-theft-017 | 打印店钱包 |
| transcript-theft-018 | 超市自助结账手机 |
| transcript-theft-019 | 校车行李架双肩包 |
| transcript-theft-020 | 摄影社活动相机 |
| transcript-theft-021 | 外卖柜取餐被盗 |
| transcript-theft-022 | 招聘会展位样品 |
| transcript-theft-023 | 游泳馆更衣柜 |
| transcript-theft-024 | 校园卡被盗刷 |

## 5. 打架类 24 份索引

### 5.1 batch-1（001–012）

| ID | 标题 |
|----|------|
| transcript-fight-001 | 宿舍卫生纠纷（受害人） |
| transcript-fight-002 | 宿舍打架（行为人陈述） |
| transcript-fight-003 | 篮球场冲突 |
| transcript-fight-004 | 食堂排队 |
| transcript-fight-005 | 社团活动室 |
| transcript-fight-006 | 酒后宿舍 |
| transcript-fight-007 | 威胁后打架 |
| transcript-fight-008 | 校外大排档 |
| transcript-fight-009 | 图书馆占座 |
| transcript-fight-010 | 实习车间 |
| transcript-fight-011 | 微信群骂升级 |
| transcript-fight-012 | 球场打架（证人） |

### 5.2 batch-2（013–024）

| ID | 标题 |
|----|------|
| transcript-fight-013 | 选修课小组作业冲突 |
| transcript-fight-014 | 体检排队推搡 |
| transcript-fight-015 | 停车位纠纷 |
| transcript-fight-016 | 支教实践基地冲突 |
| transcript-fight-017 | 考研自习室占座 |
| transcript-fight-018 | 羽毛球馆场地冲突 |
| transcript-fight-019 | 校园音乐节入口 |
| transcript-fight-020 | 兼职工资纠纷 |
| transcript-fight-021 | 实验室署名争议 |
| transcript-fight-022 | 外卖员与门卫（劝架受伤） |
| transcript-fight-023 | 拉拉队选拔（行为人） |
| transcript-fight-024 | 篮球场冲突（证人 batch-2） |

## 6. 微差变体库（同案情、不同人/时间/地点）

| 项目 | 说明 |
|------|------|
| 文件 | `backend/tests/fixtures/demo_transcripts_three_scenarios_variants.json` |
| 生成 | `python tests/scripts/build_transcript_variants.py` |
| 命名 | `transcript-fraud-001-v01` … `v04`（`parent_id` 指向基础笔录） |

每个变体在保持 **同一诈骗/盗窃/打架框架** 下，微调例如：

- 受害人姓名、性别、年级（`subject`）
- 案发日期（±1～2 天）
- 金额（约 ±5%～10%，如有 `loss_amount`）
- 地点用词（如一食堂↔二食堂、闲鱼↔转转）
- 证据表述、收款昵称等

字段 `diff_notes`、`diff_dimensions` 标明本条与母版差异维度，便于做**鲁棒性/回归测试**（模型不应因人名不同就改场景分类）。

```bash
python -m pytest tests/test_demo_transcript_variants.py -v
```

## 7. 使用方式

### 校验结构

```bash
cd backend
python -m pytest tests/test_demo_transcripts.py -v
```

### 当作 pipeline 输入

将 `body` 或 `plain_summary` 作为 `UserMessage.text` 做抽取/摘要试验：

```python
import json
from pathlib import Path
from app.core.pipeline import run_pipeline
from app.core.state import UserMessage

data = json.loads(Path("tests/fixtures/demo_transcripts_three_scenarios.json").read_text(encoding="utf-8"))
case = next(t for t in data["transcripts"] if t["id"] == "transcript-fraud-001")
state = run_pipeline(UserMessage(text=case["body"], case_id=case["id"]))
```

### 与口语案例的区别

| 对比项 | `demo_cases.json` | 本笔录库 |
|--------|-------------------|----------|
| 文体 | 学生口语一两句话 | 规范问答应笔录 |
| 用途 | 预接待首轮输入 | 摘要生成、结构化抽取、警方侧文书 |
| 长度 | 短 | 长（多轮问答） |

## 8. 重新生成

```bash
python tests/scripts/build_transcripts_three_scenarios.py
```

修改 `build_transcripts_three_scenarios.py` 中 `FRAUD` / `THEFT` / `FIGHT`，或 `transcripts_batch2.py` 中 batch-2 列表后执行上述命令；再执行 `build_transcript_variants.py` 同步变体。
