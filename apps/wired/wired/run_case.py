"""Single-case CLI runner for wired oil-burning fixtures."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import Any, cast

APP_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_ROOT = Path(__file__).resolve().parents[3]
CASES_DIR = APP_ROOT / "tests" / "fixtures" / "oil_cases"


def _bootstrap_lab_paths() -> None:
    """Expose editable lab source trees for direct ``python -m wired.run_case`` runs."""
    for relative in (
        "labs/comlab",
        "labs/dnalab",
        "labs/dtclab",
        "labs/gaslab",
        "labs/obdlab",
        "labs/symptomlab",
        "labs/vinlab",
        ".",
    ):
        path = str(WORKSPACE_ROOT / relative)
        if path not in sys.path:
            sys.path.insert(0, path)


def _case_path(case_id: str) -> Path:
    """Return the fixture path for a case identifier."""
    normalized = case_id.upper() if case_id.upper().startswith("MW-") else case_id
    return CASES_DIR / f"{normalized}.json"


def load_case(case_id: str) -> dict[str, Any]:
    """Load one oil-case raw-input fixture by case ID."""
    fixture_path = _case_path(case_id)
    if not fixture_path.exists():
        available = ", ".join(path.stem for path in sorted(CASES_DIR.glob("*.json")))
        raise FileNotFoundError(f"unknown case {case_id!r}; available cases: {available}")
    return cast(dict[str, Any], json.loads(fixture_path.read_text(encoding="utf-8")))


def main(argv: Sequence[str] | None = None) -> int:
    """Run one fixture through ``diagnose()`` and print its verdict."""
    parser = argparse.ArgumentParser(description="Run one wired oil-burning fixture.")
    parser.add_argument("--case", required=True, help="Oil case ID, e.g. MW-002")
    parser.add_argument(
        "--fatal-gates",
        action="store_true",
        help="Enable COMLab Stage-A fatal gates for invalid/incomplete samples.",
    )
    args = parser.parse_args(argv)

    _bootstrap_lab_paths()
    from wired import diagnose

    try:
        raw_inputs = load_case(args.case)
    except FileNotFoundError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    result = diagnose(raw_inputs, enable_fatal_gates=args.fatal_gates)
    verdict = result.diagnostic_verdict
    print(
        f"fault_code={verdict.fault_code} "
        f"confidence={verdict.confidence_score:.2f} "
        f"degradation={result.execution_meta.degradation_mode}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
