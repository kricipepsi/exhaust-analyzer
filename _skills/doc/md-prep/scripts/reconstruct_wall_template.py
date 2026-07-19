"""
reconstruct_wall_template.py — Configurable wall-of-text reconstruction engine.

PURPOSE
-------
When a .md file has been exported with all paragraph / heading line-breaks
stripped (wall-of-text lines of 2000+ chars), this script restores structure
using a document-specific config dict that you define at the top of the file
(or supply via --config).

HOW TO USE FOR A NEW DOCUMENT
------------------------------
1. Run diagnose_wall.py to identify wall lines and archetype.
2. Run optimize_markdown.py to get the prepped baseline.
3. Open this template, fill in CONFIG below (or create my_doc_config.py with
   the same CONFIG dict and run with --config my_doc_config.py).
4. Run:
       python3 scripts/reconstruct_wall_template.py \\
           /path/to/doc_prepped.md \\
           /path/to/doc_prepped.md   # overwrites prepped with reconstructed

CONFIG REFERENCE
----------------
HEADINGS : list of (level: int, title: str)
    All known heading titles in the order they appear in the wall, with their
    intended H1/H2/H3 level. The title must match EXACTLY as it appears in the
    wall (same Unicode, same punctuation).

TABLE_REPLACEMENTS : list of (blob: str, markdown: str)
    Each entry replaces a concatenated table blob (headers + cells run together)
    with a proper Markdown table string. Build the blob by copying the run-on
    text from the wall. The markdown string should start and end with \\n.

BOX_DRAWING_REPLACEMENTS : list of (start_anchor: str, end_anchor: str, replacement: str)
    For ASCII box-drawing diagrams. The engine finds the first line containing
    start_anchor and the next line containing end_anchor, then replaces the
    entire span with replacement. If start_anchor == end_anchor, only that line
    is replaced.

SEC2_ANCHOR : str or None
    If the document has a properly-structured "Section 2" after the wall (like
    DtcDoc.md), set this to the first distinctive text of that section. The
    engine will process only the wall (before sec2_anchor) and re-join Section 2
    unchanged. Set to None to process the whole body.

PROMOTE_HEADINGS_REGEX : str or None
    Optional regex applied to Section 2 headings to promote levels.
    E.g. r'^### (Cluster \\d+:)' → '## \\1'
"""

import re
import sys
import importlib.util
from pathlib import Path

# ===========================================================================
# EDIT THIS CONFIG FOR YOUR DOCUMENT
# (Or provide a --config my_config.py that defines CONFIG = {...})
# ===========================================================================
CONFIG = {
    "headings": [
        # (level, "Exact heading title as it appears in the wall")
        # Example:
        # (1, "Advanced Diagnostic Correlation Between Multi-Gas Exhaust Signatures"),
        # (2, "Theoretical Framework of Combustion Stoichiometry"),
    ],

    "table_replacements": [
        # (blob_string, markdown_table_string)
        # Example:
        # (
        #     "Gas ComponentChemical Indicator TypeIdeal ReadingDeviation",
        #     "\n<!-- TABLE: gas_ref -->\n| Gas Component | Type | Reading | Deviation |\n...\n"
        # ),
    ],

    "box_drawing_replacements": [
        # (start_anchor, end_anchor, replacement_text)
        # Example (replace an entire box between top and bottom lines):
        # ("┌───", "└───", "\n**ERA A → ERA B → ERA C**\n"),
    ],

    "sec2_anchor": None,
    # Example: "Building on the previous report"

    "promote_headings_regex": None,
    # Example: (r'^### (Cluster \\d+:)', r'## \\1')
}
# ===========================================================================


def load_external_config(config_path: str) -> dict:
    spec = importlib.util.spec_from_file_location("cfg", config_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.CONFIG


def insert_headings(text: str, headings: list) -> str:
    for level, title in headings:
        if title in text:
            marker = f"\n\n{'#' * level} {title}\n\n"
            text = text.replace(title, marker, 1)
        else:
            print(f"  WARNING: heading anchor not found: {title[:60]!r}")
    return text


def replace_tables(text: str, replacements: list) -> str:
    for blob, md in replacements:
        if blob in text:
            text = text.replace(blob, md, 1)
            print(f"  TABLE replaced: {blob[:50]!r}")
        else:
            print(f"  WARNING: table blob not matched: {blob[:50]!r}")
    return text


def replace_box_drawings(lines: list, replacements: list) -> list:
    """Operate on the raw line list to replace box-drawing spans."""
    if not replacements:
        return lines

    result = []
    i = 0
    while i < len(lines):
        line = lines[i]
        matched = False
        for start_anchor, end_anchor, replacement in replacements:
            if start_anchor in line:
                # Find end
                j = i
                if start_anchor == end_anchor:
                    result.append(replacement)
                    i += 1
                    matched = True
                    break
                else:
                    while j < len(lines) and end_anchor not in lines[j]:
                        j += 1
                    result.append(replacement)
                    i = j + 1
                    matched = True
                    break
        if not matched:
            result.append(line)
            i += 1
    return result


def split_sentences(text: str) -> str:
    """Light sentence splitting outside LaTeX blocks."""
    segments = re.split(r'(\$\$.*?\$\$)', text, flags=re.DOTALL)
    out = []
    for idx, seg in enumerate(segments):
        if idx % 2 == 1:
            out.append(seg)
        else:
            seg = re.sub(r'(?<=[a-z0-9\)])(\. )(?=[A-Z])', r'.\n\n', seg)
            out.append(seg)
    return ''.join(out)


def fix_block_equations(text: str) -> str:
    """
    Ensure $$...$$ block equations are on their own lines with inline fallback.
    Matches the full $$...$$  unit and surrounds it with blank lines.
    """
    def fmt(m):
        inner = m.group(1).strip()
        clean = re.sub(r'\\[a-zA-Z]+', '', inner)
        clean = re.sub(r'[{}_^]', '', clean).strip()[:100]
        return f"\n\n$${inner}$$\nInline fallback: {clean}\n\n"

    return re.sub(r'\$\$(.+?)\$\$', fmt, text, flags=re.DOTALL)


def reconstruct(input_path: str, output_path: str, cfg: dict) -> None:
    raw = Path(input_path).read_text(encoding='utf-8')
    lines = raw.splitlines(keepends=True)

    # Find frontmatter end
    fm_end = 0
    dash_count = 0
    for i, line in enumerate(lines):
        if line.strip() == '---':
            dash_count += 1
            if dash_count == 2:
                fm_end = i + 1
                break

    frontmatter = ''.join(lines[:fm_end])
    body_lines = lines[fm_end:]

    # Apply box-drawing replacements on raw lines first (before wall processing)
    body_lines_clean = replace_box_drawings(
        [l.rstrip('\r\n') for l in body_lines],
        cfg.get('box_drawing_replacements', [])
    )
    body = '\n'.join(body_lines_clean)

    # Split wall vs section 2 if anchor given
    sec2_anchor = cfg.get('sec2_anchor')
    if sec2_anchor and sec2_anchor in body:
        sec2_pos = body.find(sec2_anchor)
        wall = body[:sec2_pos]
        section2 = body[sec2_pos:]
    else:
        wall = body
        section2 = ''

    # Process wall
    wall = replace_tables(wall, cfg.get('table_replacements', []))
    wall = insert_headings(wall, cfg.get('headings', []))
    wall = fix_block_equations(wall)
    wall = split_sentences(wall)
    wall = re.sub(r'\n{4,}', '\n\n\n', wall)

    # Process section 2
    if section2 and cfg.get('promote_headings_regex'):
        pattern, repl = cfg['promote_headings_regex']
        section2 = re.sub(pattern, repl, section2, flags=re.MULTILINE)

    # Reassemble
    sep = '\n\n---\n\n' if section2 else ''
    full = frontmatter + '\n' + wall.strip() + sep + section2.strip() + '\n'

    Path(output_path).write_text(full, encoding='utf-8')
    lc = full.count('\n')
    print(f"Written: {output_path}  ({lc} lines, {len(full.encode())} bytes)")


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Reconstruct wall-of-text .md files")
    parser.add_argument('input',  help="Input _prepped.md path")
    parser.add_argument('output', help="Output path (can be same as input to overwrite)")
    parser.add_argument('--config', help="Optional Python file defining CONFIG dict")
    args = parser.parse_args()

    cfg = load_external_config(args.config) if args.config else CONFIG
    reconstruct(args.input, args.output, cfg)
