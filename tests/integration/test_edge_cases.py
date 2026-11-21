
from io import BytesIO

import pymupdf
from docx import Document

from core.matching_pipeline import run_matching_pipeline


def create_docx(text: str) -> bytes:
    """Create a DOCX file in memory from plain text."""
    document = Document()

    for line in text.splitlines():
        document.add_paragraph(line)

    buffer = BytesIO()
    document.save(buffer)
    return buffer.getvalue()


def create_pdf(text: str) -> bytes:
    """Create a text-based PDF file in memory."""
    pdf = pymupdf.open()
    page = pdf.new_page()
    page.insert_text((50, 50), text, fontsize=11)

    pdf_bytes = pdf.tobytes()
    pdf.close()

    return pdf_bytes


def build_test_resumes() -> list:
    """Build synthetic resumes covering different edge cases."""

    missing_education = """
Aarav Missing
aarav@example.com

Professional Summary
Python developer with machine learning knowledge.

Work Experience
Total Experience: 3 years

Technical Skills
Python, Machine Learning, Pandas, NumPy
"""

    missing_experience = """
Meera Fresher
meera@example.com

Professional Summary
Computer Science graduate interested in machine learning.

Technical Skills
Python, Machine Learning, Pandas, NumPy

Education
B.Tech in Computer Science
"""

    missing_contact = """
Kabir Contact
Professional Summary
Machine learning developer with three years of experience.

Work Experience
Total Experience: 3 years

Technical Skills
Python, Machine Learning, Pandas, NumPy

Education
B.Tech in Information Technology
"""

    unrelated_degree = """
Rohan Commerce
rohan@example.com

Professional Summary
Python developer with machine learning experience.

Work Experience
Total Experience: 3 years

Technical Skills
Python, Machine Learning, Pandas, NumPy

Education
B.Com in Finance
"""

    valid_pdf_text = """
Ishita PDF
ishita@example.com

Professional Summary
Machine learning engineer.

Work Experience
Total Experience: 4 years

Technical Skills
Python, Machine Learning, Pandas, NumPy

Education
B.Tech in Computer Science
"""

    empty_pdf = pymupdf.open()
    empty_pdf.new_page()
    empty_pdf_bytes = empty_pdf.tobytes()
    empty_pdf.close()

    corrupted_pdf = b"This is not a valid PDF file."

    return [
        ("missing_education.docx", create_docx(missing_education)),
        ("missing_experience.docx", create_docx(missing_experience)),
        ("missing_contact.docx", create_docx(missing_contact)),
        ("unrelated_degree.docx", create_docx(unrelated_degree)),
        ("valid_resume.pdf", create_pdf(valid_pdf_text)),
        ("empty_resume.pdf", empty_pdf_bytes),
        ("corrupted_resume.pdf", corrupted_pdf),
    ]


def main():
    job_description = """
Job Title: Machine Learning Engineer

Required Skills:
Python, Machine Learning, Pandas, NumPy

Minimum Experience:
2 years

Required Qualifications:
B.Tech in Computer Science, IT or related technical field
"""

    resume_files = build_test_resumes()

    print("Running edge-case integration tests...")

    result = run_matching_pipeline(
        job_description,
        resume_files,
    )

    print("\nPIPELINE SUMMARY")
    print("----------------")
    print("Total resumes:", result["total_resumes"])
    print("Successfully processed:", result["successfully_processed"])
    print("Failed resumes:", result["failed_resumes"])

    candidates = {
        candidate["filename"]: candidate
        for candidate in result["ranked_candidates"]
    }

    print("\nVALID RESUME CHECKS")
    print("-------------------")

    expected_valid = [
        "missing_education.docx",
        "missing_experience.docx",
        "missing_contact.docx",
        "unrelated_degree.docx",
        "valid_resume.pdf",
    ]

    for filename in expected_valid:
        assert filename in candidates, (
            f"{filename} was not successfully processed."
        )
        print(f"PASS: {filename} processed successfully.")

    print("\nMISSING EDUCATION CHECK")
    print("-----------------------")

    candidate = candidates["missing_education.docx"]
    detected = candidate["qualifications"]["detected_qualifications"]

    print("Detected qualifications:", detected)
    assert not detected, (
        "A qualification was detected even though education was omitted."
    )
    print("PASS: No qualification was falsely detected.")

    print("\nMISSING EXPERIENCE CHECK")
    print("------------------------")

    candidate = candidates["missing_experience.docx"]
    experience = candidate["experience"]

    print("Extracted experience:", experience["total_experience_years"])
    assert experience["total_experience_years"] is None, (
        "Missing experience should remain unknown."
    )
    print("PASS: Missing experience remains unknown.")

    print("\nMISSING CONTACT CHECK")
    print("---------------------")

    candidate = candidates["missing_contact.docx"]

    print("Candidate:", candidate["candidate_name"])
    print("Email:", candidate["email"])
    print("Phone:", candidate["phone"])

    assert candidate["email"] is None
    assert candidate["phone"] is None
    print("PASS: Missing contact details do not stop processing.")

    print("\nUNRELATED DEGREE CHECK")
    print("----------------------")

    candidate = candidates["unrelated_degree.docx"]
    qualifications = candidate["qualifications"]

    print(
        "Detected qualifications:",
        qualifications["detected_qualifications"],
    )
    print("Qualification status:", qualifications["status"])

    assert qualifications["score"] < 100, (
        "An unrelated degree should not receive a perfect qualification score."
    )
    print("PASS: Unrelated degree does not receive a perfect score.")

    print("\nPDF AND DOCX FORMAT CHECK")
    print("-------------------------")

    assert "valid_resume.pdf" in candidates
    assert "missing_contact.docx" in candidates
    print("PASS: Both PDF and DOCX formats were processed.")

    print("\nINVALID PDF CHECK")
    print("-----------------")

    errors = {
        error["filename"]: error["error"]
        for error in result["processing_errors"]
    }

    assert "empty_resume.pdf" in errors
    assert "corrupted_resume.pdf" in errors

    for filename, error in errors.items():
        print(f"EXPECTED FAILURE: {filename}")
        print("Reason:", error)

    print("\nALL EDGE-CASE CHECKS PASSED.")


if __name__ == "__main__":
    main()
