"""
diagnose_wall.py — Quick structural diagnostic for export-stripped .md files.

Usage:
    python3 scripts/diagnose_wall.py <input.md>

Prints a summary report that tells you:
  - Whether the file has wall-of-text lines (export-stripped paragraphs)
  - Whether box-drawing characters are present
  - What archetype the file matches (A, B, or mixed)
  - Recommended repair strategy

Exit codes:
  0 — file looks clean, no wall repair needed
  1 — wall-of-text or box-drawing detected, repair needed
"""

import sys
import unicodedata
from pathlib import Path


def diagnose(path: str) -> int:
    data = open(path, "rb").read()
    text = data.decode("utf-8", errors="replace")
    lines = text.splitlines()

    total = len(lines)
    byte_size = len(data)

    # Classify each line
    wall_lines   = [(i + 1, len(l)) for i, l in enumerate(lines) if len(l) > 2000]
    medium_lines = [(i + 1, len(l)) for i, l in enumerate(lines) if 500 < len(l) <= 2000]
    box_lines    = [(i + 1, l[:60]) for i, l in enumerate(lines)
                    if any(0x2500 <= ord(c) <= 0x257F for c in l)]
    null_count   = data.count(b"\x00")

    has_wall = len(wall_lines) > 0
    has_box  = len(box_lines) > 0

    print(f"=== Wall Diagnostic: {Path(path).name} ===")
    print(f"  Total lines : {total}")
    print(f"  Byte size   : {byte_size:,}")
    print(f"  Null bytes  : {null_count}")
    print()

    if wall_lines:
        print(f"  WALL-OF-TEXT lines ({len(wall_lines)}):")
        for lineno, length in wall_lines[:8]:
            print(f"    L{lineno:03d}: {length:,} chars")
        if len(wall_lines) > 8:
            print(f"    ... and {len(wall_lines) - 8} more")
    else:
        print("  Wall-of-text lines: NONE")

    if medium_lines:
        print(f"  Medium-length lines (500–2000 chars): {len(medium_lines)}")

    if box_lines:
        print(f"\n  BOX-DRAWING lines ({len(box_lines)}):")
        for lineno, snippet in box_lines[:5]:
            print(f"    L{lineno:03d}: {repr(snippet)}")
    else:
        print("  Box-drawing chars: NONE")

    print()

    # Determine archetype
    if has_wall and not has_box:
        archetype = "A"
        desc = "Wall-of-text only (export-stripped headings + tables, structured section 2)"
    elif has_wall and has_box:
        archetype = "B"
        desc = "Wall-of-text + ASCII box-drawing diagrams"
    elif has_box and not has_wall:
        archetype = "B-lite"
        desc = "Box-drawing only (no wall-of-text)"
    else:
        archetype = "CLEAN"
        desc = "No structural issues detected"

    print(f"  ARCHETYPE : {archetype}")
    print(f"  DIAGNOSIS : {desc}")
    print()

    if archetype == "CLEAN":
        print("  ACTION: Run optimize_markdown.py directly (standard prep flow).")
        return 0

    print("  ACTION: Use wall-of-text repair flow (Step 10 in SKILL.md).")
    print()
    print("  Repair script selection:")
    if archetype == "A":
        print("    → scripts/reconstruct_wall_template.py  (configure heading anchors + table blobs)")
        print("    → or adapt scripts/reconstruct_dtcdoc.py if file matches DtcDoc-type pattern")
    elif archetype in ("B", "B-lite"):
        print("    → scripts/reconstruct_wall_template.py  (configure heading anchors + diagram handling)")
        print("    → or adapt scripts/reconstruct_dtcdoc2.py if file matches DtcDoc2-type pattern")

    print()
    print("  Next step: run optimize_markdown.py first to get the prepped baseline,")
    print("  then run the reconstruction script on the prepped output.")

    return 1


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: python3 {sys.argv[0]} <input.md>")
        sys.exit(2)
    sys.exit(diagnose(sys.argv[1]))
