from app.core.state import CaseState, NextAction


def decide_next_action(state: CaseState) -> NextAction:
    if state.risk_level == "high":
        return "handoff_human"
    if state.missing_fields:
        return "ask_followup"
    return "give_guidance"


def generate_next_question(state: CaseState) -> str:
    if state.next_action == "handoff_human":
        return "Please confirm whether you are currently safe and where you are now."
    if state.missing_fields:
        return f"Please add this information: {', '.join(state.missing_fields)}."
    return "The key information is complete. I will prepare a brief summary for the officer."

