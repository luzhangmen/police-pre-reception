from datetime import datetime

from pydantic import BaseModel, Field

from app.core.state import CaseState


class PreAcceptanceDocumentRequest(BaseModel):
    """Generate a pre-acceptance form from a pipeline CaseState."""

    case_state: CaseState = Field(..., description="Structured case output from /api/v1/reason or dialogue.")


class DocumentGenerationMetadata(BaseModel):
    document_version: str = "2.0"
    narrative_preview: str = ""
    cleaned_user_text_preview: str = ""
    high_risk_flags: list[str] = Field(default_factory=list)
    missing_field_count: int = 0
    completeness_percent: int = 0
    section_count: int = 13


class PreAcceptanceDocumentResponse(BaseModel):
    case_id: str
    filename: str
    file_path: str = Field(..., description="Server-relative path under backend/generated/.")
    download_url: str
    generated_at: datetime
    format: str = Field(default="docx", description="Document format; PDF may be added later.")
    metadata: DocumentGenerationMetadata = Field(default_factory=DocumentGenerationMetadata)
