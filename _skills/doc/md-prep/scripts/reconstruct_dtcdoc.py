"""
Reconstruct DtcDoc_prepped.md: restore heading/paragraph/table structure
from the wall-of-text Section 1, then join with the already-structured Section 2.
"""

import re
import sys
from pathlib import Path

PREPPED_IN  = Path("/sessions/dazzling-beautiful-fermi/mnt/4DLab/TestSuite/DTC/DtcDoc_prepped.md")
PREPPED_OUT = Path("/sessions/dazzling-beautiful-fermi/mnt/4DLab/TestSuite/DTC/DtcDoc_prepped.md")

# ---------------------------------------------------------------------------
# Known section headings: (level, exact-text-as-it-appears-in-the-wall)
# ---------------------------------------------------------------------------
HEADINGS = [
    (1, "Advanced Diagnostic Correlation Between Multi-Gas Exhaust Signatures and OBD-II Powertrain Control Module Logic"),
    (2, "Theoretical Framework of Combustion Stoichiometry and Gas Analysis"),
    (2, "Powertrain Cluster 1: Fuel and Air Metering (P00xx, P01xx, P02xx)"),
    (3, "The Rich Mixture Diagnostic Case"),
    (3, "The Lean Mixture Diagnostic Case"),
    (2, "Powertrain Cluster 2: Ignition System and Misfire Detection (P03xx)"),
    (3, "The Combustion Quality Failure (Misfire) Case"),
    (2, "Powertrain Cluster 3: Auxiliary Emission Controls (P04xx)"),
    (3, "The Catalyst Efficiency Failure Case"),
    (3, "The NOx and EGR Interaction Case"),
    (3, "The EVAP System Leak Case"),
    (2, "Powertrain Cluster 4: Vehicle Speed and Idle Control (P05xx)"),
    (3, "The Idle Stability and Gas Signature Case"),
    (2, "Powertrain Cluster 5: Computer and Output Circuit (P06xx)"),
    (3, "Internal PCM Faults and Enabling Criteria"),
    (2, "Powertrain Cluster 6: Transmission Control (P07xx, P08xx, P09xx)"),
    (3, "Shift Strategy and Electronic-Hydraulic Correlation"),
    (3, "Mechanical Faults and the POA Signature Case"),
    (2, "Advanced Diagnostic Synthesis: Correlating Gas Signatures with DTC Clusters"),
    (2, 'The "False Lean" and Exhaust Dilution Phenomenon'),
    (2, "Conclusion of Diagnostic Integration"),
]

# ---------------------------------------------------------------------------
# Reconstructed Markdown tables (verbatim replacement of concatenated blobs)
# ---------------------------------------------------------------------------

GAS_BLOB = (
    "Gas ComponentChemical Indicator TypeIdeal Stoichiometric ReadingDeviation Implication"
    "Carbon Monoxide (CO)Richness Indicator< 0.5%"
    "Result of incomplete combustion due to insufficient $\\text{O}_2$."
    "Hydrocarbons (HC)Combustion Quality< 35 ppm"
    "Indicator of unburned fuel from misfires or mechanical failure."
    "Oxygen ($\\text{O}_2$)Leanness Indicator0.0% - 0.5%"
    "Evidence of excess air or exhaust system leaks."
    "Carbon Dioxide ($\\text{CO}_2$)Efficiency Indicator14.5% - 16%"
    "Peak levels indicate high volumetric and thermal efficiency."
    "Nitrogen Oxides ($\\text{NO}_x$)Temperature/Pressure< 100 ppm"
    "Produced by combustion temperatures exceeding $2500^\\circ\\text{F}$."
    "Lambda ($\\lambda$)Air-Fuel Balance0.995 - 1.005"
    "The master calculation for determining fuel control accuracy."
)
GAS_MD = """
<!-- TABLE: gas_component_reference -->
| Gas Component | Chemical Indicator Type | Ideal Stoichiometric Reading | Deviation Implication |
|---|---|---|---|
| Carbon Monoxide (CO) | Richness Indicator | < 0.5% | Result of incomplete combustion due to insufficient $\\text{O}_2$. |
| Hydrocarbons (HC) | Combustion Quality | < 35 ppm | Indicator of unburned fuel from misfires or mechanical failure. |
| Oxygen ($\\text{O}_2$) | Leanness Indicator | 0.0%–0.5% | Evidence of excess air or exhaust system leaks. |
| Carbon Dioxide ($\\text{CO}_2$) | Efficiency Indicator | 14.5%–16% | Peak levels indicate high volumetric and thermal efficiency. |
| Nitrogen Oxides ($\\text{NO}_x$) | Temperature/Pressure | < 100 ppm | Produced by combustion temperatures exceeding $2500^\\circ\\text{F}$. |
| Lambda ($\\lambda$) | Air-Fuel Balance | 0.995–1.005 | The master calculation for determining fuel control accuracy. |

"""

FUEL_BLOB = (
    "Fuel Control Condition"
    "Lambda (λ)CO (%)O2​ (%)CO2​ (%)Corresponding DTCs"
    "Rich Mixture< 1.0001.5 - 10.0+0.0 - 0.38.0 - 12.0P0172, P0175, P0200"
    "Lean Mixture> 1.0000.0 - 0.21.5 - 5.0+10.0 - 13.0P0171, P0174, P0102"
    "Stoichiometric1.000< 0.5< 0.514.5 - 16.0None (Operational)"
)
FUEL_MD = """
<!-- TABLE: fuel_control_conditions -->
| Fuel Control Condition | Lambda (λ) | CO (%) | O₂ (%) | CO₂ (%) | Corresponding DTCs |
|---|---|---|---|---|---|
| Rich Mixture | < 1.000 | 1.5–10.0+ | 0.0–0.3 | 8.0–12.0 | P0172, P0175, P0200 |
| Lean Mixture | > 1.000 | 0.0–0.2 | 1.5–5.0+ | 10.0–13.0 | P0171, P0174, P0102 |
| Stoichiometric | 1.000 | < 0.5 | < 0.5 | 14.5–16.0 | None (Operational) |

"""

EMISSION_BLOB = (
    "Emission ComponentFailure ModeGas Signature TrendPrimary DTCs"
    "CatalystEfficiency LossElevated Tailpipe CO & HCP0420, P0430"
    "EGR SystemFlow RestrictedSpike in $\\text{NO}_x$ under loadP0401"
    "EVAP SystemLeakageNormal (Minor), Rich (Saturated)P0442, P0455"
    "Secondary AirPump FailureElevated HC at start-upP0411"
)
EMISSION_MD = """
<!-- TABLE: emission_control_faults -->
| Emission Component | Failure Mode | Gas Signature Trend | Primary DTCs |
|---|---|---|---|
| Catalyst | Efficiency Loss | Elevated Tailpipe CO & HC | P0420, P0430 |
| EGR System | Flow Restricted | Spike in $\\text{NO}_x$ under load | P0401 |
| EVAP System | Leakage | Normal (Minor), Rich (Saturated) | P0442, P0455 |
| Secondary Air | Pump Failure | Elevated HC at start-up | P0411 |

"""

MASTER_BLOB = (
    "Diagnostic Case (Wiki)Primary Gas IndicatorCalculated Lambda (λ)"
    "Viable DTC MappingPCM Module Cluster"
    "Rich MixtureHigh CO (>1.5%)< 1.000P0172, P0175, P0201Fuel & Air Metering"
    "Lean MixtureHigh $\\text{O}_2$ (>1.5%)> 1.000P0171, P0174, P0101Fuel & Air Metering"
    "Misfire (Balanced)HC 800-2000 ppm$\\approx 1.000$P0300, P030x, P035xIgnition System"
    "Catalyst FailurePost-cat CO > 0.8%$\\approx 1.000$P0420, P0430Auxiliary Emissions"
    "External Air LeakHigh $\\text{O}_2$, low CO> 1.000 (False)P0171 (False Positive)Auxiliary Emissions"
    "Vacuum LeakLean-side HC spike> 1.000P0171, P0174, P1136Fuel & Air Metering"
    "Oil Burning (POA)HC > 2000 ppm$\\approx 1.000$P250C (Oil Level)Advanced Interactions"
    "Transmission LoadN/AN/AP0700, P0760, P0705Transmission"
)
MASTER_MD = """
<!-- TABLE: master_dtc_gas_correlation -->
| Diagnostic Case (Wiki) | Primary Gas Indicator | Calculated Lambda (λ) | Viable DTC Mapping | PCM Module Cluster |
|---|---|---|---|---|
| Rich Mixture | High CO (>1.5%) | < 1.000 | P0172, P0175, P0201 | Fuel & Air Metering |
| Lean Mixture | High $\\text{O}_2$ (>1.5%) | > 1.000 | P0171, P0174, P0101 | Fuel & Air Metering |
| Misfire (Balanced) | HC 800–2000 ppm | $\\approx 1.000$ | P0300, P030x, P035x | Ignition System |
| Catalyst Failure | Post-cat CO > 0.8% | $\\approx 1.000$ | P0420, P0430 | Auxiliary Emissions |
| External Air Leak | High $\\text{O}_2$, low CO | > 1.000 (False) | P0171 (False Positive) | Auxiliary Emissions |
| Vacuum Leak | Lean-side HC spike | > 1.000 | P0171, P0174, P1136 | Fuel & Air Metering |
| Oil Burning (POA) | HC > 2000 ppm | $\\approx 1.000$ | P250C (Oil Level) | Advanced Interactions |
| Transmission Load | N/A | N/A | P0700, P0760, P0705 | Transmission |

"""


def replace_tables(text):
    ok = []
    for name, blob, md in [("GAS", GAS_BLOB, GAS_MD),
                            ("FUEL", FUEL_BLOB, FUEL_MD),
                            ("EMISSION", EMISSION_BLOB, EMISSION_MD),
                            ("MASTER", MASTER_BLOB, MASTER_MD)]:
        if blob in text:
            text = text.replace(blob, md, 1)
            ok.append(name)
        else:
            print(f"  WARNING: {name} table blob not matched")
    print(f"  Tables replaced: {ok}")
    return text


def insert_headings(text):
    for level, title in HEADINGS:
        marker = f"\n\n{'#' * level} {title}\n\n"
        if title in text:
            text = text.replace(title, marker, 1)
        else:
            print(f"  WARNING: heading not found: {title[:60]!r}")
    return text


def fix_block_equations(text):
    """Ensure $$...$$ blocks are on their own lines."""
    # Insert blank line before $$ that is preceded by non-whitespace
    text = re.sub(r'([^\n])([$][$])', r'\1\n\n\2', text)
    # Insert blank line after $$ that is followed by non-whitespace
    text = re.sub(r'([$][$])([^\n$])', r'\1\n\nInline fallback: see LaTeX above.\n\n\2', text)
    return text


def split_sentences(text):
    """Light sentence splitting outside LaTeX blocks."""
    segments = re.split(r'(\$\$.*?\$\$)', text, flags=re.DOTALL)
    result = []
    for i, seg in enumerate(segments):
        if i % 2 == 1:
            result.append(seg)
        else:
            seg = re.sub(r'(?<=[a-z0-9\)])(\. )(?=[A-Z])', r'.\n\n', seg)
            result.append(seg)
    return "".join(result)


def fix_heading_skip(text):
    """Promote ### Cluster N: headings in Section 2 to ## to match Section 1."""
    text = re.sub(r'^### (Cluster \d+:)', r'## \1', text, flags=re.MULTILINE)
    return text


def clean_frontmatter(text):
    text = text.replace('domain: "<fill in>"', 'domain: "DTCLab / OBD-II Powertrain"')
    text = re.sub(r'^title: "Dtcdoc"', 'title: "Advanced Diagnostic Correlation: Multi-Gas Signatures and OBD-II Logic"', text, flags=re.MULTILINE)
    text = re.sub(r'^suggested_fixes:.*$', 'suggested_fixes: []', text, flags=re.MULTILINE)
    return text


def main():
    raw = PREPPED_IN.read_text(encoding="utf-8")
    lines = raw.splitlines(keepends=True)

    # Find frontmatter end (second "---")
    fm_end = 0; dash_count = 0
    for i, line in enumerate(lines):
        if line.strip() == "---":
            dash_count += 1
            if dash_count == 2:
                fm_end = i + 1; break

    # Find Section 2 boundary
    sec2_start = None
    for i in range(fm_end, len(lines)):
        if lines[i].lstrip().startswith("Building on the previous report"):
            sec2_start = i; break

    if sec2_start is None:
        print("ERROR: Section 2 boundary not found"); sys.exit(1)

    frontmatter = "".join(lines[:fm_end])
    wall        = "".join(lines[fm_end:sec2_start])
    section2    = "".join(lines[sec2_start:])

    print(f"Wall chars: {len(wall)}, Section2 lines: {len(section2.splitlines())}")

    # Process wall
    wall = replace_tables(wall)
    wall = insert_headings(wall)
    wall = fix_block_equations(wall)
    wall = split_sentences(wall)
    wall = re.sub(r'\n{4,}', '\n\n\n', wall)

    # Fix Section 2 heading levels
    section2 = fix_heading_skip(section2)

    # Reassemble
    full = frontmatter + "\n" + wall.strip() + "\n\n---\n\n" + section2.strip() + "\n"
    full = clean_frontmatter(full)

    PREPPED_OUT.write_text(full, encoding="utf-8")
    line_count = full.count('\n')
    print(f"Written: {PREPPED_OUT}")
    print(f"  Lines: {line_count}, Size: {len(full.encode())} bytes")


if __name__ == "__main__":
    main()
