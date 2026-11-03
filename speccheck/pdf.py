"""Reads text from a PDF."""
from io import BytesIO

from pypdf import PdfReader

MAX_CHARACTERS = 80_000


class SpecFileError(ValueError):
    """The spec file cannot be used."""


def read_pdf(data: bytes) -> str:
    try:
        reader = PdfReader(BytesIO(data))
        pages = [(page.extract_text() or "").strip() for page in reader.pages]
    except Exception as error:
        raise SpecFileError("I could not read this PDF. It may be damaged or password protected.") from error
    text = "\n\n".join(p for p in pages if p)
    if not text:
        raise SpecFileError("This PDF has no readable text. It may be a scan.")
    if len(text) > MAX_CHARACTERS:
        raise SpecFileError(f"This spec is too long. The limit is {MAX_CHARACTERS:,} characters.")
    return text
