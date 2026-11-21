
from core.experience_extractor import extract_experience


sample_resume = """
Candidate has 2 years of experience in Python development.

Worked as a Data Analyst for 1 year 6 months.

Completed a 6 months internship in Machine Learning.

Total experience: 3 years.
"""

result = extract_experience(sample_resume)

print("Total Experience:", result["total_experience_years"], "years")

print("\nMentioned Durations:")

for item in result["mentioned_durations"]:
    print(
        item["duration"],
        "->",
        item["months"],
        "months"
    )
