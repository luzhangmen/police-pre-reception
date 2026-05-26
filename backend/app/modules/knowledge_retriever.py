from __future__ import annotations

from pathlib import Path

from app.core.state import Scenario


KB_DIR = Path(__file__).resolve().parents[1] / "kb"

SCENARIO_KB_FILES: dict[Scenario, str] = {
    "telecom_fraud": "fraud.md",
    "property_loss": "property_loss.md",
    "dorm_conflict": "dorm_conflict.md",
    "personal_safety_threat": "safety_threat.md",
    "unknown": "",
}

DEFAULT_SNIPPETS: dict[Scenario, list[str]] = {
    "telecom_fraud": [
        "先停止继续转账或付款，保留聊天记录、转账凭证、平台订单、对方账号和拉黑记录。",
        "如果对方仍在诱导付款或远程操控手机，应优先止损并转人工处理。",
        "记录被骗平台、被骗方式、损失金额、转账渠道和对方收款信息。",
    ],
    "property_loss": [
        "记录丢失物品、最后确认时间、发现丢失时间、地点和物品明显特征。",
        "涉及身份证、银行卡、校园卡或手机账号时，建议尽快挂失或修改关键密码。",
        "如疑似被盗，补充现场监控、目击者、定位记录或可疑人员线索。",
    ],
    "dorm_conflict": [
        "先避免继续正面冲突，记录冲突时间地点、参与人员、起因和已沟通情况。",
        "出现威胁、推搡、打架或持续骚扰时，应提高风险并联系人工介入。",
        "普通宿舍矛盾可优先建议宿管、辅导员或学院调解。",
    ],
    "personal_safety_threat": [
        "先确认当事人当前位置和是否安全，正在发生现实危险时应立即转人工或报警。",
        "保留威胁短信、聊天记录、通话录音、监控线索和对方身份信息。",
        "涉及跟踪、堵截、伤害威胁或自伤风险时，按高风险处理。",
    ],
    "unknown": [
        "先确认用户描述属于诈骗、财物遗失、宿舍冲突还是人身安全威胁。",
    ],
}

KEYWORDS: dict[Scenario, list[str]] = {
    "telecom_fraud": ["转账", "付款", "被骗", "诈骗", "账号", "平台", "证据", "scam", "fraud"],
    "property_loss": ["丢", "遗失", "被盗", "物品", "证件", "身份证", "银行卡", "手机", "挂失", "lost", "missing"],
    "dorm_conflict": ["宿舍", "室友", "冲突", "调解", "威胁", "打架", "dorm", "roommate"],
    "personal_safety_threat": ["威胁", "跟踪", "危险", "安全", "报警", "证据", "threat", "danger"],
    "unknown": [],
}

SKIP_PREFIXES = (">", "|", "```")
SKIP_CONTAINS = (
    "case_schemas.yaml",
    "第一周测试字段口径",
    "字段 |",
    "必填 |",
    "示例 |",
    "用户报告",
    "场景定义",
    "不属于本场景",
)
GUIDANCE_MARKERS = ("建议", "优先", "记录", "保留", "确认", "停止", "冻结", "挂失", "联系", "补充", "转人工", "报警")


def _read_kb_snippets(scenario: Scenario) -> list[str]:
    file_name = SCENARIO_KB_FILES.get(scenario)
    if not file_name:
        return []

    kb_path = KB_DIR / file_name
    if not kb_path.exists():
        return []

    snippets: list[str] = []
    for raw_line in kb_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip().lstrip("-").strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith(SKIP_PREFIXES) or any(token in line for token in SKIP_CONTAINS):
            continue
        if any(marker in line for marker in GUIDANCE_MARKERS):
            snippets.append(line)
    return snippets


def _score_snippet(scenario: Scenario, query: str, snippet: str) -> int:
    query_lowered = query.lower()
    snippet_lowered = snippet.lower()
    score = 0
    for keyword in KEYWORDS.get(scenario, []):
        keyword_lowered = keyword.lower()
        if keyword_lowered in query_lowered and keyword_lowered in snippet_lowered:
            score += 3
        elif keyword_lowered in snippet_lowered:
            score += 1
    return score


def retrieve_knowledge(scenario: Scenario, query: str, limit: int = 3) -> list[str]:
    """Return small knowledge snippets related to the current scenario."""
    candidates = [*DEFAULT_SNIPPETS.get(scenario, []), *_read_kb_snippets(scenario)]
    if not candidates:
        return []

    ranked = sorted(
        candidates,
        key=lambda snippet: _score_snippet(scenario, query, snippet),
        reverse=True,
    )
    deduped = list(dict.fromkeys(ranked))
    return deduped[:limit]
