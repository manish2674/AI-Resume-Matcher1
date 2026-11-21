
from pathlib import Path
from core.matching_pipeline import run_matching_pipeline

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

sample_folder = Path("sample_data/synthetic_resumes")
resume_files = []

for file_path in sample_folder.iterdir():
    if file_path.suffix.lower() in [".pdf", ".docx"]:
        resume_files.append((file_path.name, file_path.read_bytes()))

print("Total resumes loaded:", len(resume_files))

results = run_matching_pipeline(sample_jd, resume_files)

print("\nPipeline Results")
print("Total Resumes:", results["total_resumes"])
print("Successfully Processed:", results["successfully_processed"])
print("Failed Resumes:", results["failed_resumes"])

print("\nCandidate Rankings")

for candidate in results["ranked_candidates"]:
    print(
        f"Rank {candidate['rank']} | "
        f"{candidate['candidate_name']} | "
        f"{candidate['final_score']}%"
    )

if results["processing_errors"]:
    print("\nProcessing Errors")
    for error in results["processing_errors"]:
        print(error)
