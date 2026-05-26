import json
import os

from app.core.state import CaseState
from app.services.llm_client import call_llm_json

_PROMPT_PATH = os.path.join(os.path.dirname(__file__), "..", "prompts", "summary.md")

with open(_PROMPT_PATH, "r", encoding="utf-8") as f:
    _SYSTEM_PROMPT = f.read()


def generate_police_summary(state: CaseState) -> str:
    result = generate_police_summary_payload(state)
    if result and isinstance(result.get("summary"), str):
        return result["summary"]
    return str(result) if result else "暂无摘要"


def generate_police_summary_payload(state: CaseState) -> dict:
    user_prompt = (
        f"案件状态：\n"
        f"- 场景：{state.scenario}\n"
        f"- 用户原话：{state.user_text}\n"
        f"- 已抽取字段：{json.dumps(state.slots, ensure_ascii=False)}\n"
        f"- 缺失字段：{', '.join(state.missing_fields) or '无'}\n"
        f"- 风险等级：{state.risk_level}\n"
        f"- 完整度分数：{state.completeness_score:.2f}\n"
        f"- 情绪：{state.emotion}\n"
    )
    result = call_llm_json(
        user_prompt=user_prompt,
        system_prompt=_SYSTEM_PROMPT,
    )
    return result if isinstance(result, dict) else {}
