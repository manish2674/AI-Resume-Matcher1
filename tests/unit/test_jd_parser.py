
from core.jd_parser import parse_job_description


sample_jd = """
Job Title: Machine Learning Engineer

Job Description:
We are looking for a Python developer with experience
in Machine Learning and Deep Learning.

Required Skills:
Python
Machine Learning
Pandas
NumPy
Scikit-learn
SQL

Preferred Skills:
TensorFlow
PyTorch
Docker
AWS

Experience:
Minimum 2 years of experience.

Qualifications:
B.Tech or Bachelor's degree in Computer Science.
"""

result = parse_job_description(sample_jd)


print("\n REQUIRED SKILLS ")

for category, skills in result["required_skills"].items():
    print(category, ":", skills)


print("\n PREFERRED SKILLS ")

for category, skills in result["preferred_skills"].items():
    print(category, ":", skills)


print("\n ALL SKILLS")

for category, skills in result["all_skills"].items():
    print(category, ":", skills)


print("\n EXPERIENCE ")
print(result["minimum_experience_years"], "years")


print("\n QUALIFICATIONS")
print(result["qualifications"])
