"""R3 fix-chain probes. Evidence only, never product code.

Run from the repo root:  python -m pytest -q audit/scratch/R3/test_r3_probes.py
Against another tree:    R3_TREE=<worktree> python -m pytest -q audit/scratch/R3/test_r3_probes.py
(the tree's labs/vinlab, labs/symptomlab, apps/ui, apps/wired and labs/comlab go first on sys.path).

`closed_*` probes: the finding's minimal input; expected to FAIL on audit-r2 and PASS at the tip.
`viol_*` probes: R3 findings; expected to FAIL at the tip. Each expected value cites its independent source.
"""
from __future__ import annotations

import csv
import logging
import os
import re
import sqlite3
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[3]
TREE = Path(os.environ.get("R3_TREE", REPO)).resolve()
for p in ("labs/comlab", "apps/wired", "apps/ui", "labs/symptomlab", "labs/vinlab"):
    sys.path.insert(0, str(TREE / p))
logging.disable(logging.WARNING)

import vinlab  # noqa: E402
from vinlab import VINDecodeError, decode  # noqa: E402

assert Path(vinlab.__file__).resolve().is_relative_to(TREE), vinlab.__file__
EXTRACT = REPO / "labs/vinlab/tools/data/tecdoc_1q2019_engine_extract.csv"  # T-VINA-13a deliverable (tip)


def _extract_brands(code: str) -> set[str]:
    norm = re.sub(r"[^A-Z0-9]", "", code.upper())
    with open(EXTRACT, newline="", encoding="utf-8") as fh:
        return {r["brand"] for r in csv.DictReader(fh) if re.sub(r"[^A-Z0-9]", "", r["engine_code"].upper()) == norm}


# ---------------------------------------------------------------- (a) closure probes
def test_closed_aud1c_mil_flashing_only_requires_ff():
    """T-AUD-1c: MIL-flashing-only form (a DTC dict is sent) asks for the 12 freeze-frame fields."""
    import ui_payload as up

    w = {"gas_module": True, "obd_module": True, "dtc_module": True, "dtc_mil_flashing": True,
         "dtc_memory_status": "Normal", "triage_tier_1": "—", "triage_tier_2": "—",
         "triage_occurs_during": "Always", "triage_engine_state": "Running", "active_number_of_banks": 1,
         "active_upstream_o2_type": "NARROWBAND"}
    assert set(up.FF_REQUIRED_FIELDS) <= {i.field for i in up.validate_widgets(w)}


@pytest.mark.parametrize("vin,year", [("WVWZZZ1GZLW000001", 1990)])
def test_closed_vina1_l_is_1990(vin, year):
    """F-C6-3 expected: 'L resolves to 1990 for the 1990-2010 fleet'."""
    assert decode(vin).model_year == year


@pytest.mark.parametrize("vin", ["WVWZZZ1GZJW000001", "SAXXNNAMMBD029559"])
def test_closed_vina1_out_of_scope_refused(vin):
    """F-C6-3/F-C6-8 expected: a pre-1990 code (J=1988) and B (2011) are not decoded as in-scope years."""
    with pytest.raises(VINDecodeError, match="1990-2010"):
        decode(vin)


def test_closed_vina8_missing_load_state_refused():
    """F-C6-12 expected: a schema-1.2 payload without load_state is refused, not turned into idle."""
    from symptomlab import resolve
    from symptomlab.models import SymptomDNA, SymptomValidationError

    p = resolve("rough_idle_shudder", "surging_hunting_idle", occurs_during="always",
                engine_state="running", load_state="idle").to_json_payload()
    del p["environmental_conditions"]["load_state"]
    with pytest.raises(SymptomValidationError):
        SymptomDNA.from_json(p)


@pytest.mark.parametrize("tier", [1, 2.5, True])
def test_closed_vina8_scalar_non_string_tier_refused(tier):
    """F-C6-13 class, scalars the row's own test does not try: SymptomValidationError, never TypeError."""
    from symptomlab import resolve
    from symptomlab.models import SymptomValidationError

    with pytest.raises(SymptomValidationError):
        resolve(tier, "surging_hunting_idle", occurs_during="always", engine_state="running", load_state="idle")


def test_closed_vina2_mercedes_type_code_no_year():
    """F-C6-3 expected: 'A European WMI whose position 10 is not a year code gives model_year=None'."""
    assert decode("WDB1240261A102470").model_year is None


def test_closed_vina3_row_outside_window_not_applied():
    """F-C6-4: 1995 Subaru, EJ20 row window 1998-2010 -> no Euro 4 at HIGH."""
    d = decode("JF1BG5LJ4SG009089")
    assert d.model_year == 1995
    assert not (d.euro_emission_category.value == "EURO_4" and d.confidence.value == "HIGH")


@pytest.mark.parametrize("vin,make", [
    ("WDB1240261A102470", "MERCEDES-BENZ"), ("KMHBF31SPMU250917", "HYUNDAI"), ("JSAEAB35S00110744", "SUZUKI"),
    ("JN1BCAN1480756536", "NISSAN"), ("SAXXNNAZRWD148244", "ROVER"),
])
def test_closed_vina5_true_make(vin, make):
    """F-C6-2 expected: WDB->Mercedes-Benz, KMH->Hyundai, JSA->Suzuki, JN1->Nissan, SAX->Rover."""
    assert decode(vin).make.upper() == make


def test_closed_vina13b_72_original_rows_unchanged():
    """T-VINA-13b claim: the 72 original rows keep every value (compared by column name with audit-r2's db)."""
    old = REPO / ".r3_vref_audit_r2.db"
    old.write_bytes(subprocess.run(["git", "-C", str(REPO), "show", "origin/audit-r2:labs/vinlab/vinlab/data/vref.db"],
                                   capture_output=True, check=True).stdout)
    try:
        def rows(p):
            c = sqlite3.connect(p)
            c.row_factory = sqlite3.Row
            return {r["engine_code"]: dict(r) for r in c.execute("select * from engine_ref")}
        a, b = rows(old), rows(TREE / "labs/vinlab/vinlab/data/vref.db")
    finally:
        old.unlink()
    assert len(a) == 72
    assert {k: b.get(k) for k in a} == a


# ---------------------------------------------------------------- R3 violations
@pytest.mark.parametrize("vin,engine_brand", [
    ("JTEHH20V000092225", "TOYOTA"),   # engine 1AZ-FE  (labs/vinlab/cylinder_count_resolved.md)
    ("JTMDEREV00D119221", "TOYOTA"),   # engine 3ZR-FAE
    ("KNEDC221246348997", "KIA"),      # engine A3E
])
def test_viol_r3_2_wmi_make_matches_engine_owner(vin, engine_brand):
    """F-R3-2: same class as F-C6-2. The TecDoc 1Q2019 extract (T-VINA-13a) lists the engine code this VIN
    resolves to under exactly one brand; the decoded make must be that brand."""
    d = decode(vin)
    code = vinlab._get_decoder(vinlab._DEFAULT_DATA_DIR)._resolve_engine(d.vin, d.make, [])["engine_code"]
    assert _extract_brands(code) == {engine_brand}
    assert d.make.upper() == engine_brand


def test_viol_r3_3_vsa_type_code_no_year():
    """F-R3-3: VSA (wmi.csv: MERCEDES-BENZ) Vito W638 type code 638234 at positions 4-9, '1' at position 10.
    F-C6-3 expected and T-VINA-2's own rule (wiki/10 §10.6): no model year from position 10."""
    assert decode("VSA63823413020157").model_year is None


def test_viol_r3_4_adr0006_states_21_pairs():
    """F-R3-4: F-C6-11 residue. ADR-0006 is Accepted and still names the 18-pair invariant; ADR-0008 says 21."""
    text = (TREE / "labs/symptomlab/docs/ADR_SymptomLab.md").read_text(encoding="utf-8")
    adr6 = text.split("## ADR-0006")[1].split("## ADR-0007")[0]
    assert "18-pair" not in adr6
