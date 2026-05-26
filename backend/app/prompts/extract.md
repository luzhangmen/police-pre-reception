# 字段抽取任务

根据用户原话和已确定的场景，从文本中抽取所有结构化字段。

## 规则

- 严格按照下方提供的 Schema 抽取字段。
- 如果用户在文本中明确提及了某个字段，填写实际值。
- 如果用户没有提及某个字段，值设为 `null`（不要省略键）。
- `loss_amount` 等数值字段尽量转为数字类型（如 480）。
- 不要编造信息，只抽原文中出现的内容。
- 如果同一段原文同时支持多个字段，应尽量拆分到各自字段，不要只合并到一个大字段里。

## 特别注意

### 财物遗失 / 疑似被盗

- `ownership_proof`：只放能证明物品属于用户的材料，如购买记录、发票、账号绑定、照片。
- `serial_number_or_unique_mark`：如果原文提到序列号、IMEI、设备编号、唯一编号、特殊刻印或唯一标记，应单独填写到这里；不要只放进 `ownership_proof`。
- `evidence`：如果原文提到定位截图、监控线索、照片、视频、聊天记录、报警记录、门禁/消费记录等证据，应填写到这里。
- `last_seen_trace`：如果原文提到“最后一次确认还在”的时间、地点、座位、路线或轨迹，应填写到这里。
- `surveillance_possible`：如果原文提到“现场有监控”“应该能调监控”等，填写 `true`。
- `suspected_theft`：只有用户明确说被偷、被拿走、有可疑人员、包被翻动等明显被盗迹象时才填 `true`；如果只是“不确定是否被拿走”，可填 `false` 或 `null`。

## 输出格式

必须且仅返回一个 JSON 对象，不要包含任何解释或 markdown 代码块标记。示例：

```json
{
  "fraud_method": "二手交易诈骗",
  "loss_amount": 480,
  "transfer_channel": "微信",
  "platform": "闲鱼",
  "recipient_account": null,
  "still_contacting": false,
  "evidence": null
}
```
