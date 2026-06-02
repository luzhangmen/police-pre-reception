from app.core.state import CaseState
from app.modules.narrative_polish import clean_colloquial_text, synthesize_incident_narrative


def test_clean_colloquial_removes_fillers():
    raw = "那个嗯……警官你好，我就是，然后手机丢了，反正很慌"
    cleaned = clean_colloquial_text(raw)
    assert "嗯" not in cleaned
    assert "那个" not in cleaned
    assert "警官你好" in cleaned
    assert "手机丢了" in cleaned


def test_collect_high_risk_flags():
    from app.modules.narrative_polish import collect_high_risk_flag_labels

    state = CaseState(
        case_id="t2",
        user_text="还在转钱",
        scenario="telecom_fraud",
        slots={"still_transferring": True},
    )
    flags = collect_high_risk_flag_labels(state)
    assert any("转账" in f for f in flags)


def test_synthesize_property_loss_from_slots():
    state = CaseState(
        case_id="t1",
        user_text="嗯那个手机丢了",
        scenario="property_loss",
        slots={
            "lost_time": "昨天下午",
            "lost_location": "图书馆三楼",
            "lost_item": "手机",
            "item_features": "黑色 iPhone",
            "suspected_theft": True,
            "account_or_id_risk": True,
        },
    )
    narrative = synthesize_incident_narrative(state)
    assert "报案人反映" in narrative
    assert "图书馆三楼" in narrative
    assert "疑似被盗" in narrative or "被盗" in narrative
