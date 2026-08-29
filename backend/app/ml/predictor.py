from pathlib import Path

import joblib


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[3]

MODEL_PATH = (
    BASE_DIR
    / "models"
    / "resume_category_model.pkl"
)

VECTORIZER_PATH = (
    BASE_DIR
    / "models"
    / "resume_tfidf_vectorizer.pkl"
)


# ============================================================
# LOAD ARTIFACTS
# ============================================================

if not MODEL_PATH.exists():
    raise FileNotFoundError(
        f"Model not found: {MODEL_PATH}"
    )

if not VECTORIZER_PATH.exists():
    raise FileNotFoundError(
        f"Vectorizer not found: {VECTORIZER_PATH}"
    )


model = joblib.load(
    MODEL_PATH
)

vectorizer = joblib.load(
    VECTORIZER_PATH
)


# ============================================================
# PREDICTION
# ============================================================

def predict_category(
    resume_text: str,
    job_text: str,
) -> str:

    resume_text = str(
        resume_text
    ).strip()

    job_text = str(
        job_text
    ).strip()

    if not resume_text:
        raise ValueError(
            "Resume text cannot be empty."
        )

    if not job_text:
        raise ValueError(
            "Job description cannot be empty."
        )

    combined_text = (
        "RESUME: "
        + resume_text
        + " JOB DESCRIPTION: "
        + job_text
    )

    features = vectorizer.transform(
        [combined_text]
    )

    prediction = model.predict(
        features
    )[0]

    return str(prediction)