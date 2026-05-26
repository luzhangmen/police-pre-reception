from app.core.pipeline import run_pipeline
from app.core.state import CaseState, UserMessage
from app.modules.completeness import check_missing_fields, get_required_fields, score_completeness
from app.modules.emotion_detector import detect_emotion
from app.modules.knowledge_retriever import retrieve_knowledge
from app.modules.risk_triage import triage_risk
from app.modules import dialogue_policy, schema_extractor, summary_generator


def test_pipeline_returns_state(monkeypatch):
    monkeypatch.setattr(
        schema_extractor,
        "call_llm_json",
        lambda **_: {
            "reporter_name": "Alex",
            "reporter_contact": "13800000000",
            "incident_time": "yesterday afternoon",
            "incident_location": "online ticket platform",
            "fraud_method": "ticket scam",
            "loss_amount": 500,
            "transfer_time": "yesterday afternoon",
            "transfer_channel": "wechat",
            "recipient_account": "wxid-demo",
            "recipient_name": "unknown seller",
            "suspect_contact_info": "wechat seller account",
            "evidence": "chat history",
        },
    )
    monkeypatch.setattr(
        dialogue_policy,
        "call_llm_json",
        lambda **_: {"next_question": "Do you still have the chat history?"},
    )
    monkeypatch.setattr(
        summary_generator,
        "call_llm_json",
        lambda **_: {
            "summary": "User lost 500 yuan in a ticket scam.",
            "key_facts": ["loss_amount: 500"],
            "suggested_next_steps": ["save chat history"],
        },
    )

    state = run_pipeline(UserMessage(text="I was scammed when buying a ticket."))

    assert state.scenario == "telecom_fraud"
    assert state.missing_fields == []
    assert state.completeness_score == 1.0
    assert state.next_action in {"ask_followup", "give_guidance", "handoff_human"}
    assert state.next_question == "Do you still have the chat history?"
    assert state.police_summary == "User lost 500 yuan in a ticket scam."
    assert state.key_facts == ["loss_amount: 500"]
    assert state.suggested_next_steps == ["save chat history"]


def test_completeness_accepts_false_and_zero_values():
    slots = {
        "reporter_name": "Alex",
        "reporter_contact": "13800000000",
        "lost_item": "campus card",
        "lost_time": "today noon",
        "lost_location": "library",
        "item_features": "blue card holder",
        "item_value": 0,
        "ownership_proof": "student account record",
        "suspected_theft": False,
        "account_or_id_risk": False,
    }

    assert check_missing_fields("property_loss", slots) == []
    assert score_completeness("property_loss", slots) == 1.0


def test_completeness_loads_required_fields_from_schema():
    required = get_required_fields("telecom_fraud")

    assert "reporter_name" in required
    assert "recipient_account" in required
    assert "evidence" in required


def test_emotion_detector_supports_chinese_keywords():
    assert detect_emotion("我现在很害怕，有人一直跟踪我") == "fearful"
    assert detect_emotion("太过分了，我很生气") == "angry"
    assert detect_emotion("我很着急，不知道怎么办") == "anxious"


def test_high_risk_fraud_rule_detects_active_transfer():
    state = CaseState(
        user_text="我还在按他说继续转账，已经转了800块",
        scenario="telecom_fraud",
        slots={"still_transferring": True, "loss_amount": 800},
    )

    assert triage_risk(state) == "high"


def test_dialogue_policy_uses_field_fallback_when_llm_fails(monkeypatch):
    monkeypatch.setattr(dialogue_policy, "call_llm_json", lambda **_: {})
    state = CaseState(
        user_text="我在闲鱼买票被骗了，微信转了480",
        scenario="telecom_fraud",
        risk_level="medium",
        missing_fields=["evidence", "recipient_account"],
    )
    state.next_action = dialogue_policy.decide_next_action(state)

    assert state.next_action == "ask_followup"
    assert "聊天记录" in dialogue_policy.generate_next_question(state)


def test_knowledge_retriever_returns_relevant_snippets():
    snippets = retrieve_knowledge("property_loss", "手机和身份证丢了")

    assert snippets
    assert any("挂失" in snippet for snippet in snippets)
    assert all("case_schemas.yaml" not in snippet for snippet in snippets)
    assert all(not snippet.startswith((">", "|")) for snippet in snippets)
