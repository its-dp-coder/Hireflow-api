from datetime import datetime

from pydantic import BaseModel, ConfigDict


class JobCreate(BaseModel):
    title: str
    description: str
    location: str
    employment_type: str


class JobResponse(BaseModel):
    id: int
    title: str
    description: str
    location: str
    employment_type: str
    recruiter_id: int
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )