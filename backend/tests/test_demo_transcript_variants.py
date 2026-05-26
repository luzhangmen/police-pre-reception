"""Validate transcript micro-variants."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

FIXTURES = Path(__file__).resolve().parent / "fixtures"
BASE_PATH = FIXTURES / "demo_transcripts_three_scenarios.json"
VARIANTS_PATH = FIXTURES / "demo_transcripts_three_scenarios_variants.json"

REQUIRED_FIELDS = {
    "telecom_fraud": ["fraud_method", "loss_amount", "transfer_channel", "evidence"],
    "property_loss": ["lost_item", "lost_time", "lost_location", "item_features"],
    "dorm_conflict": ["parties", "conflict_reason", "time_location", "expected_resolution"],
}


def load_bases() -> list[dict]:
    return json.loads(BASE_PATH.read_text(encoding="utf-8"))["transcripts"]


def load_variants() -> list[dict]:
    return json.loads(VARIANTS_PATH.read_text(encoding="utf-8"))["variants"]


@pytest.fixture(scope="module")
def bases() -> list[dict]:
    return load_bases()


@pytest.fixture(scope="module")
def variants() -> list[dict]:
    return load_variants()


def test_variant_count(variants: list[dict], bases: list[dict]):
    assert len(variants) == len(bases) * 4


def test_each_parent_has_four_variants(variants: list[dict], bases: list[dict]):
    parent_ids = {b["id"] for b in bases}
    for pid in parent_ids:
        count = sum(1 for v in variants if v["parent_id"] == pid)
        assert count == 4, f"{pid} has {count} variants"


def test_variant_ids_unique(variants: list[dict]):
    ids = [v["id"] for v in variants]
    assert len(ids) == len(set(ids))


@pytest.mark.parametrize("variant", load_variants(), ids=lambda v: v["id"])
def test_variant_links_parent(variant: dict, bases: list[dict]):
    parent_ids = {b["id"] for b in bases}
    assert variant["parent_id"] in parent_ids
    assert variant["id"].startswith(variant["parent_id"] + "-v")


@pytest.mark.parametrize("variant", load_variants(), ids=lambda v: v["id"])
def test_variant_preserves_scenario(variant: dict, bases: list[dict]):
    parent = next(b for b in bases if b["id"] == variant["parent_id"])
    assert variant["scenario"] == parent["scenario"]
    assert variant["category"] == parent["category"]
    assert variant["expected_risk"] == parent["expected_risk"]


@pytest.mark.parametrize("variant", load_variants(), ids=lambda v: v["id"])
def test_variant_body_still_qa_format(variant: dict):
    assert "问：" in variant["body"] and "答：" in variant["body"]
    assert len(variant["body"]) >= 60


@pytest.mark.parametrize("variant", load_variants(), ids=lambda v: v["id"])
def test_variant_differs_from_parent_in_some_field(variant: dict, bases: list[dict]):
    parent = next(b for b in bases if b["id"] == variant["parent_id"])
    changed = (
        variant["subject"] != parent["subject"]
        or variant["body"] != parent["body"]
        or variant["plain_summary"] != parent["plain_summary"]
        or variant.get("expected_slots") != parent.get("expected_slots")
    )
    assert changed, f"{variant['id']} identical to parent"


@pytest.mark.parametrize("variant", load_variants(), ids=lambda v: v["id"])
def test_variant_missing_fields_consistent(variant: dict):
    req = REQUIRED_FIELDS[variant["scenario"]]
    actual = [f for f in req if not variant["expected_slots"].get(f)]
    assert actual == variant["expected_missing_fields"]


def test_theft_variants_keep_suspected_theft(variants: list[dict]):
    for v in variants:
        if v["category"] == "theft":
            assert v["expected_slots"].get("suspected_theft") is True


def test_fight_variants_keep_physical_conflict(variants: list[dict]):
    for v in variants:
        if v["category"] == "fight":
            assert v["expected_slots"].get("physical_conflict") is True
