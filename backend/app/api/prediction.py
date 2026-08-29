from fastapi import APIRouter, HTTPException

from backend.app.ml.predictor import predict_category
from backend.app.schemas.prediction import (
    PredictionRequest,
    PredictionResponse,
)


router = APIRouter(
    prefix="/api",
    tags=["AI Prediction"],
)


@router.post(
    "/predict",
    response_model=PredictionResponse,
)
def predict_resume(request: PredictionRequest):
    try:
        category = predict_category(request.resume_text)

        return PredictionResponse(
            predicted_category=category
        )

    except (ValueError, TypeError) as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )
