
from core.jd_parser import parse_job_description


sample_jd = """
Job Title: Machine Learning Engineer

Required Skills:
Python, Machine Learning, Pandas, NumPy, Scikit-learn, SQL

Preferred Skills:
TensorFlow, PyTorch, Docker, AWS

Experience:
Minimum 2 years of experience in Machine Learning.

Education:
B.Tech in Computer Science or related field.

Responsibilities:
Develop machine learning models, perform data analysis,
build predictive systems, and work with AI technologies.
"""

result = parse_job_description(sample_jd)

print("\nREQUIRED SKILLS")
print(result["required_skills"])

print("\nPREFERRED SKILLS")
print(result["preferred_skills"])

print("\nALL SKILLS")
print(result["all_skills"])

print("\nMINIMUM EXPERIENCE")
print(result["minimum_experience_years"])

print("\nQUALIFICATIONS")
print(result["qualifications"])
