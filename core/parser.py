
from io import BytesIO

import pymupdf
from docx import Document


def extract_pdf_text(file_bytes: bytes) -> str:
    """Extract text from PDF files."""

    extracted_pages = []

    with pymupdf.open(
        stream=file_bytes,
        filetype="pdf"
    ) as pdf:

        for page in pdf:
            page_text = page.get_text("text")
            extracted_pages.append(page_text)

    return "\n".join(extracted_pages)


def extract_docx_text(file_bytes: bytes) -> str:
    """Extract text from DOCX files."""

    document = Document(BytesIO(file_bytes))

    extracted_content = []

    # Extract paragraphs
    for paragraph in document.paragraphs:
        if paragraph.text.strip():
            extracted_content.append(paragraph.text.strip())

    # Extract tables
    for table in document.tables:
        for row in table.rows:
            for cell in row.cells:
                if cell.text.strip():
                    extracted_content.append(cell.text.strip())

    return "\n".join(extracted_content)


def extract_text(filename: str, file_bytes: bytes) -> str:
    """Identify file type and extract its text."""

    extension = filename.lower().rsplit(".", 1)[-1]

    if extension == "pdf":
        text = extract_pdf_text(file_bytes)

    elif extension == "docx":
        text = extract_docx_text(file_bytes)

    else:
        raise ValueError("Only PDF and DOCX files are supported.")

    if not text.strip():
        raise ValueError(
            "No text extracted. The document may be scanned or empty."
        )

    return text.strip()
