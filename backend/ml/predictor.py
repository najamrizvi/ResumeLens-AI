from pathlib import Path
import joblib


# Project root:
# ResumeLens-AI/
PROJECT_ROOT = Path(__file__).resolve().parents[3]

MODEL_PATH = PROJECT_ROOT / "models" / "resume_category_model.pkl"
VECTORIZER_PATH = PROJECT_ROOT / "models" / "resume_tfidf_vectorizer.pkl"


# Load artifacts once when the module is imported
model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)


def predict_category(resume_text: str) -> str:
    """
    Predict the most likely resume category.
    """

    if not isinstance(resume_text, str):
        raise TypeError("resume_text must be a string.")

    resume_text = resume_text.strip()

    if not resume_text:
        raise ValueError("resume_text cannot be empty.")

    # Convert resume text into TF-IDF features
    features = vectorizer.transform([resume_text])

    # Predict category
    prediction = model.predict(features)[0]

    return str(prediction)