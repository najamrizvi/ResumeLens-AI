from pydantic import BaseModel, Field
from typing import List


class AnalyzeRequest(BaseModel):
    resume_text: str = Field(
        ...,
        min_length=20,
        description="Candidate resume text."
    )

    job_description: str = Field(
        ...,
        min_length=20,
        description="Target job description."
    )


class AnalyzeResponse(BaseModel):
    predicted_category: str
    fit_score: float
    resume_skills: List[str]
    required_skills: List[str]
    matched_skills: List[str]
    missing_skills: List[str]
    total_required_skills: int
