from app.core.state import CaseState, UserMessage
from app.modules.completeness import check_missing_fields, score_completeness
from app.modules.dialogue_policy import decide_next_action, generate_next_question
from app.modules.emotion_detector import detect_emotion
from app.modules.knowledge_retriever import retrieve_knowledge
from app.modules.risk_triage import triage_risk
from app.modules.scenario_classifier import classify_scenario
from app.modules.schema_extractor import extract_slots
from app.modules.address_extractor import extract_addresses
from app.modules.geocoder import geocode_addresses
from app.modules.summary_generator import generate_police_summary_payload


def _as_string_list(value: object) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value if item]
    if isinstance(value, str) and value.strip():
        return [value.strip()]
    return []


def run_pipeline(message: UserMessage) -> CaseState:
    state = CaseState(case_id=message.case_id or "demo-case", user_text=message.text)
    state.scenario = classify_scenario(message.text)
    state.emotion = detect_emotion(message.text)
    state.slots = extract_slots(message.text, state.scenario)
    state.missing_fields = check_missing_fields(state.scenario, state.slots)
    state.completeness_score = score_completeness(state.scenario, state.slots)
    state.risk_level = triage_risk(state)
    state.knowledge_snippets = retrieve_knowledge(state.scenario, message.text)
    state.next_action = decide_next_action(state)
    state.next_question = generate_next_question(state)
    summary_result = generate_police_summary_payload(state)
    state.police_summary = summary_result.get("summary") or "暂无摘要"
    state.key_facts = _as_string_list(summary_result.get("key_facts"))
    state.suggested_next_steps = _as_string_list(summary_result.get("suggested_next_steps"))
    if not state.suggested_next_steps:
        state.suggested_next_steps = state.knowledge_snippets
    state.extracted_addresses = extract_addresses(message.text, state.slots)
    state.map_locations = geocode_addresses(state.extracted_addresses)
    return state
