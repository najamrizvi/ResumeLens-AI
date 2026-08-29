import re
from typing import List, Dict


def normalize_skill(skill: str) -> str:
    """Normalize a skill for reliable comparison."""
    skill = skill.lower().strip()
    skill = re.sub(r"[^a-z0-9+#.\-/ ]", "", skill)
    skill = re.sub(r"\s+", " ", skill)
    return skill


def parse_skills(skills) -> List[str]:
    """Convert a skill list/string into normalized unique skills."""
    if skills is None:
        return []

    if isinstance(skills, list):
        items = skills
    else:
        items = re.split(r",|;|\||\n", str(skills))

    normalized = []

    for skill in items:
        skill = normalize_skill(skill)

        if skill and skill not in normalized:
            normalized.append(skill)

    return normalized


def calculate_job_fit(
    resume_skills,
    required_skills,
) -> Dict:
    """
    Compare resume skills against required job skills.

    Returns matched skills, missing skills and a percentage fit score.
    """

    resume = set(parse_skills(resume_skills))
    required = set(parse_skills(required_skills))

    if not required:
        return {
            "fit_score": 0.0,
            "matched_skills": [],
            "missing_skills": [],
            "total_required_skills": 0,
        }

    matched = sorted(resume.intersection(required))
    missing = sorted(required.difference(resume))

    score = (len(matched) / len(required)) * 100

    return {
        "fit_score": round(score, 2),
        "matched_skills": matched,
        "missing_skills": missing,
        "total_required_skills": len(required),
    }
