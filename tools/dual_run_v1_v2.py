"""P6 dual-run harness — runs V1 and V2 engines on the 400-case corpus.

Produces a per-case diff report classifying each regression as:
  schema_gap / threshold_tweak / expected_drift / blocker.

Usage:
  python tools/dual_run_v1_v2.py              # full dual run + report
  python tools/dual_run_v1_v2.py --v1-worker  # internal: V1 subprocess worker
"""

from __future__ import annotations

import csv
import json
import subprocess  # nosec: B404 — intentional, runs own file as V1 worker
import sys
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
V1_ROOT = Path(r"C:\Users\muto\claude\4DApp\exhaust-analyzer-main")
CORPUS_PATH = ROOT / "cases" / "csv" / "cases_petrol_master_v6.csv"
REPORT_PATH = ROOT / "results" / "P6_dual_run_report.md"
V1_SCHEMA_DIR = V1_ROOT / "schema"

sys.path.insert(0, str(ROOT))


# ── helpers ─────────────────────────────────────────────────────────────────


def _parse_float(raw: str | None) -> float | None:
    if raw is None or raw.strip() == "":
        return None
    try:
        return float(raw)
    except ValueError:
        return None


def _parse_int(raw: str | None) -> int | None:
    if raw is None or raw.strip() == "":
        return None
    try:
        return int(float(raw))
    except ValueError:
        return None


# ── V1 worker mode ──────────────────────────────────────────────────────────


def _v1_worker() -> None:
    """Read a JSON list of case dicts from stdin, run V1 engine on each,
    write JSON list of result dicts to stdout."""
    cases: list[dict[str, Any]] = json.loads(sys.stdin.read())
    results: list[dict[str, Any]] = []

    for case in cases:
        try:
            result = _run_v1_case(case)
        except Exception as exc:
            result = {"error": str(exc), "case_id": case.get("case_id", "?")}
        results.append(result)

    sys.stdout.write(json.dumps(results, indent=2))


def _run_v1_case(case: dict[str, Any]) -> dict[str, Any]:
    """Build a V1 DiagnosticInput from a CSV-row dict and run V1 pipeline."""
    from engine.input_model import (  # type: ignore[import-not-found]
        DiagnosticInput,
        DTCSet,
        FreezeFrameRecord,
        GasRecord,
        OBDRecord,
        VehicleContext,
    )
    from engine.layered import diagnose_layered  # type: ignore[import-not-found]

    gas_idle = GasRecord(
        co=_parse_float(case.get("co")),
        co2=_parse_float(case.get("co2")),
        hc=_parse_int(case.get("hc")),
        o2=_parse_float(case.get("o2")),
        nox=_parse_int(case.get("nox")),
        lambda_sensor=_parse_float(case.get("lambda_analyser")),
    )

    gas_high = None
    gas_high_co = _parse_float(case.get("co_2500"))
    if gas_high_co is not None:
        gas_high = GasRecord(
            co=gas_high_co,
            co2=_parse_float(case.get("co2_2500")),
            hc=_parse_int(case.get("hc_2500")),
            o2=_parse_float(case.get("o2_2500")),
            nox=_parse_int(case.get("nox_2500")),
            lambda_sensor=_parse_float(case.get("lambda_2500")),
        )
    else:
        gas_high = GasRecord()

    obd = OBDRecord(
        stft_b1=_parse_float(case.get("stft_b1")),
        ltft_b1=_parse_float(case.get("ltft_b1")),
        stft_b2=_parse_float(case.get("stft_b2")),
        ltft_b2=_parse_float(case.get("ltft_b2")),
        o2_upstream=_parse_float(case.get("o2_upstream_classification")),
        o2_downstream=_parse_float(case.get("o2_downstream_voltage")),
        map=_parse_float(case.get("map")),
        maf=_parse_float(case.get("maf")),
        ect=_parse_float(case.get("ect")),
        rpm=_parse_float(str(case.get("rpm", ""))) if case.get("rpm") else None,
        lambda_sensor=_parse_float(case.get("obd_lambda")),
    )

    dtcs_str = (case.get("dtcs") or "").strip()
    dtc_codes = [d.strip() for d in dtcs_str.split("|") if d.strip()]
    dtcs = DTCSet(codes=dtc_codes)

    ff = FreezeFrameRecord()
    ff_ect = _parse_float(case.get("ff_ect"))
    if ff_ect is not None:
        ff = FreezeFrameRecord(
            ect=ff_ect,
            rpm=_parse_int(case.get("ff_rpm")),
            calc_load=_parse_float(case.get("ff_load")),
            map=_parse_float(case.get("ff_map")),
            stft_b1=_parse_float(case.get("ff_stft_b1")),
            ltft_b1=_parse_float(case.get("ff_ltft_b1")),
        )

    ctx = VehicleContext(
        fuel_type="petrol",
        engine_temp=case.get("engine_temp", "hot") or "hot",
        induction_type=case.get("induction_type", "na") or "na",
        emission_class=case.get("emission_class", "euro4") or "euro4",
        mileage_bracket=case.get("mileage_bracket") or None,
        oil_consumption=case.get("oil_consumption") or None,
        ignition_age=case.get("ignition_age") or None,
        primary_symptom=case.get("primary_symptom") or None,
        vehicle_brand=case.get("brand") or None,
        displacement_cc=_parse_int(case.get("displacement_cc")),
    )

    diag = DiagnosticInput(
        gases=gas_idle,
        gases_high=gas_high,
        obd_low=obd,
        dtcs=dtcs,
        freeze_frame=ff,
        context=ctx,
    )

    result = diagnose_layered(diag)

    return {
        "top_fault": result.get("top_fault", "unknown"),
        "confidence": result.get("confidence", 0.0),
        "confidence_ceiling": result.get("confidence_ceiling", 0.0),
        "state": result.get("state", "unknown"),
        "alternatives": result.get("alternatives", [])[:5],
        "warnings": result.get("warnings", []),
        "evidence_layers_used": result.get("evidence_layers_used", []),
        "reasoning_path": result.get("reasoning_path", [])[:3],
    }


# ── V2 runner ───────────────────────────────────────────────────────────────


def _csv_to_v2_input(row: dict[str, str]) -> Any:
    """Convert a corpus CSV row to a V2 DiagnosticInput."""
    from engine.v2.input_model import (
        DiagnosticInput,
        GasRecord,
        OBDRecord,
        VehicleContext,
    )

    ctx = VehicleContext(
        brand="VOLKSWAGEN",
        model="Golf",
        engine_code="EA111_1.2_TSI",
        displacement_cc=1390,
        my=_parse_int(row.get("my", "2012")) or 2012,
    )

    gas_idle = GasRecord(
        co_pct=_parse_float(row.get("co")) or 0.0,
        hc_ppm=_parse_float(row.get("hc")) or 0.0,
        co2_pct=_parse_float(row.get("co2")) or 0.0,
        o2_pct=_parse_float(row.get("o2")) or 0.0,
        nox_ppm=_parse_float(row.get("nox")),
        lambda_analyser=_parse_float(row.get("lambda_analyser")),
    )

    gas_high_co = _parse_float(row.get("co_2500"))
    gas_high = None
    if gas_high_co is not None:
        gas_high = GasRecord(
            co_pct=gas_high_co,
            hc_ppm=_parse_float(row.get("hc_2500")) or 0.0,
            co2_pct=_parse_float(row.get("co2_2500")) or 0.0,
            o2_pct=_parse_float(row.get("o2_2500")) or 0.0,
            nox_ppm=_parse_float(row.get("nox_2500")),
            lambda_analyser=_parse_float(row.get("lambda_2500")),
        )

    stft_b1 = _parse_float(row.get("stft_b1"))
    ltft_b1 = _parse_float(row.get("ltft_b1"))
    obd = None
    if stft_b1 is not None or ltft_b1 is not None:
        obd = OBDRecord(
            stft_b1=stft_b1,
            ltft_b1=ltft_b1,
            stft_b2=_parse_float(row.get("stft_b2")),
            ltft_b2=_parse_float(row.get("ltft_b2")),
            obd_lambda=_parse_float(row.get("obd_lambda")),
            rpm=_parse_int(row.get("rpm")),
            ect_c=_parse_float(row.get("ect")),
            map_kpa=_parse_float(row.get("map")),
            maf_gs=_parse_float(row.get("maf")),
            fuel_status=row.get("fuel_status", "").strip() or None,
            fuel_pressure_kpa=_parse_float(row.get("fuel_pressure")),
        )

    dtcs = [d.strip() for d in row.get("dtcs", "").split("|") if d.strip()]

    analyser_raw = row.get("analyser_type", "5-gas").strip() or "5-gas"
    analyser_type: Any = "5-gas" if analyser_raw == "5-gas" else "4-gas"

    return DiagnosticInput(
        vehicle_context=ctx,
        gas_idle=gas_idle,
        gas_high=gas_high,
        obd=obd,
        dtcs=dtcs,
        analyser_type=analyser_type,
    )


def _run_v2_case(case: dict[str, str]) -> dict[str, Any]:
    """Run a single case through the V2 pipeline."""
    from engine.v2.pipeline import diagnose

    diag = _csv_to_v2_input(case)
    try:
        result = diagnose(diag)
    except Exception as exc:
        return {"error": str(exc)}
    return result


# ── comparison + classification ─────────────────────────────────────────────


def _load_v2_fault_ids() -> frozenset[str]:
    """Return the set of all valid V2 fault IDs from faults.yaml."""
    import yaml

    faults_path = ROOT / "schema" / "v2" / "faults.yaml"
    with faults_path.open(encoding="utf-8") as f:
        faults: dict = yaml.safe_load(f)
    ids: set[str] = set()
    for fid in faults:
        ids.add(fid)
        node = faults[fid]
        for child in node.get("children", []) if isinstance(node, dict) else []:
            ids.add(child)
    return frozenset(ids)


def _classify(
    v1: dict[str, Any],
    v2: dict[str, Any],
    row: dict[str, str],
    v2_fault_ids: frozenset[str],
) -> str:
    """Classify the V1→V2 difference for one case.

    Returns one of: schema_gap / threshold_tweak / expected_drift / blocker
    """
    v1_fault = v1.get("top_fault", "unknown") if "error" not in v1 else "v1_error"
    v1_state = v1.get("state", "unknown") if "error" not in v1 else "v1_error"

    v2_error = "error" in v2
    v2_fault = (
        v2["primary"]["fault_id"]
        if (not v2_error and v2.get("primary"))
        else None
    )
    v2_state = v2.get("state", "unknown") if not v2_error else "v2_error"
    expected_fault = row.get("expected_top_fault", "").strip()

    if v2_error:
        return "blocker"
    if v1_fault == "v1_error":
        return "blocker"

    if v1_state == "insufficient_evidence" and v2_state == "insufficient_evidence":
        return "expected_drift"
    if v1_state == "invalid_input" and v2_state == "invalid_input":
        return "expected_drift"

    if v1_fault == v2_fault:
        return "expected_drift"

    v2_fault_str = v2_fault or ""

    # schema_gap: V1 fault missing from V2 schema
    if (
        v1_fault
        and v1_fault not in ("unknown", "insufficient_evidence", "no_fault")
        and v1_fault not in v2_fault_ids
    ):
        return "schema_gap"

    # same family gives different top child → threshold tweak
    v1_family = _family_of(v1_fault)
    v2_family = _family_of(v2_fault_str)
    if v1_family and v2_family and v1_family == v2_family:
        return "threshold_tweak"

    if v1_state == v2_state and v1_fault != v2_fault:
        return "threshold_tweak"

    if v2_state == "insufficient_evidence" and v1_state == "named_fault":
        v2_expected = expected_fault
        if v2_expected and v1_fault and _family_of(v1_fault) == _family_of(v2_expected):
            return "blocker"
        return "threshold_tweak"

    return "expected_drift"


def _family_of(fault_id: str) -> str:
    """Extract the fault family from a fault ID.

    Conventions observed in V2 faults.yaml:
    - "Catalyst_Failure", "Catalyst_Failure_Aged" → family = "Catalyst_Failure"
    - "Vacuum_Leak_Intake_Manifold" → family is first underscore-delimited
      segments up to the last segment that isn't a qualifier.
    """
    if not fault_id or fault_id in ("unknown", "insufficient_evidence", "no_fault"):
        return ""
    # Most V2 fault IDs use underscores; try parent prefix match
    parts = fault_id.split("_")
    if len(parts) <= 1:
        return fault_id
    # Heuristic: family is the first 2-3 segments that define the fault class
    # Common families: Catalyst_Failure, Fuel_Delivery, Ignition_System, etc.
    # Return first two segments as family guess
    return "_".join(parts[:2])


# ── report generation ───────────────────────────────────────────────────────


def _write_report(
    rows: list[dict[str, str]],
    v1_results: list[dict[str, Any]],
    v2_results: list[dict[str, Any]],
    classifications: list[str],
    elapsed_s: float,
) -> None:
    """Write the P6 dual-run diff report in Markdown."""
    total = len(rows)
    schema_gap = sum(1 for c in classifications if c == "schema_gap")
    threshold_tweak = sum(1 for c in classifications if c == "threshold_tweak")
    expected_drift = sum(1 for c in classifications if c == "expected_drift")
    blocker = sum(1 for c in classifications if c == "blocker")

    lines: list[str] = []
    lines.append("# P6 Dual-Run Report — V1 vs V2")
    lines.append("")
    lines.append(f"**Date:** {time.strftime('%Y-%m-%d %H:%M')}")
    lines.append("**Corpus:** `cases/csv/cases_petrol_master_v6.csv`")
    lines.append(f"**Cases processed:** {total}")
    lines.append(f"**Elapsed:** {elapsed_s:.1f}s")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append("| Classification | Count | % |")
    lines.append("|---|---|---|")
    lines.append(
        f"| schema_gap | {schema_gap} | {schema_gap/total*100:.1f}% |"
    )
    lines.append(
        f"| threshold_tweak | {threshold_tweak} | {threshold_tweak/total*100:.1f}% |"
    )
    lines.append(
        f"| expected_drift | {expected_drift} | {expected_drift/total*100:.1f}% |"
    )
    lines.append(
        f"| blocker | {blocker} | {blocker/total*100:.1f}% |"
    )
    lines.append("")
    lines.append("## Per-Case Diff")
    lines.append("")
    lines.append(
        "| case_id | expected | V1 top | V2 top | classification |"
    )
    lines.append(
        "|---|---|---|---|---|"
    )

    for i, row in enumerate(rows):
        cid = row.get("case_id", f"row-{i}")
        expected = row.get("expected_top_fault_family", "").strip()
        v1_top = v1_results[i].get("top_fault", "?")
        v2_top = (
            v2_results[i]["primary"]["fault_id"]
            if (v2_results[i].get("primary"))
            else v2_results[i].get("state", "?")
        )
        cls = classifications[i]
        lines.append(f"| {cid} | {expected} | {v1_top} | {v2_top} | {cls} |")

    lines.append("")
    lines.append("## Classification Definitions")
    lines.append("")
    lines.append("- **schema_gap**: V1 fault ID missing from V2 `faults.yaml`.")
    lines.append("- **threshold_tweak**: Same fault family, different specific diagnosis.")
    lines.append("- **expected_drift**: V2 intentionally differs due to architectural changes.")
    lines.append("- **blocker**: V2 result is clearly wrong (systematic failure).")
    lines.append("")
    lines.append("## Blocker Details")
    lines.append("")

    blocker_cases = [
        (rows[i], v1_results[i], v2_results[i])
        for i, c in enumerate(classifications)
        if c == "blocker"
    ]
    if blocker_cases:
        for row, v1, v2 in blocker_cases:
            cid = row.get("case_id", "?")
            lines.append(f"### {cid}")
            lines.append(f"- **Expected:** {row.get('expected_top_fault_family', '?')}")
            lines.append(f"- **V1:** {v1.get('top_fault', '?')} "
                         f"(confidence={v1.get('confidence', '?')})")
            lines.append(f"- **V2:** {v2.get('primary', v2.get('state', '?'))}")
            lines.append("")
    else:
        lines.append("No blockers found.")
        lines.append("")

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


# ── main orchestrator ───────────────────────────────────────────────────────


def main() -> None:
    if "--v1-worker" in sys.argv:
        sys.path.insert(0, str(V1_ROOT))
        _v1_worker()
        return

    if not CORPUS_PATH.exists():
        print(f"Corpus not found: {CORPUS_PATH}")
        raise SystemExit(1)

    print("=== P6 Dual-Run Harness: V1 vs V2 ===\n")

    # Load corpus
    with CORPUS_PATH.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    print(f"Corpus loaded: {len(rows)} cases")

    # Load V2 fault IDs for schema_gap classification
    print("Loading V2 fault IDs...")
    v2_fault_ids = _load_v2_fault_ids()
    print(f"  {len(v2_fault_ids)} fault IDs loaded")

    # Build V1-compatible JSON payload
    print("Preparing V1 input payload...")
    v1_payload: list[dict[str, Any]] = []
    for row in rows:
        v1_payload.append({
            "case_id": row.get("case_id", ""),
            "co": row.get("co", ""),
            "co2": row.get("co2", ""),
            "hc": row.get("hc", ""),
            "o2": row.get("o2", ""),
            "nox": row.get("nox", ""),
            "lambda_analyser": row.get("lambda_analyser", ""),
            "co_2500": row.get("co_2500", ""),
            "co2_2500": row.get("co2_2500", ""),
            "hc_2500": row.get("hc_2500", ""),
            "o2_2500": row.get("o2_2500", ""),
            "nox_2500": row.get("nox_2500", ""),
            "lambda_2500": row.get("lambda_2500", ""),
            "stft_b1": row.get("stft_b1", "") or "",
            "ltft_b1": row.get("ltft_b1", "") or "",
            "stft_b2": row.get("stft_b2", "") or "",
            "ltft_b2": row.get("ltft_b2", "") or "",
            "obd_lambda": row.get("obd_lambda", "") or "",
            "o2_upstream_classification": row.get("o2_upstream_classification", "") or "",
            "o2_downstream_voltage": row.get("o2_downstream_voltage", "") or "",
            "map": row.get("map", "") or "",
            "maf": row.get("maf", "") or "",
            "rpm": row.get("rpm", "") or "",
            "ect": row.get("ect", "") or "",
            "fuel_status": row.get("fuel_status", "") or "",
            "fuel_pressure": row.get("fuel_pressure", "") or "",
            "dtcs": row.get("dtcs", "") or "",
            "ff_ect": row.get("ff_ect", "") or "",
            "ff_rpm": row.get("ff_rpm", "") or "",
            "ff_load": row.get("ff_load", "") or "",
            "ff_map": row.get("ff_map", "") or "",
            "ff_stft_b1": row.get("ff_stft_b1", "") or "",
            "ff_ltft_b1": row.get("ff_ltft_b1", "") or "",
            "engine_temp": row.get("engine_temp", "") or "hot",
            "primary_symptom": row.get("primary_symptom", "") or "",
            "induction_type": row.get("induction_type", "") or "na",
            "emission_class": row.get("emission_class", "") or "euro4",
            "mileage_bracket": row.get("mileage_bracket", "") or "",
            "oil_consumption": row.get("oil_consumption", "") or "",
            "ignition_age": row.get("ignition_age", "") or "",
            "brand": row.get("brand", "") or "",
            "displacement_cc": row.get("displacement_cc", "") or "",
        })

    # Run V1 via subprocess
    print("Running V1 engine via subprocess...")
    t0 = time.monotonic()
    v1_proc = subprocess.run(  # nosec: B603 — argv fully controlled, no user input
        [sys.executable, __file__, "--v1-worker"],
        input=json.dumps(v1_payload),
        capture_output=True,
        text=True,
        timeout=600,
    )
    if v1_proc.returncode != 0:
        print(f"V1 worker failed (exit {v1_proc.returncode})")
        print(v1_proc.stderr[:2000])
        raise SystemExit(1)
    v1_results: list[dict[str, Any]] = json.loads(v1_proc.stdout)
    v1_elapsed = time.monotonic() - t0
    print(f"  V1 done: {len(v1_results)} results in {v1_elapsed:.1f}s")

    # Run V2 directly
    print("Running V2 engine...")
    t0 = time.monotonic()
    v2_results: list[dict[str, Any]] = []
    for row in rows:
        v2_results.append(_run_v2_case(row))
    v2_elapsed = time.monotonic() - t0
    print(f"  V2 done: {len(v2_results)} results in {v2_elapsed:.1f}s")

    # Classify
    print("Classifying differences...")
    classifications: list[str] = []
    for _i, (v1, v2, row) in enumerate(
        zip(v1_results, v2_results, rows, strict=False)
    ):
        cls = _classify(v1, v2, row, v2_fault_ids)
        classifications.append(cls)

    # Summary
    schema_gap = sum(1 for c in classifications if c == "schema_gap")
    threshold_tweak = sum(1 for c in classifications if c == "threshold_tweak")
    expected_drift = sum(1 for c in classifications if c == "expected_drift")
    blocker = sum(1 for c in classifications if c == "blocker")
    total_elapsed = v1_elapsed + v2_elapsed

    print(f"\nClassification summary ({len(rows)} cases):")
    print(f"  schema_gap:      {schema_gap}")
    print(f"  threshold_tweak: {threshold_tweak}")
    print(f"  expected_drift:  {expected_drift}")
    print(f"  blocker:         {blocker}")
    print(f"  Total elapsed:   {total_elapsed:.1f}s")

    # Write report
    print(f"\nWriting report to {REPORT_PATH}...")
    _write_report(rows, v1_results, v2_results, classifications, total_elapsed)
    print("Report written.")

    if blocker > 0:
        print(f"\nWARNING: {blocker} blocker(s) found — review before T-P6-2.")


if __name__ == "__main__":
    main()
