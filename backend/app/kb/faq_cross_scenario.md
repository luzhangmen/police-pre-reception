# 跨场景常见问题（FAQ）

## Q1：用户只说「我被骗了」怎么办？

- 先判 `telecom_fraud`，追问：金额、渠道、是否仍在转账。
- 案例：`fraud-003`、`dlg-full-001`。

## Q2：「东西丢了」和「转账被骗」怎么分？

- 有转账、对方失联 → `telecom_fraud`。
- 物理丢失、无支付给对方 → `property_loss`。
- 案例：`dlg-misclass-001`、`fraud-007`、`loss-011`。

## Q3：室友威胁 vs 校外威胁？

- 宿舍语境、室友关系 → 优先 `dorm_conflict`（conflict-005）。
- 死亡威胁、校外人员、跟踪 → `personal_safety_threat`（threat-007、threat-010）。
- 可接受双分类见 `docs/scenario_disambiguation.md`。

## Q4：什么时候必须转人工？

- `still_transferring`、证件未挂失、`physical_conflict`、`ongoing_threat`/`current_danger`。
- 案例：fraud-002、loss-003、threat-001、threat-009。

## Q5：完整度已经 1.0 为什么还要追问？

- 第一周：必填齐 → `give_guidance` 或补充**可选**线索（监控、账号）。
- 案例：loss-001、loss-007。

## Q6：小额损失要不要重视？

- 要记录；风险可 low/medium，但仍需证据与渠道。
- 案例：`fraud-012`（50 元话费）。

## Q7：多轮对话如何合并 slots？

- 每轮 `expected_slots_delta` 合并进 state.slots，重算 missing 与 completeness。
- 参考：`demo_dialogues.json`。

## Q8：警方摘要应包含什么？

- 场景、关键事实、金额/物品、风险、已采取措施、待补充项。
- 模板见 `police_summary_templates.md`。
