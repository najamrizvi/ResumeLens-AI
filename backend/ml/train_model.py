from pathlib import Path

import joblib
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

DATA_PATH = BASE_DIR / "data" / "job_resume_fit.csv"
MODEL_DIR = BASE_DIR / "models"

MODEL_PATH = MODEL_DIR / "resume_category_model.pkl"
VECTORIZER_PATH = MODEL_DIR / "resume_tfidf_vectorizer.pkl"


# ============================================================
# CONFIGURATION
# ============================================================

TEST_SIZE = 0.20
RANDOM_STATE = 42
MAX_FEATURES = 15000


# ============================================================
# HEADER
# ============================================================

print("=" * 70)
print("ResumeLens AI - Model Training")
print("=" * 70)


# ============================================================
# 1. LOAD DATASET
# ============================================================

print("\n[1/7] Loading dataset...")

if not DATA_PATH.exists():
    raise FileNotFoundError(
        f"Dataset not found: {DATA_PATH}"
    )

df = pd.read_csv(DATA_PATH)

print(f"Dataset shape: {df.shape}")


# ============================================================
# 2. VALIDATE + CLEAN DATA
# ============================================================

print("\n[2/7] Validating dataset...")

required_columns = [
    "resume_text",
    "job_text",
    "category",
]

missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Missing required columns: {missing_columns}"
    )

df = df.dropna(
    subset=required_columns
).copy()

df["resume_text"] = (
    df["resume_text"]
    .astype(str)
    .str.strip()
)

df["job_text"] = (
    df["job_text"]
    .astype(str)
    .str.strip()
)

df["category"] = (
    df["category"]
    .astype(str)
    .str.strip()
)

df = df[
    (df["resume_text"] != "")
    & (df["job_text"] != "")
    & (df["category"] != "")
].copy()

print(f"Samples after cleaning: {len(df)}")
print(f"Number of categories: {df['category'].nunique()}")


# ============================================================
# 3. CREATE COMBINED TEXT FEATURES
# ============================================================

print("\n[3/7] Preparing text features...")

df["combined_text"] = (
    "RESUME: "
    + df["resume_text"]
    + " JOB DESCRIPTION: "
    + df["job_text"]
)

X = df["combined_text"]
y = df["category"]

print("Feature source:")
print("  Resume + Job Description")

print("\nCategories:")
for category in sorted(y.unique()):
    print(f"  - {category}")


# ============================================================
# 4. TRAIN / TEST SPLIT
# ============================================================

print("\n[4/7] Splitting dataset...")

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=TEST_SIZE,
    random_state=RANDOM_STATE,
    stratify=y,
)

print(f"Training samples: {len(X_train)}")
print(f"Testing samples:  {len(X_test)}")


# ============================================================
# 5. TF-IDF FEATURE EXTRACTION
# ============================================================

print("\n[5/7] Creating TF-IDF vectorizer...")

vectorizer = TfidfVectorizer(
    lowercase=True,
    stop_words="english",
    ngram_range=(1, 2),
    max_features=MAX_FEATURES,
    sublinear_tf=True,
)

X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

print(f"TF-IDF training matrix: {X_train_tfidf.shape}")
print(f"Vocabulary size: {len(vectorizer.vocabulary_)}")


# ============================================================
# 6. TRAIN MODEL
# ============================================================

print("\n[6/7] Training Logistic Regression model...")

model = LogisticRegression(
    max_iter=2000,
    class_weight="balanced",
    random_state=RANDOM_STATE,
)

model.fit(
    X_train_tfidf,
    y_train,
)

print("Model training completed.")


# ============================================================
# 7. EVALUATION + SAVE ARTIFACTS
# ============================================================

print("\n[7/7] Evaluating model...")

predictions = model.predict(X_test_tfidf)

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


# ============================================================
# RESULTS
# ============================================================

print("\n" + "=" * 70)
print("MODEL RESULTS")
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


# ============================================================
# SAVE MODEL ARTIFACTS
# ============================================================

MODEL_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

joblib.dump(
    model,
    MODEL_PATH,
)

joblib.dump(
    vectorizer,
    VECTORIZER_PATH,
)


# ============================================================
# VERIFY SAVED FILES
# ============================================================

print("\n" + "=" * 70)
print("MODEL ARTIFACTS SAVED")
print("=" * 70)

print(f"\nModel:")
print(f"  {MODEL_PATH}")

print("\nVectorizer:")
print(f"  {VECTORIZER_PATH}")

print("\nFile verification:")

if MODEL_PATH.exists():
    print(
        f"  Model: OK ({MODEL_PATH.stat().st_size:,} bytes)"
    )
else:
    print("  Model: FAILED")

if VECTORIZER_PATH.exists():
    print(
        f"  Vectorizer: OK "
        f"({VECTORIZER_PATH.stat().st_size:,} bytes)"
    )
else:
    print("  Vectorizer: FAILED")


print("\n" + "=" * 70)
print("Training completed successfully.")
print("=" * 70)