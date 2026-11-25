"""Creates example spec PDFs for testing "Check your own spec".

Each one is a short version of a real public spec section (VA master specs and two
university design standards). The real sections are templates: values are left as
choices like "// 208 // 480 //" or "as shown on the drawings". These examples pick the
choices and add a ratings schedule, the way a real project's drawings would, so the
tool has actual values to check. They are test documents, not official specs.
"""
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

OUT = Path(__file__).parent.parent / "data" / "examples"

EXAMPLES = {
    "example_va_mv_switchgear": {
        "title": "Section 26 13 13: Medium-Voltage Circuit Breaker Switchgear",
        "project": "Example project: Hospital Central Energy Plant, 13.8 kV main switchgear",
        "source": "Based on VA master specification 26 13 13 (U.S. Department of Veterans Affairs, public).",
        "parts": [
            ("Part 1: General", [
                ("1.1 Description", ["This section specifies the furnishing, installation, connection, and testing of "
                                     "medium-voltage circuit breaker switchgear for the 13.8 kV service."]),
                ("1.2 Factory tests", ["Switchgear shall be tested with the circuit breakers in the connected position, "
                                       "in accordance with IEEE C37.09. The Owner shall witness factory tests."]),
            ]),
            ("Part 2: Products", [
                ("2.1 General requirements", [
                    "Switchgear shall be a complete, grounded, continuous-duty, integral assembly, metal clad, "
                    "dead-front, dead-rear, self-supporting, indoor type switchgear assembly.",
                    "Switchgear shall comply with IEEE C37.20.2.",
                    "Ratings shall not be less than shown in the schedule below.",
                ]),
                ("2.2 Circuit breakers", ["Circuit breakers shall be vacuum type, electrically operated, drawout."]),
                ("2.3 Seismic", ["The switchgear shall be seismic certified to the International Building Code."]),
            ]),
            ("Part 3: Delivery", [
                ("3.1 Schedule", ["Delivery shall be within 40 weeks after approval of shop drawings."]),
            ]),
        ],
        "schedule": [
            ["Rated maximum voltage", "15 kV"], ["Basic impulse level (BIL)", "110 kV"],
            ["Main bus continuous current", "2000 A"], ["Short-circuit rating", "80 kA symmetrical"],
            ["Frequency", "60 Hz"], ["Phases", "3 phase, 3 wire"], ["Enclosure", "NEMA 1, indoor"],
            ["Control power", "125 VDC"], ["Maximum lineup height", "88 in."],
        ],
    },
    "example_va_lv_switchgear": {
        "title": "Section 26 23 00: Low-Voltage Switchgear",
        "project": "Example project: Outpatient Clinic, 480 V main switchgear",
        "source": "Based on VA master specification 26 23 00 (U.S. Department of Veterans Affairs, public).",
        "parts": [
            ("Part 1: General", [
                ("1.1 Description", ["This section specifies the furnishing, installation, connection, and testing of "
                                     "low-voltage switchgear for the main 480 V distribution."]),
            ]),
            ("Part 2: Products", [
                ("2.1 General requirements", [
                    "Switchgear shall be a complete, grounded, continuous-duty, integral assembly, metal clad, "
                    "dead-front, dead-rear, self-supporting, indoor type switchgear assembly.",
                    "Switchgear shall comply with IEEE C37.20.1 and shall be listed to UL 1558.",
                    "Short circuit ratings shall not be less than 250 kA.",
                ]),
                ("2.2 Circuit breakers", [
                    "Circuit breakers shall be air type, 3 pole, 600 volts AC and below, 60 Hz, with solid state trip devices.",
                    "Main and feeder breakers shall be drawout breakers.",
                    "Trip units shall include an arc flash maintenance mode switch.",
                ]),
                ("2.3 Environment", ["Equipment shall operate at an ambient temperature of 40 C without derating."]),
            ]),
            ("Part 3: Delivery", [
                ("3.1 Schedule", ["Delivery shall be within 30 weeks after approval of shop drawings."]),
            ]),
        ],
        "schedule": [
            ["System voltage", "480 V, 3 phase, 4 wire"], ["Frequency", "60 Hz"],
            ["Main bus continuous current", "12000 A, copper"], ["Short-circuit rating", "250 kA"],
            ["Enclosure", "NEMA 1, indoor"], ["Cable entry", "bottom"],
        ],
    },
    "example_university_lv_switchgear": {
        "title": "Section 26 23 00: Low-Voltage Switchgear",
        "project": "Example project: Campus Science Building, 480/277 V double-ended switchgear",
        "source": "Based on a public university design standard, Section 26 23 00 (Northwestern University).",
        "parts": [
            ("Part 1: General", [
                ("1.1 Summary", ["This section includes metal-enclosed, drawout, low-voltage power circuit breaker "
                                 "switchgear rated 1000 V and less for use in AC systems."]),
                ("1.2 Quality assurance", ["Comply with UL 1558."]),
            ]),
            ("Part 2: Products", [
                ("2.1 Manufacturers", ["Eaton or Siemens, or equal as approved by the Owner."]),
                ("2.2 Ratings", [
                    "Nominal system voltage 480/277 V, 4 wire, 60 Hz.",
                    "Main bus continuous: 3200 A.",
                    "Short-time and short-circuit current: 250 kA.",
                ]),
                ("2.3 Fabrication", [
                    "Factory assembled and tested and complying with IEEE C37.20.1 and UL 1558.",
                    "Indoor enclosure material: steel.",
                ]),
                ("2.4 Circuit breakers", [
                    "Main and tie circuit breakers shall have a minimum 3200 A frame and shall be drawout breakers.",
                    "Trip units shall include an arc flash maintenance mode switch.",
                ]),
            ]),
        ],
        "schedule": [
            ["System voltage", "480/277 V, 3 phase, 4 wire"], ["Frequency", "60 Hz"],
            ["Main bus continuous current", "3200 A"], ["Short-circuit rating", "250 kA"],
            ["Enclosure", "NEMA 1, indoor, steel"], ["Maximum section height", "80 in."],
        ],
    },
    "example_va_ups": {
        "title": "Section 26 33 53: Static Uninterruptible Power Supply",
        "project": "Example project: Data Center Expansion, 500 kVA UPS",
        "source": "Based on VA master specification 26 33 53 (U.S. Department of Veterans Affairs, public).",
        "parts": [
            ("Part 1: General", [
                ("1.1 Description", ["This section specifies a three-phase, on-line, double-conversion static "
                                     "uninterruptible power supply (UPS) with batteries and maintenance bypass."]),
            ]),
            ("Part 2: Products", [
                ("2.1 AC input", ["Voltage 480 volts line-to-line, 3-phase, 3-wire, plus ground. Frequency: 60 Hz, plus or minus 5 percent."]),
                ("2.2 AC output", [
                    "Voltage 480 volts line-to-line, 3-phase.",
                    "Overload capability: 125 percent load for 10 minutes.",
                ]),
                ("2.3 System", [
                    "The UPS shall be listed to UL 1778.",
                    "The UPS shall be rated not less than 500 kVA and 500 kW.",
                    "Double-conversion efficiency shall be at least 99 percent at full load.",
                    "Batteries shall be VRLA and shall support full load for 10 minutes.",
                    "A maintenance bypass shall be provided.",
                    "The UPS shall be provided in a NEMA 1 enclosure.",
                ]),
            ]),
            ("Part 3: Delivery", [
                ("3.1 Schedule", ["Delivery shall be within 20 weeks after approval of shop drawings."]),
            ]),
        ],
        "schedule": [
            ["Rating", "500 kVA / 500 kW"], ["Input and output voltage", "480 V, 3 phase"],
            ["Frequency", "60 Hz"], ["Battery", "VRLA, 10 minutes at full load"],
            ["Efficiency", "99 percent minimum"], ["Enclosure", "NEMA 1, indoor"],
        ],
    },
    "example_university_ups": {
        "title": "Section 26 33 53: Static Uninterruptible Power Supply",
        "project": "Example project: Campus Network Room, 100 kVA UPS",
        "source": "Based on a public university design standard, Section 26 33 53 (Washington State University).",
        "parts": [
            ("Part 1: General", [
                ("1.1 Summary", ["This section describes a three-phase continuous duty, on-line, double conversion, "
                                 "solid-state uninterruptible power system for critical loads."]),
                ("1.2 System description", ["The UPS shall consist of the UPS module, battery cabinets, and an "
                                            "integrated maintenance bypass and distribution cabinet."]),
            ]),
            ("Part 2: Products", [
                ("2.1 Manufacturers", ["Pre-approved manufacturers: Eaton, Square D (Schneider Electric), General Electric."]),
                ("2.2 Ratings", [
                    "The UPS shall be rated 100 kVA at 600 V, 3 phase, 60 Hz.",
                    "Battery runtime shall be at least 15 minutes at full load.",
                    "The UPS shall be listed to UL 1778.",
                ]),
                ("2.3 Options", [
                    "An integrated maintenance bypass shall be provided.",
                    "Lithium-ion batteries are preferred.",
                ]),
            ]),
        ],
        "schedule": [
            ["Rating", "100 kVA"], ["Voltage", "600 V, 3 phase"], ["Frequency", "60 Hz"],
            ["Battery runtime", "15 minutes at full load"],
        ],
    },
}


def req(n, section, parameter, quote, number=None, unit="", text=None, mandatory=True):
    return dict(id=f"R{n}", section=section, parameter=parameter, source_quote=quote,
                value_number=number, unit=unit, value_text=text, mandatory=mandatory)


def numbered(kind, rows):
    return {"equipment_type": kind, "requirements": [req(i, *row) for i, row in enumerate(rows, 1)]}


S = "Schedule"
# The requirements a reader would pull out of each example, so the app can show them without calling Claude.
LABELS = {
    "example_va_mv_switchgear": numbered("mv_switchgear", [
        (S, "voltage_kv", "15 kV", 15, "kV"), (S, "bil_kv", "110 kV", 110, "kV"),
        (S, "bus_current_a", "2000 A", 2000, "A"), (S, "short_circuit_ka", "80 kA symmetrical", 80, "kA"),
        (S, "frequency_hz", "60 Hz", 60, "Hz"), (S, "phases", "3 phase, 3 wire", 3),
        (S, "control_voltage_vdc", "125 VDC", 125, "VDC"), (S, "enclosure", "NEMA 1, indoor", None, "", "NEMA 1"),
        ("2.1", "location", "indoor type switchgear assembly", None, "", "indoor"),
        ("2.1", "standards", "comply with IEEE C37.20.2", None, "", "IEEE C37.20.2"),
        ("2.2", "breaker_type", "vacuum type", None, "", "vacuum"),
        ("2.2", "features", "drawout", None, "", "drawout breakers"),
        ("2.3", "features", "seismic certified", None, "", "seismic certified"),
        (S, "height_in", "88 in.", 88, "in"), ("3.1", "lead_time_weeks", "within 40 weeks", 40, "weeks"),
    ]),
    "example_va_lv_switchgear": numbered("lv_switchgear", [
        (S, "voltage_kv", "480 V, 3 phase, 4 wire", 480, "V"), (S, "frequency_hz", "60 Hz", 60, "Hz"),
        (S, "phases", "3 phase", 3), (S, "bus_current_a", "12000 A", 12000, "A"),
        (S, "bus_material", "copper", None, "", "copper"),
        ("2.1", "short_circuit_ka", "not be less than 250 kA", 250, "kA"),
        ("2.1", "standards", "comply with IEEE C37.20.1", None, "", "IEEE C37.20.1"),
        ("2.1", "standards", "listed to UL 1558", None, "", "UL 1558"),
        ("2.1", "location", "indoor type switchgear assembly", None, "", "indoor"),
        ("2.2", "breaker_type", "air type", None, "", "air"),
        ("2.2", "features", "drawout breakers", None, "", "drawout breakers"),
        ("2.2", "features", "arc flash maintenance mode", None, "", "arc flash maintenance mode"),
        (S, "enclosure", "NEMA 1, indoor", None, "", "NEMA 1"), (S, "cable_entry", "bottom", None, "", "bottom"),
        ("2.3", "max_ambient_c", "ambient temperature of 40 C", 40, "C"),
        ("3.1", "lead_time_weeks", "within 30 weeks", 30, "weeks"),
    ]),
    "example_university_lv_switchgear": numbered("lv_switchgear", [
        ("2.2", "voltage_kv", "480/277 V", 480, "V"), ("2.2", "frequency_hz", "60 Hz", 60, "Hz"),
        (S, "phases", "3 phase, 4 wire", 3), ("2.2", "bus_current_a", "Main bus continuous: 3200 A", 3200, "A"),
        ("2.2", "short_circuit_ka", "short-circuit current: 250 kA", 250, "kA"),
        ("1.2", "standards", "Comply with UL 1558", None, "", "UL 1558"),
        ("2.3", "standards", "complying with IEEE C37.20.1", None, "", "IEEE C37.20.1"),
        ("2.3", "enclosure_material", "enclosure material: steel", None, "", "steel"),
        ("2.3", "location", "Indoor", None, "", "indoor"),
        ("2.4", "features", "drawout breakers", None, "", "drawout breakers"),
        ("2.4", "features", "arc flash maintenance mode", None, "", "arc flash maintenance mode"),
        (S, "enclosure", "NEMA 1, indoor, steel", None, "", "NEMA 1"), (S, "height_in", "80 in.", 80, "in"),
    ]),
    "example_va_ups": numbered("ups", [
        ("2.3", "power_kva", "not less than 500 kVA", 500, "kVA"), ("2.3", "power_kw", "500 kW", 500, "kW"),
        ("2.1", "voltage_kv", "Voltage 480 volts line-to-line", 480, "V"), ("2.1", "frequency_hz", "60 Hz", 60, "Hz"),
        ("2.1", "phases", "3-phase, 3-wire", 3), ("2.3", "efficiency_pct", "at least 99 percent", 99, "%"),
        ("2.3", "runtime_min", "full load for 10 minutes", 10, "minutes"),
        ("2.3", "battery_type", "Batteries shall be VRLA", None, "", "VRLA"),
        ("2.3", "standards", "listed to UL 1778", None, "", "UL 1778"),
        ("2.3", "features", "maintenance bypass shall be provided", None, "", "maintenance bypass"),
        ("2.3", "enclosure", "NEMA 1 enclosure", None, "", "NEMA 1"),
        ("3.1", "lead_time_weeks", "within 20 weeks", 20, "weeks"),
    ]),
    "example_university_ups": numbered("ups", [
        ("2.2", "power_kva", "rated 100 kVA", 100, "kVA"), ("2.2", "voltage_kv", "600 V", 600, "V"),
        ("2.2", "phases", "3 phase", 3), ("2.2", "frequency_hz", "60 Hz", 60, "Hz"),
        ("2.2", "runtime_min", "at least 15 minutes", 15, "minutes"),
        ("2.2", "standards", "listed to UL 1778", None, "", "UL 1778"),
        ("2.3", "features", "maintenance bypass shall be provided", None, "", "maintenance bypass"),
        ("2.3", "battery_type", "Lithium-ion batteries are preferred", None, "", "lithium-ion", False),
    ]),
}

# Items the public catalog has no data for are left out so every row can be checked as pass or fail.
DROP = {
    "example_va_mv_switchgear": {"R5", "R6", "R7", "R8", "R12", "R15"},
    "example_va_lv_switchgear": {"R2", "R3", "R5", "R12", "R14", "R15", "R16"},
    "example_university_lv_switchgear": {"R2", "R3", "R8", "R11"},
    "example_va_ups": {"R1", "R7", "R10", "R11", "R12"},
    "example_university_ups": {"R1", "R5", "R7"},
}
for _name, _data in LABELS.items():
    _data["requirements"] = [r for r in _data["requirements"] if r["id"] not in DROP[_name]]


def build(name: str, spec: dict) -> Path:
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f"{name}.pdf"
    styles = getSampleStyleSheet()
    note = ParagraphStyle("note", parent=styles["Normal"], fontSize=8.5, textColor=colors.HexColor("#555555"), leading=11)
    body = ParagraphStyle("body", parent=styles["Normal"], fontSize=10, leading=13.5, spaceAfter=4)
    head = ParagraphStyle("head", parent=styles["Heading3"], fontSize=10.5, spaceBefore=6, spaceAfter=2)
    part = ParagraphStyle("part", parent=styles["Heading2"], fontSize=12, spaceBefore=10, spaceAfter=4)
    doc = SimpleDocTemplate(str(path), pagesize=letter, leftMargin=60, rightMargin=60, topMargin=54, bottomMargin=54,
                            title=spec["title"])
    flow = [Paragraph(spec["title"], styles["Title"]), Paragraph(spec["project"], styles["Heading4"]),
            Paragraph(f'{spec["source"]} Template choices were filled in and a ratings schedule was added so the '
                      "tool has real values to check. Example for testing only, not an official document.", note),
            Spacer(1, 8)]
    for part_title, sections in spec["parts"]:
        flow.append(Paragraph(part_title, part))
        for sec_title, lines in sections:
            flow.append(Paragraph(sec_title, head))
            flow += [Paragraph(line, body) for line in lines]
    flow += [Paragraph("Ratings schedule (from the project drawings)", part)]
    table = Table([["Item", "Required"]] + spec["schedule"], colWidths=[220, 250])
    table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"), ("FONTSIZE", (0, 0), (-1, -1), 9.5),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#efece6")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#c9c2b6")), ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    flow += [table, Spacer(1, 10), Paragraph("End of section.", note)]
    doc.build(flow)
    return path


if __name__ == "__main__":
    import json
    for name, spec in EXAMPLES.items():
        print(build(name, spec))
        (OUT / f"{name}.requirements.json").write_text(json.dumps(LABELS[name], indent=2), encoding="utf-8")
