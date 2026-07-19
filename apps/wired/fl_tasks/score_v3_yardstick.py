#!/usr/bin/env python3
"""Score any wired engine build against the frozen FL v3 yardstick."""

from __future__ import annotations

import argparse
import contextlib
import csv
import hashlib
import io
import json
import os
import subprocess
import sys
from collections import Counter
from collections.abc import Mapping, Sequence
from datetime import datetime
from pathlib import Path
from typing import Any

WORKSPACE_ROOT = Path(__file__).resolve().parents[3]
for relative in (
    "apps/wired",
    "labs/comlab",
    "labs/dnalab",
    "labs/dtclab",
    "labs/gaslab",
    "labs/obdlab",
    "labs/symptomlab",
    "labs/vinlab",
):
    path = str(WORKSPACE_ROOT / relative)
    if path not in sys.path:
        sys.path.insert(0, path)

from v7.load_corpus import DEFAULT_CSV_PATH, row_to_raw_inputs  # noqa: E402
from v7.run_suite import score_case  # noqa: E402
from wired.composition import diagnose  # noqa: E402

FL_YARDSTICK_NAME = "FL_YARDSTICK_2026-06-30"
V3_YARDSTICK_2026_06_30_NAME = "V3_YARDSTICK_2026-06-30"
V3_YARDSTICK_2026_07_01_NAME = "V3_YARDSTICK_2026-07-01"
V3_YARDSTICK_2026_07_05_NAME = "V3_YARDSTICK_2026-07-05"
V3_YARDSTICK_2026_07_05_C3B_NAME = "V3_YARDSTICK_2026-07-05-C3B"
V3_YARDSTICK_2026_07_05_C6B_NAME = "V3_YARDSTICK_2026-07-05-C6B"
V3_YARDSTICK_2026_07_06_C5B_NAME = "V3_YARDSTICK_2026-07-06-C5B"
V3_YARDSTICK_2026_07_06_C4B_NAME = "V3_YARDSTICK_2026-07-06-C4B"
V3_YARDSTICK_2026_07_06_C9B_NAME = "V3_YARDSTICK_2026-07-06-C9B"
V3_YARDSTICK_NAME = V3_YARDSTICK_2026_07_06_C9B_NAME
YARDSTICK_NAME = V3_YARDSTICK_2026_07_06_C9B_NAME
LOCALIZATION_NAME = "FL_LOCALIZATION_2026-06-30"
DEFAULT_LOCALIZATION_PATH = WORKSPACE_ROOT / "apps/wired/fl_tasks/reports/FL_LOCALIZATION_2026-06-30.md"
DEFAULT_BASELINE_RESULTS = WORKSPACE_ROOT / "apps/wired/v7/runs/20260630_163900/results.json"
SCORER_PATH = WORKSPACE_ROOT / "apps/wired/v7/run_suite.py"
FROZEN_WORKSPACE_COMMIT = "fe3b827cfa4c80b099873a6c3c4b17833b50ae98"
FL_CSV_SHA256 = "a94a7731bcc55a1ab826bdc46d5c9658d47dd86984902e3c93d7bab3be02a2ae"
FL_ORACLE_SUBSET_SHA256 = "a4de411098eb3c08d23d4881f4863fa1bd0a204cbb4041acb595474a1cecad7d"
V3_CSV_SHA256_2026_06_30 = "47182b3d9c4d4cb9e08645746a07fbae0d09b5db3d913fe00e1567965dd86dc9"
V3_ORACLE_SUBSET_SHA256_2026_06_30 = "192d7be1a339ce45afa7682d710ccfca7b1a0102bff447d037a63a64a73879f5"
V3_CSV_SHA256_2026_07_01 = "5e41bafe85f634f07050627661d411df20c71bdb0e4390b54d6b9787c108a809"
V3_ORACLE_SUBSET_SHA256_2026_07_01 = "3088a7c3d0c4b643e1dbf47b0ee05740a7d28416f08fe26a251cc3740948d127"
V3_CSV_SHA256_2026_07_05 = "3df2e8cbd82a866c3b8f12a72fdee837ac35cc1f09a19db65a10baa499282ddc"
V3_ORACLE_SUBSET_SHA256_2026_07_05 = "3088a7c3d0c4b643e1dbf47b0ee05740a7d28416f08fe26a251cc3740948d127"
V3_CSV_SHA256_2026_07_05_C3B = "9f530695dc3cf5586c9248a2b9de2f474950170326dcf5f62c1aefc36683e283"
V3_ORACLE_SUBSET_SHA256_2026_07_05_C3B = "3088a7c3d0c4b643e1dbf47b0ee05740a7d28416f08fe26a251cc3740948d127"
V3_CSV_SHA256_2026_07_05_C6B = "bf7393688230caf7f15054cc2473343e26351aa72c4615ca83044c7eb12fc0de"
V3_ORACLE_SUBSET_SHA256_2026_07_05_C6B = "3088a7c3d0c4b643e1dbf47b0ee05740a7d28416f08fe26a251cc3740948d127"
V3_CSV_SHA256_2026_07_06_C5B = "c49c17af1182a3eb07056a3fbf27c101378a32f35e375b18b3104d3928d8c7fd"
V3_ORACLE_SUBSET_SHA256_2026_07_06_C5B = "3088a7c3d0c4b643e1dbf47b0ee05740a7d28416f08fe26a251cc3740948d127"
V3_CSV_SHA256_2026_07_06_C4B = "1063be61234aaa27d4ddaf7b28a2f6a666270ebe77694445553562a4a6862136"
V3_ORACLE_SUBSET_SHA256_2026_07_06_C4B = "3088a7c3d0c4b643e1dbf47b0ee05740a7d28416f08fe26a251cc3740948d127"
V3_CSV_SHA256_2026_07_06_C9B = "8ec81201688d1354557d996e9a855260227eb922d561c571fd60813e9a430bfb"
V3_ORACLE_SUBSET_SHA256_2026_07_06_C9B = "3088a7c3d0c4b643e1dbf47b0ee05740a7d28416f08fe26a251cc3740948d127"
FROZEN_SCORER_SHA256 = "dc47eb4fc7701ae6e5b942c369411af51dca54c5aea4890f2bd401935cc75966"
ACTIVE_CSV_SHA256 = V3_CSV_SHA256_2026_07_06_C9B
ACTIVE_ORACLE_SUBSET_SHA256 = V3_ORACLE_SUBSET_SHA256_2026_07_06_C9B
ACTIVE_SCORER_SHA256 = FROZEN_SCORER_SHA256
SURFACE_DIMS = ("fault_code", "confidence", "perception_gap", "demotion_note_contains")
MODE_ORDER = ("SURFACE_DEFECT", "ORACLE_SUSPECT", "PRODUCER_GAP", "PRUNED_OTHER", "OUTRANKED", "DATA_GAP")
BUILD_ENV_KEYS = ("USE_V2_REGISTRY", "WIRED_OTEL")

# v3 metrics: top-3 + abstain thresholds from T-V3-0 report (v3/reports/V3_TOPK_CEILING_2026-06-30.md)
ABSTAIN_FLOOR = 0.80  # winner_score below this -> abstain
ABSTAIN_MARGIN = 0.02  # top1 - top2 within this -> abstain

def load_rule_family_map() -> dict[str, str]:
    """Load rule_id -> fault_family mapping from v2 registry rule JSONs.
    Mirrors v3/measure_topk.py:load_registry_rule_families().
    """
    rule_map: dict[str, str] = {}
    registry_rules_dir = WORKSPACE_ROOT / "labs/comlab/registry/rules"
    for fp in sorted(registry_rules_dir.glob("*.json")):
        import json
        data = json.loads(fp.read_text(encoding="utf-8"))
        fam = data.get("fault_family", "?")
        for rule in data.get("rules", []):
            rid = rule.get("rule_id", "")
            if rid:
                rule_map[rid] = fam
    return rule_map

def load_synthetic_case_ids() -> dict[str, set[str]]:
    """Return {cluster: case_ids} for every provisional-synthetic seed side file.

    T-SHIP-2 (canon `4DLab_CLAUDE.md`, Provisional synthetic signals, point 3): the
    scoreboard must keep a synthetic-vs-real split so no metric is mistaken for
    field accuracy. Provenance source = the `v3/data/*_synthetic_seed_*.csv` side
    files (the `synthetic=true` flag carriers). Missing directory -> empty map
    (split renders as all-real), never an error.
    """
    seed_dir = WORKSPACE_ROOT / "v3" / "data"
    clusters: dict[str, set[str]] = {}
    if not seed_dir.is_dir():
        return clusters
    for seed_path in sorted(seed_dir.glob("*_synthetic_seed_*.csv")):
        cluster = seed_path.name.split("_")[0].upper()
        with seed_path.open(newline="", encoding="utf-8") as handle:
            ids = {str(row["case_id"]) for row in csv.DictReader(handle) if row.get("case_id")}
        clusters.setdefault(cluster, set()).update(ids)
    return clusters


def sibling_family(sib: Mapping[str, Any], rule_map: Mapping[str, str]) -> str:
    """Resolve a differential sibling to its fault_family.

    Prefers explicit fault_family field if present (T-V3-3 engine change),
    otherwise maps fault_id via rule_map (current KG resolve).
    """
    # T-V3-3 will add fault_family to DifferentialSiblingOut
    fam = sib.get("fault_family")
    if fam:
        return str(fam)
    # Fallback: map fault_id via rule_map
    fid = sib.get("fault_id", "")
    if fid:
        return rule_map.get(fid, "unspecified")
    return "unspecified"


def collect_top3_families(
    winner_family: str,
    siblings: Sequence[Mapping[str, Any]],
    rule_map: Mapping[str, str],
) -> set[str]:
    """Return the 3-distinct-family top-3 window: winner + first 2 distinct sibling families.

    T-V3-D6-SCORERWIN correctness fix: ``top3_family`` must count three *distinct*
    families, as its name claims — not the first two sibling *entries*. Walking
    ``differential_siblings`` in rank order, collect non-winner sibling families until two
    distinct ones are gathered; skip ``unspecified``, the winner's own family, and any
    family already collected. Mirrors the family-aware dedupe precedent in T-V3-3C.
    """
    collected: list[str] = []
    for sib in siblings:
        if len(collected) >= 2:  # two distinct non-winner families is a full window
            break
        fam = sibling_family(sib, rule_map)
        if fam == "unspecified" or fam == winner_family or fam in collected:
            continue
        collected.append(fam)
    return {winner_family} | set(collected)


class YardstickRefusalError(RuntimeError):
    """Raised when the current files no longer match the frozen yardstick."""


class ScoreboardInputError(RuntimeError):
    """Raised when a supplied run result cannot be scored against the yardstick."""


def sha256_file(path: Path) -> str:
    """Return the SHA-256 digest of a file's exact bytes."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_csv_rows(csv_path: Path) -> list[dict[str, str]]:
    """Return corpus rows using the exact CSV header names."""
    with csv_path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def oracle_subset_sha256(rows: Sequence[Mapping[str, str]]) -> str:
    """Return the T-FL-1 oracle-subset digest for the loaded CSV rows."""
    expected_fields = [field for field in rows[0] if field.startswith("expected_")]
    fieldnames = ["case_id", "tag", *expected_fields, "accuracy_excluded"]
    lines = [",".join(fieldnames)]
    for row in rows:
        output = []
        for field in fieldnames:
            value = str(row.get(field, ""))
            if any(token in value for token in (",", '"', "\n", "\r")):
                value = '"' + value.replace('"', '""') + '"'
            output.append(value)
        lines.append(",".join(output))
    return hashlib.sha256(("\n".join(lines) + "\n").encode()).hexdigest()


def check_hash_lock(csv_path: Path, allow_new_yardstick: str | None = None) -> dict[str, Any]:
    """Verify the current corpus/oracle/scorer still match the active V3 yardstick."""
    rows = read_csv_rows(csv_path)
    observed = {
        "csv_sha256": sha256_file(csv_path),
        "oracle_subset_sha256": oracle_subset_sha256(rows),
        "scorer_sha256": sha256_file(SCORER_PATH),
    }
    expected = {
        "csv_sha256": ACTIVE_CSV_SHA256,
        "oracle_subset_sha256": ACTIVE_ORACLE_SUBSET_SHA256,
        "scorer_sha256": ACTIVE_SCORER_SHA256,
    }
    mismatches = [key for key, expected_value in expected.items() if observed[key] != expected_value]
    status = "ok" if not mismatches else "OVERRIDDEN" if allow_new_yardstick else "REFUSED"
    lock = {
        "yardstick": YARDSTICK_NAME,
        "status": status,
        "expected": expected,
        "observed": observed,
        "mismatches": mismatches,
        "override_yardstick": allow_new_yardstick,
    }
    if mismatches and not allow_new_yardstick:
        details = ", ".join(f"{key}: expected {expected[key]} observed {observed[key]}" for key in mismatches)
        raise YardstickRefusalError(
            f"hash-lock refusal: {YARDSTICK_NAME} mismatch ({details}). "
            "Create a new named yardstick or rerun with --allow-new-yardstick NAME."
        )
    return lock


def parse_localization_modes(localization_path: Path) -> dict[str, dict[str, str]]:
    """Read T-FL-3 case modes from the localization report's per-case table."""
    modes: dict[str, dict[str, str]] = {}
    in_table = False
    for line in localization_path.read_text(encoding="utf-8").splitlines():
        if line.startswith("| case_id | expected | predicted | stage_of_first_divergence | mode | evidence_ref |"):
            in_table = True
            continue
        if not in_table or not line.startswith("|") or line.startswith("| ---"):
            continue
        parts = [part.strip().strip("`") for part in line.strip().strip("|").split("|")]
        if len(parts) < 5:
            continue
        modes[parts[0]] = {
            "expected": parts[1],
            "predicted": parts[2],
            "stage": parts[3],
            "mode": parts[4],
        }
    return modes


def git_sha() -> str:
    """Return the current workspace commit, or an explicit unavailable marker."""
    try:
        completed = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=WORKSPACE_ROOT,
            check=True,
            capture_output=True,
            text=True,
            timeout=5,
        )
    except (OSError, subprocess.SubprocessError):
        return "unavailable"
    return completed.stdout.strip() or "unavailable"


def build_identity(label: str) -> dict[str, Any]:
    """Return the minimal build identity required for before/after comparison."""
    return {
        "label": label,
        "git_sha": git_sha(),
        "env": {key: os.environ.get(key, "<unset>") for key in BUILD_ENV_KEYS},
        "python": sys.executable,
        "captured_at": datetime.now().isoformat(timespec="seconds"),
    }


def baseline_identity() -> dict[str, Any]:
    """Return T-FL-1's frozen identity for the legacy baseline result JSON."""
    return {
        "label": "frozen-v2-baseline",
        "git_sha": FROZEN_WORKSPACE_COMMIT,
        "env": {"USE_V2_REGISTRY": "<unset>", "WIRED_OTEL": "<unset>"},
        "python": "/agent_workspace/.venv-wired/bin/python",
        "captured_at": "2026-06-30T16:39:00",
    }


def run_current_engine(rows: Sequence[Mapping[str, str]], show_engine_log: bool = False) -> list[dict[str, Any]]:
    """Run every corpus row through the public wired diagnose() path and score it."""
    results: list[dict[str, Any]] = []
    for row in rows:
        tag = str(row["tag"])
        result_dict: dict[str, Any] | None = None
        raised_exception: Exception | None = None
        try:
            raw_inputs = row_to_raw_inputs(dict(row))
            if show_engine_log:
                result = diagnose(raw_inputs, enable_fatal_gates=(tag == "invalid"))
            else:
                with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                    result = diagnose(raw_inputs, enable_fatal_gates=(tag == "invalid"))
            result_dict = result.model_dump()
        except Exception as exc:  # noqa: BLE001 - scoring needs the exception branch from v7.run_suite
            raised_exception = exc
        dimensions = score_case(result_dict, dict(row), raised_exception)
        crashed = raised_exception is not None and str(row.get("expected_crash_abort", "none")).strip() == "none"
        if crashed:
            outcome = "CRASH"
        elif tag == "invalid":
            outcome = "PASS" if all(value == "PASS" for value in dimensions.values()) else "FAIL"
        elif str(row.get("accuracy_excluded", "")).lower() == "true":
            outcome = "RAN" if raised_exception is None else "ERROR"
        else:
            outcome = "PASS" if all(value != "FAIL" for value in dimensions.values()) else "FAIL"
        results.append(
            {
                "case_id": row["case_id"],
                "category": row.get("source_category", ""),
                "tag": tag,
                "accuracy_excluded": str(row.get("accuracy_excluded", "")).lower() == "true",
                "crashed": crashed,
                "outcome": outcome,
                "dimensions": dimensions,
                "verdict": result_dict.get("diagnostic_verdict") if result_dict else None,
            }
        )
    return results


def load_result_rows(
    results_path: Path,
    rows_by_case: Mapping[str, Mapping[str, str]],
    force_rescore: bool = False,
) -> list[dict[str, Any]]:
    """Load an existing run_suite/scoreboard result set."""
    payload = json.loads(results_path.read_text(encoding="utf-8"))
    raw_results = payload.get("results")
    if not isinstance(raw_results, list):
        raise ScoreboardInputError(f"{results_path} does not contain a results[] array")
    loaded_by_case = {str(row.get("case_id")): row for row in raw_results if isinstance(row, dict)}
    missing = sorted(case_id for case_id in rows_by_case if case_id not in loaded_by_case)
    if missing:
        preview = ", ".join(missing[:5])
        raise ScoreboardInputError(f"{results_path} is missing {len(missing)} corpus rows; first missing: {preview}")
    scored: list[dict[str, Any]] = []
    for case_id, oracle_row in rows_by_case.items():
        source_row = loaded_by_case[case_id]
        verdict = source_row.get("verdict")
        stored_dimensions = source_row.get("dimensions")
        if isinstance(stored_dimensions, dict) and not force_rescore:
            dimensions = {key: str(value) for key, value in stored_dimensions.items()}
        else:
            result_dict = {"diagnostic_verdict": verdict} if verdict is not None else None
            dimensions = score_case(result_dict, dict(oracle_row), None)
        tag = str(oracle_row["tag"])
        accuracy_excluded = str(oracle_row.get("accuracy_excluded", "")).lower() == "true"
        if tag == "invalid":
            outcome = source_row.get("outcome", "FAIL")
        elif accuracy_excluded:
            outcome = "RAN" if verdict is not None else "ERROR"
        else:
            outcome = "PASS" if all(value != "FAIL" for value in dimensions.values()) else "FAIL"
        scored.append(
            {
                "case_id": case_id,
                "category": oracle_row.get("source_category", ""),
                "tag": tag,
                "accuracy_excluded": accuracy_excluded,
                "crashed": bool(source_row.get("crashed", False)),
                "outcome": outcome,
                "dimensions": dimensions,
                "verdict": verdict,
            }
        )
    return scored


def accuracy_rows(rows: Sequence[Mapping[str, str]]) -> list[Mapping[str, str]]:
    """Return the frozen denominator: non-invalid, non-excluded accuracy rows."""
    return [
        row
        for row in rows
        if str(row.get("tag", "")) != "invalid"
        and str(row.get("accuracy_excluded", "")).lower() != "true"
    ]


def primary_pass(dimensions: Mapping[str, str]) -> bool:
    """Return whether the primary family+state routing dimensions both pass."""
    return dimensions.get("fault_family") == "PASS" and dimensions.get("state") == "PASS"


def pct(numerator: int, denominator: int) -> float:
    """Return a safe percentage value."""
    return (numerator / denominator * 100.0) if denominator else 0.0


def summarize(
    *,
    label: str,
    result_rows: Sequence[Mapping[str, Any]],
    corpus_rows: Sequence[Mapping[str, str]],
    localization_modes: Mapping[str, Mapping[str, str]],
    identity: Mapping[str, Any],
) -> dict[str, Any]:
    """Build scoreboard metrics from a run result set."""
    results_by_case = {str(row["case_id"]): row for row in result_rows}
    denominator_rows = accuracy_rows(corpus_rows)
    missing_modes = sorted(row["case_id"] for row in denominator_rows if row["case_id"] not in localization_modes)
    if missing_modes:
        preview = ", ".join(missing_modes[:5])
        raise ScoreboardInputError(f"localization report misses {len(missing_modes)} accuracy rows: {preview}")

    # Load rule family map for sibling fault_id -> family resolution
    rule_map = load_rule_family_map()

    family: dict[str, dict[str, int]] = {}
    mode_totals: Counter[str] = Counter()
    mode_remaining_misses: Counter[str] = Counter()
    mode_primary_passes: Counter[str] = Counter()
    surface = {dim: {"PASS": 0, "FAIL": 0, "NA": 0} for dim in SURFACE_DIMS}
    primary_correct = 0
    family_only = 0
    state_only = 0

    # v3 metrics
    top3_family_pass = 0
    top3_on_covered_pass = 0
    total_abstained = 0
    covered_cases = 0  # non-abstained
    # T-SHIP-2: synthetic-vs-real split over top3_family banks
    synthetic_clusters = load_synthetic_case_ids()
    synthetic_ids: set[str] = set().union(*synthetic_clusters.values()) if synthetic_clusters else set()
    top3_banked_real = 0
    top3_banked_synthetic_by_cluster: Counter[str] = Counter()

    for row in denominator_rows:
        case_id = row["case_id"]
        result = results_by_case.get(case_id)
        if result is None:
            raise ScoreboardInputError(f"result set misses accuracy row {case_id}")
        dimensions = result.get("dimensions", {})
        verdict = result.get("verdict") or {}
        family_name = str(row.get("expected_fault_family", "unspecified")) or "unspecified"
        family.setdefault(family_name, {"total": 0, "family_pass": 0, "state_pass": 0, "primary_pass": 0})
        family[family_name]["total"] += 1

        # Check abstained flag
        abstained = bool(verdict.get("abstained", False))
        if abstained:
            total_abstained += 1
        else:
            covered_cases += 1

        # Primary (single-verdict) metrics - only for non-abstained cases
        if not abstained:
            if dimensions.get("fault_family") == "PASS":
                family[family_name]["family_pass"] += 1
                family_only += 1
            if dimensions.get("state") == "PASS":
                family[family_name]["state_pass"] += 1
                state_only += 1
            passed_primary = primary_pass(dimensions)
            if passed_primary:
                family[family_name]["primary_pass"] += 1
                primary_correct += 1
        else:
            passed_primary = False

        # v3: top3_family - expected family in {winner} U {first 2 distinct sibling families}
        # T-V3-D6-SCORERWIN: count 3 DISTINCT families, not the first 2 sibling entries.
        winner_family = verdict.get("fault_family", "")
        differential_siblings = verdict.get("differential_siblings", [])
        top3_families = collect_top3_families(winner_family, differential_siblings, rule_map)
        top3_hit = family_name in top3_families

        if top3_hit:
            top3_family_pass += 1
            if not abstained:
                top3_on_covered_pass += 1
            if case_id in synthetic_ids:
                for cluster, ids in synthetic_clusters.items():
                    if case_id in ids:
                        top3_banked_synthetic_by_cluster[cluster] += 1
                        break
            else:
                top3_banked_real += 1

        mode = localization_modes[case_id]["mode"]
        mode_totals[mode] += 1
        if not abstained:
            if passed_primary:
                mode_primary_passes[mode] += 1
            else:
                mode_remaining_misses[mode] += 1

        for dim in SURFACE_DIMS:
            value = str(dimensions.get(dim, "NA"))
            surface[dim][value if value in ("PASS", "FAIL", "NA") else "NA"] += 1

    denominator = len(denominator_rows)
    oracle_suspect_total = mode_totals["ORACLE_SUSPECT"]
    adjudicated_primary = primary_correct + oracle_suspect_total

    # v3 metric calculations
    coverage = covered_cases / denominator if denominator else 0.0
    top3_on_covered_pct = pct(top3_on_covered_pass, covered_cases) if covered_cases else 0.0

    return {
        "label": label,
        "identity": dict(identity),
        "total_run": len(result_rows),
        "accuracy_denominator": denominator,
        "overall": {
            "family_pass": family_only,
            "state_pass": state_only,
            "primary_pass": primary_correct,
            "primary_pct": pct(primary_correct, denominator),
            "adjudicated_primary_pass": adjudicated_primary,
            "adjudicated_primary_pct": pct(adjudicated_primary, denominator),
            "oracle_suspect_adjustment": oracle_suspect_total,
            # v3 metrics
            "top3_family_pass": top3_family_pass,
            "top3_family_pct": pct(top3_family_pass, denominator),
            "coverage": coverage,
            "top3_on_covered_pass": top3_on_covered_pass,
            "top3_on_covered_pct": top3_on_covered_pct,
            "total_abstained": total_abstained,
            # T-SHIP-2 synthetic-vs-real split (canon Provisional-synthetic #3)
            "top3_banked_real": top3_banked_real,
            "top3_banked_real_pct": pct(top3_banked_real, denominator),
            "top3_banked_synthetic": int(sum(top3_banked_synthetic_by_cluster.values())),
            "top3_banked_synthetic_by_cluster": dict(sorted(top3_banked_synthetic_by_cluster.items())),
        },
        "family": dict(sorted(family.items())),
        "mode_totals": {mode: mode_totals.get(mode, 0) for mode in MODE_ORDER},
        "mode_primary_passes": {mode: mode_primary_passes.get(mode, 0) for mode in MODE_ORDER},
        "mode_remaining_primary_misses": {mode: mode_remaining_misses.get(mode, 0) for mode in MODE_ORDER},
        "surface_dimensions": surface,
    }


def write_scoreboard_result(
    output_path: Path,
    *,
    rows: Sequence[Mapping[str, Any]],
    hash_lock: Mapping[str, Any],
    identity: Mapping[str, Any],
    summary: Mapping[str, Any],
) -> None:
    """Write a comparison-ready result set under an ignored run directory."""
    payload = {
        "schema": "wired-fl-scoreboard-result-v1",
        "timestamp": datetime.now().strftime("%Y%m%d_%H%M%S"),
        "yardstick": hash_lock,
        "build_identity": identity,
        "summary": summary,
        "results": list(rows),
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def identity_for_loaded_result(results_path: Path) -> dict[str, Any]:
    """Return recorded identity from a result JSON, or the frozen baseline identity."""
    payload = json.loads(results_path.read_text(encoding="utf-8"))
    if isinstance(payload.get("build_identity"), dict):
        return payload["build_identity"]
    if results_path.resolve() == DEFAULT_BASELINE_RESULTS.resolve():
        return baseline_identity()
    return {
        "label": results_path.name,
        "git_sha": "unrecorded",
        "env": {key: "unrecorded" for key in BUILD_ENV_KEYS},
        "python": "unrecorded",
        "captured_at": "unrecorded",
    }


def render_score(summary: Mapping[str, Any], hash_lock: Mapping[str, Any], result_source: str) -> str:
    """Render one scoreboard summary for terminal use."""
    overall = summary["overall"]
    denominator = int(summary["accuracy_denominator"])
    lines = [
        "WIRED-FL V3 SCOREBOARD — SCORE",
        f"Yardstick: {YARDSTICK_NAME}; localization: {LOCALIZATION_NAME}",
        f"Hash lock: {hash_lock['status']}",
        f"Result source: {result_source}",
        _identity_line("Build", summary["identity"]),
        "",
        "OVERALL PRIMARY ROUTING (frozen single-verdict baseline)",
        f"  family+state: {overall['primary_pass']}/{denominator} = {overall['primary_pct']:.2f} %",
        f"  family only : {overall['family_pass']}/{denominator} = {pct(int(overall['family_pass']), denominator):.2f} %",
        f"  state only  : {overall['state_pass']}/{denominator} = {pct(int(overall['state_pass']), denominator):.2f} %",
        f"  adjudicated : {overall['adjudicated_primary_pass']}/{denominator} = {overall['adjudicated_primary_pct']:.2f} % (ORACLE_SUSPECT +{overall['oracle_suspect_adjustment']})",
        "",
        "V3 TOP-3 + ABSTAIN METRICS",
        f"  top3_family       : {overall.get('top3_family_pass', 0)}/{denominator} = {overall.get('top3_family_pct', 0.0):.2f} %",
        f"  coverage          : {overall.get('coverage', 0.0):.2f}  ({int(denominator * overall.get('coverage', 0.0))}/{denominator} non-abstained)",
        f"  top3_on_covered   : {overall.get('top3_on_covered_pass', 0)}/{int(denominator * overall.get('coverage', 0.0)) or 0} = {overall.get('top3_on_covered_pct', 0.0):.2f} %",
        f"  total_abstained   : {overall.get('total_abstained', 0)}",
        f"  abstain_floor     : {ABSTAIN_FLOOR}  (winner_score < floor -> abstain)",
        f"  abstain_margin    : {ABSTAIN_MARGIN}  (top1 - top2 <= margin -> abstain)",
        "",
        "SYNTHETIC-VS-REAL SPLIT (canon: not field accuracy until real data replaces seeds)",
        f"  banked on real-only columns : {overall.get('top3_banked_real', 0)}/{denominator} = {overall.get('top3_banked_real_pct', 0.0):.2f} %",
        f"  banked with synthetic seeds : {overall.get('top3_banked_synthetic', 0)}"
        + (
            "  (" + ", ".join(f"{k} {v}" for k, v in overall.get("top3_banked_synthetic_by_cluster", {}).items()) + ")"
            if overall.get("top3_banked_synthetic_by_cluster") else ""
        ),
        "",
        "PER-FAMILY PRIMARY ROUTING",
        table(
            ("Family", "Cases", "Primary", "%"),
            [
                (family, data["total"], data["primary_pass"], f"{pct(data['primary_pass'], data['total']):.1f}")
                for family, data in summary["family"].items()
            ],
        ),
        "",
        "PER-MODE COUNTS (frozen T-FL-3 buckets; remaining misses are lower-is-better)",
        table(
            ("Mode", "Bucket", "Primary pass", "Remaining miss"),
            [
                (
                    mode,
                    summary["mode_totals"].get(mode, 0),
                    summary["mode_primary_passes"].get(mode, 0),
                    summary["mode_remaining_primary_misses"].get(mode, 0),
                )
                for mode in MODE_ORDER
            ],
        ),
        "",
        "SURFACE DIMENSIONS (reported separately; T-FL-1 non-fail = PASS + NA)",
        table(
            ("Dimension", "Non-fail", "FAIL", "Raw PASS", "Raw NA"),
            [
                (dim, data["PASS"] + data["NA"], data["FAIL"], data["PASS"], data["NA"])
                for dim, data in summary["surface_dimensions"].items()
            ],
        ),
    ]
    return "\n".join(lines)


def render_compare(before: Mapping[str, Any], after: Mapping[str, Any], hash_lock: Mapping[str, Any]) -> str:
    """Render a before/after delta report."""
    before_overall = before["overall"]
    after_overall = after["overall"]
    denominator = int(before["accuracy_denominator"])
    before_primary = int(before_overall["primary_pass"])
    after_primary = int(after_overall["primary_pass"])
    lines = [
        "WIRED-FL V3 SCOREBOARD — COMPARE",
        f"Yardstick: {YARDSTICK_NAME}; localization: {LOCALIZATION_NAME}",
        f"Hash lock: {hash_lock['status']}",
        _identity_line("Before", before["identity"]),
        _identity_line("After ", after["identity"]),
        "",
        "OVERALL DELTA (primary family+state; higher is better)",
        f"  {before_primary}/{denominator} ({pct(before_primary, denominator):.2f} %) -> {after_primary}/{denominator} ({pct(after_primary, denominator):.2f} %); Δ {after_primary - before_primary:+d} cases / {pct(after_primary - before_primary, denominator):+.2f} pp",
        "",
        "PER-FAMILY DELTA (primary family+state passes; higher is better)",
        table(
            ("Family", "Cases", "Before", "After", "Δ cases", "Δ pp"),
            [
                _family_delta_row(family, before["family"][family], after["family"][family])
                for family in before["family"]
            ],
        ),
        "",
        "PER-MODE DELTA (remaining primary misses in frozen T-FL-3 buckets; lower is better)",
        table(
            ("Mode", "Bucket", "Before miss", "After miss", "Δ misses"),
            [
                (
                    mode,
                    before["mode_totals"].get(mode, 0),
                    before["mode_remaining_primary_misses"].get(mode, 0),
                    after["mode_remaining_primary_misses"].get(mode, 0),
                    after["mode_remaining_primary_misses"].get(mode, 0) - before["mode_remaining_primary_misses"].get(mode, 0),
                )
                for mode in MODE_ORDER
            ],
        ),
    ]
    return "\n".join(lines)


def top3_family_pass(result: Mapping[str, Any], expected_family: str, rule_map: Mapping[str, str]) -> bool:
    """Return whether the expected family is in the 3-distinct-family top-3 window.

    T-V3-D6-SCORERWIN: the window is winner + first 2 distinct non-winner sibling
    families (see ``collect_top3_families``), so this helper and the main loop agree.
    """
    verdict = result.get("verdict")
    if not isinstance(verdict, Mapping):
        verdict = {}
    winner_family = str(verdict.get("fault_family", ""))
    siblings = verdict.get("differential_siblings", [])
    if not isinstance(siblings, list):
        siblings = []
    families = collect_top3_families(winner_family, siblings, rule_map)
    return expected_family in families


def v3_case_metrics(result: Mapping[str, Any], expected_family: str, rule_map: Mapping[str, str]) -> dict[str, bool]:
    """Classify one case on the v3 single-verdict plus top-3 pass surface."""
    dimensions = result.get("dimensions", {})
    if not isinstance(dimensions, Mapping):
        dimensions = {}
    single_verdict = primary_pass({key: str(value) for key, value in dimensions.items()})
    top3_family = top3_family_pass(result, expected_family, rule_map)
    return {
        "single_verdict": single_verdict,
        "top3_family": top3_family,
        "passed": single_verdict or top3_family,
    }


def diff_result_sets(
    *,
    before_rows: Sequence[Mapping[str, Any]],
    after_rows: Sequence[Mapping[str, Any]],
    corpus_rows: Sequence[Mapping[str, str]],
    localization_modes: Mapping[str, Mapping[str, str]],
) -> dict[str, Any]:
    """Build per-case v3 movement and regression rows for two result sets."""
    before_by_case = {str(row["case_id"]): row for row in before_rows}
    after_by_case = {str(row["case_id"]): row for row in after_rows}
    rule_map = load_rule_family_map()
    rows: list[dict[str, Any]] = []
    regressions: list[str] = []
    family_net: dict[str, dict[str, int]] = {}

    for oracle_row in accuracy_rows(corpus_rows):
        case_id = oracle_row["case_id"]
        if case_id not in before_by_case:
            raise ScoreboardInputError(f"before result set misses accuracy row {case_id}")
        if case_id not in after_by_case:
            raise ScoreboardInputError(f"after result set misses accuracy row {case_id}")
        if case_id not in localization_modes:
            raise ScoreboardInputError(f"localization report misses accuracy row {case_id}")
        expected_family = str(oracle_row.get("expected_fault_family", "unspecified")) or "unspecified"
        before_metrics = v3_case_metrics(before_by_case[case_id], expected_family, rule_map)
        after_metrics = v3_case_metrics(after_by_case[case_id], expected_family, rule_map)
        before_passed = before_metrics["passed"]
        after_passed = after_metrics["passed"]
        if before_passed and not after_passed:
            movement = "newly_fail"
            regressions.append(case_id)
        elif not before_passed and after_passed:
            movement = "newly_pass"
        else:
            movement = "unchanged"

        family_counts = family_net.setdefault(expected_family, {"total": 0, "newly_pass": 0, "newly_fail": 0, "net": 0})
        family_counts["total"] += 1
        if movement == "newly_pass":
            family_counts["newly_pass"] += 1
            family_counts["net"] += 1
        elif movement == "newly_fail":
            family_counts["newly_fail"] += 1
            family_counts["net"] -= 1

        before_mode = "PASS" if before_passed else localization_modes[case_id]["mode"]
        after_mode = "PASS" if after_passed else localization_modes[case_id]["mode"]
        rows.append(
            {
                "case_id": case_id,
                "expected_family": expected_family,
                "movement": movement,
                "before_mode": before_mode,
                "after_mode": after_mode,
                "failure_mode_change": f"{before_mode}->{after_mode}",
                "before_single_verdict": before_metrics["single_verdict"],
                "after_single_verdict": after_metrics["single_verdict"],
                "before_top3_family": before_metrics["top3_family"],
                "after_top3_family": after_metrics["top3_family"],
            }
        )

    movement_counts = Counter(str(row["movement"]) for row in rows)
    return {
        "movement_counts": {
            "newly_pass": movement_counts.get("newly_pass", 0),
            "newly_fail": movement_counts.get("newly_fail", 0),
            "unchanged": movement_counts.get("unchanged", 0),
        },
        "family_net": dict(sorted(family_net.items())),
        "regressions": regressions,
        "cases": rows,
    }


def render_diff(
    diff: Mapping[str, Any],
    hash_lock: Mapping[str, Any],
    before_identity: Mapping[str, Any],
    after_identity: Mapping[str, Any],
) -> str:
    """Render a per-case v3 movement report."""
    movement_counts = diff["movement_counts"]
    regressions = diff["regressions"]
    family_net = diff["family_net"]
    cases = diff["cases"]
    lines = [
        "WIRED-FL V3 SCOREBOARD — DIFF",
        f"Yardstick: {YARDSTICK_NAME}; localization: {LOCALIZATION_NAME}",
        f"Hash lock: {hash_lock['status']}",
        _identity_line("Before", before_identity),
        _identity_line("After ", after_identity),
        "",
        "MOVEMENT SUMMARY (v3 pass = single_verdict OR top3_family)",
        f"  newly_pass : {movement_counts['newly_pass']}",
        f"  newly_fail : {movement_counts['newly_fail']}",
        f"  unchanged  : {movement_counts['unchanged']}",
        f"REGRESSIONS: {', '.join(regressions) if regressions else '(empty)'}",
        "",
        "PER-FAMILY NET MOVEMENT",
        table(
            ("Family", "Cases", "Newly pass", "Newly fail", "Net"),
            [
                (family, data["total"], data["newly_pass"], data["newly_fail"], f"{data['net']:+d}")
                for family, data in family_net.items()
            ],
        ),
        "",
        "PER-CASE MOVEMENT",
        table(
            ("Case", "Family", "Movement", "Mode change", "Single B->A", "Top3 B->A"),
            [
                (
                    row["case_id"],
                    row["expected_family"],
                    row["movement"],
                    row["failure_mode_change"],
                    f"{row['before_single_verdict']}->{row['after_single_verdict']}",
                    f"{row['before_top3_family']}->{row['after_top3_family']}",
                )
                for row in cases
            ],
        ),
    ]
    return "\n".join(lines)


def write_diff_artifacts(diff: Mapping[str, Any], *, json_path: Path | None = None, md_path: Path | None = None) -> None:
    """Optionally write the per-case movement report as JSON and Markdown."""
    if json_path is not None:
        json_path.parent.mkdir(parents=True, exist_ok=True)
        json_path.write_text(json.dumps(diff, indent=2, sort_keys=True), encoding="utf-8")
    if md_path is not None:
        md_path.parent.mkdir(parents=True, exist_ok=True)
        md_path.write_text(
            table(
                ("Case", "Family", "Movement", "Mode change", "Single B->A", "Top3 B->A"),
                [
                    (
                        row["case_id"],
                        row["expected_family"],
                        row["movement"],
                        row["failure_mode_change"],
                        f"{row['before_single_verdict']}->{row['after_single_verdict']}",
                        f"{row['before_top3_family']}->{row['after_top3_family']}",
                    )
                    for row in diff["cases"]
                ],
            )
            + "\n",
            encoding="utf-8",
        )


def _family_delta_row(family: str, before: Mapping[str, int], after: Mapping[str, int]) -> tuple[Any, ...]:
    total = before["total"]
    delta = after["primary_pass"] - before["primary_pass"]
    return (family, total, before["primary_pass"], after["primary_pass"], f"{delta:+d}", f"{pct(delta, total):+.1f}")


def _identity_line(prefix: str, identity: Mapping[str, Any]) -> str:
    env = identity.get("env", {})
    env_text = ", ".join(f"{key}={env.get(key, 'unrecorded')}" for key in BUILD_ENV_KEYS)
    return f"{prefix}: git_sha={identity.get('git_sha', 'unrecorded')} env=({env_text}) label={identity.get('label', 'unlabeled')}"


def table(headers: Sequence[Any], rows: Sequence[Sequence[Any]]) -> str:
    """Render a compact GitHub-flavored Markdown table."""
    text_rows = [[str(cell) for cell in row] for row in rows]
    header = [str(cell) for cell in headers]
    widths = [len(cell) for cell in header]
    for row in text_rows:
        for index, cell in enumerate(row):
            widths[index] = max(widths[index], len(cell))
    lines = [
        "| " + " | ".join(cell.ljust(widths[index]) for index, cell in enumerate(header)) + " |",
        "| " + " | ".join("-" * widths[index] for index in range(len(widths))) + " |",
    ]
    lines.extend(
        "| " + " | ".join(cell.ljust(widths[index]) for index, cell in enumerate(row)) + " |"
        for row in text_rows
    )
    return "\n".join(lines)


def load_inputs(csv_path: Path, localization_path: Path) -> tuple[list[dict[str, str]], dict[str, dict[str, str]]]:
    """Load the corpus and the frozen T-FL-3 localization map."""
    rows = read_csv_rows(csv_path)
    return rows, parse_localization_modes(localization_path)


def command_score(args: argparse.Namespace) -> int:
    """Run or load one result set, then print scoreboard metrics."""
    csv_path = Path(args.csv).resolve()
    hash_lock = check_hash_lock(csv_path, args.allow_new_yardstick)
    rows, modes = load_inputs(csv_path, Path(args.localization).resolve())
    rows_by_case = {row["case_id"]: row for row in rows}
    if args.results:
        result_source = str(Path(args.results).resolve())
        result_rows = load_result_rows(Path(args.results).resolve(), rows_by_case, force_rescore=bool(args.allow_new_yardstick))
        identity = identity_for_loaded_result(Path(args.results).resolve())
    else:
        result_source = "current installed wired engine"
        identity = build_identity(args.label)
        result_rows = run_current_engine(rows, show_engine_log=args.show_engine_log)
    summary = summarize(
        label=args.label,
        result_rows=result_rows,
        corpus_rows=rows,
        localization_modes=modes,
        identity=identity,
    )
    if args.write_results:
        write_scoreboard_result(Path(args.write_results).resolve(), rows=result_rows, hash_lock=hash_lock, identity=identity, summary=summary)
    print(render_score(summary, hash_lock, result_source))
    if args.write_results:
        print(f"\nWrote comparison-ready result set: {Path(args.write_results).resolve()}")
    return 0


def command_compare(args: argparse.Namespace) -> int:
    """Compare two result sets on the frozen yardstick."""
    csv_path = Path(args.csv).resolve()
    hash_lock = check_hash_lock(csv_path, args.allow_new_yardstick)
    rows, modes = load_inputs(csv_path, Path(args.localization).resolve())
    rows_by_case = {row["case_id"]: row for row in rows}
    before_path = Path(args.before).resolve()
    after_path = Path(args.after).resolve()
    before_rows = load_result_rows(before_path, rows_by_case)
    after_rows = load_result_rows(after_path, rows_by_case)
    before = summarize(
        label="before",
        result_rows=before_rows,
        corpus_rows=rows,
        localization_modes=modes,
        identity=identity_for_loaded_result(before_path),
    )
    after = summarize(
        label="after",
        result_rows=after_rows,
        corpus_rows=rows,
        localization_modes=modes,
        identity=identity_for_loaded_result(after_path),
    )
    print(render_compare(before, after, hash_lock))
    return 0


def command_diff(args: argparse.Namespace) -> int:
    """Compare two result sets case-by-case on the v3 pass surface."""
    csv_path = Path(args.csv).resolve()
    hash_lock = check_hash_lock(csv_path, args.allow_new_yardstick)
    rows, modes = load_inputs(csv_path, Path(args.localization).resolve())
    rows_by_case = {row["case_id"]: row for row in rows}
    before_path = Path(args.before).resolve()
    after_path = Path(args.after).resolve()
    before_rows = load_result_rows(before_path, rows_by_case)
    after_rows = load_result_rows(after_path, rows_by_case)
    diff = diff_result_sets(
        before_rows=before_rows,
        after_rows=after_rows,
        corpus_rows=rows,
        localization_modes=modes,
    )
    print(render_diff(diff, hash_lock, identity_for_loaded_result(before_path), identity_for_loaded_result(after_path)))
    write_diff_artifacts(diff, json_path=args.write_json, md_path=args.write_md)
    if args.write_json:
        print(f"\nWrote per-case diff JSON: {Path(args.write_json).resolve()}")
    if args.write_md:
        print(f"\nWrote per-case diff Markdown: {Path(args.write_md).resolve()}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser for score and compare operations."""
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    score_parser = subparsers.add_parser("score", help="score one result set or the current engine")
    add_common_args(score_parser)
    score_parser.add_argument("--results", type=Path, help="existing run_suite/scoreboard result JSON to score")
    score_parser.add_argument("--write-results", type=Path, help="write comparison-ready result JSON")
    score_parser.add_argument("--label", default="current-engine", help="build label recorded for a live run")
    score_parser.add_argument("--show-engine-log", action="store_true", help="do not suppress engine stdout/stderr during live scoring")
    score_parser.set_defaults(func=command_score)

    compare_parser = subparsers.add_parser("compare", help="compare two result JSON files")
    add_common_args(compare_parser)
    compare_parser.add_argument("--before", type=Path, required=True, help="baseline/before result JSON")
    compare_parser.add_argument("--after", type=Path, required=True, help="candidate/after result JSON")
    compare_parser.set_defaults(func=command_compare)

    diff_parser = subparsers.add_parser("diff", help="compare two result JSON files case-by-case")
    add_common_args(diff_parser)
    diff_parser.add_argument("--before", type=Path, required=True, help="baseline/before result JSON")
    diff_parser.add_argument("--after", type=Path, required=True, help="candidate/after result JSON")
    diff_parser.add_argument("--write-json", type=Path, help="write per-case movement JSON")
    diff_parser.add_argument("--write-md", type=Path, help="write per-case movement Markdown table")
    diff_parser.set_defaults(func=command_diff)
    return parser


def add_common_args(parser: argparse.ArgumentParser) -> None:
    """Add yardstick-bound input arguments shared by every subcommand."""
    parser.add_argument("--csv", type=Path, default=DEFAULT_CSV_PATH, help="frozen v7 corpus CSV")
    parser.add_argument(
        "--localization",
        type=Path,
        default=DEFAULT_LOCALIZATION_PATH,
        help="frozen T-FL-3 localization report",
    )
    parser.add_argument(
        "--allow-new-yardstick",
        metavar="NAME",
        help="override hash refusal only after creating/naming a replacement yardstick",
    )


def main(argv: Sequence[str] | None = None) -> int:
    """CLI entry point."""
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except (ScoreboardInputError, YardstickRefusalError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
