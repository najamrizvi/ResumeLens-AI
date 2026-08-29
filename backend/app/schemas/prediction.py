from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    resume_text: str = Field(
        ...,
        min_length=20,
        description="Resume text to classify."
    )


class PredictionResponse(BaseModel):
    predicted_category: str
