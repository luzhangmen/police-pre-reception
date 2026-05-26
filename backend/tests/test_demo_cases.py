"""Validate demo case fixtures and rule-module ground truth alignment."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

REQUIRED_FIELDS: dict[str, list[str]] = {
    "telecom_fraud": ["fraud_method", "loss_amount", "transfer_channel", "evidence"],
    "property_loss": ["lost_item", "lost_time", "lost_location", "item_features"],
    "dorm_conflict": ["parties", "conflict_reason", "time_location", "expected_resolution"],
    "personal_safety_threat": [
        "threat_type",
        "suspect_info",
        "current_location",
        "danger_level",
    ],
}


def check_missing_fields(scenario: str, slots: dict) -> list[str]:
    required = REQUIRED_FIELDS.get(scenario, [])
    return [field for field in required if not slots.get(field)]


def score_completeness(scenario: str, slots: dict) -> float:
    required = REQUIRED_FIELDS.get(scenario, [])
    if not required:
        return 0.0
    filled = len([field for field in required if slots.get(field)])
    return round(filled / len(required), 2)

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"
CASES_PATH = FIXTURES_DIR / "demo_cases.json"
SCHEMA_PATH = FIXTURES_DIR / "demo_cases.schema.json"

VALID_SCENARIOS = {
    "telecom_fraud",
    "property_loss",
    "dorm_conflict",
    "personal_safety_threat",
}
VALID_RISKS = {"low", "medium", "high"}
VALID_ACTIONS = {"ask_followup", "give_guidance", "handoff_human"}
REQUIRED_CASE_KEYS = {
    "id",
    "scenario",
    "input",
    "expected_risk",
    "expected_slots",
    "expected_missing_fields",
    "expected_next_question",
}


def load_demo_cases() -> list[dict]:
    with CASES_PATH.open(encoding="utf-8") as handle:
        return json.load(handle)


@pytest.fixture(scope="module")
def demo_cases() -> list[dict]:
    return load_demo_cases()


def test_fixture_file_exists():
    assert CASES_PATH.is_file()


def test_at_least_sixty_cases(demo_cases: list[dict]):
    assert len(demo_cases) >= 60


def test_each_scenario_has_at_least_fifteen_cases(demo_cases: list[dict]):
    counts: dict[str, int] = {scenario: 0 for scenario in VALID_SCENARIOS}
    for case in demo_cases:
        counts[case["scenario"]] += 1
    for scenario, count in counts.items():
        assert count >= 15, f"{scenario} only has {count} cases"


def test_unique_ids(demo_cases: list[dict]):
    ids = [case["id"] for case in demo_cases]
    assert len(ids) == len(set(ids))


@pytest.mark.parametrize("case", load_demo_cases(), ids=lambda c: c["id"])
def test_case_has_required_keys(case: dict):
    missing = REQUIRED_CASE_KEYS - case.keys()
    assert not missing, f"missing keys: {missing}"


@pytest.mark.parametrize("case", load_demo_cases(), ids=lambda c: c["id"])
def test_case_enums(case: dict):
    assert case["scenario"] in VALID_SCENARIOS
    assert case["expected_risk"] in VALID_RISKS
    if "expected_next_action" in case:
        assert case["expected_next_action"] in VALID_ACTIONS


@pytest.mark.parametrize("case", load_demo_cases(), ids=lambda c: c["id"])
def test_missing_fields_match_completeness_module(case: dict):
    scenario = case["scenario"]
    slots = case["expected_slots"]
    assert case["expected_missing_fields"] == check_missing_fields(scenario, slots)


@pytest.mark.parametrize("case", load_demo_cases(), ids=lambda c: c["id"])
def test_completeness_score_when_documented(case: dict):
    if "expected_completeness" not in case:
        pytest.skip("no expected_completeness")
    actual = score_completeness(case["scenario"], case["expected_slots"])
    assert actual == case["expected_completeness"]


@pytest.mark.parametrize("case", load_demo_cases(), ids=lambda c: c["id"])
def test_follow_up_question_keywords(case: dict):
    keywords = case.get("expected_next_question_keywords", [])
    if not keywords:
        pytest.skip("no keywords")
    question = case["expected_next_question"]
    for keyword in keywords:
        assert keyword in question, f"keyword {keyword!r} not in question"


def test_demo_star_cases_exist(demo_cases: list[dict]):
    stars = [case for case in demo_cases if "demo_star" in case.get("tags", [])]
    assert len(stars) >= 5


def test_high_risk_cases_exist(demo_cases: list[dict]):
    high = [case for case in demo_cases if case["expected_risk"] == "high"]
    assert len(high) >= 6


def test_boundary_cases_exist(demo_cases: list[dict]):
    boundary = [case for case in demo_cases if "boundary" in case.get("tags", [])]
    assert len(boundary) >= 8


def test_all_cases_have_metadata(demo_cases: list[dict]):
    for case in demo_cases:
        assert case.get("tags"), f"{case['id']} missing tags"
        assert case.get("difficulty"), f"{case['id']} missing difficulty"
        assert "expected_completeness" in case, f"{case['id']} missing expected_completeness"
        assert case.get("expected_next_action"), f"{case['id']} missing expected_next_action"
        assert case.get("evaluator_notes"), f"{case['id']} missing evaluator_notes"


def test_field_labels_zh_exists():
    labels_path = FIXTURES_DIR / "field_labels_zh.json"
    assert labels_path.is_file()
    labels = json.loads(labels_path.read_text(encoding="utf-8"))
    for scenario in VALID_SCENARIOS:
        assert scenario in labels["slots"]
