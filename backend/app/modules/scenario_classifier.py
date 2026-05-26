from app.core.state import Scenario

FRAUD_HINTS = (
    "fraud",
    "scam",
    "transfer",
    "ticket",
    "诈骗",
    "被骗",
    "骗局",
    "刷单",
    "垫付",
    "拉黑",
    "闲鱼",
    "咸鱼",
    "保证金",
    "安全账户",
    "校园贷",
    "杀猪",
    "补单",
    "米没了",
    "客服理赔",
    "假客服",
    "投资平台",
    "验证码",
    "钓鱼",
    "客服",
    "qq",
    "游戏装备",
    "游戏皮肤",
    "游戏点卡",
    "投资",
    "虚拟货币",
    "票务",
    "欠费",
    "链接",
    "面交",
    "杀猪",
    "网恋",
)

LOSS_HINTS = (
    "lost",
    "missing",
    "wallet",
    "phone",
    "丢了",
    "遗失",
    "不见",
    "被偷",
    "顺走",
    "落了",
    "落图书馆",
    "丢失",
    "掉了",
    "丢包",
    "钱包",
    "不见了",
    "u盘",
    "钥匙",
    "眼镜",
    "快递",
    "被偷",
    "手机",
)

DORM_HINTS = (
    "roommate",
    "dorm",
    "conflict",
    "室友",
    "舍友",
    "宿舍",
    "换宿舍",
    "换宿",
    "辅导员",
    "宿管",
    "打游戏",
    "举报",
    "抽烟",
    "空调",
    "卫生",
    "插排",
    "排挤",
    "仓鼠",
    "宠物",
)

THREAT_HINTS = (
    "threat",
    "danger",
    "follow",
    "harass",
    "威胁",
    "跟踪",
    "堵我",
    "堵着",
    "不让我走",
    "杀了我",
    "杀死",
    "刀的照片",
    "恐吓",
    "吓唬",
    "尾随",
    "死亡威胁",
    "表白墙",
    "算账",
    "吓人",
    "跟着",
    "喊叫",
    "滋扰",
    "围墙",
    "害怕",
    "不想活",
    "一了百了",
    "不敢一个人",
    "喊我名字",
    "打我",
    "说要打",
)

STRONG_THREAT_HINTS = ("杀", "堵", "跟踪", "刀", "杀了我", "杀死", "不让我走", "堵着")


def _contains_any(text: str, hints: tuple[str, ...]) -> bool:
    return any(hint in text for hint in hints)


NON_CASE_HINTS = (
    "选课",
    "热水器",
    "坏了",
    "维修",
    "红烧肉",
    "作文",
    "asdfgh",
    "派出所周末",
    "欠我两百",
    "在吗",
    "help me write",
)


def classify_scenario(text: str) -> Scenario:
    """Return one of the four project scenarios (ZH + EN keyword rules)."""
    lowered = text.lower()
    original = text

    if _contains_any(original, NON_CASE_HINTS) or _contains_any(lowered, NON_CASE_HINTS):
        return "unknown"

    if _contains_any(lowered, FRAUD_HINTS) or _contains_any(original, FRAUD_HINTS):
        return "telecom_fraud"

    has_roommate = "室友" in original or "舍友" in original or "roommate" in lowered
    if has_roommate and not _contains_any(original, STRONG_THREAT_HINTS):
        if _contains_any(original, DORM_HINTS) or _contains_any(
            original, ("吵", "揍", "打我", "针对", "合不来", "摔门", "偷用")
        ):
            return "dorm_conflict"

    if _contains_any(lowered, THREAT_HINTS) or _contains_any(original, THREAT_HINTS):
        return "personal_safety_threat"

    if _contains_any(lowered, LOSS_HINTS) or _contains_any(original, LOSS_HINTS):
        return "property_loss"

    if _contains_any(lowered, DORM_HINTS) or _contains_any(original, DORM_HINTS):
        if "宿舍" in original and _contains_any(
            original, ("丢了", "遗失", "不见", "被偷", "快递", "钱包", "手机丢", "手机不见")
        ):
            return "property_loss"
        if "宿舍" in original and _contains_any(
            original, ("害怕", "不想活", "跟踪", "尾随", "恐吓", "杀了我", "堵我")
        ):
            return "personal_safety_threat"
        return "dorm_conflict"

    return "unknown"
