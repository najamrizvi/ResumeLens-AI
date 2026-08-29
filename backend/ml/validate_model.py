import os
import joblib
import pandas as pd

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix,
)
from sklearn.model_selection import train_test_split


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DATASET_PATH = os.path.join(
    BASE_DIR,
    "data",
    "job_resume_fit.csv",
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "resume_category_model.pkl",
)

VECTORIZER_PATH = os.path.join(
    BASE_DIR,
    "models",
    "resume_tfidf_vectorizer.pkl",
)


def main():

    print("=" * 70)
    print("ResumeLens AI - ML Model Validation")
    print("=" * 70)

    # ---------------------------------------------------------
    # 1. Load dataset
    # ---------------------------------------------------------
    print("\n[1/5] Loading dataset...")

    df = pd.read_csv(DATASET_PATH)

    df = df.dropna(
        subset=["resume_text", "category"]
    )

    X = df["resume_text"].astype(str)
    y = df["category"].astype(str)

    print(f"Dataset samples: {len(df)}")
    print(f"Categories: {y.nunique()}")

    # ---------------------------------------------------------
    # 2. Recreate the same test split
    # ---------------------------------------------------------
    print("\n[2/5] Creating validation split...")

    _, X_test, _, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y,
    )

    print(f"Validation samples: {len(X_test)}")

    # ---------------------------------------------------------
    # 3. Load trained artifacts
    # ---------------------------------------------------------
    print("\n[3/5] Loading trained model...")

    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)

    print("Model loaded successfully.")
    print("Vectorizer loaded successfully.")

    # ---------------------------------------------------------
    # 4. Generate predictions
    # ---------------------------------------------------------
    print("\n[4/5] Generating predictions...")

    X_test_tfidf = vectorizer.transform(X_test)

    predictions = model.predict(X_test_tfidf)

    # ---------------------------------------------------------
    # 5. Calculate metrics
    # ---------------------------------------------------------
    print("\n[5/5] Calculating evaluation metrics...")

    accuracy = accuracy_score(
        y_test,
        predictions,
    )

    precision = precision_score(
        y_test,
        predictions,
        average="weighted",
        zero_division=0,
    )

    recall = recall_score(
        y_test,
        predictions,
        average="weighted",
        zero_division=0,
    )

    f1 = f1_score(
        y_test,
        predictions,
        average="weighted",
        zero_division=0,
    )

    print("\n" + "=" * 70)
    print("MODEL VALIDATION RESULTS")
    print("=" * 70)

    print(f"\nAccuracy : {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall   : {recall:.4f}")
    print(f"F1 Score : {f1:.4f}")

    print("\nClassification Report:")
    print(
        classification_report(
            y_test,
            predictions,
            zero_division=0,
        )
    )

    print("\nConfusion Matrix:")
    print(
        confusion_matrix(
            y_test,
            predictions,
        )
    )

    print("\n" + "=" * 70)
    print("Validation completed successfully.")
    print("=" * 70)


if __name__ == "__main__":
    main()
