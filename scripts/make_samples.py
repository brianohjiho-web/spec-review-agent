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
    "ridgeline_cable_bus": ("Ridgeline Data Center: Section 26 25 00, Cable Bus", [
        ("1. Scope", ["This section covers the 13.8 kV cable bus from the outdoor transformer yard to the main switchgear at a fictional data center."]),
        ("2. Ratings", [
            "The cable bus shall be rated 15 kV maximum with a BIL of 95 kV.",
            "Continuous current shall be 3000 A.",
            "Short-circuit rating shall be 50 kA symmetrical with a momentary rating of 130 kA peak.",
            "System frequency is 60 Hz.",
        ]),
        ("3. Construction", [
            "Conductors shall be copper with EPR insulation.",
            "The enclosure shall be aluminum with a ventilated enclosure design.",
            "The installation location is outdoor, and the enclosure shall be NEMA 3R.",
            "The assembly shall comply with IEEE C37.23.",
        ]),
        ("4. Delivery", ["Delivery shall be within 28 weeks."]),
    ]),
    "lakeshore_iso_bus": ("Lakeshore Generating Station: Isolated Phase Bus", [
        ("A. Scope", ["Furnish isolated phase bus between the generator and the step-up transformer at a fictional power station."]),
        ("B. Ratings", [
            "The bus shall be rated 15.5 kV maximum with a BIL of 110 kV.",
            "Continuous current shall be 12,000 A, self-cooled.",
            "The momentary rating shall be 350 kA peak.",
            "System frequency is 60 Hz.",
        ]),
        ("C. Construction", [
            "Conductors shall be aluminum, and the enclosure shall be aluminum.",
            "The bus runs outdoor.",
            "Seal-off bushings are required at the building wall.",
            "Expansion joints shall be provided.",
            "Dry air pressurization is preferred.",
            "The assembly shall comply with IEEE C37.23.",
        ]),
        ("D. Delivery", ["Delivery shall be within 44 weeks."]),
    ]),
    "prairie_non_seg": ("Prairie Compute Campus: Non-Segregated Phase Bus", [
        ("1. Scope", ["Furnish non-segregated phase bus between the 13.8 kV main transformer and switchgear at a fictional campus."]),
        ("2. Ratings", [
            "The bus shall be rated 15 kV maximum with a BIL of 95 kV.",
            "Continuous current shall be 6000 A.",
            "Short-circuit rating shall be 63 kA.",
            "System frequency is 60 Hz.",
        ]),
        ("3. Construction", [
            "Conductors shall be tin-plated copper.",
            "The enclosure shall be NEMA 3R and made of aluminum.",
            "Space heaters shall be provided.",
            "Flexible connections shall be provided at each termination.",
            "The assembly shall comply with IEEE C37.23.",
        ]),
        ("4. Delivery", ["Delivery shall be within 30 weeks."]),
    ]),
    "mill_creek_utility": ("Mill Creek Data Center: Utility Service Section", [
        ("1. Scope", ["Furnish the utility service section for the incoming 13.8 kV feed at a fictional data center."]),
        ("2. Ratings", [
            "The section shall be rated 15 kV maximum with a BIL of 95 kV.",
            "Continuous current shall be 1200 A.",
            "Short-circuit rating shall be 25 kA.",
            "System frequency is 60 Hz.",
        ]),
        ("3. Construction", [
            "The enclosure shall be NEMA 3R, and the location is outdoor.",
            "Provide revenue metering and a utility disconnect.",
            "The assembly shall comply with IEEE C37.20.3.",
        ]),
        ("4. Delivery", ["Delivery shall be within 26 weeks."]),
    ]),
    "summit_transformer": ("Summit Campus: Main Power Transformer", [
        ("A. Scope", ["Furnish one main power transformer for a fictional data center campus."]),
        ("B. Ratings", [
            "The transformer shall be rated 30 MVA.",
            "Primary voltage shall be 34.5 kV with a BIL of 150 kV.",
            "Secondary voltage shall be 13.8 kV.",
            "Impedance shall be 8%.",
            "System frequency is 60 Hz.",
        ]),
        ("C. Construction", [
            "Cooling shall be ONAN.",
            "The insulating fluid shall be natural ester.",
            "The location is outdoor.",
            "The unit shall comply with IEEE C57.12.00.",
        ]),
        ("D. Delivery", ["Delivery shall be within 80 weeks."]),
    ]),
    "orion_ups": ("Orion Data Hall: UPS System", [
        ("1. Scope", ["Furnish one UPS system for a fictional AI data hall."]),
        ("2. Ratings", [
            "The UPS shall be rated 1.5 MW at 480 V and 60 Hz.",
            "Battery runtime shall be 10 minutes at full load.",
            "Efficiency shall be 97%.",
        ]),
        ("3. Construction", [
            "The battery type shall be lithium-ion.",
            "A maintenance bypass is required.",
            "Hot-swappable modules are preferred.",
            "The system shall comply with UL 1778.",
            "The location is indoor.",
        ]),
        ("4. Delivery", ["Delivery shall be within 32 weeks."]),
    ]),
    "atlas_server_racks": ("Atlas AI Hall: Server Racks", [
        ("1. Scope", ["Furnish server racks for high-density AI systems at a fictional data hall."]),
        ("2. Requirements", [
            "Racks shall be 48U high and 600 mm wide.",
            "Each rack shall support 100 kW.",
            "Static load shall be 3,300 lb.",
            "Cooling shall be direct-to-chip.",
            "Racks shall comply with EIA-310.",
            "Racks shall be seismic certified.",
        ]),
        ("3. Delivery", ["Delivery shall be within 16 weeks."]),
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
    "ridgeline_cable_bus": {
        "equipment_type": "cable_bus",
        "requirements": numbered([
            (("2", "voltage_kv", "rated 15 kV maximum"), dict(number=15, unit="kV")),
            (("2", "bil_kv", "BIL of 95 kV"), dict(number=95, unit="kV")),
            (("2", "bus_current_a", "Continuous current shall be 3000 A"), dict(number=3000, unit="A")),
            (("2", "short_circuit_ka", "50 kA symmetrical"), dict(number=50, unit="kA")),
            (("2", "momentary_ka", "momentary rating of 130 kA peak"), dict(number=130, unit="kA")),
            (("2", "frequency_hz", "frequency is 60 Hz"), dict(number=60, unit="Hz")),
            (("3", "bus_material", "Conductors shall be copper"), dict(text="copper")),
            (("3", "insulation", "EPR insulation"), dict(text="EPR")),
            (("3", "enclosure_material", "enclosure shall be aluminum"), dict(text="aluminum")),
            (("3", "features", "ventilated enclosure"), dict(text="ventilated enclosure")),
            (("3", "location", "location is outdoor"), dict(text="outdoor")),
            (("3", "enclosure", "enclosure shall be NEMA 3R"), dict(text="NEMA 3R")),
            (("3", "standards", "comply with IEEE C37.23"), dict(text="IEEE C37.23")),
            (("4", "lead_time_weeks", "within 28 weeks"), dict(number=28, unit="weeks")),
        ]),
    },
    "lakeshore_iso_bus": {
        "equipment_type": "iso_phase_bus",
        "requirements": numbered([
            (("B", "voltage_kv", "rated 15.5 kV maximum"), dict(number=15.5, unit="kV")),
            (("B", "bil_kv", "BIL of 110 kV"), dict(number=110, unit="kV")),
            (("B", "bus_current_a", "Continuous current shall be 12,000 A"), dict(number=12000, unit="A")),
            (("B", "cooling", "self-cooled"), dict(text="self-cooled")),
            (("B", "momentary_ka", "momentary rating shall be 350 kA"), dict(number=350, unit="kA")),
            (("B", "frequency_hz", "frequency is 60 Hz"), dict(number=60, unit="Hz")),
            (("C", "bus_material", "Conductors shall be aluminum"), dict(text="aluminum")),
            (("C", "enclosure_material", "the enclosure shall be aluminum"), dict(text="aluminum")),
            (("C", "location", "The bus runs outdoor"), dict(text="outdoor")),
            (("C", "features", "Seal-off bushings are required"), dict(text="seal-off bushings")),
            (("C", "features", "Expansion joints shall be provided"), dict(text="expansion joints")),
            (("C", "features", "Dry air pressurization is preferred"), dict(text="dry air pressurization", mandatory=False)),
            (("C", "standards", "comply with IEEE C37.23"), dict(text="IEEE C37.23")),
            (("D", "lead_time_weeks", "within 44 weeks"), dict(number=44, unit="weeks")),
        ]),
    },
    "prairie_non_seg": {
        "equipment_type": "non_seg_bus",
        "requirements": numbered([
            (("2", "voltage_kv", "rated 15 kV maximum"), dict(number=15, unit="kV")),
            (("2", "bil_kv", "BIL of 95 kV"), dict(number=95, unit="kV")),
            (("2", "bus_current_a", "Continuous current shall be 6000 A"), dict(number=6000, unit="A")),
            (("2", "short_circuit_ka", "Short-circuit rating shall be 63 kA"), dict(number=63, unit="kA")),
            (("2", "frequency_hz", "frequency is 60 Hz"), dict(number=60, unit="Hz")),
            (("3", "bus_material", "tin-plated copper"), dict(text="tin-plated copper")),
            (("3", "enclosure", "enclosure shall be NEMA 3R"), dict(text="NEMA 3R")),
            (("3", "enclosure_material", "made of aluminum"), dict(text="aluminum")),
            (("3", "features", "Space heaters shall be provided"), dict(text="space heaters")),
            (("3", "features", "Flexible connections shall be provided"), dict(text="flexible connections")),
            (("3", "standards", "comply with IEEE C37.23"), dict(text="IEEE C37.23")),
            (("4", "lead_time_weeks", "within 30 weeks"), dict(number=30, unit="weeks")),
        ]),
    },
    "mill_creek_utility": {
        "equipment_type": "utility_service",
        "requirements": numbered([
            (("2", "voltage_kv", "rated 15 kV maximum"), dict(number=15, unit="kV")),
            (("2", "bil_kv", "BIL of 95 kV"), dict(number=95, unit="kV")),
            (("2", "bus_current_a", "Continuous current shall be 1200 A"), dict(number=1200, unit="A")),
            (("2", "short_circuit_ka", "Short-circuit rating shall be 25 kA"), dict(number=25, unit="kA")),
            (("2", "frequency_hz", "frequency is 60 Hz"), dict(number=60, unit="Hz")),
            (("3", "enclosure", "enclosure shall be NEMA 3R"), dict(text="NEMA 3R")),
            (("3", "location", "location is outdoor"), dict(text="outdoor")),
            (("3", "features", "revenue metering"), dict(text="revenue metering")),
            (("3", "features", "utility disconnect"), dict(text="utility disconnect")),
            (("3", "standards", "comply with IEEE C37.20.3"), dict(text="IEEE C37.20.3")),
            (("4", "lead_time_weeks", "within 26 weeks"), dict(number=26, unit="weeks")),
        ]),
    },
    "summit_transformer": {
        "equipment_type": "transformer",
        "requirements": numbered([
            (("B", "power_kva", "rated 30 MVA"), dict(number=30, unit="MVA")),
            (("B", "voltage_kv", "Primary voltage shall be 34.5 kV"), dict(number=34.5, unit="kV")),
            (("B", "bil_kv", "BIL of 150 kV"), dict(number=150, unit="kV")),
            (("B", "secondary_voltage_kv", "Secondary voltage shall be 13.8 kV"), dict(number=13.8, unit="kV")),
            (("B", "impedance_pct", "Impedance shall be 8%"), dict(number=8, unit="%")),
            (("B", "frequency_hz", "frequency is 60 Hz"), dict(number=60, unit="Hz")),
            (("C", "cooling", "Cooling shall be ONAN"), dict(text="ONAN")),
            (("C", "insulating_fluid", "natural ester"), dict(text="natural ester")),
            (("C", "location", "location is outdoor"), dict(text="outdoor")),
            (("C", "standards", "comply with IEEE C57.12.00"), dict(text="IEEE C57.12.00")),
            (("D", "lead_time_weeks", "within 80 weeks"), dict(number=80, unit="weeks")),
        ]),
    },
    "orion_ups": {
        "equipment_type": "ups",
        "requirements": numbered([
            (("2", "power_kw", "rated 1.5 MW"), dict(number=1.5, unit="MW")),
            (("2", "voltage_kv", "at 480 V"), dict(number=480, unit="V")),
            (("2", "frequency_hz", "60 Hz"), dict(number=60, unit="Hz")),
            (("2", "runtime_min", "10 minutes at full load"), dict(number=10, unit="minutes")),
            (("2", "efficiency_pct", "Efficiency shall be 97%"), dict(number=97, unit="%")),
            (("3", "battery_type", "lithium-ion"), dict(text="lithium-ion")),
            (("3", "features", "maintenance bypass is required"), dict(text="maintenance bypass")),
            (("3", "features", "Hot-swappable modules are preferred"), dict(text="hot-swappable modules", mandatory=False)),
            (("3", "standards", "comply with UL 1778"), dict(text="UL 1778")),
            (("3", "location", "location is indoor"), dict(text="indoor")),
            (("4", "lead_time_weeks", "within 32 weeks"), dict(number=32, unit="weeks")),
        ]),
    },
    "atlas_server_racks": {
        "equipment_type": "server_rack",
        "requirements": numbered([
            (("2", "rack_units", "48U high"), dict(number=48, unit="U")),
            (("2", "rack_width_mm", "600 mm wide"), dict(number=600, unit="mm")),
            (("2", "rack_power_kw", "support 100 kW"), dict(number=100, unit="kW")),
            (("2", "static_load_kg", "Static load shall be 3,300 lb"), dict(number=3300, unit="lb")),
            (("2", "cooling", "direct-to-chip"), dict(text="direct-to-chip")),
            (("2", "standards", "comply with EIA-310"), dict(text="EIA-310")),
            (("2", "features", "seismic certified"), dict(text="seismic certified")),
            (("3", "lead_time_weeks", "within 16 weeks"), dict(number=16, unit="weeks")),
        ]),
    },
}

EXPECTED = {
    "red_oak_mv": {"recommended": "MVA-15-3000", "top_ranked": "MVA-15-3000", "top_ranked_fails": []},
    "harbor_lv": {"recommended": "LVS-508-5000", "top_ranked": "LVS-508-5000", "top_ranked_fails": []},
    "high_desert_mv": {"recommended": None, "top_ranked": "MVA-38-3000",
                       "top_ranked_fails": ["arc_resistance", "max_altitude_m", "max_ambient_c"]},
    "ridgeline_cable_bus": {"recommended": "CBL-15-4000", "top_ranked": "CBL-15-4000", "top_ranked_fails": []},
    "lakeshore_iso_bus": {"recommended": "IPB-15-12000", "top_ranked": "IPB-15-12000", "top_ranked_fails": []},
    "prairie_non_seg": {"recommended": None, "top_ranked": "NSB-15-5000", "top_ranked_fails": ["bus_current_a"]},
    "mill_creek_utility": {"recommended": "UTL-15-1200", "top_ranked": "UTL-15-1200", "top_ranked_fails": []},
    "summit_transformer": {"recommended": "XFM-38-30000", "top_ranked": "XFM-38-30000", "top_ranked_fails": []},
    "orion_ups": {"recommended": "UPS-480-1500", "top_ranked": "UPS-480-1500", "top_ranked_fails": []},
    "atlas_server_racks": {"recommended": "RCK-48-120", "top_ranked": "RCK-48-120", "top_ranked_fails": []},
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
