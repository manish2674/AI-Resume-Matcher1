
from pathlib import Path

from core.parser import extract_text


SAMPLE_DIR = Path("sample_data")

for file_path in SAMPLE_DIR.iterdir():

    if file_path.suffix.lower() not in [".pdf", ".docx"]:
        continue

    print("\n" + "=" * 60)
    print(f"Processing: {file_path.name}")
    print("=" * 60)

    try:
        file_bytes = file_path.read_bytes()

        extracted_text = extract_text(
            file_path.name,
            file_bytes
        )

        print("Status: SUCCESS")
        print("Characters extracted:", len(extracted_text))
        print("\nExtracted text preview:\n")
        print(extracted_text[:1000])

    except Exception as error:
        print("Status: FAILED")
        print("Error:", error)
