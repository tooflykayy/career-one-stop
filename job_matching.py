from career_matching import match_careers
from job_data import JOBS


def recommend_jobs(saved_skills):
    career_matches = {
        career["id"]: career
        for career in match_careers(saved_skills)
    }

    recommendations = []

    for job in JOBS:
        career = career_matches.get(job["career_id"])

        if career is None:
            continue

        recommendations.append({
            **job,
            "career_title": career["title"],
            "match_percentage": career["match_percentage"],
            "matched_skills": career["matched_skills"],
            "skill_gaps": career["skill_gaps"],
        })

    return sorted(
        recommendations,
        key=lambda job: (-job["match_percentage"], job["title"]),
    )
