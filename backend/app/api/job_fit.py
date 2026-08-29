from fastapi import APIRouter, HTTPException

from backend.app.schemas.job_fit import (
    JobFitRequest,
    JobFitResponse,
)
from backend.app.services.job_fit import calculate_job_fit


router = APIRouter(
    prefix="/api",
    tags=["Job Fit Analysis"],
)


@router.post(
    "/job-fit",
    response_model=JobFitResponse,
)
def analyze_job_fit(request: JobFitRequest):
    try:
        result = calculate_job_fit(
            request.resume_skills,
            request.required_skills,
        )

        return JobFitResponse(**result)

    except (ValueError, TypeError) as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )
