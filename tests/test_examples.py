from pathlib import Path

from pypdf import PdfReader

EXAMPLES = Path(__file__).parent.parent / "data" / "examples"


def test_example_pdfs_have_text_and_values():
    files = sorted(EXAMPLES.glob("*.pdf"))
    assert len(files) == 5
    for f in files:
        text = " ".join(page.extract_text() for page in PdfReader(f).pages)
        assert "shall" in text and "Example for testing only" in text
        assert any(unit in text for unit in (" kV", " kVA", " A"))


def test_example_requirements_quote_the_pdf():
    import json
    import re

    from speccheck.pdf import read_pdf

    for f in sorted(EXAMPLES.glob("*.requirements.json")):
        text = re.sub(r"\s+", " ", read_pdf((EXAMPLES / f.name.replace(".requirements.json", ".pdf")).read_bytes()))
        for r in json.loads(f.read_text())["requirements"]:
            assert r["source_quote"] in text, (f.name, r["source_quote"])


def test_original_pdfs_are_kept_for_download():
    originals = Path(__file__).parent.parent / "data" / "originals"
    assert len(list(originals.glob("*.pdf"))) == 5
