from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependencies import require_role
from app.db.database import get_db
from app.models import Job, User
from app.schemas.job import JobCreate, JobResponse


router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"],
)


@router.post(
    "",
    response_model=JobResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_job(
    job_data: JobCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("recruiter")),
):
    job = Job(
        title=job_data.title,
        description=job_data.description,
        location=job_data.location,
        employment_type=job_data.employment_type,
        recruiter_id=current_user.id,
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    return job