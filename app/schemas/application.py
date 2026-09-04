from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ApplicationCreate(BaseModel):
    cover_letter: str | None = None


class ApplicationStatusUpdate(BaseModel):
    status: str


class ApplicationResponse(BaseModel):
    id: int
    job_id: int
    candidate_id: int
    cover_letter: str | None
    status: str
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )