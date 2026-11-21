
import re
from datetime import datetime


MONTHS = {
    "jan": 1, "january": 1,
    "feb": 2, "february": 2,
    "mar": 3, "march": 3,
    "apr": 4, "april": 4,
    "may": 5,
    "jun": 6, "june": 6,
    "jul": 7, "july": 7,
    "aug": 8, "august": 8,
    "sep": 9, "sept": 9, "september": 9,
    "oct": 10, "october": 10,
    "nov": 11, "november": 11,
    "dec": 12, "december": 12,
}


EMPLOYMENT_HEADINGS = {
    "experience",
    "work experience",
    "professional experience",
    "employment history",
    "work history",
    "career history",
    "relevant experience",
}


OTHER_SECTION_HEADINGS = {
    "education",
    "academic background",
    "educational background",
    "qualifications",
    "skills",
    "technical skills",
    "projects",
    "personal projects",
    "certifications",
    "certificates",
    "achievements",
    "interests",
    "hobbies",
    "references",
    "publications",
    "professional summary",
    "summary",
    "career objective",
}


DATE_TOKEN = (
    r"(?:"
    r"(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|"
    r"Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:t|tember)?|"
    r"Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+\d{4}"
    r"|(?:0?[1-9]|1[0-2])[/-]\d{4}"
    r"|\d{4}"
    r"|present|current|now"
    r")"
)


DATE_RANGE_PATTERN = re.compile(
    rf"(?P<start>{DATE_TOKEN})\s*(?:-|–|—|to)\s*(?P<end>{DATE_TOKEN})",
    re.IGNORECASE,
)


DURATION_PATTERN = re.compile(
    r"(?:(?P<years>\d+(?:\.\d+)?)\s*(?:years?|yrs?)"
    r"(?:\s+(?P<months>\d+)\s*(?:months?|mos?))?"
    r"|(?P<months_only>\d+)\s*(?:months?|mos?))",
    re.IGNORECASE,
)


TOTAL_EXPERIENCE_PATTERN = re.compile(
    r"(?:total|overall|professional)"
    r"\s+(?:work\s+)?experience"
    r"\s*[:\-]?\s*"
    r"(?P<duration>"
    r"\d+(?:\.\d+)?\s*(?:years?|yrs?)"
    r"(?:\s+\d+\s*(?:months?|mos?))?"
    r"|"
    r"\d+\s*(?:months?|mos?)"
    r")",
    re.IGNORECASE,
)


def normalize_heading(line: str) -> str:
    """Normalize a resume section heading."""

    line = re.sub(r"^\s*[-*•]\s*", "", line)
    return line.strip().lower().rstrip(":").strip()


def extract_employment_section(text: str) -> str:
    """
    Extract the employment section.

    If no employment heading exists, use the full resume
    as a fallback. This supports resumes that list job
    titles and dates without a dedicated heading.
    """

    lines = text.splitlines()

    capturing = False
    found_employment_heading = False
    employment_lines = []

    for line in lines:
        heading = normalize_heading(line)

        if heading in EMPLOYMENT_HEADINGS:
            capturing = True
            found_employment_heading = True
            continue

        if heading in OTHER_SECTION_HEADINGS:
            if capturing:
                break
            continue

        if capturing:
            employment_lines.append(line)

    if not found_employment_heading:
        return text

    return "\n".join(employment_lines)


def duration_to_months(duration_text: str) -> int:
    """Convert a duration such as 2 years 6 months into months."""

    match = DURATION_PATTERN.search(duration_text)

    if not match:
        return 0

    if match.group("months_only"):
        return int(match.group("months_only"))

    years = float(match.group("years") or 0)
    months = int(match.group("months") or 0)

    return round(years * 12) + months


def parse_date_to_month(date_text: str, is_end: bool = False):
    """
    Convert a date into a continuous month index.

    Supports:
    Jan 2022
    January 2022
    01/2022
    2022
    Present
    """

    date_text = date_text.strip().lower()

    today = datetime.now()
    current_month_index = today.year * 12 + today.month - 1

    if date_text in {"present", "current", "now"}:
        return current_month_index

    if date_text.isdigit():
        year = int(date_text)

        if year < 1900 or year > today.year:
            return None

        month = 12 if is_end else 1
        return year * 12 + month - 1

    numeric_match = re.fullmatch(
        r"(0?[1-9]|1[0-2])[/-](\d{4})",
        date_text,
    )

    if numeric_match:
        month = int(numeric_match.group(1))
        year = int(numeric_match.group(2))

        if year < 1900 or year > today.year:
            return None

        month_index = year * 12 + month - 1

        if month_index > current_month_index:
            return None

        return month_index

    month_match = re.fullmatch(
        r"([a-z]+)\s+(\d{4})",
        date_text,
    )

    if month_match:
        month_name = month_match.group(1)
        year = int(month_match.group(2))
        month = MONTHS.get(month_name)

        if not month or year < 1900 or year > today.year:
            return None

        month_index = year * 12 + month - 1

        if month_index > current_month_index:
            return None

        return month_index

    return None


def calculate_date_range_experience(text: str) -> int:
    """
    Calculate total employment months from date ranges.

    Overlapping employment periods are merged to avoid
    counting the same month more than once.
    """

    intervals = []

    for match in DATE_RANGE_PATTERN.finditer(text):
        start_month = parse_date_to_month(
            match.group("start")
        )

        end_month = parse_date_to_month(
            match.group("end"),
            is_end=True,
        )

        if start_month is None or end_month is None:
            continue

        if end_month < start_month:
            continue

        intervals.append((start_month, end_month))

    if not intervals:
        return 0

    intervals.sort()

    total_months = 0
    current_start, current_end = intervals[0]

    for start, end in intervals[1:]:
        if start <= current_end + 1:
            current_end = max(current_end, end)
        else:
            total_months += current_end - current_start + 1
            current_start, current_end = start, end

    total_months += current_end - current_start + 1

    return total_months


def extract_experience(text: str) -> dict:
    """Extract total professional experience from resume text."""

    if not isinstance(text, str):
        raise TypeError("Input must be a string.")

    if not text.strip():
        return {
            "total_experience_months": None,
            "total_experience_years": None,
            "extraction_method": None,
            "mentioned_durations": [],
            "date_range_experience_months": 0,
        }

    total_match = TOTAL_EXPERIENCE_PATTERN.search(text)

    explicit_total = None

    if total_match:
        explicit_total = duration_to_months(
            total_match.group("duration")
        )

    employment_text = extract_employment_section(text)

    mentioned_durations = []

    for match in DURATION_PATTERN.finditer(employment_text):
        duration_text = match.group().strip()
        months = duration_to_months(duration_text)

        if months > 0:
            mentioned_durations.append({
                "duration": duration_text,
                "months": months,
                "years": round(months / 12, 2),
            })

    date_range_total = calculate_date_range_experience(
        employment_text
    )

    if explicit_total is not None:
        total_months = explicit_total
        extraction_method = "explicit_total"

    elif date_range_total > 0:
        total_months = date_range_total
        extraction_method = "employment_dates"

    else:
        total_months = None
        extraction_method = None

    return {
        "total_experience_months": total_months,
        "total_experience_years": (
            round(total_months / 12, 2)
            if total_months is not None
            else None
        ),
        "extraction_method": extraction_method,
        "mentioned_durations": mentioned_durations,
        "date_range_experience_months": date_range_total,
    }
