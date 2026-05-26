# 宿舍冲突（dorm_conflict）

> 室友/宿舍成员之间的矛盾、排挤、生活习惯冲突；含威胁但语境在宿舍时优先本场景。

## 1. 场景定义

冲突双方为**宿舍同住关系**，核心是解决宿舍矛盾、调解、换宿等，而非校外跟踪（见 `personal_safety_threat`）。

**边界**

| 情况 | 主场景 | 可接受备选 |
|------|--------|------------|
| 室友说“要打你” | `dorm_conflict` | `personal_safety_threat` |
| 室友说“要杀死你” | 两者皆可 | 死亡威胁更强时偏 `personal_safety_threat` |
| 校外前男友楼下堵人 | `personal_safety_threat` | — |

## 2. 字段说明

| 字段 | 必填 | 说明 |
|------|------|------|
| `parties` | 是 | 冲突双方 |
| `conflict_reason` | 是 | 起因 |
| `time_location` | 是 | 时间地点 |
| `expected_resolution` | 是 | 用户期望处理方式 |
| `frequency` | 否 | 发生频率 |
| `physical_conflict` | 否 | 肢体冲突，**高风险** |
| `threat` | 否 | 口头威胁，**高风险** |
| `emotional_intensity` | 否 | 情绪强度 |

## 3. 高风险判定

- `physical_conflict == true`
- `threat == true` 且当事人明显恐惧、仍在宿舍

## 4. 处置要点

1. **安全**：是否仍在冲突现场、对方是否在场。
2. **调解路径**：沟通、宿管、辅导员、换宿舍。
3. **受伤**：肢体冲突 → 转人工/医务与保卫。
4. **冷暴力/排挤**：记录持续时间，建议辅导员介入。

## 5. 常见起因

噪音（游戏外放）、卫生分工、空调温度、私人物品、喝酒闹事、小团体排挤。

## 6. 追问优先级

1. 威胁或肢体冲突（**最高**）
2. 起因、时间地点
3. 期望处理方式

## 7. 子类型速查

| 子类型 | 案例 ID |
|--------|---------|
| 噪音生活习惯 | conflict-001、conflict-008 |
| 长期矛盾换宿 | conflict-002 |
| 肢体冲突 | conflict-003 |
| 极短输入 | conflict-004 |
| 口头威胁 | conflict-005 |
| 排挤冷暴力 | conflict-006 |
| 私人物品侵权 | conflict-007 |
| 群内辱骂 | conflict-011 |
| 调解无效 | conflict-012 |
| 抽烟/访客 | conflict-009、conflict-010 |

## 8. 与 threat 对照

| 表述 | 建议 |
|------|------|
| 「要打你」 | dorm_conflict（conflict-005） |
| 「要杀死你」 | threat-007 或 conflict-005 |
| 校外堵人 | personal_safety_threat |

## 9. 多轮参考

`dlg-conflict-001`、`dlg-conflict-002`、`dlg-misclass-002`

## 10. 推荐案例 ID

`conflict-001`–`conflict-012`；★ `conflict-003` `conflict-008`
