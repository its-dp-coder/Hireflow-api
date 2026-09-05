from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.application import ApplicationStatus


class ApplicationCreate(BaseModel):
    cover_letter: str | None = None


class ApplicationStatusUpdate(BaseModel):
    status: ApplicationStatus


class ApplicationResponse(BaseModel):
    id: int
    job_id: int
    candidate_id: int
    cover_letter: str | None
    status: ApplicationStatus
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )