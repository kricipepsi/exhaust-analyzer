"""
AUDIT-CORPUS: one-shot curation script.

Reads cases_petrol_master_v6.csv + cvsgaps.md + Jaeger failure blueprint
and emits corpus_curated.csv + corpus_meta.json.

Idempotent — re-running on the same inputs produces the same outputs.
"""
from __future__ import annotations

import csv
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field

__all__ = [
    "CaseMeta",
    "CorpusMeta",
    "main",
    "print_summary",
]

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

REGISTRY_DIR = Path(__file__).resolve().parents[1]
WORKSPACE = Path(__file__).resolve().parents[4]
MASTER_CSV = WORKSPACE / "apps" / "wired" / "harness" / "data" / "cases_petrol_master_v6.csv"
BLUEPRINT = (
    WORKSPACE
    / "apps"
    / "wired"
    / "_jaeger"
    / "runs"
    / "20260527-044325"
    / "FAILURE_BLUEPRINT.md"
)
OUT_DIR = REGISTRY_DIR
CURATED_CSV = OUT_DIR / "corpus_curated.csv"
META_JSON = OUT_DIR / "corpus_meta.json"

# ---------------------------------------------------------------------------
# Pydantic models (inline — no registry package dependency)
# ---------------------------------------------------------------------------

Disposition = Literal["keep", "drop", "relabel", "new"]
Source = Literal["cvsgaps", "jaeger", "csv", "new"]


class CaseMeta(BaseModel):
    case_id: str
    expected_top_fault_family: str
    disposition: Disposition
    relabel_to: str | None = None
    rationale: str
    source: Source
    chemistry_signature: str | None = None
    dtcs: list[str] = Field(default_factory=list)
    notes: str | None = None


class CorpusMeta(BaseModel):
    generated_at: str
    master_csv_total: int
    curated_count: int
    dropped_count: int
    relabel_count: int
    new_count: int
    cases: list[CaseMeta]


# ---------------------------------------------------------------------------
# cvsgaps.md proposed dispositions (extracted and verified against the doc)
# ---------------------------------------------------------------------------

# Each entry: (category, rationale_tag, set of case_ids)
CVSGAPS_DROP_PROPOSALS: list[tuple[str, str, set[str]]] = [
    # §1 — Invalid input / sentinel cases (keep 2-3, ditch the rest)
    (
        "sentinel_invalid_input",
        "Analyser or probe error, not an engine fault. Sentinel/validation-only case.",
        {
            "CSV-081", "CSV-083", "YAML-CSV81", "YAML-CSV83",
            "CASE-041", "CASE-043", "CASE-045", "CASE-046", "CASE-047", "CASE-048",
            "case_020", "case_021",
            "case_011",
            "YAML-CSV16", "YAML-CSV100",
            "RULE-NOx-1", "YAML-RULE_CO2_1", "YAML-RULE_NOx_1",
            "YAML-TC11", "YAML-TC21", "YAML-TC48",
            "YAML-PDF_HI_007", "YAML-PDF_HI_008",
        },
    ),
    # §2 — Obsolete / extremely rare hardware
    (
        "obsolete_hardware",
        "Obsolete or extremely rare hardware: leaded fuel, SAI, GPF, swirl flaps — out of petrol v1 scope.",
        {
            "CASE-010",
            "CSV-129", "CSV-130", "EXT-238", "EXT-239",
            "EXP-N025",
            "EXP-N029",
        },
    ),
    # §3 — Overly contrived / low-probability multi-fault combinations
    (
        "contrived_multifault",
        "Overly contrived or extremely low-probability multi-fault combination.",
        {
            "EXP-N019", "case_038",
            "CASE-028", "CASE-029",
            "EXP-N030",
            "EXP-N022",
        },
    ),
    # §4 — Hybrid-only edge cases
    (
        "hybrid_only",
        "Hybrid-only edge case — out of petrol v1 scope per PRD §5.",
        {"EXP-N018", "CASE-039"},
    ),
    # §5 — Altitude / BARO edge cases
    (
        "altitude_baro_edge",
        "Altitude/BARO edge case — low real-world diagnostic impact, context-dependent.",
        {"case_014", "CASE-022"},
    ),
    # §6 — Duplicates / over-represented scenarios
    (
        "duplicate_baseline",
        "Duplicate or over-represented scenario — covered by other cases in the corpus.",
        {
            "case_040", "case_043",
            "PDF-HI-005", "PDF-HI-010",
            "YAML-TC1", "YAML-CSV1",
            "CASE-041",  # also in §1 but listed here for exhaust-leak-at-probe duplication
        },
    ),
]

# Sentinels to explicitly KEEP (cvsgaps says "keep 2-3")
CVSGAPS_KEEP_SENTINELS = {"CSV-081", "CASE-046", "case_011"}

# Healthy baselines to keep (cvsgaps says "keep 2-3 of ...")
CVSGAPS_KEEP_BASELINES = {"PDF-HI-005", "PDF-HI-010", "YAML-TC1"}

# New families to add (from cvsgaps.md "Practical Action Plan")
NEW_FAMILIES: list[dict] = [
    {
        "family": "vacuum_leak",
        "count": 4,
        "rationale": "Vacuum leak is the most frequent root cause of lean-condition DTCs. "
        "Dedicated family enables precise evaluation of a separate diagnostic pathway "
        "distinct from fuel-delivery lean.",
        "detection_signal": "Lean trims at idle that correct at 2500 RPM (Brettschneider-confirmed).",
    },
    {
        "family": "overheating",
        "count": 4,
        "rationale": "Cooling system faults are a leading engine problem. "
        "Minimal dedicated testing exists in the current corpus.",
        "detection_signal": "High coolant temp + RPM behaviour; not always DTC-driven.",
    },
    {
        "family": "charging_system",
        "count": 3,
        "rationale": "Alternator and battery are crucial for modern ECUs. "
        "Sensor drift or noise from a failing alternator can trigger spurious faults.",
        "detection_signal": "Low/bouncing voltage, sensor noise, ghost misfires.",
    },
]

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def load_master_csv() -> tuple[list[str], list[dict]]:
    """Return (fieldnames, rows) from the master CSV."""
    with open(MASTER_CSV, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames or [])
        rows = list(reader)
    return fieldnames, rows


def parse_blueprint() -> dict[str, dict]:
    """
    Parse FAILURE_BLUEPRINT.md, deduplicate, return per-case v1 behaviour.

    Returns: {case_id: {expected_family, predicted_family, match_status, phase, drop_reason}}
    """
    text = BLUEPRINT.read_text(encoding="utf-8")
    cases: dict[str, dict] = {}
    in_table = False
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("| case_id |"):
            in_table = True
            continue
        if in_table and line.startswith("| ") and not line.startswith("| case_id"):
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 7:
                cid = parts[1]
                if cid in ("", "case_id", "UNKNOWN"):
                    continue
                if cid not in cases:
                    cases[cid] = {
                        "expected_family": parts[2],
                        "predicted_family": parts[3],
                        "match_status": parts[4],
                        "phase": parts[5],
                        "drop_reason": parts[6],
                    }
    return cases


def build_cvsgaps_map() -> dict[str, tuple[str, str]]:
    """
    Build {case_id: (category, rationale)} from cvsgaps proposals.
    """
    mapping: dict[str, tuple[str, str]] = {}
    for category, rationale, case_ids in CVSGAPS_DROP_PROPOSALS:
        for cid in case_ids:
            mapping[cid] = (category, rationale)
    return mapping


# ---------------------------------------------------------------------------
# Curation logic
# ---------------------------------------------------------------------------

# Fault families that are in-scope for petrol v1
PETROL_V1_FAMILIES = {
    "lean_condition", "rich_mixture", "misfire", "catalyst_failure",
    "exhaust_leak", "sensor_fault", "ecu_fault", "cam_timing",
    "mechanical_wear", "non_starter", "ignition_fault", "invalid_input",
    "no_fault",
}

# Families to add in v2
NEW_FAMILY_NAMES = {"vacuum_leak", "overheating", "charging_system"}

# Pipeline-bug phases: cases failing here have correct ground truth but v1 can't
# process them. Do NOT drop these cases — the label is good, the pipeline is broken.
PIPELINE_BUG_PHASES = {
    "_run_dtclab",     # DTCLabPayload validation error — FIX-ENUM-1
    "_run_gaslab",     # gas_hc out of range — FIX-GAS-1
    "lab.obdlab.translate",  # 999.0 sentinel — FIX-OBD-1
    "lab.dtclab.sanitize",   # malformed DTC — FIX-DTC-1
}


def classify_case(
    csv_row: dict,
    blueprint: dict | None,
    cvsgaps_map: dict[str, tuple[str, str]],
) -> CaseMeta:
    """Determine disposition for a single master-CSV case."""
    cid = csv_row["case_id"]
    family = csv_row.get("expected_top_fault_family", "") or ""
    dtcs_raw = csv_row.get("dtcs", "") or ""
    dtcs_list = [d.strip() for d in dtcs_raw.split(",") if d.strip()] if dtcs_raw else []
    bp = blueprint or {}
    phase = bp.get("phase", "unknown")

    # ---- cvsgaps proposal ----
    cvsgaps_cat, cvsgaps_rationale = cvsgaps_map.get(cid, ("", ""))

    # ---- Decision rules ----

    # RULE: Explicit keep sentinels (before cvsgaps drop)
    if cid in CVSGAPS_KEEP_SENTINELS and cvsgaps_cat == "sentinel_invalid_input":
        return CaseMeta(
            case_id=cid, expected_top_fault_family=family,
            disposition="keep",
            rationale="Kept as one of the 2–3 representative sentinel/validation cases "
            "per cvsgaps.md guidance. Tests input-validation path.",
            source="cvsgaps", dtcs=dtcs_list,
        )

    # RULE: Explicit keep baselines (before cvsgaps drop)
    if cid in CVSGAPS_KEEP_BASELINES and cvsgaps_cat == "duplicate_baseline":
        return CaseMeta(
            case_id=cid, expected_top_fault_family=family,
            disposition="keep",
            rationale="Kept as one of the 2–3 representative healthy-baseline cases "
            "per cvsgaps.md guidance.",
            source="cvsgaps", dtcs=dtcs_list,
        )

    # RULE: cvsgaps drop proposals — verified and applied
    # A contrived/obsolete/sentinel case is dropped even if v1 crashes on it.
    if cvsgaps_cat:
        return CaseMeta(
            case_id=cid, expected_top_fault_family=family,
            disposition="drop", rationale=cvsgaps_rationale,
            source="cvsgaps", dtcs=dtcs_list,
            notes=f"Phase '{phase}' — cvsgaps drop ({cvsgaps_cat}) applied.",
        )

    # RULE: Pipeline-bug cases → KEEP (ground truth label is correct)
    if phase in PIPELINE_BUG_PHASES:
        return CaseMeta(
            case_id=cid, expected_top_fault_family=family,
            disposition="keep",
            rationale=f"v1 pipeline bug at '{phase}' — being fixed separately "
            f"(Tier 1 schema fixes). Ground-truth label is correct. "
            f"Jaeger: {bp.get('drop_reason', '')}",
            source="jaeger", dtcs=dtcs_list,
        )

    # RULE: Verify family is in petrol v1 scope
    if family and family not in PETROL_V1_FAMILIES and family not in NEW_FAMILY_NAMES:
        return CaseMeta(
            case_id=cid, expected_top_fault_family=family,
            disposition="drop",
            rationale=f"Family '{family}' is not in petrol v1 scope per PRD §5.",
            source="csv", dtcs=dtcs_list,
        )

    # RULE: Default — KEEP
    v1_note = ""
    if bp:
        v1_note = (
            f"v1: {bp.get('match_status', '')} → predicted '{bp.get('predicted_family', '')}' "
            f"at phase '{bp.get('phase', '')}'. "
        )
    return CaseMeta(
        case_id=cid, expected_top_fault_family=family,
        disposition="keep",
        rationale=f"{v1_note}Core diagnostic case for family '{family}' — "
        f"retained in curated v2 corpus.",
        source="csv", dtcs=dtcs_list,
    )


# ---------------------------------------------------------------------------
# New case synthesis
# ---------------------------------------------------------------------------

# The master CSV has 66 columns. For new cases, we synthesize plausible values
# matching the schema, leaving unknown fields blank.
MASTER_CSV_COLUMNS: list[str] = []


def build_new_case(case_id: str, family: str, description: str, idx: int) -> dict:
    """Synthesize a new CSV row for a new fault-family case."""
    row = {col: "" for col in MASTER_CSV_COLUMNS}
    row["case_id"] = case_id
    row["expected_top_fault_family"] = family
    row["description"] = description
    row["fuel_type"] = "petrol"
    row["induction_type"] = ""
    row["bank_config"] = "single"
    row["expected_state"] = "named_fault"
    row["expected_confidence_min"] = "0.65"
    row["expected_confidence_max"] = "0.90"
    # Leave gas and OBD columns blank — they will be filled during case
    # authoring in the REG-V2-AUTHOR tasks. The NEW- cases are placeholders
    # that reserve the fault-family slot in the curated corpus.
    return row


def synthesize_new_cases() -> list[dict]:
    """Produce new-case CSV rows for the three new families."""
    rows: list[dict] = []
    idx = 1
    for fam in NEW_FAMILIES:
        for i in range(fam["count"]):
            cid = f"NEW-{fam['family']}-{i + 1:02d}"
            desc = (
                f"[PLACEHOLDER] {fam['family'].replace('_', ' ').title()} "
                f"case {i + 1}/{fam['count']}. {fam['detection_signal']}"
            )
            rows.append(build_new_case(cid, fam["family"], desc, idx))
            idx += 1
    return rows


def build_new_metas(new_rows: list[dict]) -> list[CaseMeta]:
    """Build CaseMeta entries for new cases."""
    metas: list[CaseMeta] = []
    for row in new_rows:
        cid = row["case_id"]
        family = row["expected_top_fault_family"]
        fam_info = next((f for f in NEW_FAMILIES if f["family"] == family), None)
        rationale = fam_info["rationale"] if fam_info else ""
        metas.append(CaseMeta(
            case_id=cid,
            expected_top_fault_family=family,
            disposition="new",
            rationale=rationale,
            source="new",
            notes=f"Placeholder case. To be populated with real gas/OBD values "
            f"during REG-V2-AUTHOR-{family}.",
        ))
    return metas


# ---------------------------------------------------------------------------
# Audit summary
# ---------------------------------------------------------------------------


def print_summary(metas: list[CaseMeta], kept: int, dropped: int, relabeled: int, new: int) -> None:
    """Print summary stats for CORPUS_AUDIT.md authoring."""
    by_family_keep: dict[str, int] = defaultdict(int)
    by_family_drop: dict[str, int] = defaultdict(int)
    for m in metas:
        if m.disposition == "keep":
            by_family_keep[m.expected_top_fault_family] += 1
        elif m.disposition == "drop":
            by_family_drop[m.expected_top_fault_family] += 1

    print("=== CURATION SUMMARY ===")
    print(f"Total master cases: {len(metas)}")
    print(f"Kept: {kept} | Dropped: {dropped} | Relabeled: {relabeled} | New: {new}")
    print(f"Curated corpus size: {kept + new}")
    print()
    print("=== KEEP by family ===")
    for fam, count in sorted(by_family_keep.items(), key=lambda x: -x[1]):
        print(f"  {fam}: {count}")
    print()
    print("=== DROP by family ===")
    for fam, count in sorted(by_family_drop.items(), key=lambda x: -x[1]):
        print(f"  {fam}: {count}")
    print()
    print("=== DROP by category ===")
    by_cat: dict[str, int] = defaultdict(int)
    for m in metas:
        if m.disposition == "drop":
            cat = m.rationale[:60]
            by_cat[cat] += 1
    for cat, count in sorted(by_cat.items(), key=lambda x: -x[1]):
        print(f"  {cat}: {count}")
    print()
    print("=== NEW families ===")
    for fam in NEW_FAMILIES:
        print(f"  {fam['family']}: {fam['count']} cases — {fam['rationale'][:80]}...")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    global MASTER_CSV_COLUMNS

    # 1. Load inputs
    print("Loading master CSV...", file=sys.stderr)
    fieldnames, csv_rows = load_master_csv()
    MASTER_CSV_COLUMNS = fieldnames
    print(f"  {len(csv_rows)} rows, {len(fieldnames)} columns", file=sys.stderr)

    print("Parsing Jaeger failure blueprint...", file=sys.stderr)
    blueprint = parse_blueprint()
    print(f"  {len(blueprint)} unique case IDs", file=sys.stderr)

    print("Building cvsgaps proposal map...", file=sys.stderr)
    cvsgaps_map = build_cvsgaps_map()
    print(f"  {len(cvsgaps_map)} proposed dispositions", file=sys.stderr)

    # 2. Classify each master case
    print("Classifying cases...", file=sys.stderr)
    metas: list[CaseMeta] = []
    kept_rows: list[dict] = []
    csv_id_set: set[str] = set()

    for row in csv_rows:
        cid = row["case_id"]
        if not cid:
            continue
        bp = blueprint.get(cid)
        meta = classify_case(row, bp, cvsgaps_map)
        metas.append(meta)

        if meta.disposition in ("keep", "relabel"):
            kept_rows.append(row)
            csv_id_set.add(cid)

    # 3. Synthesize new cases
    print("Synthesizing new cases...", file=sys.stderr)
    new_rows = synthesize_new_cases()
    new_metas = build_new_metas(new_rows)

    for nr in new_rows:
        kept_rows.append(nr)
        csv_id_set.add(nr["case_id"])

    all_metas = metas + new_metas

    # 4. Counts
    kept = sum(1 for m in metas if m.disposition == "keep")
    dropped = sum(1 for m in metas if m.disposition == "drop")
    relabeled = sum(1 for m in metas if m.disposition == "relabel")
    new = len(new_metas)

    # 5. Write corpus_curated.csv
    print(f"Writing {len(kept_rows)} rows to {CURATED_CSV}...", file=sys.stderr)
    with open(CURATED_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(kept_rows)

    # 6. Write corpus_meta.json
    print(f"Writing {len(all_metas)} entries to {META_JSON}...", file=sys.stderr)
    corpus_meta = CorpusMeta(
        generated_at=datetime.now(timezone.utc).isoformat(),
        master_csv_total=len(csv_rows),
        curated_count=kept + new,
        dropped_count=dropped,
        relabel_count=relabeled,
        new_count=new,
        cases=all_metas,
    )
    with open(META_JSON, "w", encoding="utf-8") as f:
        f.write(corpus_meta.model_dump_json(indent=2))

    # 7. Print summary
    print_summary(metas, kept, dropped, relabeled, new)

    # 8. Contract checks
    print("=== CONTRACT CHECKS ===", file=sys.stderr)
    curated_ids = set()
    with open(CURATED_CSV, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            curated_ids.add(r["case_id"])
    meta_ids = {m.case_id for m in all_metas if m.disposition in ("keep", "new", "relabel")}
    missing_in_meta = curated_ids - meta_ids
    missing_in_csv = meta_ids - curated_ids
    if missing_in_meta:
        print(f"FAIL: CSV rows lack meta: {missing_in_meta}", file=sys.stderr)
    if missing_in_csv:
        print(f"FAIL: meta references missing CSV rows: {missing_in_csv}", file=sys.stderr)
    if not missing_in_meta and not missing_in_csv:
        print(f"PASS: CSV ↔ meta contract clean ({len(curated_ids)} rows)", file=sys.stderr)

    print("\nDone.", file=sys.stderr)


if __name__ == "__main__":
    main()
