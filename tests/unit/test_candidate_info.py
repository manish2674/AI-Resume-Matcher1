
from core.candidate_info import extract_candidate_info


sample_resume = """
Rahul Sharma
rahul.sharma@example.com
+91 98765 43210

PROFESSIONAL SUMMARY

Python developer with experience in Machine Learning,
Pandas, NumPy and Scikit-learn.
"""

result = extract_candidate_info(sample_resume)

print("Candidate Information:")

for key, value in result.items():
    print(f"{key}: {value}")
