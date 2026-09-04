from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CompanyCreate(BaseModel):
    name: str
    description: str
    website: str | None = None
    location: str


class CompanyResponse(BaseModel):
    id: int
    name: str
    description: str
    website: str | None
    location: str
    recruiter_id: int
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )