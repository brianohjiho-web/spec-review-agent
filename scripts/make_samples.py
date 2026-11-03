"""Creates the sample spec PDFs. All projects and companies in them are made up."""
import json
from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

SAMPLES = Path(__file__).parent.parent / "data" / "samples"

SPECS = {
    "red_oak_mv": ("Project Red Oak Data Center: Section 26 13 13, Medium-Voltage Switchgear", [
        ("1.1 Scope", ["This section covers the 13.8 kV main-tie-main lineup for Building 2 of a fictional data center campus."]),
        ("2.1 Electrical ratings", [
            "The switchgear shall be rated 15 kV maximum and shall have a BIL of 95 kV.",
            "The main bus shall be rated 3000 A continuous.",
            "The short-circuit rating shall be 40 kA symmetrical.",
            "The system frequency is 60 Hz.",
            "Breaker control power shall be 125 VDC from the station battery.",
        ]),
        ("2.2 Construction", [
            "The switchgear shall be metal-clad and built to IEEE C37.20.2.",
            "The enclosure shall be NEMA 1 for indoor use.",
            "The lineup shall be arc-resistant, accessibility Type 2B, and tested to IEEE C37.20.7.",
            "Circuit breakers shall be vacuum type.",
            "Remote racking is required for all breakers.",
            "The lineup shall be seismic certified.",
            "Infrared windows are preferred at all cable compartments.",
        ]),
        ("3.1 Site conditions", [
            "Equipment shall operate at an ambient temperature of 40 C.",
            "The site altitude is 300 m.",
        ]),
        ("4.1 Delivery and testing", [
            "Delivery shall be within 56 weeks of purchase order.",
            "The Owner shall witness factory acceptance testing at the seller's plant.",
        ]),
    ]),
    "harbor_lv": ("Harbor Colo: Low-Voltage Power Distribution Switchgear", [
        ("A. General", ["This document describes the 480 V service switchgear for a fictional colocation site. Mechanical work is not included."]),
        ("B. Ratings", [
            "System voltage shall be 480 V, three phase, 60 Hz.",
            "Main bus: 4,000 A continuous, tin-plated copper.",
            "Short-circuit rating must be 85 kA.",
            "Control voltage must be 125 VDC.",
        ]),
        ("C. Requirements", [
            "Assemblies shall be listed to UL 1558 and comply with IEEE C37.20.1.",
            "Power circuit breakers shall be air type with drawout breakers.",
            "Zone selective interlocking shall be provided.",
            "An arc flash maintenance mode shall be provided.",
            "The enclosure shall be NEMA 1.",
            "Bottom cable entry is required.",
        ]),
        ("D. Site and schedule", [
            "Maximum ambient temperature: 40 C. Site altitude: 250 m.",
            "Equipment must ship within 34 weeks.",
        ]),
    ]),
    "high_desert_mv": ("High Desert Compute Campus: 34.5 kV Outdoor Switchgear", [
        ("1. Overview", ["The 34.5 kV collector switchgear is outdoors at a fictional high-altitude site."]),
        ("2. Ratings", [
            "Rated maximum voltage shall be 38 kV with a BIL of 150 kV.",
            "Main bus shall be 3000 A and short-circuit rating shall be 40 kA.",
            "Control power shall be 125 VDC at 60 Hz.",
        ]),
        ("3. Construction", [
            "The enclosure shall be NEMA 3R.",
            "The lineup shall be arc-resistant, accessibility Type 2B.",
            "Remote racking shall be provided.",
        ]),
        ("4. Site", [
            "The site is at 6,500 ft elevation.",
            "Equipment shall be rated for 113 F ambient.",
            "Delivery shall be within 64 weeks.",
        ]),
    ]),
}


def req(n, section, parameter, quote, number=None, unit="", text=None, mandatory=True):
    return dict(id=f"R{n}", section=section, parameter=parameter, source_quote=quote,
                value_number=number, unit=unit, value_text=text, mandatory=mandatory)


def numbered(items):
    return [req(i, *item[0], **item[1]) for i, item in enumerate(items, 1)]


LABELS = {
    "red_oak_mv": {
        "equipment_type": "mv_switchgear",
        "requirements": numbered([
            (("2.1", "voltage_kv", "rated 15 kV maximum"), dict(number=15, unit="kV")),
            (("2.1", "bil_kv", "BIL of 95 kV"), dict(number=95, unit="kV")),
            (("2.1", "bus_current_a", "rated 3000 A continuous"), dict(number=3000, unit="A")),
            (("2.1", "short_circuit_ka", "40 kA symmetrical"), dict(number=40, unit="kA")),
            (("2.1", "frequency_hz", "frequency is 60 Hz"), dict(number=60, unit="Hz")),
            (("2.1", "control_voltage_vdc", "control power shall be 125 VDC"), dict(number=125, unit="VDC")),
            (("2.2", "standards", "built to IEEE C37.20.2"), dict(text="IEEE C37.20.2")),
            (("2.2", "enclosure", "enclosure shall be NEMA 1"), dict(text="NEMA 1")),
            (("2.2", "arc_resistance", "accessibility Type 2B"), dict(text="Type 2B")),
            (("2.2", "standards", "tested to IEEE C37.20.7"), dict(text="IEEE C37.20.7")),
            (("2.2", "breaker_type", "Circuit breakers shall be vacuum type"), dict(text="vacuum")),
            (("2.2", "features", "Remote racking is required"), dict(text="remote racking")),
            (("2.2", "features", "shall be seismic certified"), dict(text="seismic certified")),
            (("2.2", "features", "Infrared windows are preferred"), dict(text="infrared windows", mandatory=False)),
            (("3.1", "max_ambient_c", "ambient temperature of 40 C"), dict(number=40, unit="C")),
            (("3.1", "max_altitude_m", "altitude is 300 m"), dict(number=300, unit="m")),
            (("4.1", "lead_time_weeks", "within 56 weeks"), dict(number=56, unit="weeks")),
            (("4.1", "other", "Owner shall witness factory acceptance testing"), dict(text="Witnessed factory testing")),
        ]),
    },
    "harbor_lv": {
        "equipment_type": "lv_switchgear",
        "requirements": numbered([
            (("B", "voltage_kv", "System voltage shall be 480 V"), dict(number=480, unit="V")),
            (("B", "frequency_hz", "three phase, 60 Hz"), dict(number=60, unit="Hz")),
            (("B", "bus_current_a", "4,000 A continuous"), dict(number=4000, unit="A")),
            (("B", "bus_material", "tin-plated copper"), dict(text="tin-plated copper")),
            (("B", "short_circuit_ka", "Short-circuit rating must be 85 kA"), dict(number=85, unit="kA")),
            (("B", "control_voltage_vdc", "Control voltage must be 125 VDC"), dict(number=125, unit="VDC")),
            (("C", "standards", "listed to UL 1558"), dict(text="UL 1558")),
            (("C", "standards", "comply with IEEE C37.20.1"), dict(text="IEEE C37.20.1")),
            (("C", "breaker_type", "shall be air type"), dict(text="air")),
            (("C", "features", "drawout breakers"), dict(text="drawout breakers")),
            (("C", "features", "Zone selective interlocking shall be provided"), dict(text="zone selective interlocking")),
            (("C", "features", "arc flash maintenance mode shall be provided"), dict(text="arc flash maintenance mode")),
            (("C", "enclosure", "enclosure shall be NEMA 1"), dict(text="NEMA 1")),
            (("C", "cable_entry", "Bottom cable entry is required"), dict(text="bottom")),
            (("D", "max_ambient_c", "Maximum ambient temperature: 40 C"), dict(number=40, unit="C")),
            (("D", "max_altitude_m", "Site altitude: 250 m"), dict(number=250, unit="m")),
            (("D", "lead_time_weeks", "ship within 34 weeks"), dict(number=34, unit="weeks")),
        ]),
    },
    "high_desert_mv": {
        "equipment_type": "mv_switchgear",
        "requirements": numbered([
            (("2", "voltage_kv", "Rated maximum voltage shall be 38 kV"), dict(number=38, unit="kV")),
            (("2", "bil_kv", "BIL of 150 kV"), dict(number=150, unit="kV")),
            (("2", "bus_current_a", "Main bus shall be 3000 A"), dict(number=3000, unit="A")),
            (("2", "short_circuit_ka", "short-circuit rating shall be 40 kA"), dict(number=40, unit="kA")),
            (("2", "control_voltage_vdc", "Control power shall be 125 VDC"), dict(number=125, unit="VDC")),
            (("2", "frequency_hz", "at 60 Hz"), dict(number=60, unit="Hz")),
            (("3", "enclosure", "enclosure shall be NEMA 3R"), dict(text="NEMA 3R")),
            (("3", "arc_resistance", "accessibility Type 2B"), dict(text="Type 2B")),
            (("3", "features", "Remote racking shall be provided"), dict(text="remote racking")),
            (("4", "max_altitude_m", "6,500 ft elevation"), dict(number=6500, unit="ft")),
            (("4", "max_ambient_c", "rated for 113 F ambient"), dict(number=113, unit="F")),
            (("4", "lead_time_weeks", "within 64 weeks"), dict(number=64, unit="weeks")),
        ]),
    },
}

EXPECTED = {
    "red_oak_mv": {"recommended": "MVA-15-3000", "top_ranked": "MVA-15-3000", "top_ranked_fails": []},
    "harbor_lv": {"recommended": "LVS-508-5000", "top_ranked": "LVS-508-5000", "top_ranked_fails": []},
    "high_desert_mv": {"recommended": None, "top_ranked": "MVA-38-3000",
                       "top_ranked_fails": ["arc_resistance", "max_altitude_m", "max_ambient_c"]},
}


def make_pdf(path, title, sections):
    styles = getSampleStyleSheet()
    story = [Paragraph(title, styles["Title"]),
             Paragraph("Sample document for a software demo. Fictional project.", styles["Italic"]),
             Spacer(1, 12)]
    for heading, sentences in sections:
        story.append(Paragraph(heading, styles["Heading3"]))
        story.append(Paragraph(" ".join(sentences), styles["BodyText"]))
    doc = SimpleDocTemplate(str(path), pagesize=letter, title=title, author="SpecCheck AI demo")
    doc.build(story)


if __name__ == "__main__":
    SAMPLES.mkdir(parents=True, exist_ok=True)
    for name, (title, sections) in SPECS.items():
        make_pdf(SAMPLES / f"{name}.pdf", title, sections)
        (SAMPLES / f"{name}.requirements.json").write_text(json.dumps(LABELS[name], indent=2), encoding="utf-8")
        (SAMPLES / f"{name}.expected.json").write_text(json.dumps(EXPECTED[name], indent=2), encoding="utf-8")
    print(f"Wrote {len(SPECS)} samples to {SAMPLES}")
