# 下阶段工作执行方案

## 1. 阶段目标

当前项目已经完成文本预处理后端 MVP：用户输入自然语言描述后，系统可以完成场景分类、字段抽取、缺失字段判断、完整度评分、风险分级、知识库建议、下一句追问和警方摘要生成。

下一阶段的核心目标是：先完成各个单一功能模块的独立闭环，最后一周再进行系统级整合，形成从群众表达、数字人交互到警方侧输出的完整流程。

最终系统闭环如下：

```text
视频/文本输入
→ 多模态情绪分析
→ 警务文本推理 pipeline
→ 多轮追问补全
→ 风险分级与知识库建议
→ 警方摘要
→ Word/PDF 预受理信息单
→ 前端群众侧与警方侧展示
```

## 2. 当前项目基础

已完成内容：

- FastAPI 后端接口：`POST /api/v1/reason`
- 统一状态对象：`CaseState`
- 四类警务场景：电信/网络诈骗、财物遗失、宿舍冲突、人身安全威胁
- Kimi 大模型接入：场景分类、字段抽取、追问生成、警方摘要
- 规则模块：完整度判断、风险分级、情绪初判、知识库检索
- 本地知识库：`backend/app/kb/`
- 测试资产：单轮案例、多轮对话、负例、变体、笔录类数据
- Swagger 后端测试入口：`http://127.0.0.1:8000/docs`

当前不足：

- 前端仍是占位目录，尚未与后端联调。
- 知识库仍是关键词检索，还没有向量数据库和 RAG。
- 多轮追问逻辑还没有形成真实会话状态。
- 多模态情绪分析尚未接入后端主流程。
- 警务 Word/PDF 文档生成模块尚未实现。
- 评测指标已有初步文档，但缺少自动化评测脚本和统一结果输出。

## 3. 成员分工总览

| 成员 | 负责方向 | 核心目标 | 主要交付物 |
|------|----------|----------|------------|
| 瞿逸凡 | 评测指标体系 | 建立可量化的系统评测方式，证明系统效果 | `docs/evaluation_plan.md`、`backend/app/evaluation/metrics.py`、`backend/scripts/evaluate_pipeline.py` |
| 陈誉 | 多轮追问机制 | 根据缺失字段连续追问，并在用户补充后更新案件状态 | `backend/app/core/session.py`、`backend/app/core/session_store.py`、`backend/app/modules/slot_merger.py`、`POST /api/v1/dialogue/turn` |
| 何达煜 | RAG 知识库升级 | 搭建知识库向量检索能力，提高知识召回质量 | `backend/app/rag/`、`backend/scripts/build_kb_index.py`、`backend/storage/vector_db/` |
| 陆宣辰 | 警务 Word/PDF 文档生成 | 将结构化案件信息填入预受理信息单模板 | `backend/app/templates/pre_acceptance_template.docx`、`backend/app/modules/document_generator.py`、文档生成接口 |
| 张圣康 | 前后端联动、多模态情绪接入、RAG 接入协作 | 打通页面、后端 pipeline、多模态情绪结果和系统演示链路 | `frontend/`、CORS 与接口联调、多模态接入接口、RAG 与 pipeline 的集成 |
| 全员协同 | 工程清理与文档更新 | 保证项目结构清晰，接口说明与实际代码一致 | README、API 文档、运行说明、模块说明 |

## 4. 按成员执行方案

### 4.1 瞿逸凡：评测指标体系

目标：证明系统不是“能跑”，而是“有可评价的效果”。

需要完成：

- 新建 `docs/evaluation_plan.md`
- 新建 `backend/app/evaluation/metrics.py`
- 新建 `backend/scripts/evaluate_pipeline.py`
- 统一测试数据与 `case_schemas.yaml` 的字段口径
- 输出可放入 PPT 的评测结果表

核心指标：

- 场景分类准确率
- 风险分级准确率
- 高风险漏判率
- 字段抽取 Precision / Recall / F1
- 缺失字段判断准确率
- 完整度评分误差
- 追问字段命中率
- 警方摘要要点覆盖率

验收标准：

- 能通过一条命令运行评测脚本。
- 能输出每类场景的指标结果。
- 高风险案例不得出现明显漏判。

依赖关系：

- 需要使用 `backend/tests/fixtures/` 中已有测试资产。
- 需要和陈誉确认多轮追问的评测口径。
- 需要和张圣康确认最终前端展示所需的指标格式。

### 4.2 陈誉：多轮追问机制

目标：将系统从“单轮分析”升级为“接待流程”。

需要完成：

- 新建 `backend/app/core/session.py`
- 新建 `backend/app/core/session_store.py`
- 新建 `backend/app/modules/slot_merger.py`
- 新增接口：`POST /api/v1/dialogue/turn`

基本流程：

```text
第一轮用户输入
→ 生成 CaseState
→ 读取 missing_fields
→ 生成 next_question
→ 用户补充回答
→ 合并 slots
→ 重算 completeness_score / risk_level / next_action
→ 继续追问或生成总结
```

重点规则：

- 已经问过的字段不重复追问。
- 高风险字段优先追问。
- 用户补充信息可以覆盖原来的 `null` 字段。
- 每一轮都返回更新后的 `CaseState`。

验收标准：

- 至少跑通一个三轮对话案例。
- 财物遗失案例可以通过追问补全关键信息。
- 高风险场景可以提前触发 `handoff_human`。

依赖关系：

- 需要复用现有 `CaseState`、`run_pipeline`、`missing_fields` 和 `next_question`。
- 需要给张圣康提供稳定的多轮接口，方便前端调用。
- 需要给瞿逸凡提供可评测的多轮输出。

### 4.3 何达煜：RAG 知识库升级

目标：将当前关键词检索升级为向量检索，提高知识召回质量。

需要完成：

- 新建 `backend/app/rag/chunker.py`
- 新建 `backend/app/rag/vector_store.py`
- 新建 `backend/app/rag/retriever.py`
- 新建 `backend/scripts/build_kb_index.py`
- 新建本地向量库目录：`backend/storage/vector_db/`

知识库来源：

- `backend/app/kb/fraud.md`
- `backend/app/kb/property_loss.md`
- `backend/app/kb/dorm_conflict.md`
- `backend/app/kb/safety_threat.md`
- `backend/app/kb/faq_cross_scenario.md`
- `backend/app/kb/police_summary_templates.md`

建议技术：

- 第一版可以使用 Chroma 或 FAISS。
- RAG 输出继续保持为 `knowledge_snippets: list[str]`，保证和当前 pipeline 兼容。
- 如果向量库不可用，自动回退到现有关键词检索。

验收标准：

- 能构建本地知识库索引。
- 能根据用户描述召回相关处置建议。
- 财物遗失、诈骗、人身威胁至少各有一条可解释召回结果。

依赖关系：

- 需要与张圣康协作完成 RAG 与 `retrieve_knowledge` / pipeline 的接入。
- 需要与陆宣辰确认知识库输出如何进入警务文档。
- 需要与瞿逸凡确认 RAG 召回质量的评测方式。

### 4.4 陆宣辰：警务 Word/PDF 文档生成

目标：将 `CaseState` 转换为警方可查看、可归档的预受理信息单。

推荐名称：

- 预受理信息单
- 接警辅助摘要
- 笔录辅助草稿

需要完成：

- 新建 `backend/app/templates/pre_acceptance_template.docx`
- 新建 `backend/app/modules/document_generator.py`
- 新建 `backend/app/core/document_models.py`
- 新增接口：`POST /api/v1/documents/pre-acceptance`
- 更新 `backend/requirements.txt`

建议依赖：

```text
python-docx
jinja2
```

文档字段：

- 案件编号
- 报案人姓名
- 报案人联系方式
- 案件类型
- 风险等级
- 完整度评分
- 事件时间
- 事件地点
- 事件经过
- 已抽取结构化字段
- 缺失字段
- 证据材料
- 知识库处置建议
- 警方摘要
- 建议下一步
- 民警备注区

验收标准：

- 输入一个 `CaseState`，可以生成 `.docx` 文件。
- 文档结构清晰、中文不乱码。
- 至少生成财物遗失、诈骗、人身安全威胁三个样例。
- 后续可扩展 PDF 导出。

依赖关系：

- 需要使用后端统一的 `CaseState` 输出。
- 需要与张圣康确认前端如何触发文档生成与下载。
- 需要与何达煜确认 `knowledge_snippets` 如何填入文档。

### 4.5 张圣康：前后端联动

目标：让用户能够在页面中完成输入、查看数字人回应，并让警方侧看到结构化案件信息。

建议技术栈：

```text
Vite + React + TypeScript
```

需要完成：

- 初始化 `frontend`
- 配置后端 CORS
- 封装接口请求：
  - `POST /api/v1/reason`
  - `POST /api/v1/dialogue/turn`
  - `POST /api/v1/documents/pre-acceptance`
- 建立群众侧页面
- 建立警方侧页面

群众侧页面：

- 文本输入框
- 数字人回复区域
- 当前追问
- 情绪状态展示
- 提交按钮

警方侧页面：

- 案件类型
- 风险等级
- 完整度评分
- `slots` 字段表
- `missing_fields`
- `knowledge_snippets`
- `police_summary`
- `suggested_next_steps`
- 生成 Word/PDF 按钮

验收标准：

- 前端可以成功调用 `/api/v1/reason`。
- 页面可以展示完整 `CaseState`。
- 能完成至少一轮追问交互。
- 能触发文档生成。

依赖关系：

- 需要陈誉提供多轮追问接口。
- 需要陆宣辰提供文档生成接口。
- 需要何达煜提供 RAG 检索结果字段。

### 4.6 张圣康：多模态情绪分析接入

目标：将语音、面部表情、文本语义的情绪融合结果接入警务 pipeline。

需要完成：

- 新增 `backend/app/core/emotion_state.py`
- 新增 `backend/app/modules/emotion_fusion.py`
- 新增接口：`POST /api/v1/emotion/fuse`
- 新增接口：`POST /api/v1/multimodal/reason`

输入示例：

```json
{
  "asr_text": "警官你好，我的手机昨晚在图书馆丢了。",
  "modal_emotions": {
    "voice": "情绪平稳",
    "face": "悲伤低落",
    "text": "情绪平稳"
  }
}
```

输出字段：

- `final_emotion`
- `police_description`
- `avatar_response`
- `next_question`
- `empathy_strategy`
- `avatar_performance`
- `case_state`

接入逻辑：

```text
ASR 文本
→ 文本警务 pipeline
→ 多模态情绪融合
→ 数字人回应策略
→ 数字人表现参数
```

验收标准：

- 能接收多模态情绪模块输出的 JSON。
- 能将 `asr_text` 送入现有文本 pipeline。
- 能生成数字人话术和表现参数。
- 情绪状态能够影响回应语气。

依赖关系：

- 需要现有文本 pipeline 稳定返回 `CaseState`。
- 需要前端可以展示 `avatar_response` 和 `avatar_performance`。
- 需要与评测模块确认情绪输出的基本检查规则。

### 4.7 全员协同：工程清理与文档更新

目标：保证项目结构清晰，方便答辩演示和后续开发。

需要完成：

- 新增 `.gitignore`
- 清理 `__pycache__/`
- 清理 `.pytest_cache/`
- 更新 `README.md`
- 更新 `backend/README.md`
- 更新 `docs/api_contract.md`
- 新增 `docs/system_roadmap.md`
- 整理 `docs` 文件夹中过期的 Week 1 文档

建议 `.gitignore` 内容：

```text
.env
__pycache__/
.pytest_cache/
backend/storage/
backend/generated/
*.pyc
```

验收标准：

- 项目目录没有明显缓存文件。
- README 可以指导新成员从零启动项目。
- API 文档与实际接口一致。

分工方式：

- 各模块负责人负责补充自己模块的接口说明、运行方式和测试方式。
- 张圣康负责最后统一 README、API 文档和演示说明。

## 5. 协作接口与集成约定

为避免最后一周整合时接口对不上，各模块需要尽量围绕统一数据结构开发。

统一输入输出核心：

- 文本推理主输入：`UserMessage`
- 文本推理主输出：`CaseState`
- 多轮追问更新对象：`CaseState`
- 知识库输出字段：`knowledge_snippets: list[str]`
- 文档生成输入：`CaseState`
- 多模态输入文本字段：`asr_text`
- 数字人输出字段：`avatar_response`、`avatar_performance`

最低联调要求：

- 陈誉的多轮接口必须能被前端直接调用。
- 何达煜的 RAG 输出必须保持 `knowledge_snippets` 格式兼容。
- 陆宣辰的文档生成接口必须能接收 `CaseState`。
- 张圣康的前端必须能展示 `CaseState`、多模态情绪结果和文档生成状态。
- 瞿逸凡的评测脚本需要能读取 fixtures，并输出模块级评测结果。

## 6. 最后一周整合目标

最后一周不再大规模新增功能，重点进行系统级整合和演示稳定性优化。

整合目标：

- 文本输入可以完整跑通警务 pipeline。
- 视频/语音转写文本可以进入同一 pipeline。
- 多模态情绪结果可以影响数字人话术。
- 多轮追问可以逐步补全案件字段。
- 警方侧可以看到结构化案件状态。
- 系统可以生成 Word/PDF 预受理信息单。
- 演示流程稳定，不依赖临时手动拼接。

最终演示路径：

```text
用户描述事件
→ 数字人安抚并追问
→ 系统抽取案件字段
→ 系统判断风险等级
→ 系统提示缺失信息
→ 系统生成警方摘要
→ 系统生成预受理信息单
→ 警方侧查看并接手处理
```

## 7. 阶段性成果清单

下阶段结束时，建议至少交付以下内容：

- `docs/evaluation_plan.md`
- `backend/scripts/evaluate_pipeline.py`
- `backend/app/core/session.py`
- `backend/app/modules/slot_merger.py`
- `backend/app/rag/`
- `backend/scripts/build_kb_index.py`
- `backend/app/modules/document_generator.py`
- `backend/app/templates/pre_acceptance_template.docx`
- `backend/app/modules/emotion_fusion.py`
- `frontend/` 可运行前端项目
- 更新后的 `README.md`
- 更新后的 `docs/api_contract.md`

## 8. 风险与优先级

最高优先级：

- 高风险事件不能漏判。
- 多轮追问不能重复、跑偏。
- 警方侧输出必须清晰、稳定。

中优先级：

- RAG 检索质量。
- 前端视觉完善。
- Word/PDF 格式美化。

低优先级：

- 复杂实时视频流。
- 高精度数字人动作控制。
- 完全自动生成正式笔录。

当前阶段应优先保证功能闭环，再优化视觉和细节。
