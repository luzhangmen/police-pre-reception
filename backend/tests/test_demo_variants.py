"""Validate variant and negative fixture files."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

FIXTURES = Path(__file__).resolve().parent / "fixtures"
MAIN_CASES = json.loads((FIXTURES / "demo_cases.json").read_text(encoding="utf-8"))
MAIN_IDS = {c["id"] for c in MAIN_CASES}


def load(path: str) -> list[dict]:
    return json.loads((FIXTURES / path).read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def variants() -> list[dict]:
    return load("demo_cases_variants.json")


@pytest.fixture(scope="module")
def negative() -> list[dict]:
    return load("demo_cases_negative.json")


def test_variants_count(variants: list[dict]):
    assert len(variants) >= 20


def test_negative_count(negative: list[dict]):
    assert len(negative) >= 10


@pytest.mark.parametrize("variant", load("demo_cases_variants.json"), ids=lambda v: v["variant_id"])
def test_variant_parent_exists(variant: dict):
    assert variant["parent_id"] in MAIN_IDS


@pytest.mark.parametrize("variant", load("demo_cases_variants.json"), ids=lambda v: v["variant_id"])
def test_variant_has_type(variant: dict):
    assert variant.get("variant_type") in {
        "typo",
        "slang",
        "dialect",
        "sparse",
        "noise_prefix",
        "emotion",
        "boundary",
        "code_mix",
        "emoji",
        "oral",
        "punctuation",
        "verbose",
        "repetition",
        "tone",
        "emphasis",
        "channel",
        "number_format",
        "vague_time",
    }
