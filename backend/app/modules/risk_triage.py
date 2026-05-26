from __future__ import annotations

import re
from typing import Any

from app.core.state import CaseState, RiskLevel
from app.modules.completeness import get_high_risk_fields, is_filled


HIGH_URGENCY_KEYWORDS = [
    "正在被",
    "正在发生",
    "救命",
    "现在不安全",
    "现在有危险",
    "不安全",
    "有危险",
    "在门口",
    "跟踪",
    "堵我",
    "恐吓",
    "打我",
    "要打我",
    "动手",
    "拿刀",
    "伤害我",
    "自杀",
    "in danger",
    "right now",
    "threatening",
    "hurt me",
    "suicide",
]

FRAUD_HIGH_KEYWORDS = [
    "还在转",
    "继续转账",
    "继续打钱",
    "催我继续",
    "催我补单",
    "补单",
    "正在转账",
    "让我再转",
    "借钱继续",
    "继续投",
    "诱导付款",
    "keep paying",
    "still transferring",
]

FRAUD_MEDIUM_KEYWORDS = ["被骗", "诈骗", "拉黑", "转账", "scam", "fraud", "transfer"]
PROPERTY_MEDIUM_KEYWORDS = ["被偷", "疑似被盗", "手机", "钱包", "身份证", "银行卡", "校园卡"]
DORM_MEDIUM_KEYWORDS = ["一直", "多次", "反复", "吵", "冲突", "辱骂", "骚扰"]
DORM_HIGH_KEYWORDS = [
    "打架",
    "打起来",
    "动手",
    "推搡",
    "推了我",
    "擦破",
    "威胁",
    "恐吓",
    "要打",
    "揍我",
    "physical",
]

PROPERTY_HIGH_KEYWORDS = ["身份证", "银行卡", "校园卡", "支付宝", "微信", "转账"]


def _contains_any(text: str, keywords: list[str]) -> bool:
    lowered = text.lower()
    return any(keyword.lower() in lowered for keyword in keywords)


def _slot_as_bool(value: Any) -> bool:
    if not is_filled(value):
        return False
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return value > 0

    normalized = str(value).strip().lower()
    negative_words = ["false", "no", "not", "否", "没有", "未", "停止", "不是"]
    positive_words = ["true", "yes", "是", "有", "正在", "还在", "继续", "危险", "高"]
    if any(word in normalized for word in negative_words):
        return False
    return any(word in normalized for word in positive_words)


def _has_truthy_slot(slots: dict[str, Any], field_names: list[str]) -> bool:
    return any(_slot_as_bool(slots.get(field_name)) for field_name in field_names)


def _extract_amount(slots: dict[str, Any], text: str) -> float:
    value = slots.get("loss_amount")
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        matched = re.search(r"\d+(?:\.\d+)?", value.replace(",", ""))
        if matched:
            return float(matched.group())

    normalized = text.lower().replace(",", "")
    amount_patterns = [
        r"(\d+(?:\.\d+)?)\s*万",
        r"(\d+(?:\.\d+)?)\s*(?:元|块|rmb|yuan)",
        r"(?:转了|被骗|损失|loss|paid)\s*(\d+(?:\.\d+)?)",
    ]
    for pattern in amount_patterns:
        matched = re.search(pattern, normalized)
        if matched:
            amount = float(matched.group(1))
            if "万" in pattern:
                amount *= 10000
            return amount
    return 0.0


def _has_schema_high_risk_slot(state: CaseState) -> bool:
    high_risk_fields = get_high_risk_fields(state.scenario)
    return _has_truthy_slot(state.slots, high_risk_fields)


def triage_risk(state: CaseState) -> RiskLevel:
    """Use conservative local rules before model-based judgement."""
    text = state.user_text

    if _has_schema_high_risk_slot(state) or _contains_any(text, HIGH_URGENCY_KEYWORDS):
        return "high"

    if state.scenario == "personal_safety_threat":
        return "high"

    if state.scenario == "telecom_fraud":
        amount = _extract_amount(state.slots, text)
        if _contains_any(text, FRAUD_HIGH_KEYWORDS):
            return "high"
        if amount >= 3000:
            return "high"
        if amount > 0 or _contains_any(text, FRAUD_MEDIUM_KEYWORDS):
            return "medium"
        return "low"

    if state.scenario == "property_loss":
        if _slot_as_bool(state.slots.get("account_or_id_risk")) or _contains_any(
            text, PROPERTY_HIGH_KEYWORDS
        ):
            return "high"
        if _slot_as_bool(state.slots.get("suspected_theft")) or _contains_any(text, PROPERTY_MEDIUM_KEYWORDS):
            return "medium"
        return "low"

    if state.scenario == "dorm_conflict":
        if _slot_as_bool(state.slots.get("physical_conflict")) or _contains_any(text, DORM_HIGH_KEYWORDS):
            return "high"
        if _contains_any(text, DORM_MEDIUM_KEYWORDS):
            return "medium"
        return "low"

    if state.scenario != "unknown" and state.completeness_score < 0.25:
        return "medium"
    return "low"
