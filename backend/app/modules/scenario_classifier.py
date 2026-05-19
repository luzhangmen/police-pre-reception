from app.core.state import Scenario


def classify_scenario(text: str) -> Scenario:
    """Return one of the four project scenarios."""
    lowered = text.lower()
    if any(word in lowered for word in ["fraud", "scam", "transfer", "ticket"]):
        return "telecom_fraud"
    if any(word in lowered for word in ["lost", "missing", "wallet", "phone"]):
        return "property_loss"
    if any(word in lowered for word in ["roommate", "dorm", "conflict"]):
        return "dorm_conflict"
    if any(word in lowered for word in ["threat", "danger", "follow", "harass"]):
        return "personal_safety_threat"
    return "unknown"

