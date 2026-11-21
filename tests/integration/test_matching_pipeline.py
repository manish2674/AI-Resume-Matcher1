
from pathlib import Path

from core.matching_pipeline import run_matching_pipeline


sample_jd = """
Job Title: Machine Learning Engineer

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


# Load available PDF and DOCX resumes
resume_files = []

sample_folder = Path("sample_data")

for file_path in sample_folder.iterdir():

    if file_path.suffix.lower() in [".pdf", ".docx"]:

        file_bytes = file_path.read_bytes()

        resume_files.append(
            (file_path.name, file_bytes)
        )


# Run the complete matching pipeline
results = run_matching_pipeline(
    sample_jd,
    resume_files
)


print("\nTotal Resumes:", results["total_resumes"])
print("Successfully Processed:", results["successfully_processed"])
print("Failed Resumes:", results["failed_resumes"])


print("\nRanked Candidates:")

for candidate in results["ranked_candidates"]:

    print(
        f"Rank {candidate['rank']} | "
        f"{candidate['candidate_name']} | "
        f"{candidate['final_score']}%"
    )


print("\nProcessing Errors:")

for error in results["processing_errors"]:
    print(error)
