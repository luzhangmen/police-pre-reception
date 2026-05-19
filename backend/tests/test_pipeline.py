from app.core.pipeline import run_pipeline
from app.core.state import UserMessage


def test_pipeline_returns_state():
    state = run_pipeline(UserMessage(text="I was scammed when buying a ticket."))

    assert state.scenario == "telecom_fraud"
    assert state.next_action in {"ask_followup", "give_guidance", "handoff_human"}

