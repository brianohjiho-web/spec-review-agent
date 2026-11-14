from io import BytesIO

import pytest
from reportlab.pdfgen import canvas

from speccheck import pdf
from speccheck.pdf import SpecFileError, read_pdfs


def make_pdf(text: str) -> bytes:
    data = BytesIO()
    page = canvas.Canvas(data)
    page.drawString(72, 720, text)
    page.save()
    return data.getvalue()


def test_combines_several_pdfs_in_order():
    text = read_pdfs([("spec.pdf", make_pdf("Main bus shall be 2000 A.")),
                      ("addendum.pdf", make_pdf("Main bus shall now be 3000 A."))])
    assert text.index("Document 1: spec.pdf") < text.index("Document 2: addendum.pdf")
    assert "3000 A" in text


def test_one_pdf_has_no_header():
    assert "=== Document" not in read_pdfs([("spec.pdf", make_pdf("Rated 15 kV."))])


def test_bad_file_names_the_file():
    with pytest.raises(SpecFileError, match="broken.pdf"):
        read_pdfs([("good.pdf", make_pdf("Rated 15 kV.")), ("broken.pdf", b"not a pdf")])


def test_limit_applies_to_the_total(monkeypatch):
    monkeypatch.setattr(pdf, "MAX_CHARACTERS", 60)
    one = make_pdf("Rated 15 kV with a BIL of 95 kV.")
    with pytest.raises(SpecFileError, match="too long"):
        read_pdfs([("a.pdf", one), ("b.pdf", one)])


def test_no_files():
    with pytest.raises(SpecFileError):
        read_pdfs([])
