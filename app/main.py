from fastapi import FastAPI


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
* Role-Based Access Control
""",
    version="1.0.0",
)


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