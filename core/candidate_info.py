import re


EMAIL_PATTERN = re.compile(
    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
)

PHONE_PATTERN = re.compile(
    r"(?<!\w)\+?\d[\d\s().-]{5,}\d(?!\w)"
)

SKIP_NAME_LINES = {
    "resume",
    "curriculum vitae",
    "cv",
    "profile",
    "contact",
    "contact information",
    "professional summary",
    "summary",
    "about me",
    "work experience",
    "professional experience",
    "education",
    "skills",
}


def extract_email(text: str):
    match = EMAIL_PATTERN.search(text)
    return match.group().strip() if match else None


def extract_phone(text: str):
    matches = PHONE_PATTERN.finditer(text)

    for match in matches:
        phone = match.group().strip()

        digits = re.sub(r"\D", "", phone)

        # Standard international phone number length
        if not 7 <= len(digits) <= 15:
            continue

        # Avoid interpreting simple numeric date ranges as phone numbers
        if re.fullmatch(r"\d{4}\s*[-–—]\s*\d{4}", phone):
            continue

        return phone

    return None


def extract_name(text: str):
    """
    Heuristic name extraction from the first few non-empty lines.
    """

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    for line in lines[:8]:

        # Extract the first section before common contact separators
        line = re.split(r"[|•]", line)[0].strip()

        if line.casefold() in SKIP_NAME_LINES:
            continue

        if EMAIL_PATTERN.search(line):
            continue

        if PHONE_PATTERN.search(line):
            continue

        if re.search(
            r"https?://|www\.|linkedin|github|portfolio",
            line,
            re.IGNORECASE
        ):
            continue

        words = line.split()

        if not 2 <= len(words) <= 4:
            continue

        # Support Unicode letters, hyphens and apostrophes
        valid_name = all(
            all(
                character.isalpha() or character in {"-", "'", "’"}
                for character in word
            )
            and any(character.isalpha() for character in word)
            for word in words
        )

        if valid_name:
            return line

    return None


def extract_candidate_info(text: str) -> dict:

    if not isinstance(text, str):
        raise TypeError("Input must be a string.")

    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
    }
