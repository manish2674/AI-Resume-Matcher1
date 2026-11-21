
import re

from core.jd_parser import extract_qualifications


SCORING_WEIGHTS = {
    "skills": 40,
    "semantic": 30,
    "experience": 20,
    "qualification": 10,
}


DEGREE_LEVELS = {
    "B.Tech": 1,
    "B.E.": 1,
    "B.Sc": 1,
    "BCA": 1,
    "Bachelor's degree": 1,
    "M.Tech": 2,
    "M.E.": 2,
    "M.Sc": 2,
    "MCA": 2,
    "Master's degree": 2,
    "PhD": 3,
}


TECHNICAL_FIELD_ALIASES = {
    "computer science": [
        "computer science",
        "computer science and engineering",
        "computer science engineering",
        "cse",
        "cs",
    ],
    "computer engineering": [
        "computer engineering",
        "computer engineering technology",
    ],
    "information technology": [
        "information technology",
        "information technology engineering",
        "information technology and engineering",
        "it",
    ],
    "information systems": [
        "information systems",
        "management information systems",
    ],
    "data science": [
        "data science",
        "data analytics",
    ],
    "artificial intelligence": [
        "artificial intelligence",
        "ai",
    ],
    "machine learning": [
        "machine learning",
    ],
    "software engineering": [
        "software engineering",
        "software development",
    ],
}


RELATED_FIELD_GROUPS = [
    {
        "computer science",
        "computer engineering",
        "information technology",
        "information systems",
        "data science",
        "artificial intelligence",
        "machine learning",
        "software engineering",
    }
]


EDUCATION_HEADINGS = {
    "education",
    "educational background",
    "academic background",
    "academic qualification",
    "academic qualifications",
    "qualification",
    "qualifications",
    "required qualifications",
    "preferred qualifications",
    "educational requirements",
}

OTHER_SECTION_HEADINGS = {
    "experience",
    "work experience",
    "professional experience",
    "employment history",
    "work history",
    "skills",
    "technical skills",
    "projects",
    "personal projects",
    "certifications",
    "certificates",
    "achievements",
    "interests",
    "hobbies",
    "publications",
    "references",
    "professional summary",
    "summary",
    "career objective",
}


def normalize_heading(line: str) -> str:
    """Normalize a possible document section heading."""

    line = re.sub(r"^\s*[-*•]\s*", "", line)
    return line.strip().lower().rstrip(":").strip()


def flatten_skills(skills_by_category: dict) -> list:
    """Flatten categorized skills into a unique list."""

    if not isinstance(skills_by_category, dict):
        return []

    all_skills = []

    for category_skills in skills_by_category.values():
        if isinstance(category_skills, list):
            all_skills.extend(
                skill
                for skill in category_skills
                if isinstance(skill, str) and skill.strip()
            )

    return list(dict.fromkeys(all_skills))


def calculate_skill_score(jd_data: dict, resume_data: dict) -> dict:
    """Calculate required and preferred skill coverage."""

    required_skills = flatten_skills(
        jd_data.get("required_skills", {})
    )

    preferred_skills = flatten_skills(
        jd_data.get("preferred_skills", {})
    )

    required_set = {
        skill.casefold() for skill in required_skills
    }

    preferred_skills = [
        skill for skill in preferred_skills
        if skill.casefold() not in required_set
    ]

    candidate_skills = flatten_skills(
        resume_data.get("skills", {})
    )

    candidate_skill_set = {
        skill.casefold() for skill in candidate_skills
    }

    matched_required = [
        skill for skill in required_skills
        if skill.casefold() in candidate_skill_set
    ]

    missing_required = [
        skill for skill in required_skills
        if skill.casefold() not in candidate_skill_set
    ]

    matched_preferred = [
        skill for skill in preferred_skills
        if skill.casefold() in candidate_skill_set
    ]

    missing_preferred = [
        skill for skill in preferred_skills
        if skill.casefold() not in candidate_skill_set
    ]

    required_score = (
        len(matched_required) / len(required_skills) * 100
        if required_skills else None
    )

    preferred_score = (
        len(matched_preferred) / len(preferred_skills) * 100
        if preferred_skills else None
    )

    if required_score is not None and preferred_score is not None:
        skill_score = (
            required_score * 0.80
            + preferred_score * 0.20
        )
    elif required_score is not None:
        skill_score = required_score
    elif preferred_score is not None:
        skill_score = preferred_score
    else:
        skill_score = None

    return {
        "score": (
            round(skill_score, 2)
            if skill_score is not None
            else None
        ),
        "required_score": (
            round(required_score, 2)
            if required_score is not None
            else None
        ),
        "preferred_score": (
            round(preferred_score, 2)
            if preferred_score is not None
            else None
        ),
        "matched_required": matched_required,
        "missing_required": missing_required,
        "matched_preferred": matched_preferred,
        "missing_preferred": missing_preferred,
    }


def calculate_experience_score(jd_data: dict, resume_data: dict):
    """Compare candidate experience against the JD minimum."""

    required_years = jd_data.get("minimum_experience_years")

    experience_data = resume_data.get("experience", {})
    candidate_years = experience_data.get("total_experience_years")

    if required_years is None or candidate_years is None:
        return None

    if required_years <= 0:
        return None

    score = min(
        candidate_years / required_years * 100,
        100
    )

    return round(score, 2)


def extract_technical_fields(text: str) -> list:
    """Identify technical education fields in supplied text."""

    if not isinstance(text, str) or not text.strip():
        return []

    normalized_text = re.sub(
        r"[^a-z0-9+#]+",
        " ",
        text.casefold()
    )

    detected_fields = []

    for canonical_field, aliases in TECHNICAL_FIELD_ALIASES.items():
        for alias in aliases:
            normalized_alias = alias.casefold()

            pattern = (
                r"(?<![a-z0-9])"
                + re.escape(normalized_alias)
                + r"(?![a-z0-9])"
            )

            if re.search(pattern, normalized_text):
                detected_fields.append(canonical_field)
                break

    return list(dict.fromkeys(detected_fields))


def extract_qualification_context(text: str) -> str:
    """
    Extract education-related evidence.

    Education sections are captured until another known section begins.
    If no education heading exists, only explicit degree-containing
    lines are used. The entire resume is never used as a field fallback.
    """

    if not isinstance(text, str) or not text.strip():
        return ""

    lines = text.splitlines()
    relevant_lines = []

    capturing = False
    found_education_heading = False

    for line in lines:
        heading = normalize_heading(line)

        if heading in EDUCATION_HEADINGS:
            capturing = True
            found_education_heading = True
            relevant_lines.append(line)
            continue

        if heading in OTHER_SECTION_HEADINGS:
            if capturing:
                capturing = False
            continue

        if capturing:
            relevant_lines.append(line)

    if found_education_heading:
        return "\n".join(relevant_lines)

    degree_lines = []

    for line in lines:
        if extract_qualifications(line):
            degree_lines.append(line)

    return "\n".join(dict.fromkeys(degree_lines))


def get_degree_level(qualifications: list) -> int:
    """Return the highest recognized degree level."""

    levels = [
        DEGREE_LEVELS.get(qualification, 0)
        for qualification in qualifications
    ]

    return max(levels, default=0)


def fields_are_related(
    required_fields: list,
    candidate_fields: list
) -> bool:
    """Determine whether two technical education fields are related."""

    if not required_fields or not candidate_fields:
        return False

    for group in RELATED_FIELD_GROUPS:
        required_match = any(
            field in group for field in required_fields
        )

        candidate_match = any(
            field in group for field in candidate_fields
        )

        if required_match and candidate_match:
            return True

    return any(
        required == candidate
        for required in required_fields
        for candidate in candidate_fields
    )


def calculate_qualification_score(
    jd_data: dict,
    resume_data: dict
):
    """Evaluate required and preferred educational qualifications."""

    required_qualifications = jd_data.get(
        "qualifications", []
    )

    preferred_qualifications = jd_data.get(
        "preferred_qualifications", []
    )

    if not required_qualifications:
        return None

    jd_text = jd_data.get("job_description", "")
    resume_text = resume_data.get("resume_text", "")

    jd_education_context = extract_qualification_context(
        jd_text
    )

    candidate_education_context = extract_qualification_context(
        resume_text
    )

    # No education evidence means the qualification score is unknown.
    if not candidate_education_context.strip():
        return {
            "score": None,
            "matched": [],
            "matched_preferred": [],
            "detected": [],
            "candidate_fields": [],
            "match_reason": (
                "Education information was not found in the resume."
            ),
            "status": "Qualification information unavailable.",
        }

    # Extract degrees only from education-related evidence.
    candidate_qualifications = extract_qualifications(
        candidate_education_context
    )

    candidate_set = {
        qualification.casefold()
        for qualification in candidate_qualifications
    }

    matched = [
        qualification
        for qualification in required_qualifications
        if qualification.casefold() in candidate_set
    ]

    matched_preferred = [
        qualification
        for qualification in preferred_qualifications
        if qualification.casefold() in candidate_set
    ]

    required_fields = extract_technical_fields(
        jd_education_context
    )

    candidate_fields = extract_technical_fields(
        candidate_education_context
    )

    related_field_match = fields_are_related(
        required_fields,
        candidate_fields
    )

    accepts_related_field = bool(
        re.search(
            r"\b(?:related|relevant)\s+technical\s+field\b",
            jd_text,
            re.IGNORECASE
        )
        or re.search(
            r"\b(?:related|relevant)\s+field\b",
            jd_text,
            re.IGNORECASE
        )
    )

    required_level = get_degree_level(
        required_qualifications
    )

    candidate_level = get_degree_level(
        candidate_qualifications
    )

    # Education exists, but no recognized degree was identified.
    if not candidate_qualifications:
        return {
            "score": 0,
            "matched": [],
            "matched_preferred": [],
            "detected": [],
            "candidate_fields": candidate_fields,
            "match_reason": (
                "Education information was found, but no recognized "
                "degree was detected."
            ),
            "status": "Required qualification not matched.",
        }

    exact_degree_match = bool(matched)

    degree_level_match = (
        required_level > 0
        and candidate_level >= required_level
    )

    if exact_degree_match:
        if not required_fields or related_field_match:
            score = 100
            match_reason = (
                "Required qualification and relevant field matched."
            )
        else:
            score = 0
            matched = []
            match_reason = (
                "Degree detected, but the relevant education field "
                "could not be verified."
            )

    elif (
        degree_level_match
        and required_fields
        and related_field_match
    ):
        score = 100

        matched = [
            qualification
            for qualification in candidate_qualifications
            if DEGREE_LEVELS.get(qualification, 0) >= required_level
        ]

        match_reason = (
            "Equivalent or higher degree in a related technical field."
        )

    elif (
        degree_level_match
        and not required_fields
        and not accepts_related_field
    ):
        score = 100

        matched = [
            qualification
            for qualification in candidate_qualifications
            if DEGREE_LEVELS.get(qualification, 0) >= required_level
        ]

        match_reason = (
            "Equivalent or higher educational qualification matched."
        )

    else:
        score = 0
        matched = []

        if candidate_level == 0:
            match_reason = (
                "No recognized educational degree was detected."
            )
        elif required_fields and not candidate_fields:
            match_reason = (
                "Degree detected, but the candidate's education "
                "field could not be identified."
            )
        elif required_fields and not related_field_match:
            match_reason = (
                "Degree detected, but the education field does not "
                "match the required technical field."
            )
        else:
            match_reason = (
                "The candidate's degree does not meet the "
                "required qualification level."
            )

    status = (
        "Required qualification matched."
        if score == 100
        else "Required qualification not matched."
    )

    return {
        "score": score,
        "matched": matched,
        "matched_preferred": matched_preferred,
        "detected": candidate_qualifications,
        "candidate_fields": candidate_fields,
        "match_reason": match_reason,
        "status": status,
    }


def calculate_final_score(
    jd_data: dict,
    resume_data: dict,
    semantic_result: dict
) -> dict:
    """Combine available matching components into a final score."""

    skill_result = calculate_skill_score(
        jd_data,
        resume_data
    )

    semantic_score = semantic_result.get(
        "semantic_similarity"
    )

    experience_score = calculate_experience_score(
        jd_data,
        resume_data
    )

    qualification_result = calculate_qualification_score(
        jd_data,
        resume_data
    )

    component_scores = {
        "skills": skill_result["score"],
        "semantic": semantic_score,
        "experience": experience_score,
        "qualification": (
            qualification_result["score"]
            if qualification_result is not None
            else None
        ),
    }

    available_components = {
        name: score
        for name, score in component_scores.items()
        if score is not None
    }

    total_available_weight = sum(
        SCORING_WEIGHTS[name]
        for name in available_components
    )

    if total_available_weight == 0:
        raise ValueError(
            "No matching components are available."
        )

    final_score = sum(
        score * SCORING_WEIGHTS[name]
        for name, score in available_components.items()
    ) / total_available_weight

    return {
        "final_score": round(final_score, 2),
        "component_scores": component_scores,
        "skill_analysis": skill_result,
        "qualification_analysis": qualification_result,
    }
