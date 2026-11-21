
from pathlib import Path

from core.resume_processor import process_resume


# Select one resume from sample_data
resume_path = Path("sample_data/Resume_sample.pdf")

# Read the file as bytes
file_bytes = resume_path.read_bytes()

# Process the complete resume
result = process_resume(
    filename=resume_path.name,
    file_bytes=file_bytes
)

print("\n========== CANDIDATE INFORMATION ==========")
print(result["candidate_info"])

print("\n========== EXTRACTED SKILLS ==========")

for category, skills in result["skills"].items():
    print(f"\n{category}:")
    for skill in skills:
        print("-", skill)

print("\n========== EXPERIENCE ==========")
print(result["experience"])

print("\n========== RESUME TEXT PREVIEW ==========")
print(result["resume_text"][:500])
