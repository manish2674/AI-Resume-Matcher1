
from core.experience_extractor import extract_experience


sample_resume = """
Rahul Sharma

Data Analyst
Jan 2021 - Dec 2022

Machine Learning Engineer
Jan 2023 - Present
"""

result = extract_experience(sample_resume)

print("Total Experience:", result["total_experience_years"], "years")

print("Experience in Months:", result["total_experience_months"])

print("Extraction Method:", result["extraction_method"])

print("Date Range Experience:", result["date_range_experience_months"])
