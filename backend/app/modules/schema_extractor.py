import json
import os

import yaml

from app.core.state import Scenario
from app.services.llm_client import call_llm_json

_PROMPT_PATH = os.path.join(os.path.dirname(__file__), "..", "prompts", "extract.md")
_SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "..", "schemas", "case_schemas.yaml")

with open(_PROMPT_PATH, "r", encoding="utf-8") as f:
    _SYSTEM_PROMPT = f.read()

with open(_SCHEMA_PATH, "r", encoding="utf-8") as f:
    _SCHEMAS = yaml.safe_load(f)


def extract_slots(text: str, scenario: Scenario) -> dict:
    schema = _SCHEMAS.get(scenario, {})
    user_prompt = (
        f"用户原话：{text}\n\n"
        f"场景：{scenario}\n\n"
        f"该场景的字段 Schema（required 为必填，optional 为可选，high_risk 为高风险字段）：\n"
        f"{yaml.dump(schema, allow_unicode=True)}"
    )
    result = call_llm_json(
        user_prompt=user_prompt,
        system_prompt=_SYSTEM_PROMPT,
    )
    return result if result else {}
