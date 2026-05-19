def detect_emotion(text: str) -> str:
    """Detect a rough emotion label from user text."""
    lowered = text.lower()
    if any(word in lowered for word in ["afraid", "scared", "danger"]):
        return "fearful"
    if any(word in lowered for word in ["angry", "mad"]):
        return "angry"
    if any(word in lowered for word in ["worried", "anxious", "panic"]):
        return "anxious"
    return "neutral"

