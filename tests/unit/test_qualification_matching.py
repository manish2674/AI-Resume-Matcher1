
from core.jd_parser import parse_job_description
from core.scoring_engine import calculate_qualification_score


sample_jd = """
Job Title: Machine Learning Engineer

Required Skills:
Python, Machine Learning, Pandas

Preferred Skills:
TensorFlow, PyTorch

Experience:
Minimum 2 years.

Education:
B.Tech in Computer Science or related field.
"""

jd_data = parse_job_description(sample_jd)

test_candidates = [
    {
        "name": "Aarav Mehta",
        "resume_text": "Education: B.Tech in Computer Science."
    },
    {
        "name": "Meera Kapoor",
        "resume_text": "Education: M.Tech in Data Science."
    },
    {
        "name": "Vivaan Desai",
        "resume_text": "Education: B.E. in Computer Engineering."
    },
    {
        "name": "Sana Khan",
        "resume_text": "Education: BCA."
    },
    {
        "name": "Aditya Rao",
        "resume_text": "Education: B.Com in Finance."
    },
]

for candidate in test_candidates:

    resume_data = {
        "resume_text": candidate["resume_text"]
    }

    result = calculate_qualification_score(
        jd_data,
        resume_data
    )

    print("\nCandidate:", candidate["name"])
    print("Score:", result["score"])
    print("Matched:", result["matched"])
    print("Reason:", result["match_reason"])
