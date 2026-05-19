from app.core.state import CaseState, RiskLevel


def triage_risk(state: CaseState) -> RiskLevel:
    """Use conservative rules before model-based judgement."""
    text = state.user_text.lower()
    high_risk_words = ["in danger", "right now", "threat", "suicide", "hurt me"]
    medium_risk_words = ["still contacting", "keep paying", "harass", "scam"]

    if state.scenario == "personal_safety_threat":
        return "high"
    if any(word in text for word in high_risk_words):
        return "high"
    if any(word in text for word in medium_risk_words):
        return "medium"
    if state.completeness_score < 0.5 and state.scenario != "unknown":
        return "medium"
    return "low"

