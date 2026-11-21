
from pathlib import Path

from core.matching_pipeline import run_matching_pipeline
from core.report_exporter import (
    export_json_report,
    export_csv_report
)

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


def main():
    sample_folder = Path("sample_data/synthetic_resumes")

    resume_files = []

    for file_path in sample_folder.iterdir():
        if file_path.suffix.lower() in [".pdf", ".docx"]:
            resume_files.append(
                (file_path.name, file_path.read_bytes())
            )

    print("Processing resumes...")

    results = run_matching_pipeline(sample_jd, resume_files)

    json_path = export_json_report(results)
    csv_path = export_csv_report(results)

    print("\nReport Export Results")
    print("Successfully processed:", results["successfully_processed"])
    print("Failed resumes:", results["failed_resumes"])

    print("\nJSON report created:", json_path)
    print("CSV report created:", csv_path)


if __name__ == "__main__":
    main()
