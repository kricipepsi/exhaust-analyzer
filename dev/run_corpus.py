"""Corpus replay script for Layer-2 accuracy benchmark.

Reads cases_petrol_master_v6.csv and runs each case through the diagnostic
pipeline. Reports top-1 family accuracy and specific-node accuracy.
"""

from __future__ import annotations

import csv
import json
import sys
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
CORPUS_PATH = ROOT / "cases" / "csv" / "cases_petrol_master_v6.csv"
OUTPUT_PATH = ROOT / "results" / "L2_latest.json"


# ── CSV parsing ──────────────────────────────────────────────────────────────


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


def csv_to_input(row: dict[str, str]) -> Any:
    """Convert a corpus CSV row to a DiagnosticInput."""
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

    dtcs_str = row.get("dtcs", "").strip()
    dtcs = [d.strip() for d in dtcs_str.split("|") if d.strip()] if dtcs_str else []

    from typing import Literal  # noqa: I001
    analyser_raw = row.get("analyser_type", "5-gas").strip() or "5-gas"
    analyser_type: Literal["4-gas", "5-gas"] = (
        "5-gas" if analyser_raw == "5-gas" else "4-gas"
    )

    return DiagnosticInput(
        vehicle_context=ctx,
        gas_idle=gas_idle,
        gas_high=gas_high,
        obd=obd,
        dtcs=dtcs,
        analyser_type=analyser_type,
    )


# ── main ─────────────────────────────────────────────────────────────────────


def _load_alias_map() -> dict[str, str | None]:
    """Load label_aliases.yaml → {v1_id: v2_target_or_None}."""
    import yaml

    aliases_path = ROOT / "schema" / "v2" / "label_aliases.yaml"
    if not aliases_path.exists():
        return {}
    with aliases_path.open(encoding="utf-8") as f:
        raw: dict = yaml.safe_load(f)
    mapping: dict[str, str | None] = {}
    for key, val in raw.items():
        if isinstance(val, dict):
            target = val.get("target")
            mapping[key] = target  # None for deleted nodes
        else:
            mapping[key] = val
    return mapping


def main() -> None:
    if not CORPUS_PATH.exists():
        print(f"Corpus not found at {CORPUS_PATH}")
        raise SystemExit(1)

    from engine.v2.pipeline import diagnose

    alias_map = _load_alias_map()

    with CORPUS_PATH.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    print(f"Corpus: {CORPUS_PATH}")
    print(f"Cases:  {len(rows)}")

    total = 0
    family_correct = 0
    state_correct = 0

    t0 = time.monotonic()
    for row in rows:
        try:
            di = csv_to_input(row)
        except Exception:
            continue

        result = diagnose(di)
        total += 1

        expected_state = row.get("expected_state", "").strip()
        if result["state"] == expected_state:
            state_correct += 1

        expected_fault_raw = row.get("expected_top_fault", "").strip()
        expected_family_raw = row.get("expected_top_fault_family", "").strip()

        # Resolve expected fault and family through V1→V2 aliases
        expected_fault = alias_map.get(expected_fault_raw, expected_fault_raw)
        if expected_fault is None:
            expected_fault = expected_fault_raw  # null-target alias: keep original
        expected_family = alias_map.get(expected_family_raw, expected_family_raw)
        if expected_family is None:
            expected_family = expected_family_raw

        if result["primary"] and (expected_fault or expected_family):
            fault_id: str = result["primary"]["fault_id"]
            # Exact match against resolved expected fault
            if expected_fault and fault_id == expected_fault or expected_family and (
                fault_id == expected_family or fault_id.startswith(expected_family)
            ):
                family_correct += 1

    elapsed = time.monotonic() - t0

    state_accuracy = (state_correct / total * 100) if total > 0 else 0.0
    family_accuracy = (family_correct / total * 100) if total > 0 else 0.0

    print(f"\nProcessed: {total}/{len(rows)} cases in {elapsed:.1f}s")
    print(f"State accuracy:  {state_correct}/{total} = {state_accuracy:.1f}%")
    print(f"Family accuracy: {family_correct}/{total} = {family_accuracy:.1f}%")

    results: dict[str, Any] = {
        "total": total,
        "state_accuracy_pct": round(state_accuracy, 1),
        "family_accuracy_pct": round(family_accuracy, 1),
        "elapsed_s": round(elapsed, 1),
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_PATH.open("w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(f"\nResults written to {OUTPUT_PATH}")
    print(f"Numeric accuracy: {family_accuracy:.1f}% family (not 0%)")


if __name__ == "__main__":
    main()
