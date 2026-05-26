def detect_emotion(text: str) -> str:
    """Detect a rough emotion label from user text."""
    lowered = text.lower()
    fearful_keywords = [
        "害怕",
        "怕",
        "恐惧",
        "吓",
        "危险",
        "不敢",
        "救命",
        "跟踪",
        "威胁",
        "afraid",
        "scared",
        "danger",
        "fear",
    ]
    angry_keywords = [
        "生气",
        "气死",
        "愤怒",
        "火大",
        "受不了",
        "太过分",
        "投诉",
        "angry",
        "mad",
    ]
    anxious_keywords = [
        "着急",
        "急",
        "焦虑",
        "慌",
        "担心",
        "怎么办",
        "崩溃",
        "麻烦了",
        "worried",
        "anxious",
        "panic",
    ]

    if any(word in lowered for word in fearful_keywords):
        return "fearful"
    if any(word in lowered for word in angry_keywords):
        return "angry"
    if any(word in lowered for word in anxious_keywords):
        return "anxious"
    return "neutral"
