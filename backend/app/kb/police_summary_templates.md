# 警方侧摘要模板（第一周）

供 `summary_generator` 与人工评测对照。每条 3–6 句，客观陈述。

## 电信/网络诈骗

```text
【场景】电信/网络诈骗
【经过】{fraud_method}；通过{transfer_channel}损失约{loss_amount}元；平台/场景：{platform}。
【对方】{recipient_account}
【联系状态】仍在联系：{still_contacting}；仍在转账：{still_transferring}
【证据】{evidence}
【风险】{risk_level}
【建议】{next_action 对应处置}
```

**示例（fraud-001）**

```text
【场景】电信/网络诈骗
【经过】闲鱼购票诈骗；微信支付损失约480元。
【联系状态】对方已拉黑，无 ongoing 转账。
【证据】待补充聊天与转账截图。
【风险】中
【建议】保全证据后报案咨询。
```

## 财物遗失

```text
【场景】财物遗失
【物品】{lost_item}（{item_features}）
【时空】{lost_time}，{lost_location}
【性质】疑似盗窃：{suspected_theft}
【证件/账户风险】{account_or_id_risk}
【线索】{possible_clues}
【风险】{risk_level}
```

## 宿舍冲突

```text
【场景】宿舍冲突
【双方】{parties}
【起因】{conflict_reason}
【时间地点】{time_location}
【升级】肢体冲突：{physical_conflict}；威胁：{threat}
【诉求】{expected_resolution}
【既往】{previous_communication}；频率：{frequency}
```

## 人身安全威胁

```text
【场景】人身安全威胁
【类型】{threat_type}
【对方】{suspect_info}
【位置】{current_location}
【危险程度】{danger_level}
【持续/即时】ongoing={ongoing_threat}，current_danger={current_danger}
【证据】{evidence}
【建议】确保人身安全，联系保卫处/110
```

## 多轮合并示例

见 `demo_dialogues.json` 各条 `final_expected_police_summary_points`。
