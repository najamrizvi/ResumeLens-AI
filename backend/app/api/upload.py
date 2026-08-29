from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile
from pypdf import PdfReader
from docx import Document


# ============================================================
# ROUTER
# ============================================================

router = APIRouter(
    prefix="/api",
    tags=["Resume Upload"],
)


# ============================================================
# CONFIGURATION
# ============================================================

ALLOWED_EXTENSIONS = {
    ".pdf",
    ".docx",
}

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB


# ============================================================
# TEXT EXTRACTION
# ============================================================

def extract_pdf_text(file_path: Path) -> str:
    """
    Extract text from a PDF file.
    """

    reader = PdfReader(str(file_path))

    pages = []

    for page in reader.pages:
        text = page.extract_text()

        if text:
            pages.append(text)

    return "\n".join(pages).strip()


def extract_docx_text(file_path: Path) -> str:
    """
    Extract text from a DOCX file.
    """

    document = Document(str(file_path))

    paragraphs = []

    for paragraph in document.paragraphs:
        text = paragraph.text.strip()

        if text:
            paragraphs.append(text)

    return "\n".join(paragraphs).strip()


# ============================================================
# UPLOAD ENDPOINT
# ============================================================

@router.post("/upload-resume")
async def upload_resume(
    file: UploadFile = File(...),
):
    """
    Upload a resume in PDF or DOCX format.

    The endpoint:
    1. Validates the file type.
    2. Validates the file size.
    3. Temporarily saves the file.
    4. Extracts resume text.
    5. Returns the extracted text.
    """

    # --------------------------------------------------------
    # 1. Validate filename
    # --------------------------------------------------------

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file was provided.",
        )

    original_filename = Path(file.filename).name
    extension = Path(original_filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type. Please upload a PDF or DOCX resume.",
        )

    # --------------------------------------------------------
    # 2. Read uploaded file
    # --------------------------------------------------------

    contents = await file.read()

    if not contents:
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is empty.",
        )

    # --------------------------------------------------------
    # 3. Validate file size
    # --------------------------------------------------------

    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="File is too large. Maximum allowed size is 5 MB.",
        )

    # --------------------------------------------------------
    # 4. Create temporary upload directory
    # --------------------------------------------------------

    base_dir = Path(__file__).resolve().parents[3]

    upload_dir = base_dir / "data" / "uploads"

    upload_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    # --------------------------------------------------------
    # 5. Generate safe temporary filename
    # --------------------------------------------------------

    import uuid

    stored_filename = (
        f"{uuid.uuid4().hex}{extension}"
    )

    file_path = upload_dir / stored_filename

    # --------------------------------------------------------
    # 6. Save file
    # --------------------------------------------------------

    try:

        file_path.write_bytes(contents)

        # ----------------------------------------------------
        # 7. Extract text
        # ----------------------------------------------------

        if extension == ".pdf":

            extracted_text = extract_pdf_text(
                file_path
            )

        elif extension == ".docx":

            extracted_text = extract_docx_text(
                file_path
            )

        else:
            extracted_text = ""

    except Exception as exc:

        if file_path.exists():
            file_path.unlink()

        raise HTTPException(
            status_code=500,
            detail=f"Resume extraction failed: {str(exc)}",
        )

    # --------------------------------------------------------
    # 8. Validate extracted text
    # --------------------------------------------------------

    if not extracted_text:

        if file_path.exists():
            file_path.unlink()

        raise HTTPException(
            status_code=422,
            detail=(
                "No readable text was found in the resume. "
                "Please upload a text-based PDF or DOCX file."
            ),
        )

    if len(extracted_text.strip()) < 20:

        if file_path.exists():
            file_path.unlink()

        raise HTTPException(
            status_code=422,
            detail=(
                "The extracted resume content is too short. "
                "Please upload a valid resume."
            ),
        )

    # --------------------------------------------------------
    # 9. Return resume information
    # --------------------------------------------------------

    return {
        "message": "Resume uploaded and processed successfully.",
        "filename": original_filename,
        "stored_filename": stored_filename,
        "file_type": extension.replace(".", "").upper(),
        "file_size": len(contents),
        "character_count": len(extracted_text),
        "resume_text": extracted_text,
    }