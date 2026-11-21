
import re

from core.text_cleaner import clean_text
from core.skill_extractor import extract_skills


REQUIRED_HEADINGS = [
    "required skills",
    "required technical skills",
    "required skills and qualifications",
    "required skills & qualifications",
    "skills required",
    "mandatory skills",
    "must have",
    "must-have skills",
    "key skills",
    "key technical skills",
    "requirements",
    "technical requirements",
    "what you need",
]

PREFERRED_HEADINGS = [
    "preferred skills",
    "preferred technical skills",
    "good to have",
    "nice to have",
    "desired skills",
    "additional skills",
    "optional skills",
]

REQUIRED_QUALIFICATION_HEADINGS = [
    "required qualifications",
    "required qualification",
    "educational qualifications",
    "educational qualification",
    "education",
    "minimum qualifications",
    "minimum qualification",
    "academic qualifications",
    "academic qualification",
    "educational requirements",
    "required education",
]

PREFERRED_QUALIFICATION_HEADINGS = [
    "preferred qualifications",
    "preferred qualification",
    "preferred education",
    "preferred educational qualifications",
    "preferred educational qualification",
]

EXPERIENCE_HEADINGS = [
    "experience",
    "experience requirements",
    "work experience",
    "required experience",
]

OTHER_HEADINGS = [
    "responsibilities",
    "key responsibilities",
    "what you will do",
    "what you'll do",
    "about the role",
    "about the job",
    "job description",
    "role overview",
    "benefits",
    "what we offer",
    "company overview",
    "about the company",
    "location",
    "salary",
    "employment type",
    "job type",
    "job overview",
]

ALL_HEADINGS = (
    REQUIRED_HEADINGS
    + PREFERRED_HEADINGS
    + REQUIRED_QUALIFICATION_HEADINGS
    + PREFERRED_QUALIFICATION_HEADINGS
    + EXPERIENCE_HEADINGS
    + OTHER_HEADINGS
)


QUALIFICATION_ALIASES = {
    "B.Tech": [
        "B.Tech",
        "BTech",
        "Bachelor of Technology",
    ],
    "B.E.": [
        "B.E.",
        "Bachelor of Engineering",
    ],
    "B.Sc": [
        "B.Sc",
        "BSc",
        "Bachelor of Science",
    ],
    "BCA": [
        "BCA",
        "Bachelor of Computer Applications",
    ],
    "M.Tech": [
        "M.Tech",
        "MTech",
        "Master of Technology",
    ],
    "M.E.": [
        "M.E.",
        "Master of Engineering",
    ],
    "M.Sc": [
        "M.Sc",
        "MSc",
        "Master of Science",
    ],
    "MCA": [
        "MCA",
        "Master of Computer Applications",
    ],
    "Bachelor's degree": [
        "Bachelor's degree",
        "Bachelor degree",
    ],
    "Master's degree": [
        "Master's degree",
        "Master degree",
    ],
    "PhD": [
        "PhD",
        "Ph.D.",
        "Doctor of Philosophy",
    ],
}


PREFERRED_INDICATORS = [
    "preferred",
    "preferably",
    "desirable",
    "ideally",
    "nice to have",
    "good to have",
    "would be an advantage",
]


def normalize_apostrophes(text: str) -> str:
    """Normalize common apostrophe variations."""

    return (
        text.replace("’", "'")
        .replace("‘", "'")
        .replace("`", "'")
    )


def normalize_heading(line: str) -> str:
    """Normalize Markdown, numbered and bullet-style headings."""

    line = line.strip()

    line = re.sub(r"^#+\s*", "", line)
    line = re.sub(r"^\s*[-*•]\s*", "", line)
    line = re.sub(r"^\s*\d+[.)]\s*", "", line)

    line = line.replace("**", "").replace("__", "")
    line = line.replace("*", "").replace("_", "")

    return line.strip().lower().rstrip(":").strip()


def identify_heading(line: str):
    """Identify a recognized heading and optional inline content."""

    normalized = normalize_heading(line)

    for heading in sorted(ALL_HEADINGS, key=len, reverse=True):

        if normalized == heading:
            return heading, ""

        if normalized.startswith(heading):

            remaining = normalized[len(heading):]

            if remaining and remaining[0] in ":–—-":

                original = line.strip()
                original = re.sub(r"^#+\s*", "", original)
                original = re.sub(r"^\s*[-*•]\s*", "", original)
                original = original.replace("**", "").replace("__", "")
                original = original.replace("*", "").replace("_", "")

                content = original[len(heading):]
                content = re.sub(
                    r"^\s*[:–—-]\s*",
                    "",
                    content
                )

                return heading, content.strip()

    return None, None


def extract_section(text: str, headings: list) -> str:
    """Extract text belonging to one or more recognized sections."""

    lines = text.splitlines()

    target_headings = {
        heading.lower() for heading in headings
    }

    capturing = False
    section_lines = []

    for line in lines:

        heading, inline_content = identify_heading(line)

        if heading is not None:

            if heading in target_headings:
                capturing = True

                if inline_content:
                    section_lines.append(inline_content)

                continue

            if capturing:
                break

            continue

        if capturing:
            section_lines.append(line)

    return "\n".join(section_lines).strip()


def remove_duplicate_skills(
    required_skills: dict,
    preferred_skills: dict,
) -> dict:
    """Remove skills already included in required skills."""

    required_names = {
        skill.casefold()
        for skills in required_skills.values()
        for skill in skills
    }

    filtered = {}

    for category, skills in preferred_skills.items():

        remaining = [
            skill for skill in skills
            if skill.casefold() not in required_names
        ]

        if remaining:
            filtered[category] = remaining

    return filtered


def extract_min_experience(text: str):
    """Extract the minimum required experience in years."""

    patterns = [
        (
            r"(?:minimum|at least|required)\s+(?:of\s+)?"
            r"(\d+(?:\.\d+)?)\s*(years?|yrs?)"
        ),
        (
            r"(\d+(?:\.\d+)?)\s*\+\s*(years?|yrs?)"
        ),
        (
            r"(\d+(?:\.\d+)?)\s*(?:-|–|—|to)\s*"
            r"\d+(?:\.\d+)?\s*(years?|yrs?)"
        ),
        (
            r"(\d+(?:\.\d+)?)\s*(years?|yrs?)"
            r"\s+(?:of\s+)?experience"
            r"(?:\s+(?:required|minimum|needed))?"
        ),
        (
            r"(\d+)\s*(months?|mos?)"
            r"\s+(?:of\s+)?experience"
        ),
    ]

    for pattern in patterns:

        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            value = float(match.group(1))
            unit = match.group(2).lower()

            if unit.startswith(("month", "mo")):
                return round(value / 12, 2)

            return value

    return None



def extract_qualifications(text: str) -> list:
    """Extract degree names regardless of capitalization or wording."""

    if not isinstance(text, str) or not text.strip():
        return []

    normalized_text = (
        text.replace("’", "'")
        .replace("‘", "'")
        .replace("`", "'")
    )

    found = []

    # Recognize common degree descriptions.
    degree_patterns = {
        "Bachelor's degree": [
            r"\bbachelor(?:'s)?\s+degree\b",
            r"\bbachelor\s+(?:in|of)\s+[a-z][a-z\s&-]*",
        ],
        "Master's degree": [
            r"\bmaster(?:'s)?\s+degree\b",
            r"\bmaster\s+(?:in|of)\s+[a-z][a-z\s&-]*",
        ],
    }

    for canonical_name, patterns in degree_patterns.items():
        if any(
            re.search(pattern, normalized_text, re.IGNORECASE)
            for pattern in patterns
        ):
            found.append(canonical_name)

    # Recognize specific degree abbreviations and their aliases.
    for canonical_name, aliases in QUALIFICATION_ALIASES.items():

        for alias in aliases:

            pattern = (
                r"(?<![A-Za-z0-9])"
                + re.escape(alias)
                + r"(?![A-Za-z0-9])"
            )

            if re.search(
                pattern,
                normalized_text,
                re.IGNORECASE
            ):
                found.append(canonical_name)
                break

    return list(dict.fromkeys(found))



def classify_qualifications(
    required_text: str,
    preferred_text: str,
):
    """Separate required and preferred qualifications."""

    required = []
    preferred = []

    for line in required_text.splitlines():

        qualifications = extract_qualifications(line)

        if not qualifications:
            continue

        normalized = normalize_apostrophes(line).casefold()

        is_preferred = any(
            indicator in normalized
            for indicator in PREFERRED_INDICATORS
        )

        target = preferred if is_preferred else required
        target.extend(qualifications)

    for line in preferred_text.splitlines():
        preferred.extend(extract_qualifications(line))

    required = list(dict.fromkeys(required))
    preferred = list(dict.fromkeys(preferred))

    required_set = {
        item.casefold() for item in required
    }

    preferred = [
        item for item in preferred
        if item.casefold() not in required_set
    ]

    return required, preferred


def parse_job_description(jd_text: str) -> dict:
    """Parse a complete job description into structured data."""

    if not isinstance(jd_text, str):
        raise TypeError("Job description must be a string.")

    cleaned_jd = clean_text(jd_text)

    if not cleaned_jd:
        raise ValueError("Job description cannot be empty.")

    required_text = extract_section(
        cleaned_jd,
        REQUIRED_HEADINGS,
    )

    preferred_text = extract_section(
        cleaned_jd,
        PREFERRED_HEADINGS,
    )

    required_skills = extract_skills(required_text)
    preferred_skills = extract_skills(preferred_text)

    preferred_skills = remove_duplicate_skills(
        required_skills,
        preferred_skills,
    )

    required_qualification_text = extract_section(
        cleaned_jd,
        REQUIRED_QUALIFICATION_HEADINGS,
    )

    preferred_qualification_text = extract_section(
        cleaned_jd,
        PREFERRED_QUALIFICATION_HEADINGS,
    )

    required_qualifications, preferred_qualifications = (
        classify_qualifications(
            required_qualification_text,
            preferred_qualification_text,
        )
    )

    # Fallback: search the complete JD if the education
    # headings did not produce any recognized degrees.
    if not required_qualifications and not preferred_qualifications:

        for line in cleaned_jd.splitlines():

            qualifications = extract_qualifications(line)

            if not qualifications:
                continue

            normalized = normalize_apostrophes(line).casefold()

            is_preferred = any(
                indicator in normalized
                for indicator in PREFERRED_INDICATORS
            )

            target = (
                preferred_qualifications
                if is_preferred
                else required_qualifications
            )

            target.extend(qualifications)

        required_qualifications = list(
            dict.fromkeys(required_qualifications)
        )

        preferred_qualifications = list(
            dict.fromkeys(preferred_qualifications)
        )

        required_set = {
            item.casefold()
            for item in required_qualifications
        }

        preferred_qualifications = [
            item for item in preferred_qualifications
            if item.casefold() not in required_set
        ]

    all_skills = extract_skills(cleaned_jd)

    return {
        "job_description": cleaned_jd,
        "required_skills": required_skills,
        "preferred_skills": preferred_skills,
        "all_skills": all_skills,
        "minimum_experience_years": extract_min_experience(
            cleaned_jd
        ),
        "qualifications": required_qualifications,
        "preferred_qualifications": preferred_qualifications,
    }
