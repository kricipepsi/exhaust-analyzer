""".md report emitter for the generative harness.

Project rule (4DLab/CLAUDE.md): reports are always .md — never .docx, .pdf,
or other formats.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any


def write_report(
    results: list[dict[str, Any]],
    output_path: Path,
    *,
    title: str = "Harness Run Report",
    source_csv: str | None = None,
) -> None:
    """Write a .md test-run report.

    Args:
        results: Per-row result dicts from runner.run_suite().
        output_path: Path to write the .md file.
        title: Report heading.
        source_csv: Optional CSV filename for context.
    """
    passes = sum(1 for r in results if r["verdict"] == "PASS")
    failures = sum(1 for r in results if r["verdict"] == "FAIL")
    total = len(results)

    lines: list[str] = []
    lines.append(f"# {title}")
    lines.append("")
    if source_csv:
        lines.append(f"**Source:** `{source_csv}`  ")
    lines.append(f"**Date:** {_today()}  ")
    lines.append(f"**Total:** {total} | **PASS:** {passes} | **FAIL:** {failures}  ")
    lines.append("")
    lines.append("| # | case_id | Verdict | Detail | Duration (ms) |")
    lines.append("|---|---|---|---|---|")

    for i, r in enumerate(results, 1):
        lines.append(
            f"| {i} | {r['case_id']} | {r['verdict']} | {r.get('detail', '')} | {r.get('duration_ms', '')} |"
        )

    lines.append("")
    if failures > 0:
        lines.append(f"**{failures} failure(s) detected.**")
    else:
        lines.append("**All cases passed.**")

    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _today() -> str:
    from datetime import date
    return date.today().isoformat()
