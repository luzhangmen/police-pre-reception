"""Validate fraud / theft / fight transcript fixtures."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

FIXTURES = Path(__file__).resolve().parent / "fixtures"
TRANSCRIPTS_PATH = FIXTURES / "demo_transcripts_three_scenarios.json"

REQUIRED_FIELDS = {
    "telecom_fraud": ["fraud_method", "loss_amount", "transfer_channel", "evidence"],
    "property_loss": ["lost_item", "lost_time", "lost_location", "item_features"],
    "dorm_conflict": ["parties", "conflict_reason", "time_location", "expected_resolution"],
}

CATEGORY_SCENARIO = {
    "fraud": "telecom_fraud",
    "theft": "property_loss",
    "fight": "dorm_conflict",
}


def load_payload() -> dict:
    return json.loads(TRANSCRIPTS_PATH.read_text(encoding="utf-8"))


def load_transcripts() -> list[dict]:
    return load_payload()["transcripts"]


def check_missing(scenario: str, slots: dict) -> list[str]:
    return [f for f in REQUIRED_FIELDS[scenario] if not slots.get(f)]


@pytest.fixture(scope="module")
def transcripts() -> list[dict]:
    return load_transcripts()


def test_transcripts_file_exists():
    assert TRANSCRIPTS_PATH.is_file()


def test_seventy_two_transcripts(transcripts: list[dict]):
    meta = load_payload()["meta"]
    assert len(transcripts) == meta["total"] == 72


def test_each_category_has_twenty_four(transcripts: list[dict]):
    meta = load_payload()["meta"]["categories"]
    for cat in ("fraud", "theft", "fight"):
        count = sum(1 for t in transcripts if t["category"] == cat)
        assert count == meta[cat]["count"] == 24, f"{cat} has {count}"


def test_unique_ids(transcripts: list[dict]):
    ids = [t["id"] for t in transcripts]
    assert len(ids) == len(set(ids))


@pytest.mark.parametrize("t", load_transcripts(), ids=lambda x: x["id"])
def test_transcript_structure(t: dict):
    assert t["category"] in CATEGORY_SCENARIO
    assert t["scenario"] == CATEGORY_SCENARIO[t["category"]]
    assert "body" in t and "问：" in t["body"]
    assert "plain_summary" in t and len(t["plain_summary"]) >= 20
    assert "expected_slots" in t
    assert "expected_risk" in t


@pytest.mark.parametrize("t", load_transcripts(), ids=lambda x: x["id"])
def test_missing_fields_match(t: dict):
    expected = t.get("expected_missing_fields")
    if expected is None:
        pytest.skip("no expected_missing_fields")
    actual = check_missing(t["scenario"], t["expected_slots"])
    assert actual == expected


def test_theft_cases_marked_suspected_theft(transcripts: list[dict]):
    theft = [t for t in transcripts if t["category"] == "theft"]
    for t in theft:
        assert t["expected_slots"].get("suspected_theft") is True


def test_fight_cases_marked_physical_conflict(transcripts: list[dict]):
    fights = [t for t in transcripts if t["category"] == "fight"]
    for t in fights:
        assert t["expected_slots"].get("physical_conflict") is True


def test_body_can_feed_user_text_field(transcripts: list[dict]):
    """笔录 body 应足够长，可供摘要/抽取模块当 user_text 试验。"""
    for t in transcripts:
        assert len(t["body"]) >= 70
