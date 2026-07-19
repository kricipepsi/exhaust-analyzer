"""
Reconstruct DtcDoc2_prepped.md:
- Restore headings + paragraphs from wall-of-text lines
- Replace box-drawing ASCII art with Mermaid (era evolution) and bullet lists
- Reconstruct case data tables with proper Markdown table headers
"""

import re
from pathlib import Path

PREPPED_IN  = Path("/sessions/dazzling-beautiful-fermi/mnt/4DLab/TestSuite/DTC/DtcDoc2_prepped.md")
PREPPED_OUT = Path("/sessions/dazzling-beautiful-fermi/mnt/4DLab/TestSuite/DTC/DtcDoc2_prepped.md")

# ---------------------------------------------------------------------------
# Headings in L16 (intro wall)
# ---------------------------------------------------------------------------
L16_HEADINGS = [
    (1, "Architectural Evolution and Era-Based Classification of Petrol Vehicle Diagnostics"),
]

# ---------------------------------------------------------------------------
# Headings in L23 (Era A/B/C wall)
# ---------------------------------------------------------------------------
L23_HEADINGS = [
    (2, "Era A: 1990–2000 (The Dawn of OBD-I, Early OBD-II, and Narrowband Closed-Loop Control)"),
    (2, "Era B: 2000–2010 (EOBD Mandates, CAN Bus Standardization, and Port Fuel Injection Dominance)"),
    (2, "Era C: 2010–2020 (TGDI Dominance, Gasoline Particulate Filters, and Hybrid System Integration)"),
    (2, "Systematic Era Classification of Petrol Vehicle Diagnostic Cases"),
    (3, "Era A (1990–2000): Early OBD and Standard Exhaust Bench Diagnostics"),
    (3, "Era B (2000–2010): CAN-Bus OBD-II/EOBD Port Fuel Injection Diagnostics"),
]

# ---------------------------------------------------------------------------
# Headings in L33 (comprehensive table + synthesis)
# ---------------------------------------------------------------------------
L33_HEADINGS = [
    (3, "Era C (2010–2020): High-Pressure GDI, TGDI, and Hybrid Powertrain Diagnostics"),
    (2, "Synthesis of Cross-Decadal Diagnostic Strategies"),
]

# Table header blob (same in L23 and L33)
TABLE_HEADER_BLOB = "Case ID / RangeDiagnostic Features & Gas Chemistry ProfileEra Assignment Justification"
TABLE_HEADER_MD = "\n\n<!-- TABLE: case_era_assignment -->\n| Case ID / Range | Diagnostic Features & Gas Chemistry Profile | Era Assignment Justification |\n|---|---|---|\n"

# ---------------------------------------------------------------------------
# Case ID prefixes used as row-split anchors
# Each row: {case_ids}{$chemistry$}{justification text}
# ---------------------------------------------------------------------------
CASE_ID_PATTERN = re.compile(
    r'(?<!\$)(?<!\w)'       # not preceded by $ or word char (not inside LaTeX)
    r'((?:'
    r'(?:CSV|YAML|REAL|MECH|ECU|TC|EXT|CASE|case|PDF|RULE|EXP)-[\w.\-/]+(?:\s+to\s+[\w.\-/]+)?'
    r'(?:\s*(?:CSV|YAML|REAL|MECH|ECU|TC|EXT|CASE|case|PDF|RULE|EXP)-[\w.\-/]+(?:\s+to\s+[\w.\-/]+)?)*'
    r')'
    r')'
    r'(?=\s*(?:[$\\]|\())',  # followed by LaTeX or gas chemistry
)

# Simpler split: find positions where a case-ID word immediately precedes $
CASE_ROW_START = re.compile(
    r'(?<=[.!?\)])\s*'              # after end of justification sentence
    r'(?='
      r'(?:CSV|YAML|REAL|MECH|ECU|TC|EXT|CASE|case|PDF|RULE|EXP)-'
    r')'
)

def split_table_rows(table_body):
    """
    Split the concatenated case table body into (case_id, chemistry, justification) tuples.
    Strategy: scan for case-ID tokens that are directly followed by $ gas chemistry.
    """
    # Mark row boundaries with a sentinel
    # Pattern: word-ending char + case-id-prefix (not inside a $ block)
    # We'll use a two-pass approach:
    # Pass 1: find all positions that look like row starts
    # Pass 2: split and emit rows

    # Insert pipe character as sentinel before each apparent row start
    # Row start: a case-ID prefix immediately followed by $ or whitespace+$
    sentinel = "\x00"

    # Find positions: end of justification text + start of next case ID
    # Justification text ends with a period, then case ID starts
    # Pattern: r'\.([A-Z][a-z]+\-|YAML-|ECU-|etc)' won't work reliably
    # Better: split on )\s*followed by known prefix directly

    # Approach: find all matches of case_id + $ and insert newlines
    # Use the known prefixes
    prefixes = r'(?:CSV|YAML-CSV|YAML-PDF|YAML-TC|REAL|MECH|ECU|TC|EXT|CASE|case|PDF-4G|PDF-HI|RULE|EXP-N)'

    # Insert sentinels: when justification text ends and a new case ID starts
    # We detect: lowercase/punctuation char + case-ID-prefix
    def insert_sentinel(text):
        # After a sentence-ending period + optional space, before a case ID prefix
        result = re.sub(
            r'(\.)(\s*)(' + prefixes + r'-)',
            lambda m: m.group(1) + '\n' + sentinel + m.group(3),
            text
        )
        # Also catch case IDs that follow immediately after letters (no period)
        # e.g. "...control modules.ECU-003YAML-TC47..."
        result = re.sub(
            r'([a-z])(' + prefixes + r'-)',
            lambda m: m.group(1) + '\n' + sentinel + m.group(2),
            result
        )
        return result

    text = insert_sentinel(table_body)
    raw_rows = [r.strip() for r in text.split(sentinel) if r.strip()]

    rows = []
    for raw in raw_rows:
        # Each raw row is: case_ids + chemistry + justification
        # Chemistry starts at first $
        dollar_pos = raw.find('$')
        if dollar_pos < 0:
            # No chemistry found — it's a header or transitional text
            rows.append(('', '', raw))
            continue
        case_ids = raw[:dollar_pos].strip()
        rest = raw[dollar_pos:]
        # Justification starts after last gas value (period after closing $)
        # Find the boundary between chemistry and justification
        # Chemistry block ends at last matched closing $ followed by a period or .  
        # Simple heuristic: find the first '. ' followed by capital letter after a $
        chem_end = re.search(r'\$[^$]*\$\.?\s+([A-Z])', rest)
        if chem_end:
            # Find the last $ before the capital sentence start
            cap_start = chem_end.start(1)
            # Walk back to find the period
            period_pos = rest.rfind('.', 0, cap_start)
            if period_pos > 0:
                chemistry = rest[:period_pos + 1].strip()
                justification = rest[period_pos + 1:].strip()
            else:
                chemistry = rest
                justification = ''
        else:
            chemistry = rest
            justification = ''
        rows.append((case_ids, chemistry, justification))
    return rows


def format_case_table(rows):
    """Format (case_id, chemistry, justification) tuples as Markdown table rows."""
    lines = []
    for case_id, chemistry, justification in rows:
        if not case_id and not chemistry:
            continue
        # Escape pipe chars inside cells
        c1 = case_id.replace('|', '\\|').strip()
        c2 = chemistry.replace('|', '\\|').strip()
        c3 = justification.replace('|', '\\|').strip()
        if c1 or c2 or c3:
            lines.append(f"| {c1} | {c2} | {c3} |")
    return '\n'.join(lines) + '\n'


# ---------------------------------------------------------------------------
# Era evolution Mermaid diagram
# ---------------------------------------------------------------------------
ERA_BOX_TOP    = '┌─────────────────────────┐         ┌─────────────────────────┐         ┌─────────────────────────┐'
ERA_BOX_BOTTOM = '└─────────────────────────┘         └─────────────────────────┘         └─────────────────────────┘'

ERA_MERMAID = """\

```mermaid
graph LR
  A["Era A: 1990–2000<br/>Port Fuel Injection<br/>Narrowband O2 Sensors<br/>Standalone 4-Gas<br/>Legacy Analog OBD-I"]
  B["Era B: 2000–2010<br/>CAN-Bus OBD-II / EOBD<br/>Dual-Bed Catalysts<br/>Upstream Wideband O2<br/>Digital Fuel Trims"]
  C["Era C: 2010–2020<br/>Gasoline Direct Inj.<br/>Particulate Filters<br/>Hybrid Powertrains<br/>Model-Based Control"]
  A -->|transition| B
  B -->|transition| C
```

"""

# ERA B representative cases box
ERA_B_BOX_HEADER = '│                       ERA B REPRESENTATIVE CASES                           │'
ERA_B_BOX_BOTTOM = '└─────────────────────────────────────────────────────────────────────────────┘'

ERA_B_LIST = """\

**ERA B REPRESENTATIVE CASES**

- CSV-001 to CSV-100 (Core OBD-II Generic Fault Cases)
- REAL-001 to REAL-005 (Real Vehicle CAN Scans)
- MECH-001 to MECH-004, MECH-006 (Standard Mechanical Faults)
- ECU-001, ECU-002, ECU-007 to ECU-009 (Logic / Microcontroller Faults)
- EXT-201 to EXT-240 (Comprehensive Field Freeze Frame Cases)
- case_001 to case_050 (EOBD Standard Fuel Trim & Sensor Monitors)

"""


def insert_headings(text, heading_list):
    for level, title in heading_list:
        if title in text:
            marker = f"\n\n{'#' * level} {title}\n\n"
            text = text.replace(title, marker, 1)
        else:
            print(f"  WARNING: heading not found: {title[:55]!r}")
    return text


def split_sentences(text):
    segments = re.split(r'(\$\$.*?\$\$)', text, flags=re.DOTALL)
    result = []
    for i, seg in enumerate(segments):
        if i % 2 == 1:
            result.append(seg)
        else:
            seg = re.sub(r'(?<=[a-z0-9\)])(\. )(?=[A-Z])', r'.\n\n', seg)
            result.append(seg)
    return ''.join(result)


def clean_frontmatter(text):
    text = text.replace('domain: "<fill in>"', 'domain: "DTCLab / OBD-II Petrol Eras"')
    text = text.replace('title: "Dtcdoc2"',
        'title: "Architectural Evolution and Era-Based Classification of Petrol Vehicle Diagnostics"')
    text = text.replace('  - <concept-1>', '  - Era-based OBD-II diagnostic classification')
    text = text.replace('  - <concept-2>', '  - Gas chemistry profiles (HC, CO, CO2, O2, lambda)')
    text = text.replace('  - (no headings found)', '  - Architectural Evolution and Era-Based Classification')
    text = re.sub(r'^suggested_fixes:.*$', 'suggested_fixes: []', text, flags=re.MULTILINE)
    return text


def process_l16(wall):
    """Insert heading + split sentences."""
    wall = insert_headings(wall, L16_HEADINGS)
    wall = split_sentences(wall)
    return wall


def process_l23(wall):
    """Insert headings, replace table headers, split sentences.
    Note: wall ends with ERA B box top character — strip it."""
    # Strip trailing box-drawing chars (start of ERA B box at end of L23)
    box_top_era_b = '┌─────────────────────────────────────────────────────────────────────────────┐'
    if wall.rstrip().endswith(box_top_era_b):
        wall = wall.rstrip()[:-len(box_top_era_b)].rstrip()

    wall = insert_headings(wall, L23_HEADINGS)
    wall = wall.replace(TABLE_HEADER_BLOB, TABLE_HEADER_MD)
    wall = split_sentences(wall)
    return wall


def process_l33(wall):
    """Insert headings, reconstruct table, split sentences."""
    # Find table header and subsequent table body vs narrative
    header_pos = wall.find(TABLE_HEADER_BLOB)
    if header_pos < 0:
        print("  WARNING: L33 table header not found")
        wall = insert_headings(wall, L33_HEADINGS)
        return split_sentences(wall)

    pre_table = wall[:header_pos]
    after_header = wall[header_pos + len(TABLE_HEADER_BLOB):]

    # Find Era C heading in after_header to separate table from further headings
    era_c_title = "Era C (2010–2020): High-Pressure GDI, TGDI, and Hybrid Powertrain Diagnostics"
    synthesis_title = "Synthesis of Cross-Decadal Diagnostic Strategies"

    # Find Synthesis heading position (marks end of table)
    synth_pos = after_header.find(synthesis_title)
    if synth_pos >= 0:
        table_section = after_header[:synth_pos]
        narrative_section = synthesis_title + after_header[synth_pos + len(synthesis_title):]
    else:
        table_section = after_header
        narrative_section = ''

    # Process table: insert Era C sub-heading, then parse rows
    # Era C heading appears mid-table
    era_c_pos = table_section.find(era_c_title)
    if era_c_pos >= 0:
        era_b_body = table_section[:era_c_pos]
        era_c_suffix = table_section[era_c_pos + len(era_c_title):]

        era_b_rows = split_table_rows(era_b_body)
        era_b_md = format_case_table(era_b_rows)

        era_c_rows = split_table_rows(era_c_suffix)
        era_c_md = format_case_table(era_c_rows)

        table_md = (
            TABLE_HEADER_MD
            + era_b_md
            + f"\n### {era_c_title}\n\n"
            + "| Case ID / Range | Diagnostic Features & Gas Chemistry Profile | Era Assignment Justification |\n"
            + "|---|---|---|\n"
            + era_c_md
        )
    else:
        rows = split_table_rows(table_section)
        table_md = TABLE_HEADER_MD + format_case_table(rows)

    # Assemble
    wall = pre_table + table_md
    if narrative_section:
        wall += f"\n\n## {synthesis_title}\n\n{narrative_section}"

    wall = split_sentences(wall)
    return wall


def main():
    raw = PREPPED_IN.read_text(encoding='utf-8')
    lines = raw.splitlines(keepends=True)

    # Find frontmatter end
    fm_end = 0; dash_count = 0
    for i, line in enumerate(lines):
        if line.strip() == '---':
            dash_count += 1
            if dash_count == 2:
                fm_end = i + 1; break

    frontmatter = ''.join(lines[:fm_end])
    body_lines = lines[fm_end:]

    # Map line types (0-indexed in body_lines, 1-indexed as L16..L33 from original)
    # body_lines[0]  = L16 (intro wall)
    # body_lines[1]  = L17 (ERA box top)
    # body_lines[2..5] = L18-21 (ERA box rows)
    # body_lines[6]  = L22 (ERA box bottom)
    # body_lines[7]  = L23 (Era A wall)
    # body_lines[8..15] = L24-31 (ERA B box)
    # body_lines[16] = L32 (ERA B box bottom)
    # body_lines[17] = L33 (case table wall)

    # body[0]=blank, body[1]=intro wall, body[2-7]=ERA3 box,
    # body[8]=Era-A wall, body[9-17]=ERA-B box, body[18]=case table
    l16 = body_lines[1].rstrip('\r\n') if len(body_lines) > 1 else ''
    era_box_lines = [l.rstrip('\r\n') for l in body_lines[2:8]]   # ERA evolution box
    l23 = body_lines[8].rstrip('\r\n') if len(body_lines) > 8 else ''
    era_b_box_lines = [l.rstrip('\r\n') for l in body_lines[9:18]] # ERA B cases box
    l33 = body_lines[18].rstrip('\r\n') if len(body_lines) > 18 else ''

    print(f"L16: {len(l16)} chars, L23: {len(l23)} chars, L33: {len(l33)} chars")
    print(f"ERA box lines: {len(era_box_lines)}, ERA B box lines: {len(era_b_box_lines)}")

    # Process sections
    sec_intro = process_l16(l16)
    sec_era_diagram = ERA_MERMAID
    sec_era_a = process_l23(l23)
    sec_era_b_cases = ERA_B_LIST
    sec_table = process_l33(l33)

    # Collapse excess blank lines
    def collapse(text):
        return re.sub(r'\n{4,}', '\n\n\n', text)

    full = (
        frontmatter + '\n'
        + collapse(sec_intro).strip() + '\n\n'
        + sec_era_diagram
        + collapse(sec_era_a).strip() + '\n\n'
        + sec_era_b_cases
        + collapse(sec_table).strip() + '\n'
    )
    full = clean_frontmatter(full)

    PREPPED_OUT.write_text(full, encoding='utf-8')
    lc = full.count('\n')
    print(f"Written: {PREPPED_OUT}")
    print(f"  Lines: {lc}, Size: {len(full.encode())} bytes")


if __name__ == '__main__':
    main()
