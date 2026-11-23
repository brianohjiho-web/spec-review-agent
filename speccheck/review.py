"""Turns requirements into a ranked review and a CSV export."""
import csv
from io import StringIO

from .catalog import by_type
from .checks import RULES, check_product, rank_products
from .models import ProductCheck, Review, SpecRequirements


def build_review(spec: SpecRequirements, catalog: list[dict], spec_text: str | None = None, **details) -> Review:
    checks = [check_product(spec.requirements, p, spec_text) for p in by_type(catalog, spec.equipment_type)]
    ranked = rank_products(checks)
    best = ranked[0] if ranked else None
    # Python picks the product. A product with a mandatory failure is never recommended.
    recommended = best.product_id if best and best.mandatory_fails == 0 else None
    return Review(equipment_type=spec.equipment_type, ranked=ranked, recommended_id=recommended,
                  document_name=spec.document_name, **details)


def _safe_cell(value: str) -> str:
    """Stop spreadsheet apps from running spec text as a formula."""
    return f"'{value}" if value[:1] in ("=", "+", "-", "@", "\t", "\r") else value


def to_csv(check: ProductCheck) -> str:
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "Section", "Item", "Mandatory", "Required", "Product", "Status", "Note", "Source quote"])
    for r in check.results:
        req = r.requirement
        rule = RULES.get(req.parameter)
        label = rule.label if rule else "Other"
        row = [req.id, req.section, label, "Yes" if req.mandatory else "No", r.required,
               r.product_value, r.status, r.note, req.source_quote]
        writer.writerow([_safe_cell(str(cell)) for cell in row])
    return output.getvalue()


def to_pdf(check: ProductCheck, document_name: str | None = None) -> bytes:
    """Compliance list as a one-table PDF to send to a customer or engineer."""
    from datetime import date
    from io import BytesIO
    from xml.sax.saxutils import escape

    from reportlab.lib import colors
    from reportlab.lib.pagesizes import landscape, letter
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

    buf = BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=landscape(letter), leftMargin=40, rightMargin=40,
                            topMargin=36, bottomMargin=36, title=f"Compliance list: {check.product_name}")
    cell = ParagraphStyle("cell", fontName="Courier", fontSize=7.5, leading=9.5)
    quote = ParagraphStyle("quote", parent=cell, fontName="Courier-Oblique")
    color = {"PASS": "#1f7a3d", "FAIL": "#b22222", "REVIEW": "#a06e00"}
    p = lambda s, st=cell: Paragraph(escape(str(s or "")), st)

    counts = {s: sum(r.status == s for r in check.results) for s in color}
    head = ["#", "Requirement", "Spec needs", "Product has", "Result", "Why", "Section", "Spec wording"]
    rows = [head]
    for i, r in enumerate(check.results, 1):
        rule = RULES.get(r.requirement.parameter)
        rows.append([str(i), p(rule.label if rule else "Other"), p(r.required), p(r.product_value),
                     Paragraph(f'<font color="{color[r.status]}"><b>{r.status.upper()}</b></font>', cell),
                     p(r.note if r.status != "PASS" else ""), p(r.requirement.section), p(r.requirement.source_quote, quote)])
    table = Table(rows, colWidths=[22, 92, 90, 90, 48, 140, 50, 180], repeatRows=1)
    table.setStyle(TableStyle([
        ("LINEBELOW", (0, 0), (-1, 0), 0.8, colors.black),
        
        ("FONTNAME", (0, 0), (-1, 0), "Courier-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 7.5),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ALIGN", (0, 1), (0, -1), "RIGHT"),
        ("LINEBELOW", (0, 1), (-1, -1), 0.25, colors.HexColor("#999999")),
    ]))
    title = ParagraphStyle("t", fontName="Courier-Bold", fontSize=11, leading=14)
    sub = ParagraphStyle("s", fontName="Courier", fontSize=9, leading=12)
    lines = [escape(check.product_name)]
    if document_name:
        lines.append("Spec: " + escape(document_name))
    lines.append(f"{date.today():%b %d, %Y} &nbsp;·&nbsp; {counts['PASS']} pass, {counts['FAIL']} fail, {counts['REVIEW']} to check")
    def page(canvas, d):
        canvas.saveState()
        canvas.setFont("Courier", 9)
        canvas.drawRightString(d.pagesize[0] - 40, d.pagesize[1] - 24, f"{date.today():%m-%d-%y}")
        canvas.drawCentredString(d.pagesize[0] / 2, 20, f"Compliance list- {d.page}")
        canvas.restoreState()

    story = [Paragraph("COMPLIANCE LIST", title), Spacer(1, 4), Paragraph("<br/>".join(lines), sub), Spacer(1, 10), table]
    doc.build(story, onFirstPage=page, onLaterPages=page)
    return buf.getvalue()
