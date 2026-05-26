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
    text: str = Field(..., min_length=1, description="User's raw report or help-seeking message.")
    case_id: str | None = Field(default=None, description="Optional case/session id from the caller.")


class MapLocation(BaseModel):
    query: str = Field(..., description="Address phrase sent to the geocoder.")
    display_name: str = Field(..., description="Human-readable resolved place name.")
    lat: float = Field(..., description="Latitude.")
    lng: float = Field(..., description="Longitude.")
    source: str = Field(..., description="Geocoder backend, e.g. google or nominatim.")
    map_url: str = Field(..., description="External map link for the resolved place.")


class GeocodeRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Free text that may contain addresses.")
    slots: dict = Field(default_factory=dict, description="Optional structured slots from extraction.")
    max_results: int = Field(default=2, ge=1, le=5, description="Maximum locations to resolve.")


class GeocodeResponse(BaseModel):
    extracted_addresses: list[str] = Field(default_factory=list)
    map_locations: list[MapLocation] = Field(default_factory=list)
    map_provider: str = Field(default="nominatim", description="Primary geocoder when resolving.")


class CaseState(BaseModel):
    case_id: str = Field(default="demo-case", description="Case/session id.")
    user_text: str = Field(..., description="Original user message.")
    scenario: Scenario = Field(default="unknown", description="Classified scenario.")
    intent: str = Field(default="unknown", description="Reserved for future intent classification.")
    emotion: str = Field(default="neutral", description="Rule-based rough emotion label.")
    risk_level: RiskLevel = Field(default="low", description="Rule-based risk level.")
    completeness_score: float = Field(default=0.0, ge=0.0, le=1.0, description="Required-field completion ratio.")
    slots: dict = Field(default_factory=dict, description="Structured fields extracted from the user text.")
    missing_fields: list[str] = Field(default_factory=list, description="Required fields still missing.")
    evidence_checklist: list[str] = Field(default_factory=list, description="Evidence items to preserve or confirm.")
    key_facts: list[str] = Field(default_factory=list, description="Key facts for police-side reading.")
    knowledge_snippets: list[str] = Field(default_factory=list, description="Relevant local KB guidance snippets.")
    next_action: NextAction = Field(default="ask_followup", description="Recommended next system action.")
    next_question: str = Field(default="", description="Next follow-up question for the user.")
    police_summary: str = Field(default="", description="Short police-side summary.")
    suggested_next_steps: list[str] = Field(default_factory=list, description="Suggested follow-up actions.")
    extracted_addresses: list[str] = Field(
        default_factory=list,
        description="Physical location phrases extracted from text and slots.",
    )
    map_locations: list[MapLocation] = Field(
        default_factory=list,
        description="Geocoded map pins for extracted addresses (may be empty if lookup fails).",
    )
