from io import BytesIO
from pathlib import Path

from docx import Document
from pypdf import PdfReader


ALLOWED_EXTENSIONS = {".pdf", ".docx"}


def extract_text_from_file(
    file_bytes: bytes,
    filename: str,
) -> str:
    """
    Extract text from a PDF or DOCX resume.

    Args:
        file_bytes: Uploaded file content.
        filename: Original filename.

    Returns:
        Extracted and cleaned text.
    """

    extension = Path(filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError(
            "Unsupported file type. Please upload a PDF or DOCX file."
        )

    if not file_bytes:
        raise ValueError(
            "Uploaded file is empty."
        )

    # ---------------------------------------------------------
    # PDF
    # ---------------------------------------------------------

    if extension == ".pdf":
        reader = PdfReader(
            BytesIO(file_bytes)
        )

        extracted_parts = []

        for page in reader.pages:
            text = page.extract_text()

            if text:
                extracted_parts.append(text)

        extracted_text = "\n".join(
            extracted_parts
        )

    # ---------------------------------------------------------
    # DOCX
    # ---------------------------------------------------------

    else:
        document = Document(
            BytesIO(file_bytes)
        )

        extracted_parts = []

        for paragraph in document.paragraphs:
            if paragraph.text.strip():
                extracted_parts.append(
                    paragraph.text
                )

        extracted_text = "\n".join(
            extracted_parts
        )

    # ---------------------------------------------------------
    # Clean extracted text
    # ---------------------------------------------------------

    cleaned_text = "\n".join(
        line.strip()
        for line in extracted_text.splitlines()
        if line.strip()
    ).strip()

    if not cleaned_text:
        raise ValueError(
            "Could not extract readable text from the uploaded resume."
        )

    return cleaned_text