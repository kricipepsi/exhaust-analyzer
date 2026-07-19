#!/usr/bin/env python3
"""
optimize_markdown.py — Phase 1 automation for md-prep skill.

Handles the mechanical parts of markdown preparation:
  - YAML frontmatter injection
  - Heading hierarchy normalization
  - Noise removal (redundant blank lines, stray HRs)
  - Detection of patterns needing manual attention (flagged, not auto-fixed)

Usage:
    python3 optimize_markdown.py input.md output.md

Outputs:
    output.md           — cleaned file with frontmatter
    output.report.json  — suggested_fixes list for Claude to work through
"""

import re
import sys
import json
import math
import os
from pathlib import Path


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def estimate_tokens(text: str) -> int:
    """Rough estimate: 1 token ≈ 4 chars for English/technical prose."""
    return math.ceil(len(text) / 4)


def extract_title(lines: list[str]) -> str:
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    return Path(sys.argv[1]).stem.replace("_", " ").replace("-", " ").title()


def extract_concepts(text: str, n: int = 5) -> list[str]:
    """Extract top N candidate concepts from bold terms (not headings)."""
    # Bold terms are more likely to be domain concepts than heading titles
    bold = re.findall(r"\*\*([^*]{3,50})\*\*", text)
    seen: set[str] = set()
    result: list[str] = []
    for term in bold:
        # Skip terms that look like sentence fragments or headings
        stripped = term.strip().rstrip(":").strip()
        if not stripped or len(stripped.split()) > 6:
            continue
        key = stripped.lower()
        if key not in seen:
            seen.add(key)
            result.append(stripped)
        if len(result) >= n:
            break
    return result or ["<concept-1>", "<concept-2>"]


def build_toc(lines: list[str]) -> list[str]:
    """Return a flat list of H2/H3 headings for the TOC field."""
    toc = []
    for line in lines:
        m = re.match(r"^(#{2,3})\s+(.+)", line)
        if m:
            depth = len(m.group(1)) - 2  # 0 for H2, 1 for H3
            prefix = "  " * depth + "- "
            toc.append(prefix + m.group(2).strip())
    return toc


# ---------------------------------------------------------------------------
# Fix: heading hierarchy
# ---------------------------------------------------------------------------

def normalize_headings(lines: list[str]) -> tuple[list[str], list[dict]]:
    """
    Ensure no heading levels are skipped and max depth is 3.
    Returns modified lines and a list of fix records.
    """
    fixes = []
    result = []
    prev_level = 1

    for i, line in enumerate(lines):
        m = re.match(r"^(#{1,6})\s+(.*)", line)
        if m:
            hashes, title = m.group(1), m.group(2)
            level = len(hashes)

            # Cap at H3
            if level > 3:
                new_level = 3
                fixes.append({
                    "rule": "R2",
                    "line": i + 1,
                    "description": f"H{level} → H3 (depth cap): {title[:60]}",
                    "auto_fixed": True,
                })
                line = "### " + title

            # Flag skipped levels (e.g., H2 → H4)
            elif level > prev_level + 1:
                fixes.append({
                    "rule": "R2",
                    "line": i + 1,
                    "description": f"Skipped heading level: H{prev_level} → H{level} ({title[:60]})",
                    "auto_fixed": False,
                    "action": "review — promote or insert missing level",
                })

            prev_level = min(level, 3)
        result.append(line)

    return result, fixes


# ---------------------------------------------------------------------------
# Fix: noise removal
# ---------------------------------------------------------------------------

def remove_noise(lines: list[str]) -> tuple[list[str], int]:
    """Remove consecutive blank lines (keep at most 1) and stray HRs."""
    result = []
    blank_run = 0
    removed = 0

    for line in lines:
        stripped = line.strip()

        # Stray horizontal rules (--- or *** not in frontmatter, not in table)
        if re.match(r"^[-*]{3,}$", stripped) and result:
            # Keep only if surrounded by content (i.e., actual section break)
            # Simple heuristic: skip if previous line was also blank
            if result and result[-1].strip() == "":
                removed += 1
                continue

        if stripped == "":
            blank_run += 1
            if blank_run > 1:
                removed += 1
                continue
        else:
            blank_run = 0

        result.append(line)

    return result, removed


# ---------------------------------------------------------------------------
# Detect: patterns needing manual attention
# ---------------------------------------------------------------------------

ASCII_FRACTION_RE = re.compile(r"[─━═]{3,}")  # ─── or similar fraction dividers
ASCII_ARROW_RE = re.compile(r"[─━═]+[►▶→]|──►|─►")
BOX_DRAWING_RE = re.compile(r"[┌┐└┘├┤┬┴┼│─]")
BARE_FENCE_RE = re.compile(r"^```\s*$")  # backtick fence with no language tag


def detect_manual_fixes(lines: list[str]) -> list[dict]:
    fixes = []
    in_fence = False
    fence_lang = None

    for i, line in enumerate(lines):
        # Track fenced blocks
        fence_m = re.match(r"^```(\w*)", line)
        if fence_m:
            if in_fence:
                in_fence = False
                fence_lang = None
            else:
                in_fence = True
                fence_lang = fence_m.group(1)
                if not fence_lang:
                    fixes.append({
                        "rule": "R7",
                        "line": i + 1,
                        "description": "Bare ``` fence — add language tag (python/json/yaml/text/etc.)",
                        "auto_fixed": False,
                        "action": "tag the fence",
                    })
            continue

        if in_fence:
            continue  # inside a fence, skip prose checks

        # ASCII fraction dividers (equations)
        if ASCII_FRACTION_RE.search(line):
            fixes.append({
                "rule": "R4",
                "line": i + 1,
                "description": f"ASCII fraction/divider: {line.strip()[:80]}",
                "auto_fixed": False,
                "action": "convert to $$ LaTeX $$ + inline fallback",
            })

        # ASCII arrow diagrams
        if ASCII_ARROW_RE.search(line) or BOX_DRAWING_RE.search(line):
            fixes.append({
                "rule": "R6",
                "line": i + 1,
                "description": f"ASCII diagram character: {line.strip()[:80]}",
                "auto_fixed": False,
                "action": "replace with declarative sequence or Mermaid block",
            })

    return fixes


# ---------------------------------------------------------------------------
# Build frontmatter
# ---------------------------------------------------------------------------

def build_frontmatter(text: str, lines: list[str], token_count: int) -> str:
    title = extract_title(lines)
    concepts = extract_concepts(text)
    toc = build_toc(lines)

    toc_yaml = "\n".join(f"  {t}" for t in toc) if toc else "  - (no headings found)"
    concepts_yaml = "\n".join(f"  - {c}" for c in concepts)

    return f"""---
title: "{title}"
version: "1.0"
domain: "<fill in>"
target_audience: "AI Processing Agent"
tokens: {token_count}
optimized_for_llm: true
concepts:
{concepts_yaml}
toc:
{toc_yaml}
suggested_fixes: []
---
"""


def has_frontmatter(lines: list[str]) -> bool:
    return lines[0].strip() == "---" if lines else False


def strip_frontmatter(lines: list[str]) -> list[str]:
    if not has_frontmatter(lines):
        return lines
    end = next((i for i, l in enumerate(lines[1:], 1) if l.strip() == "---"), None)
    return lines[end + 1:] if end else lines


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    if len(sys.argv) < 3:
        print("Usage: optimize_markdown.py input.md output.md")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])

    text = input_path.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)

    token_count_before = estimate_tokens(text)
    all_fixes: list[dict] = []

    # Strip existing frontmatter before processing
    body_lines = strip_frontmatter(lines)

    # Fix: heading normalization
    body_lines, heading_fixes = normalize_headings(body_lines)
    all_fixes.extend(heading_fixes)

    # Fix: noise removal
    body_lines, noise_removed = remove_noise(body_lines)
    if noise_removed:
        all_fixes.append({
            "rule": "R2",
            "line": None,
            "description": f"Removed {noise_removed} redundant blank lines / stray HRs",
            "auto_fixed": True,
        })

    # Detect: manual attention required
    manual_fixes = detect_manual_fixes(body_lines)
    all_fixes.extend(manual_fixes)

    # Rebuild body text
    body_text = "".join(body_lines)

    # Inject frontmatter
    frontmatter = build_frontmatter(body_text, body_lines, estimate_tokens(body_text))
    output_text = frontmatter + "\n" + body_text

    # Write output file
    output_path.write_text(output_text, encoding="utf-8")

    token_count_after = estimate_tokens(output_text)

    # Write report JSON
    report = {
        "input_file": str(input_path),
        "output_file": str(output_path),
        "bytes_before": len(text.encode()),
        "bytes_after": len(output_text.encode()),
        "lines_before": len(lines),
        "lines_after": len(output_text.splitlines()),
        "tokens_before": token_count_before,
        "tokens_after": token_count_after,
        "auto_fixed_count": sum(1 for f in all_fixes if f.get("auto_fixed")),
        "manual_fix_count": sum(1 for f in all_fixes if not f.get("auto_fixed")),
        "suggested_fixes": all_fixes,
    }

    report_path = output_path.with_suffix("").with_name(output_path.stem + ".report.json")
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    # Summary to stdout
    auto_n = report["auto_fixed_count"]
    manual_n = report["manual_fix_count"]
    print("md-prep: " + input_path.name)
    print("  Tokens:     " + str(token_count_before) + " -> " + str(token_count_after))
    print("  Auto-fixed: " + str(auto_n))
    print("  Manual:     " + str(manual_n) + " items need attention")
    print("  Output:     " + str(output_path))
    print("  Report:     " + str(report_path))


if __name__ == "__main__":
    main()
