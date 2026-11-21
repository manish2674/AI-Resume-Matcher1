
from pathlib import Path

from core.parser import extract_text
from core.text_cleaner import clean_text
from core.skill_extractor import extract_skills

SAMPLE_DIR = Path("sample_data")

for file_path in SAMPLE_DIR.iterdir():

    if file_path.suffix.lower() not in [".pdf", ".docx"]:
        continue

    print("\n" + "=" * 50)
    print("RESUME:", file_path.name)
    print("=" * 50)

    try:
        file_bytes = file_path.read_bytes()

        # Step 1: Extract text
        text = extract_text(file_path.name, file_bytes)

        # Step 2: Clean text
        cleaned_text = clean_text(text)

        # Step 3: Extract skills
        skills = extract_skills(cleaned_text)

        print("\nEXTRACTED SKILLS:")

        for category, skill_list in skills.items():
            print(f"\n{category}:")
            for skill in skill_list:
                print("-", skill)

    except Exception as error:
        print("ERROR:", error)
