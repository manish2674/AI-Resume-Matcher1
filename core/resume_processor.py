
from core.parser import extract_text
from core.text_cleaner import clean_text
from core.candidate_info import extract_candidate_info
from core.skill_extractor import extract_skills
from core.experience_extractor import extract_experience


def process_resume(filename: str, file_bytes: bytes) -> dict:

    # 1. Extract raw text from PDF or DOCX
    raw_text = extract_text(filename, file_bytes)

    # 2. Clean extracted text
    cleaned_text = clean_text(raw_text)
    print(cleaned_text)

    # 3. Extract candidate details
    candidate_info = extract_candidate_info(cleaned_text)

    # 4. Extract skills
    skills = extract_skills(cleaned_text)

    # 5. Extract experience
    experience = extract_experience(cleaned_text)

    # 6. Combine everything into one result
    return {
        "filename": filename,
        "candidate_info": candidate_info,
        "skills": skills,
        "experience": experience,
        "resume_text": cleaned_text
    }
