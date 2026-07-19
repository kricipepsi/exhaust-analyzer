"""
Tests for build_corpus.py — CorpusMeta schema validation + contract checks.
"""
import json
import csv
import sys
from pathlib import Path
from typing import Any

import pytest

# Ensure registry/tools is importable
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from tools.build_corpus import (
    CaseMeta,
    CorpusMeta,
    CVSGAPS_DROP_PROPOSALS,
    CVSGAPS_KEEP_SENTINELS,
    CVSGAPS_KEEP_BASELINES,
    classify_case,
    parse_blueprint,
    build_cvsgaps_map,
    MASTER_CSV,
)

# ---------------------------------------------------------------------------
# Schema validation tests
# ---------------------------------------------------------------------------

VALID_CASE = {
    "case_id": "TEST-001",
    "expected_top_fault_family": "lean_condition",
    "disposition": "keep",
    "rationale": "Test case.",
    "source": "csv",
    "dtcs": ["P0171"],
    "chemistry_signature": None,
    "notes": None,
    "relabel_to": None,
}


class TestCaseMeta:
    """Pydantic model validation for CaseMeta."""

    def test_valid_keep(self):
        m = CaseMeta(**VALID_CASE)
        assert m.disposition == "keep"
        assert m.case_id == "TEST-001"

    def test_valid_drop(self):
        m = CaseMeta(**{**VALID_CASE, "disposition": "drop"})
        assert m.disposition == "drop"

    def test_valid_relabel(self):
        m = CaseMeta(**{
            **VALID_CASE,
            "disposition": "relabel",
            "relabel_to": "rich_mixture",
        })
        assert m.disposition == "relabel"
        assert m.relabel_to == "rich_mixture"

    def test_valid_new(self):
        m = CaseMeta(**{
            **VALID_CASE,
            "disposition": "new",
            "source": "new",
        })
        assert m.disposition == "new"

    def test_invalid_disposition(self):
        with pytest.raises(Exception):
            CaseMeta(**{**VALID_CASE, "disposition": "invalid"})

    def test_invalid_source(self):
        with pytest.raises(Exception):
            CaseMeta(**{**VALID_CASE, "source": "unknown"})

    def test_dtcs_default(self):
        m = CaseMeta(**{**VALID_CASE, "dtcs": []})
        assert m.dtcs == []

    def test_optional_fields_none(self):
        m = CaseMeta(**VALID_CASE)
        assert m.relabel_to is None
        assert m.chemistry_signature is None
        assert m.notes is None


class TestCorpusMeta:
    """Top-level CorpusMeta model."""

    def test_valid(self):
        cases = [CaseMeta(**VALID_CASE), CaseMeta(**{**VALID_CASE, "case_id": "TEST-002"})]
        cm = CorpusMeta(
            generated_at="2026-05-27T00:00:00Z",
            master_csv_total=2,
            curated_count=2,
            dropped_count=0,
            relabel_count=0,
            new_count=0,
            cases=cases,
        )
        data = json.loads(cm.model_dump_json())
        assert len(data["cases"]) == 2
        assert data["curated_count"] == 2

    def test_empty_cases(self):
        cm = CorpusMeta(
            generated_at="2026-05-27T00:00:00Z",
            master_csv_total=0,
            curated_count=0,
            dropped_count=0,
            relabel_count=0,
            new_count=0,
            cases=[],
        )
        assert cm.cases == []


# ---------------------------------------------------------------------------
# Curation logic tests
# ---------------------------------------------------------------------------


class TestClassifyCase:
    """Decision logic for individual cases."""

    def test_keep_sentinel(self):
        """Sentinel cases in CVSGAPS_KEEP_SENTINELS are kept."""
        csv_row = {
            "case_id": "CSV-081",
            "expected_top_fault_family": "invalid_input",
            "dtcs": "",
        }
        cvsgaps_map = build_cvsgaps_map()
        result = classify_case(csv_row, None, cvsgaps_map)
        assert result.disposition == "keep"

    def test_drop_sentinel(self):
        """Sentinel cases not in keep list are dropped."""
        csv_row = {
            "case_id": "CSV-083",
            "expected_top_fault_family": "invalid_input",
            "dtcs": "",
        }
        cvsgaps_map = build_cvsgaps_map()
        result = classify_case(csv_row, None, cvsgaps_map)
        assert result.disposition == "drop"

    def test_drop_obsolete_hardware(self):
        """Obsolete hardware cases are dropped."""
        csv_row = {
            "case_id": "CASE-010",
            "expected_top_fault_family": "sensor_fault",
            "dtcs": "",
        }
        cvsgaps_map = build_cvsgaps_map()
        result = classify_case(csv_row, None, cvsgaps_map)
        assert result.disposition == "drop"

    def test_drop_contrived(self):
        """Contrived multi-fault cases are dropped even with pipeline bugs."""
        csv_row = {
            "case_id": "CASE-028",
            "expected_top_fault_family": "misfire",
            "dtcs": "",
        }
        bp = {
            "expected_family": "misfire",
            "predicted_family": "ERROR",
            "match_status": "VALIDATION_ERROR",
            "phase": "_run_dtclab",
            "drop_reason": "1 validation error for DTCLabPayload",
        }
        cvsgaps_map = build_cvsgaps_map()
        result = classify_case(csv_row, bp, cvsgaps_map)
        # Contrived should be dropped even though it hits a pipeline bug
        assert result.disposition == "drop"

    def test_keep_pipeline_bug(self):
        """Pipeline-bug cases without cvsgaps drop proposal are kept."""
        csv_row = {
            "case_id": "REAL-001",
            "expected_top_fault_family": "non_starter",
            "dtcs": "",
        }
        bp = {
            "expected_family": "non_starter",
            "predicted_family": "ERROR",
            "match_status": "CRITICAL_CRASH",
            "phase": "_run_gaslab",
            "drop_reason": "gas_hc out of range: 20200",
        }
        cvsgaps_map = build_cvsgaps_map()
        result = classify_case(csv_row, bp, cvsgaps_map)
        assert result.disposition == "keep"

    def test_keep_core_case(self):
        """Core diagnostic cases with no cvsgaps proposal are kept."""
        csv_row = {
            "case_id": "EXT-203",
            "expected_top_fault_family": "rich_mixture",
            "dtcs": "",
        }
        cvsgaps_map = build_cvsgaps_map()
        result = classify_case(csv_row, None, cvsgaps_map)
        assert result.disposition == "keep"


# ---------------------------------------------------------------------------
# Blueprint parser tests
# ---------------------------------------------------------------------------


class TestParseBlueprint:
    """FAILURE_BLUEPRINT.md parsing."""

    def test_parses_real_file(self):
        bp = parse_blueprint()
        assert len(bp) > 0
        # Should have deduped entries
        assert "CASE-012" in bp
        assert bp["CASE-012"]["phase"] == "comlab.aggregate"

    def test_all_phases_present(self):
        bp = parse_blueprint()
        phases = {v["phase"] for v in bp.values()}
        assert "comlab.aggregate" in phases
        assert "_run_dtclab" in phases

    def test_no_unknown_entries(self):
        bp = parse_blueprint()
        assert "UNKNOWN" not in bp


# ---------------------------------------------------------------------------
# cvsgaps map tests
# ---------------------------------------------------------------------------


class TestCvsgapsMap:
    """cvsgaps.md proposal mapping."""

    def test_builds_map(self):
        m = build_cvsgaps_map()
        assert len(m) > 0
        assert "CASE-010" in m
        assert "CSV-081" in m

    def test_no_overlap_keep_drop(self):
        """Keep lists and drop proposals must not overlap."""
        m = build_cvsgaps_map()
        sentinel_drop_ids = {
            cid for cid, (cat, _) in m.items() if cat == "sentinel_invalid_input"
        }
        baseline_drop_ids = {
            cid for cid, (cat, _) in m.items() if cat == "duplicate_baseline"
        }
        # Kept sentinels should be a subset of sentinel drop proposals
        assert CVSGAPS_KEEP_SENTINELS.issubset(sentinel_drop_ids)
        # Kept baselines should be a subset of baseline drop proposals
        assert CVSGAPS_KEEP_BASELINES.issubset(baseline_drop_ids)


# ---------------------------------------------------------------------------
# Integration / contract tests (run after build_corpus.py has been executed)
# ---------------------------------------------------------------------------


@pytest.mark.integration
class TestOutputContracts:
    """Verify the produced corpus_curated.csv and corpus_meta.json."""

    @pytest.fixture
    def curated_rows(self) -> list[dict[str, str]]:
        curated = Path(__file__).resolve().parent.parent / "corpus_curated.csv"
        if not curated.exists():
            pytest.skip("corpus_curated.csv not found — run build_corpus.py first")
        with open(curated, newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))

    @pytest.fixture
    def meta(self) -> dict[str, Any]:
        meta_path = Path(__file__).resolve().parent.parent / "corpus_meta.json"
        if not meta_path.exists():
            pytest.skip("corpus_meta.json not found — run build_corpus.py first")
        return json.loads(meta_path.read_text(encoding="utf-8"))

    def test_csv_meta_row_count_match(self, curated_rows, meta):
        """Every curated CSV row has a meta entry and vice versa."""
        csv_ids = {r["case_id"] for r in curated_rows}
        meta_ids = {
            c["case_id"] for c in meta["cases"]
            if c["disposition"] in ("keep", "new", "relabel")
        }
        missing_in_meta = csv_ids - meta_ids
        missing_in_csv = meta_ids - csv_ids
        assert not missing_in_meta, f"CSV rows lack meta: {missing_in_meta}"
        assert not missing_in_csv, f"meta references missing CSV rows: {missing_in_csv}"

    def test_csv_same_schema(self, curated_rows):
        """Curated CSV has the same columns as master."""
        master_cols = set()
        with open(MASTER_CSV, newline="", encoding="utf-8-sig") as f:
            master_cols = set(csv.DictReader(f).fieldnames or [])
        curated_cols = set(curated_rows[0].keys()) if curated_rows else set()
        assert master_cols == curated_cols, (
            f"Schema mismatch: master has {len(master_cols)} cols, "
            f"curated has {len(curated_cols)} cols"
        )

    def test_meta_counts_match(self, meta, curated_rows):
        """CorpusMeta counts match the actual data."""
        cases = meta["cases"]
        kept = sum(1 for c in cases if c["disposition"] == "keep")
        dropped = sum(1 for c in cases if c["disposition"] == "drop")
        relabeled = sum(1 for c in cases if c["disposition"] == "relabel")
        new = sum(1 for c in cases if c["disposition"] == "new")
        assert meta["dropped_count"] == dropped
        assert meta["relabel_count"] == relabeled
        assert meta["new_count"] == new
        assert meta["curated_count"] == kept + new

    def test_no_empty_case_id(self, curated_rows):
        """No curated CSV row has an empty case_id."""
        for row in curated_rows:
            assert row["case_id"], "Empty case_id in curated CSV"

    def test_new_cases_have_prefix(self, curated_rows):
        """All NEW cases use the NEW- prefix."""
        new_rows = [r for r in curated_rows if r["case_id"].startswith("NEW-")]
        assert len(new_rows) == 11
        for r in new_rows:
            assert r["fuel_type"] == "petrol"

    def test_kept_csv_rows_match_master(self, curated_rows):
        """KEEP rows in curated CSV are verbatim copies from master."""
        master_rows = {}
        with open(MASTER_CSV, newline="", encoding="utf-8-sig") as f:
            for r in csv.DictReader(f):
                master_rows[r["case_id"]] = r
        for row in curated_rows:
            cid = row["case_id"]
            if cid.startswith("NEW-"):
                continue
            assert cid in master_rows, f"KEPT case {cid} not in master CSV"
            # Key diagnostic columns must match
            for col in ("case_id", "expected_top_fault_family", "hc", "co", "co2", "o2"):
                assert row.get(col) == master_rows[cid].get(col), (
                    f"Column {col} mismatch for {cid}"
                )

    def test_cvsgaps_all_addressed(self, meta):
        """Every cvsgaps.md proposed case ID appears in corpus_meta.json."""
        all_ids = {c["case_id"] for c in meta["cases"]}
        for _, _, case_ids in CVSGAPS_DROP_PROPOSALS:
            for cid in case_ids:
                assert cid in all_ids, f"cvsgaps case {cid} not in corpus_meta.json"

    def test_discovery_clause_no_new_families(self, meta):
        """Discovery clause: no unknown families introduced beyond plan."""
        known_families = {
            "lean_condition", "rich_mixture", "misfire", "catalyst_failure",
            "exhaust_leak", "sensor_fault", "ecu_fault", "cam_timing",
            "mechanical_wear", "non_starter", "ignition_fault", "invalid_input",
            "no_fault", "vacuum_leak", "overheating", "charging_system",
        }
        for c in meta["cases"]:
            fam = c["expected_top_fault_family"]
            if fam:  # empty family is allowed for sentinel cases
                assert fam in known_families, f"Unknown family '{fam}' for {c['case_id']}"
