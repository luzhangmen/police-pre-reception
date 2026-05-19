# AI 五人第一版开发安排

本周目标很简单：先不追求完整产品，先把“基础推理过程”跑通。

也就是做到：

```text
用户说一段话
-> 系统判断是哪类场景
-> 抽取关键信息
-> 看还缺什么
-> 判断风险高不高
-> 生成下一句追问
-> 生成给警察看的结构化结果
```

四类场景只做：

- 电信/网络诈骗
- 财物遗失
- 宿舍冲突
- 人身安全威胁

---

## 张圣康：总负责人，负责把大家的东西串起来

你主要负责“整个系统能不能跑起来”。

重点文件：

```text
backend/app/core/state.py
backend/app/core/pipeline.py
backend/app/main.py
docs/api_contract.md
docs/week1_demo_flow.md
```

### 第一步：先看懂整个流程

你先打开 `pipeline.py`，确认系统流程是不是这样：

```text
分类 -> 情绪判断 -> 信息抽取 -> 缺失字段 -> 完整度 -> 风险分级 -> 下一步动作 -> 警方摘要
```

你不用一开始就写复杂逻辑，先保证每一步都有函数，每个函数都能返回东西。

### 第二步：定好统一的数据格式

你主要改 `state.py`。

要确定最后大家都围绕同一个 `CaseState` 开发，比如：

```text
case_id：案件编号
user_text：用户原话
scenario：四类场景之一
emotion：情绪
risk_level：风险等级
slots：抽出来的信息
missing_fields：还缺的信息
completeness_score：完整度
next_action：下一步动作
next_question：下一句追问
police_summary：给警察看的摘要
```

这一步很重要，因为别人写的模块最后都要往这个结构里面塞结果。

### 第三步：把 API 格式写清楚

你改 `docs/api_contract.md`。

写清楚前端或测试的人怎么调用接口：

```text
POST /api/v1/reason
```

输入：

```json
{
  "case_id": "demo-001",
  "text": "我在闲鱼买演唱会票被骗了，转了500块"
}
```

输出大概长这样：

```json
{
  "scenario": "telecom_fraud",
  "risk_level": "medium",
  "slots": {},
  "missing_fields": [],
  "next_question": "",
  "police_summary": ""
}
```

### 第四步：每天检查大家模块能不能接上

你每天至少跑一次总流程：

```text
用户输入一句话
pipeline 能不能完整返回结果
```

如果某个人的模块还没写完，你就先让它返回假数据，不要让整个系统断掉。

### 第五步：准备最终演示流程

你改 `docs/week1_demo_flow.md`。

准备四个演示例子：

```text
一个诈骗
一个财物遗失
一个宿舍冲突
一个人身威胁
```

每个例子都要能展示：

```text
分类结果
抽取结果
缺失信息
风险等级
下一句追问
警方摘要
```

### 你的验收标准

- 一条用户输入能完整跑完整条 pipeline。
- 别人写的模块都能被你接进来。
- 最后可以拿 4 个案例做完整演示。

---

## 陈誉：负责四类场景字段和测试案例

你主要负责“系统到底要问用户什么”。

重点文件：

```text
backend/app/schemas/case_schemas.yaml
backend/tests/fixtures/demo_cases.json
docs/week1_demo_cases.md
```

### 第一步：给四类场景列字段

你先改 `case_schemas.yaml`。

每类场景都要分三种字段：

```text
required：必须问到的信息
optional：能问到更好，但不是必须
high_risk：一出现就可能风险较高的信息
```

比如诈骗场景：

```text
必须问：
被骗方式
损失金额
转账方式
有没有证据

可以补充：
在哪个平台
对方账号
是否还在联系
是否还在继续转账

高风险：
还在继续转账
对方还在诱导付款
```

### 第二步：每类场景写 5 条模拟案例

你改 `demo_cases.json`。

每类至少 5 条，总共至少 20 条。

不要写得太规整，要像真实学生说话，比如：

```text
“我在闲鱼买票被骗了，对方让我微信转了480，现在把我拉黑了”

“我手机昨晚在宿舍楼下不见了，里面还有银行卡和校园卡”

“我室友一直半夜外放，我跟他说了好几次，现在快吵起来了”

“有个人一直跟着我，还发消息威胁我，我现在有点害怕”
```

### 第三步：给每条案例标答案

每条案例不要只写输入，还要写预期结果：

```text
应该属于哪类场景
大概是什么风险
应该抽出哪些字段
还缺哪些字段
下一步应该问什么
```

这样后面测试系统的时候，就知道系统做得对不对。

### 第四步：帮何达煜定完整度规则

你要告诉何达煜：

```text
哪些字段必须有
缺哪个字段影响最大
哪些字段缺了还能继续
哪些字段一出现就要提高风险
```

比如人身威胁里：

```text
当前位置、是否正在危险中
```

这两个就比“对方姓名”更重要。

### 第五步：整理成文档

你改 `docs/week1_demo_cases.md`。

写清楚：

```text
四类场景分别是什么
每类需要收集什么信息
每类有哪些典型例子
每类什么时候算高风险
```

### 你的验收标准

- 四类场景字段清楚。
- 每类至少 5 条案例。
- 每条案例有标准答案。
- 后端可以根据你的 Schema 判断缺什么。

---

## 何达煜：负责后端规则、风险分级和下一步动作

你主要负责“系统不靠大模型也能做基本判断”。

重点文件：

```text
backend/app/modules/completeness.py
backend/app/modules/risk_triage.py
backend/app/modules/dialogue_policy.py
backend/tests/test_pipeline.py
```

### 第一步：实现缺失字段判断

你改 `completeness.py`。

逻辑很简单：

```text
先看当前场景是什么
再去找这个场景有哪些必填字段
然后看 slots 里面有没有这些字段
没有的就放进 missing_fields
```

比如诈骗场景必须有：

```text
fraud_method
loss_amount
transfer_channel
evidence
```

如果只抽到了金额和平台，那就要返回：

```text
缺少 fraud_method、transfer_channel、evidence
```

### 第二步：实现完整度评分

还是在 `completeness.py`。

先用最简单的算法：

```text
完整度 = 已经填好的必填字段数量 / 全部必填字段数量
```

比如 4 个必填字段，填了 2 个：

```text
完整度 = 0.5
```

后面再考虑字段权重，现在第一版不要复杂化。

### 第三步：实现风险分级

你改 `risk_triage.py`。

风险分三级：

```text
low：低风险
medium：中风险
high：高风险
```

先用规则判断：

```text
人身安全威胁，默认 medium 起步
正在被跟踪、正在被威胁、现在不安全，直接 high
诈骗还在继续转账，high
被骗但已经停止联系，medium
普通财物遗失，low 或 medium
宿舍冲突没有威胁，low 或 medium
宿舍冲突出现肢体冲突、威胁，high
```

第一版要保守一点：不确定的时候宁可风险高一点。

### 第四步：决定下一步动作

你改 `dialogue_policy.py`。

系统下一步只有三种：

```text
ask_followup：继续追问
give_guidance：给普通指引
handoff_human：转人工或提醒联系警察
```

规则可以先这样：

```text
high -> handoff_human
medium 且信息不完整 -> ask_followup
low 且信息完整 -> give_guidance
unknown -> ask_followup
```

### 第五步：写测试

你改 `test_pipeline.py`。

至少测试这些：

```text
诈骗案例能识别风险
人身威胁能变 high
缺字段能被找出来
完整度能算出来
高风险能触发 handoff_human
```

### 你的验收标准

- 系统知道缺哪些信息。
- 系统能算完整度。
- 系统能分 low / medium / high。
- 高风险情况能转人工。
- 基础测试能跑过。

---

## 陆宣辰：负责大模型、Prompt、抽取和知识库

你主要负责“让系统更聪明一点”。

重点文件：

```text
backend/app/prompts/classify.md
backend/app/prompts/extract.md
backend/app/prompts/followup.md
backend/app/prompts/summary.md
backend/app/modules/scenario_classifier.py
backend/app/modules/schema_extractor.py
backend/app/modules/summary_generator.py
backend/app/modules/knowledge_retriever.py
backend/app/services/llm_client.py
backend/app/kb/
```

### 第一步：先把 Prompt 写清楚

你先改 `prompts/` 下面四个文件。

分类 Prompt 要让模型只输出：

```text
telecom_fraud
property_loss
dorm_conflict
personal_safety_threat
unknown
```

抽取 Prompt 要让模型按 Schema 输出 JSON。

追问 Prompt 要让模型只问一句话，不要长篇解释。

摘要 Prompt 要让模型生成给警察看的短摘要。

### 第二步：做场景分类

你改 `scenario_classifier.py`。

第一版可以先这样：

```text
先用关键词规则兜底
再接大模型分类
如果模型失败，就用规则结果
```

这样系统不容易因为 API 出问题直接不能跑。

### 第三步：做信息抽取

你改 `schema_extractor.py`。

目标是输入：

```text
“我在闲鱼买票被骗了，微信转了480，对方把我拉黑了”
```

输出类似：

```json
{
  "platform": "闲鱼",
  "fraud_method": "低价票诈骗",
  "loss_amount": 480,
  "transfer_channel": "微信",
  "still_contacting": false
}
```

第一版不要求特别完美，但字段名要和 `case_schemas.yaml` 对上。

### 第四步：做警方摘要

你改 `summary_generator.py`。

摘要不要写成聊天回复，要写成警察能快速看的内容：

```text
学生疑似遭遇闲鱼演唱会票诈骗，已通过微信转账480元，对方随后拉黑。当前缺少对方账号和转账时间，已有聊天记录和转账截图待确认。风险等级：中。
```

### 第五步：做轻量知识库

你改 `kb/` 下面四个 Markdown。

每个文件写对应场景的基本处置知识：

```text
诈骗：保留聊天记录、转账截图、对方账号、平台订单信息
财物遗失：记录时间地点、物品特征、查找轨迹、证件挂失
宿舍冲突：先记录事实、避免升级、可联系辅导员或宿管
人身威胁：先确认安全、保留威胁证据、必要时立刻联系人工或报警
```

第一版 `knowledge_retriever.py` 可以先做关键词匹配，不急着上向量库。

### 第六步：封装 LLM 调用

你改 `llm_client.py`。

这个文件只做一件事：

```text
给它 prompt
它返回模型结果
```

后面换 DeepSeek、OpenAI 或别的模型，都尽量只改这个文件。

### 你的验收标准

- Prompt 能稳定让模型输出 JSON。
- 四类场景能分类。
- 能抽出核心字段。
- 能生成一句追问。
- 能生成警方摘要。
- 模型挂了也有规则兜底。

---

## 瞿逸凡：负责前端数据结构和警方侧展示方案

你现在先不用写 React 或 Vue。

你主要负责“后面页面到底要展示什么”。

重点文件：

```text
docs/frontend_data_contract.md
docs/police_dashboard_output.md
frontend/README.md
```

### 第一步：先看 API 输出

你先看 `docs/api_contract.md`。

搞清楚后端最后会给前端什么数据：

```text
场景
风险等级
抽取字段
缺失字段
完整度
下一句追问
警方摘要
建议动作
```

### 第二步：设计学生端要展示什么

学生端先不用复杂，第一版只要想清楚这些区域：

```text
聊天输入框
系统回复
数字人占位区
风险较高时的提示
继续补充信息的追问
```

注意：学生端不要展示太吓人的“高风险判定细节”，语气要温和。

### 第三步：设计警方端要展示什么

你改 `police_dashboard_output.md`。

警方端建议分几个区域：

```text
顶部：场景类型 + 风险等级
中间：案件摘要
左侧：结构化字段
右侧：缺失信息和证据清单
底部：建议下一步动作
```

警察最关心的是：

```text
发生了什么
人是否安全
钱有没有损失
证据有没有
还缺什么
下一步该怎么处理
```

### 第四步：写前端数据说明

你改 `frontend_data_contract.md`。

用大白话写清楚每个字段怎么用：

```text
scenario 用来显示案件类型
risk_level 用来显示风险颜色
slots 用来展示结构化信息
missing_fields 用来提示还要问什么
next_question 用来显示给学生看的下一句话
police_summary 用来显示给警察看的摘要
```

### 第五步：可以先画低保真页面

不用定技术栈，可以先画：

```text
纸面草图
Figma 低保真
Markdown 布局说明
```

等后端结果稳定以后，再决定用 React 还是 Vue。

### 你的验收标准

- 前端知道该接哪些字段。
- 学生端和警方端分别展示什么已经清楚。
- 警方 dashboard 的信息层级清楚。
- 后面换任何前端框架都能照这个做。

---

## 每天怎么对齐

每天结束前，每个人在群里说三句话就够：

```text
今天改了哪个文件
现在能跑到什么程度
明天还差什么
```

建议每天按这个顺序对齐：

```text
陈誉先说 Schema 和案例有没有变化
陆宣辰说模型输出字段有没有变化
何达煜说规则有没有接上
张圣康说总流程能不能跑通
瞿逸凡说前端展示需要哪些字段
```

如果字段名变了，一定要同步，不然大家的代码会对不上。

---

## 本周最终验收

到周末，至少做到：

- 四类场景都能识别。
- 每类至少 5 条测试案例。
- 能抽取一部分关键字段。
- 能判断缺哪些信息。
- 能算完整度。
- 能判断风险等级。
- 能生成下一句追问。
- 能生成警方侧摘要。
- 高风险场景能提示转人工。

第一版不要贪多。先把这条主链路跑通，后面再加语音、数字人、RAG 和前端界面。

