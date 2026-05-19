from app.core.state import CaseState, UserMessage
from app.modules.completeness import check_missing_fields, score_completeness
from app.modules.dialogue_policy import decide_next_action, generate_next_question
from app.modules.emotion_detector import detect_emotion
from app.modules.risk_triage import triage_risk
from app.modules.scenario_classifier import classify_scenario
from app.modules.schema_extractor import extract_slots
from app.modules.summary_generator import generate_police_summary


def run_pipeline(message: UserMessage) -> CaseState:
    state = CaseState(case_id=message.case_id or "demo-case", user_text=message.text)
    state.scenario = classify_scenario(message.text)
    state.emotion = detect_emotion(message.text)
    state.slots = extract_slots(message.text, state.scenario)
    state.missing_fields = check_missing_fields(state.scenario, state.slots)
    state.completeness_score = score_completeness(state.scenario, state.slots)
    state.risk_level = triage_risk(state)
    state.next_action = decide_next_action(state)
    state.next_question = generate_next_question(state)
    state.police_summary = generate_police_summary(state)
    return state

