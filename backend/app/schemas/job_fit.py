from pydantic import BaseModel, Field
from typing import List


class JobFitRequest(BaseModel):
    resume_skills: List[str] = Field(
        ...,
        min_length=1,
        description="Skills extracted from the candidate resume."
    )

    required_skills: List[str] = Field(
        ...,
        min_length=1,
        description="Skills required by the job."
    )


class JobFitResponse(BaseModel):
    fit_score: float
    matched_skills: List[str]
    missing_skills: List[str]
    total_required_skills: int
