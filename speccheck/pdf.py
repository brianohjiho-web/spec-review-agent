"""Reads text from one or more spec PDFs."""
from io import BytesIO

from pypdf import PdfReader

# About 100,000 words. Longer specs cost more API credits per review.
MAX_CHARACTERS = 600_000


class SpecFileError(ValueError):
    """The spec file cannot be used."""


def _too_long(text: str) -> None:
    if len(text) > MAX_CHARACTERS:
        raise SpecFileError(
            f"This spec is too long. The limit is {MAX_CHARACTERS:,} characters, about 100,000 words."
        )


def _extract(data: bytes, name: str = "this PDF") -> str:
    try:
        reader = PdfReader(BytesIO(data))
        pages = [(page.extract_text() or "").strip() for page in reader.pages]
    except Exception as error:
        raise SpecFileError(f"I could not read {name}. It may be damaged or password protected.") from error
    text = "\n\n".join(p for p in pages if p)
    if not text:
        raise SpecFileError(f"{name[0].upper() + name[1:]} has no readable text. It may be a scan.")
    return text


def read_pdf(data: bytes) -> str:
    text = _extract(data)
    _too_long(text)
    return text


def read_pdfs(files: list[tuple[str, bytes]]) -> str:
    """Combines several PDFs, like a spec and its addenda, in the order given."""
    if not files:
        raise SpecFileError("Add at least one PDF.")
    if len(files) == 1:
        return read_pdf(files[0][1])
    parts = [f"=== Document {i}: {name} ===\n{_extract(data, name)}" for i, (name, data) in enumerate(files, 1)]
    text = "\n\n".join(parts)
    _too_long(text)
    return text
