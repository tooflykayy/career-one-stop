from career_data import CAREERS

LEVEL_VALUES = {
    "Beginner": 1,
    "Intermediate": 2,
    "Advanced": 3,
}


def normalize_skill_name(name):
    return " ".join(name.casefold().split())


def match_careers(saved_skills):
    user_skills = {}

    for skill in saved_skills:
        name = normalize_skill_name(skill.name)
        level = LEVEL_VALUES.get(skill.proficiency, 0)

        # If duplicate skills exist, use the highest proficiency.
        user_skills[name] = max(user_skills.get(name, 0), level)

    results = []

    for career in CAREERS:
        matched_skills = []
        skill_gaps = []

        for name, required_level in career["required_skills"].items():
            current_value = user_skills.get(normalize_skill_name(name), 0)
            required_value = LEVEL_VALUES[required_level]

            if current_value >= required_value:
                matched_skills.append(name)
            else:
                current_level = next(
                    (
                        label
                        for label, value in LEVEL_VALUES.items()
                        if value == current_value
                    ),
                    "Not added",
                )

                skill_gaps.append({
                    "name": name,
                    "current_level": current_level,
                    "required_level": required_level,
                })

        total_required = len(career["required_skills"])
        match_percentage = (
            round(len(matched_skills) / total_required * 100)
            if total_required else 0
        )

        results.append({
            **career,
            "match_percentage": match_percentage,
            "matched_skills": matched_skills,
            "skill_gaps": skill_gaps,
        })

    return sorted(
        results,
        key=lambda career: (-career["match_percentage"], career["title"]),
    )