from typing import Literal

from pydantic import BaseModel, Field


Scenario = Literal[
    "telecom_fraud",
    "property_loss",
    "dorm_conflict",
    "personal_safety_threat",
    "unknown",
]

RiskLevel = Literal["low", "medium", "high"]
NextAction = Literal["ask_followup", "give_guidance", "handoff_human"]


class UserMessage(BaseModel):
    text: str
    case_id: str | None = None


class CaseState(BaseModel):
    case_id: str = "demo-case"
    user_text: str
    scenario: Scenario = "unknown"
    intent: str = "unknown"
    emotion: str = "neutral"
    risk_level: RiskLevel = "low"
    completeness_score: float = 0.0
    slots: dict = Field(default_factory=dict)
    missing_fields: list[str] = Field(default_factory=list)
    evidence_checklist: list[str] = Field(default_factory=list)
    next_action: NextAction = "ask_followup"
    next_question: str = ""
    police_summary: str = ""
    suggested_next_steps: list[str] = Field(default_factory=list)

