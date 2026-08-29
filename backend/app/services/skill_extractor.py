import re
from typing import List


SKILL_VOCABULARY = [
    "python",
    "java",
    "javascript",
    "typescript",
    "c++",
    "c#",
    "sql",
    "mysql",
    "postgresql",
    "mongodb",
    "pandas",
    "numpy",
    "scikit-learn",
    "tensorflow",
    "pytorch",
    "machine learning",
    "deep learning",
    "data science",
    "data analysis",
    "artificial intelligence",
    "natural language processing",
    "computer vision",
    "fastapi",
    "flask",
    "django",
    "react",
    "node.js",
    "docker",
    "git",
    "github",
    "linux",
    "aws",
    "azure",
    "google cloud",
    "power bi",
    "tableau",
    "excel",
    "statistics",
    "communication",
    "leadership",
    "project management",
    "problem solving",
    "human resources",
    "recruitment",
    "marketing",
    "sales",
    "customer service",
    "accounting",
    "finance",
]


def normalize_text(text: str) -> str:
    """Normalize text before skill matching."""
    text = text.lower()
    text = text.replace("scikit learn", "scikit-learn")
    text = text.replace("nodejs", "node.js")
    text = re.sub(r"\s+", " ", text)
    return text


def extract_skills(text: str) -> List[str]:
    """
    Extract known skills from resume or job-description text.

    Matching is case-insensitive and based on a controlled
    vocabulary of supported skills.
    """

    if not text or not isinstance(text, str):
        return []

    normalized_text = normalize_text(text)

    found_skills = []

    for skill in SKILL_VOCABULARY:
        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"

        if re.search(pattern, normalized_text):
            found_skills.append(skill)

    return sorted(found_skills)
