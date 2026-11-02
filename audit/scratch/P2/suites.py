"""P2 census, kind (g): run every test suite and record each non-passing test and collection error.

Mechanism: pytest --junitxml per suite root, parsed with xml.etree. Unit: one pytest node id (or one
collection-error module). Population: the suite roots in SUITES (the 8 baseline suites plus the test
directories no baseline suite collects). Blind spot: tests outside SUITES (harness/, planning/, Vault/,
_skills/, audit/) are not run; timings are dropped so the JSON is deterministic.

Usage (repo root, venv active): python audit/scratch/P2/suites.py <raw_xml_dir> > audit/scratch/P2/suites.json
"""
from __future__ import annotations

import json
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TIMEOUT_S = 420

# (name, cwd, extra pytest args, collected-by-baseline?)
SUITES = [
    ("comlab", "labs/comlab", [], True),
    ("comlab-registry", "labs/comlab", ["registry/tests"], False),
    ("dnalab", "labs/dnalab", [], True),
    ("dtclab", "labs/dtclab", [], True),
    ("gaslab", "labs/gaslab", [], True),
    ("gaslab-slow", "labs/gaslab", ["-m", "slow"], False),
    ("obdlab", "labs/obdlab", [], True),
    ("symptomlab", "labs/symptomlab", [], True),
    ("vinlab", "labs/vinlab", [], True),
    ("wired", "apps/wired", [], True),
    ("wired-v7", "apps/wired", ["v7/tests"], False),
    ("ui", "apps/ui", ["tests"], False),
    ("controls", "audit/scratch/P2/controls", ["."], False),
]


def first_line(text: str | None) -> str:
    for line in (text or "").splitlines():
        if line.strip():
            return line.strip()[:300]
    return ""


def e_line(text: str | None) -> str:
    """Last pytest 'E   ...' line of a failure/error body: the exception actually raised."""
    lines = [ln.strip()[1:].strip() for ln in (text or "").splitlines() if ln.startswith("E ")]
    lines = [ln for ln in lines if ln]
    return lines[-1][:300] if lines else ""


def run(name: str, cwd: str, args: list[str], raw: Path) -> dict:
    xml = raw / f"{name}.xml"
    cmd = [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider",
           "--continue-on-collection-errors", f"--junitxml={xml}", *args]
    try:
        proc = subprocess.run(cmd, cwd=ROOT / cwd, capture_output=True, text=True, timeout=TIMEOUT_S)
    except subprocess.TimeoutExpired:
        return {"suite": name, "cwd": cwd, "args": args, "summary": f"INCOMPLETE: timeout after {TIMEOUT_S}s",
                "non_passing": []}
    tail = [l for l in proc.stdout.splitlines() if l.strip()][-1:]  # noqa: E741
    cases = []
    if xml.exists():
        for tc in ET.parse(xml).getroot().iter("testcase"):
            node = f"{tc.get('classname')}::{tc.get('name')}"
            outcome, msg = "passed", ""
            for kind in ("failure", "error", "skipped"):
                el = tc.find(kind)
                if el is not None:
                    outcome = kind
                    msg = first_line(el.get("message")) if kind == "skipped" else (
                        e_line(el.text) or first_line(el.get("message")))
                    if kind == "skipped" and el.get("type") == "pytest.xfail":
                        outcome = "xfailed"
                    break
            if outcome != "passed":
                cases.append({"node": node, "outcome": outcome, "message": msg})
    # pytest's summary line without the timing
    summary = tail[0].rsplit(" in ", 1)[0] if tail else ""
    return {"suite": name, "cwd": cwd, "args": args, "summary": summary,
            "non_passing": sorted(cases, key=lambda c: c["node"])}


def main() -> None:
    raw = Path(sys.argv[1])
    raw.mkdir(parents=True, exist_ok=True)
    out = [dict(run(n, c, a, raw), collected_by_baseline=b) for n, c, a, b in SUITES]
    json.dump(out, sys.stdout, indent=1, sort_keys=True)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
