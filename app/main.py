from fastapi import FastAPI

from app.api.applications import router as applications_router
from app.api.auth import router as auth_router
from app.api.companies import router as companies_router
from app.api.jobs import router as jobs_router


app = FastAPI(
    title="HireFlow API",
    description="""
Production-style Job Recruitment API.

## Features

* Multi-role authentication
* Candidate profiles
* Recruiter profiles
* Company management
* Job management
* Job applications
* Application status workflow
* Role-Based Access Control
""",
    version="1.0.0",
)

app.include_router(auth_router)
app.include_router(companies_router)
app.include_router(jobs_router)
app.include_router(applications_router)


@app.get("/")
def root():
    return {
        "message": "HireFlow API is running",
        "docs": "/docs",
        "health": "/health",
    }


@app.get(
    "/health",
    tags=["Health"],
)
def health_check():
    return {"status": "ok"}