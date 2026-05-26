from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

from app.core.state import Scenario


SCHEMA_PATH = Path(__file__).resolve().parents[1] / "schemas" / "case_schemas.yaml"

FALLBACK_SCHEMA: dict[str, dict[str, list[str]]] = {
    "telecom_fraud": {
        "required": [
            "reporter_name",
            "reporter_contact",
            "incident_time",
            "incident_location",
            "fraud_method",
            "loss_amount",
            "transfer_time",
            "transfer_channel",
            "recipient_account",
            "recipient_name",
            "suspect_contact_info",
            "evidence",
        ],
        "optional": [
            "platform",
            "payment_order_or_transaction_id",
            "still_contacting",
            "still_transferring",
            "bank_or_payment_platform",
            "fraud_link_or_qr_code",
        ],
        "high_risk": ["still_transferring", "ongoing_contact"],
    },
    "property_loss": {
        "required": [
            "reporter_name",
            "reporter_contact",
            "lost_item",
            "lost_time",
            "lost_location",
            "item_features",
            "item_value",
            "ownership_proof",
            "suspected_theft",
            "account_or_id_risk",
        ],
        "optional": [
            "possible_clues",
            "serial_number_or_unique_mark",
            "last_seen_person",
            "evidence",
        ],
        "high_risk": ["account_or_id_risk"],
    },
    "dorm_conflict": {
        "required": [
            "reporter_name",
            "reporter_contact",
            "parties",
            "dorm_location",
            "incident_time",
            "conflict_reason",
            "incident_description",
            "current_status",
            "safety_risk",
            "injuries_or_property_damage",
            "witnesses_or_evidence",
            "expected_resolution",
        ],
        "optional": [
            "frequency",
            "previous_communication",
            "emotional_intensity",
            "physical_conflict",
        ],
        "high_risk": ["physical_conflict", "threat"],
    },
    "personal_safety_threat": {
        "required": [
            "reporter_name",
            "reporter_contact",
            "threat_type",
            "current_location",
            "incident_time",
            "incident_location",
            "suspect_info",
            "relationship_to_suspect",
            "threat_content",
            "current_danger",
            "injury_status",
            "evidence",
            "witnesses",
            "immediate_need",
        ],
        "optional": [
            "prior_incidents",
            "suspect_direction_or_destination",
            "protective_order_or_school_report",
        ],
        "high_risk": ["ongoing_threat", "current_danger"],
    },
    "unknown": {"required": [], "optional": [], "high_risk": []},
}

EMPTY_TOKENS = {
    "",
    "unknown",
    "none",
    "null",
    "n/a",
    "未知",
    "不详",
    "不清楚",
    "不知道",
    "未说明",
    "待确认",
}


@lru_cache(maxsize=1)
def load_case_schema() -> dict[str, dict[str, list[str]]]:
    if not SCHEMA_PATH.exists():
        return FALLBACK_SCHEMA

    with SCHEMA_PATH.open("r", encoding="utf-8") as schema_file:
        raw_schema = yaml.safe_load(schema_file) or {}

    schema: dict[str, dict[str, list[str]]] = {"unknown": FALLBACK_SCHEMA["unknown"]}
    for scenario, config in raw_schema.items():
        scenario_config = config or {}
        schema[str(scenario)] = {
            "required": list(scenario_config.get("required") or []),
            "optional": list(scenario_config.get("optional") or []),
            "high_risk": list(scenario_config.get("high_risk") or []),
        }
    return schema


def is_filled(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return value.strip().lower() not in EMPTY_TOKENS
    if isinstance(value, dict):
        return any(is_filled(item) for item in value.values())
    if isinstance(value, (list, tuple, set)):
        return any(is_filled(item) for item in value)
    return True


def get_required_fields(scenario: Scenario) -> list[str]:
    return list(load_case_schema().get(scenario, {}).get("required", []))


def get_optional_fields(scenario: Scenario) -> list[str]:
    return list(load_case_schema().get(scenario, {}).get("optional", []))


def get_high_risk_fields(scenario: Scenario) -> list[str]:
    return list(load_case_schema().get(scenario, {}).get("high_risk", []))


def check_missing_fields(
    scenario: Scenario,
    slots: dict[str, Any],
    *,
    include_optional: bool = False,
) -> list[str]:
    fields = get_required_fields(scenario)
    if include_optional:
        fields = [*fields, *get_optional_fields(scenario)]

    return [field for field in fields if not is_filled(slots.get(field))]


def score_completeness(scenario: Scenario, slots: dict[str, Any]) -> float:
    required = get_required_fields(scenario)
    if not required:
        return 0.0

    filled_count = sum(1 for field in required if is_filled(slots.get(field)))
    return round(filled_count / len(required), 2)


REQUIRED_FIELDS: dict[str, list[str]] = {
    scenario: config["required"] for scenario, config in load_case_schema().items()
}
