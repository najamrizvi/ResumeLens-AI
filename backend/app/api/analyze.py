from fastapi import APIRouter, HTTPException

from backend.app.schemas.analyze import (
    AnalyzeRequest,
    AnalyzeResponse,
)
from backend.app.ml.predictor import predict_category
from backend.app.services.skill_extractor import extract_skills
from backend.app.services.job_fit import calculate_job_fit


router = APIRouter(
    prefix="/api",
    tags=["Resume Analysis"],
)


@router.post(
    "/analyze",
    response_model=AnalyzeResponse,
)
def analyze_resume(request: AnalyzeRequest):

    try:
        # --------------------------------------------------
        # 1. Predict career category
        # --------------------------------------------------

        predicted_category = predict_category(
            request.resume_text,
            request.job_description,
        )

        # --------------------------------------------------
        # 2. Extract skills from resume
        # --------------------------------------------------

        resume_skills = extract_skills(
            request.resume_text
        )

        # --------------------------------------------------
        # 3. Extract required skills from job description
        # --------------------------------------------------

        required_skills = extract_skills(
            request.job_description
        )

        # --------------------------------------------------
        # 4. Calculate job fit
        # --------------------------------------------------

        fit_result = calculate_job_fit(
            resume_skills,
            required_skills,
        )

        # --------------------------------------------------
        # 5. Return complete analysis
        # --------------------------------------------------

        return AnalyzeResponse(
            predicted_category=predicted_category,
            fit_score=fit_result["fit_score"],
            resume_skills=resume_skills,
            required_skills=required_skills,
            matched_skills=fit_result["matched_skills"],
            missing_skills=fit_result["missing_skills"],
            total_required_skills=fit_result["total_required_skills"],
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Resume analysis failed: {str(exc)}",
        )