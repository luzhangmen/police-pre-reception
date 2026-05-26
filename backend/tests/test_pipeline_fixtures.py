"""End-to-end pipeline checks against demo case fixtures (rule + keyword layer)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from app.core.pipeline import run_pipeline
from app.core.state import UserMessage

FIXTURES = Path(__file__).resolve().parent / "fixtures"
CASES = json.loads((FIXTURES / "demo_cases.json").read_text(encoding="utf-8"))
VARIANTS = json.loads((FIXTURES / "demo_cases_variants.json").read_text(encoding="utf-8"))
NEGATIVE = json.loads((FIXTURES / "demo_cases_negative.json").read_text(encoding="utf-8"))

NON_BOUNDARY = [
    c
    for c in CASES
    if "boundary" not in c.get("tags", []) and "multi_topic" not in c.get("tags", [])
]
HIGH_RISK_CASES = [c for c in CASES if c["expected_risk"] == "high"]


def _scenario_ok(case: dict, actual: str) -> bool:
    if actual == case["scenario"]:
        return True
    alts = case.get("acceptable_alternate_scenarios", [])
    return actual in alts


@pytest.mark.parametrize("case", NON_BOUNDARY[:24], ids=lambda c: c["id"])
def test_pipeline_scenario_for_core_cases(case: dict):
    state = run_pipeline(UserMessage(text=case["input"], case_id=case["id"]))
    assert _scenario_ok(case, state.scenario), (
        f"{case['id']}: expected {case['scenario']}, got {state.scenario}"
    )


@pytest.mark.parametrize("case", HIGH_RISK_CASES, ids=lambda c: c["id"])
def test_pipeline_high_risk_handoff(case: dict):
    state = run_pipeline(UserMessage(text=case["input"], case_id=case["id"]))
    assert state.risk_level == "high", f"{case['id']}: risk={state.risk_level}"
    assert state.next_action == "handoff_human"


@pytest.mark.parametrize("case", NEGATIVE, ids=lambda c: c["id"])
def test_pipeline_negative_unknown(case: dict):
    state = run_pipeline(UserMessage(text=case["input"], case_id=case["id"]))
    assert state.scenario == "unknown"


@pytest.mark.parametrize("variant", VARIANTS, ids=lambda v: v["variant_id"])
def test_pipeline_variant_scenario(variant: dict):
    state = run_pipeline(UserMessage(text=variant["input"], case_id=variant["variant_id"]))
    expected = variant["expected_scenario"]
    alts = variant.get("acceptable_alternate_scenarios", [])
    assert state.scenario == expected or state.scenario in alts


def test_pipeline_returns_required_state_fields():
    state = run_pipeline(UserMessage(text="我在闲鱼买票被骗了，微信转了480"))
    assert state.scenario == "telecom_fraud"
    assert state.risk_level in {"low", "medium", "high"}
    assert state.next_action in {"ask_followup", "give_guidance", "handoff_human"}
    assert isinstance(state.missing_fields, list)
    assert 0.0 <= state.completeness_score <= 1.0
