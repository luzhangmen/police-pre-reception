"""Validate multi-turn dialogue fixtures."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

DIALOGUES_PATH = Path(__file__).resolve().parent / "fixtures" / "demo_dialogues.json"
VALID_SCENARIOS = {
    "telecom_fraud",
    "property_loss",
    "dorm_conflict",
    "personal_safety_threat",
    "unknown",
}


def load_dialogues() -> list[dict]:
    with DIALOGUES_PATH.open(encoding="utf-8") as handle:
        return json.load(handle)


@pytest.fixture(scope="module")
def dialogues() -> list[dict]:
    return load_dialogues()


def test_dialogues_file_exists():
    assert DIALOGUES_PATH.is_file()


def test_at_least_eighteen_dialogues(dialogues: list[dict]):
    assert len(dialogues) >= 18


def test_unique_dialogue_ids(dialogues: list[dict]):
    ids = [d["dialogue_id"] for d in dialogues]
    assert len(ids) == len(set(ids))


@pytest.mark.parametrize("dialogue", load_dialogues(), ids=lambda d: d["dialogue_id"])
def test_dialogue_structure(dialogue: dict):
    assert "scenario" in dialogue
    assert dialogue["scenario"] in VALID_SCENARIOS
    assert "turns" in dialogue and len(dialogue["turns"]) >= 2
    assert "final_expected_police_summary_points" in dialogue
    assert len(dialogue["final_expected_police_summary_points"]) >= 2


@pytest.mark.parametrize("dialogue", load_dialogues(), ids=lambda d: d["dialogue_id"])
def test_turn_numbers_sequential(dialogue: dict):
    turns = dialogue["turns"]
    for index, turn in enumerate(turns, start=1):
        assert turn.get("turn", index) == index
        assert "user" in turn and turn["user"].strip()
