# AI 五人交付清单

这份以最新分工为准。

第一版总目标：

```text
输入一句用户描述
-> 判断四类场景
-> 抽取关键信息
-> 判断缺什么
-> 判断风险等级
-> 生成下一句追问
-> 输出警方侧结构化结果
```

四类场景：

- 电信/网络诈骗
- 财物遗失
- 宿舍冲突
- 人身安全威胁

---

## 张圣康：总集成和项目把关

你负责把所有人的东西接起来，保证最后系统能跑。

### 你要交付的东西

```text
backend/app/main.py
backend/app/core/state.py
backend/app/core/pipeline.py
docs/api_contract.md
docs/week1_demo_flow.md
README.md
```

### 具体要做到

- 把后端接口搭起来。
- 定好统一的数据结构。
- 把分类、抽取、规则、摘要这些模块串成一条流程。
- 保证输入一句话后，系统能返回完整结果。
- 整理最终演示流程。
- 检查大家字段名有没有对齐。

### 你的最终结果

系统可以完整跑通一条链路：

```text
用户输入 -> pipeline -> 结构化输出
```

---

## 何达煜：知识库 + 场景字段

你负责告诉系统“四类场景分别要收集什么信息”，以及每类场景有哪些基础知识。

### 你要交付的东西

```text
backend/app/schemas/case_schemas.yaml
backend/app/kb/fraud.md
backend/app/kb/property_loss.md
backend/app/kb/dorm_conflict.md
backend/app/kb/safety_threat.md
```

### 具体要做到

- 把四类场景的字段写清楚。
- 每类都分成：
  - 必须问的信息
  - 可以补充的信息
  - 高风险信息
- 给每类场景整理基础处置知识。
- 知识库内容要短、准、能给模型参考。

### 每类场景至少要写清楚

诈骗：

```text
被骗方式、损失金额、转账方式、平台、对方账号、证据、是否还在联系
```

财物遗失：

```text
丢了什么、什么时候丢的、在哪里丢的、物品特征、是否疑似被盗、有没有证据
```

宿舍冲突：

```text
谁和谁冲突、因为什么、发生时间地点、持续多久、有没有威胁或肢体冲突、希望怎么处理
```

人身安全威胁：

```text
威胁类型、对方是谁、现在在哪里、是否正在发生、是否有现实危险、有没有证据
```

### 你的最终结果

别人可以直接根据你的 Schema 写抽取、缺失字段判断和风险规则。

---

## 陆宣辰：测试案例 + 知识库补充

你负责准备“用来测试系统的模拟案例”，并协助补充知识库内容。

### 你要交付的东西

```text
backend/tests/fixtures/demo_cases.json
docs/week1_demo_cases.md
backend/app/kb/fraud.md
backend/app/kb/property_loss.md
backend/app/kb/dorm_conflict.md
backend/app/kb/safety_threat.md
```

### 具体要做到

- 每类场景至少写 5 条测试案例。
- 总共至少 20 条案例。
- 案例要像真实学生说话，不要太官方。
- 每条案例都要标注标准答案。
- 和何达煜一起补充知识库。

### 每条案例要包含

```text
案例编号
用户原话
属于哪类场景
预期风险等级
应该抽取哪些字段
还缺哪些字段
下一步应该问什么
```

### 示例格式

```json
{
  "id": "fraud-001",
  "scenario": "telecom_fraud",
  "input": "我在闲鱼买演唱会票被骗了，微信转了480，对方把我拉黑了",
  "expected_risk": "medium",
  "expected_slots": {
    "platform": "闲鱼",
    "loss_amount": 480,
    "transfer_channel": "微信"
  },
  "expected_missing_fields": ["对方账号", "转账时间", "证据材料"],
  "expected_next_question": "你是否还保留了聊天记录、转账截图或对方账号信息？"
}
```

### 你的最终结果

系统有一批能反复测试的样例，方便判断功能到底有没有做好。

---

## 瞿逸凡：大模型调用 + Prompt 构建

你负责让大模型完成分类、抽取、追问和摘要。

### 你要交付的东西

```text
backend/app/services/llm_client.py
backend/app/prompts/classify.md
backend/app/prompts/extract.md
backend/app/prompts/followup.md
backend/app/prompts/summary.md
backend/app/modules/scenario_classifier.py
backend/app/modules/schema_extractor.py
backend/app/modules/summary_generator.py
```

### 具体要做到

- 写清楚四个 Prompt。
- 封装大模型调用函数。
- 做场景分类。
- 做字段抽取。
- 做下一句追问。
- 做警方侧摘要。
- 模型返回格式尽量固定成 JSON。

### 四个 Prompt 分别干什么

```text
classify.md：判断用户属于四类场景中的哪一类
extract.md：从用户原话里抽取结构化字段
followup.md：根据缺失字段生成下一句追问
summary.md：生成给警察看的简短摘要
```

### 你的最终结果

输入一段用户原话，大模型能帮助系统得到：

```text
场景分类
字段抽取
追问语句
警方摘要
```

---

## 陈誉：后端功能模块 + 测试规则

你负责把系统的规则判断写出来，让系统不完全依赖大模型。

### 你要交付的东西

```text
backend/app/modules/completeness.py
backend/app/modules/risk_triage.py
backend/app/modules/dialogue_policy.py
backend/app/modules/emotion_detector.py
backend/app/modules/knowledge_retriever.py
backend/tests/test_pipeline.py
```

### 具体要做到

- 判断哪些字段还没填。
- 计算信息完整度。
- 判断风险等级。
- 决定下一步动作。
- 做简单情绪判断。
- 做基础知识库检索。
- 写测试，检查 pipeline 能不能正常跑。

### 规则模块分别干什么

```text
completeness.py：看信息缺不缺，算完整度
risk_triage.py：判断 low / medium / high
dialogue_policy.py：决定继续追问、给指引，还是转人工
emotion_detector.py：粗略判断用户是焦虑、害怕、生气还是正常
knowledge_retriever.py：从知识库里找相关内容
test_pipeline.py：测试整个流程能不能跑
```

### 你的最终结果

就算大模型效果不稳定，系统也能靠基础规则跑出一个可用结果。

---

## 全员共同交付

最后全组要一起交付：

```text
1. 四类场景 Schema
2. 四类场景知识库
3. 至少 20 条测试案例
4. 后端基础 API
5. 大模型 Prompt
6. 基础规则模块
7. 一条能跑通的 pipeline
8. 周末演示案例
```

---

## 周末验收标准

周末演示时，至少做到：

- 输入一句话，能识别四类场景。
- 能抽取部分关键信息。
- 能显示还缺哪些信息。
- 能给出完整度分数。
- 能给出风险等级。
- 能生成下一句追问。
- 能生成警方侧摘要。
- 高风险情况能提示转人工。

第一版只看主链路，不追求界面漂亮，也不追求模型一次就特别完美。

