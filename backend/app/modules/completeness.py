from app.core.state import Scenario


REQUIRED_FIELDS: dict[Scenario, list[str]] = {
    "telecom_fraud": ["fraud_method", "loss_amount", "transfer_channel", "evidence"],
    "property_loss": ["lost_item", "lost_time", "lost_location", "item_features"],
    "dorm_conflict": ["parties", "conflict_reason", "time_location", "expected_resolution"],
    "personal_safety_threat": ["threat_type", "suspect_info", "current_location", "danger_level"],
    "unknown": [],
}


def check_missing_fields(scenario: Scenario, slots: dict) -> list[str]:
    required = REQUIRED_FIELDS.get(scenario, [])
    return [field for field in required if not slots.get(field)]


def score_completeness(scenario: Scenario, slots: dict) -> float:
    required = REQUIRED_FIELDS.get(scenario, [])
    if not required:
        return 0.0
    filled = len([field for field in required if slots.get(field)])
    return round(filled / len(required), 2)

