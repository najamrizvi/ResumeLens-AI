from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from backend.app.ml.predictor import predict_category
from backend.app.services.skill_extractor import extract_skills
from backend.app.services.job_fit import calculate_job_fit


router = APIRouter(
    prefix="/api",
    tags=["Resume Analysis"],
)


class ResumeAnalysisRequest(BaseModel):
    resume_text: str = Field(
        ...,
        min_length=20,
        description="Candidate resume text",
    )

    job_text: str = Field(
        ...,
        min_length=20,
        description="Target job description",
    )


@router.post("/analyze")
def analyze_resume(request: ResumeAnalysisRequest):
    """
    Analyze a resume against a job description.

    Pipeline:
        Resume + Job Description
                    ↓
             AI Category Model
                    ↓
             Skill Extraction
                    ↓
              Skill Matching
                    ↓
              Job Fit Score
    """

    resume_text = request.resume_text.strip()
    job_text = request.job_text.strip()

    if not resume_text:
        raise HTTPException(
            status_code=400,
            detail="Resume text cannot be empty.",
        )

    if not job_text:
        raise HTTPException(
            status_code=400,
            detail="Job description cannot be empty.",
        )

    try:
        # ====================================================
        # 1. AI career-category prediction
        # ====================================================

        predicted_category = predict_category(
            resume_text,
            job_text,
        )

        # ====================================================
        # 2. Extract skills
        # ====================================================

        resume_skills = extract_skills(
            resume_text
        )

        required_skills = extract_skills(
            job_text
        )

        # ====================================================
        # 3. Calculate job compatibility
        # ====================================================

        fit_result = calculate_job_fit(
            resume_skills,
            required_skills,
        )

        # ====================================================
        # 4. Return complete AI analysis
        # ====================================================

        return {
            "predicted_category": predicted_category,
            "fit_score": fit_result["fit_score"],
            "resume_skills": resume_skills,
            "required_skills": required_skills,
            "matched_skills": fit_result["matched_skills"],
            "missing_skills": fit_result["missing_skills"],
            "total_required_skills": fit_result[
                "total_required_skills"
            ],
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Resume analysis failed: {str(exc)}",
        )