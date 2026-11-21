
from core.jd_parser import parse_job_description


jd = """
# Machine Learning Engineer

**Job Type:** Full-time
**Experience:** Minimum 2 years

## Required Skills
- Python programming
- Machine Learning
- Pandas
- NumPy
- Scikit-learn
- SQL
- Deep Learning
- Data preprocessing and feature engineering
- Model evaluation and hyperparameter tuning

## Preferred Skills
- TensorFlow
- PyTorch
- Natural Language Processing (NLP)
- Computer Vision
- Docker
- AWS
- FastAPI
- Flask

## Experience Requirements
- Minimum 2 years of relevant experience.

## Educational Qualifications
- Bachelor's degree in Computer Science, Information Technology, Data Science, or a related technical field.
- Master's degree in Machine Learning, Artificial Intelligence, or Data Science is preferred.
"""

result = parse_job_description(jd)

print("\nREQUIRED SKILLS")
print(result["required_skills"])

print("\nPREFERRED SKILLS")
print(result["preferred_skills"])

print("\nMINIMUM EXPERIENCE")
print(result["minimum_experience_years"])

print("\nREQUIRED QUALIFICATIONS")
print(result["qualifications"])

print("\nPREFERRED QUALIFICATIONS")
print(result["preferred_qualifications"])
