"""C6 auditor probes: VINLab / DNALab / SymptomLab. Evidence only.

Each test asserts the CLAIM. A failing test is the defect reproduced; the failure message is
the observation. Run from the repo root:

    python -m pytest -q audit/scratch/C6/test_c6_probes.py -p no:cacheprovider -rA

The era sweep (F-C6-1 user impact) is a separate script: python audit/scratch/C6/era_sweep.py
"""

from __future__ import annotations

import collections
import csv
import sqlite3
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent))
import c6_lib as L  # noqa: E402

ROOT = L.ROOT
DATA = ROOT / "labs/vinlab/vinlab/data"


def _wmi() -> dict[str, dict[str, str]]:
    return {r["wmi"]: r for r in csv.DictReader(open(DATA / "wmi.csv", encoding="utf-8"))}


def _map_rows() -> list[dict[str, str]]:
    return list(csv.DictReader(open(DATA / "vds_engine_map.csv", encoding="utf-8")))


# ---------------------------------------------------------------------------------------------
# F-C6-1  engine not in vref.db -> EURO_1 -> HORIZON_LEGACY whatever the model year
# ---------------------------------------------------------------------------------------------
def test_f1_horizon_follows_year_when_euro_unknown():
    """LLD §10: '_year_to_horizon (used only when euro unknown): 2001-2010 -> ADAPTIVE'."""
    from vinlab.db.tecdoc_query import lookup_engine_ref
    from vinlab.overlay.horizon import _year_to_horizon

    bad, total, euro_unknown, by_year = [], 0, 0, collections.Counter()
    for v in L.real_vins():
        try:
            d = L.decode(v)
        except L.VINDecodeError:
            continue
        total += 1
        eng = L.DEC._resolve_engine(d.vin, d.make, [])
        if eng and eng.get("engine_code") and lookup_engine_ref(L.DEC.db_path, eng["engine_code"]):
            continue  # euro known from vref.db: not this finding (see F-C6-4)
        euro_unknown += 1
        if d.model_year is not None and d.resolved_horizon != _year_to_horizon(d.model_year):
            bad.append(v)
            by_year[d.model_year] += 1
    print(f"\nreal VINs decoded={total}; no vref.db row (euro unknown)={euro_unknown}; "
          f"horizon != documented year fallback: {len(bad)}")
    print("by year:", sorted(by_year.items()))
    for v in ("WVWZZZ1KZAP012480", "W0LGM6ET6E1072040", "TMAD251CAGJ331435"):
        print(L.summary(v))
    assert not bad


def test_f1_year_fallback_has_no_production_caller():
    import subprocess

    out = subprocess.run(
        ["grep", "-rn", "_year_to_horizon", str(ROOT / "labs"), str(ROOT / "apps"),
         "--include=*.py"], capture_output=True, text=True).stdout
    callers = [ln for ln in out.splitlines() if "/tests/" not in ln and "def _year_to_horizon" not in ln]
    print("\nnon-test references:", callers)
    assert callers, "documented fallback is never called"


# ---------------------------------------------------------------------------------------------
# F-C6-2  wmi.csv gives the wrong make for major WMIs
# ---------------------------------------------------------------------------------------------
@pytest.mark.parametrize("vin,expected_make", [
    ("WDB1240261A102470", "MERCEDES"),      # W124, real OPSI VIN
    ("WDB1290601F037844", "MERCEDES"),      # R129 SL, real OPSI VIN
    ("KMHBF31SPMU250917", "HYUNDAI"),       # 1991 Sonata, real OPSI VIN
    ("JSAEAB35S00110744", "SUZUKI"),        # 1.3 Swift, real OPSI VIN
    ("JN1BCAN1480756536", "NISSAN"),        # 2008 Note 1.4, real OPSI VIN
    ("SAXXNNAZRWD148244", "ROVER"),         # 1998 Rover, real OPSI VIN
])
def test_f2_make_matches_wmi_owner(vin, expected_make):
    d = L.decode(vin)
    print("\n" + L.summary(vin))
    assert expected_make in d.make.upper()


# ---------------------------------------------------------------------------------------------
# F-C6-3  model year: one 30-year cycle, L->2020 for 'modern' WMIs, European pos-10 not a year
# ---------------------------------------------------------------------------------------------
def test_f3_era_hint_population():
    w = _wmi()
    c = collections.Counter(r["era_hint"] for r in w.values())
    leg = sorted(k for k, r in w.items() if r["era_hint"] == "legacy" and len(k) == 3
                 and r["brand"] and r["country"] and k[0] in "SVWZTYJK")
    print(f"\nera_hint counts={dict(c)}; legacy European/Asian 3-char WMIs={leg}")
    for k in ("WVW", "WDB", "VF1", "VF3", "ZFA", "WBA", "W0L", "TMB"):
        print(k, w[k]["brand"], w[k]["era_hint"])


@pytest.mark.parametrize("vin,true_years", [
    ("WVWZZZ1GZLW000001", range(1990, 1991)),   # Golf II, code L = 1990
    ("WVWZZZ1GZJW000001", range(1988, 1989)),   # Golf II, code J = 1988 (pre-scope)
    ("SAXXNNAMMBD029559", range(1981, 2006)),   # real OPSI Rover; the marque ended 2005
    ("WDB1240261A102470", range(1985, 1998)),   # real OPSI W124 (built 1985-1997)
    ("WDD1770441J098476", range(2018, 2030)),   # corpus W177 A-Class (from 2018)
])
def test_f3_model_year_plausible(vin, true_years):
    try:
        d = L.decode(vin)
    except L.VINDecodeError as e:
        print(f"\n{vin} -> rejected: {e}")
        return  # rejection is acceptable for a pre-1990 VIN
    print("\n" + L.summary(vin))
    assert d.model_year is None or d.model_year in true_years


# ---------------------------------------------------------------------------------------------
# F-C6-4  vref.db row applied without its model-year window; result graded HIGH
# ---------------------------------------------------------------------------------------------
def test_f4_vref_row_window_respected():
    con = sqlite3.connect(DATA / "vref.db")
    win = {code: (s, e) for code, s, e in con.execute("select engine_code,my_start,my_end from engine_ref")}
    out = []
    for v in L.real_vins():
        try:
            d = L.decode(v)
        except L.VINDecodeError:
            continue
        eng = L.DEC._resolve_engine(d.vin, d.make, [])
        code = eng and eng.get("engine_code")
        if code in win and d.model_year is not None:
            s, e = win[code]
            if not (s <= d.model_year <= e):
                out.append((v, d.model_year, code, (s, e), d.euro_emission_category.value,
                            d.emissions.upstream_o2_type.value, d.confidence.value))
    for o in out:
        print("\n", o)
    import subprocess
    readers = subprocess.run(["grep", "-rn", "my_start\\|my_end", str(ROOT / "labs/vinlab/vinlab"),
                              "--include=*.py"], capture_output=True, text=True).stdout
    print("readers of my_start/my_end in vinlab/*.py:", readers.splitlines())
    assert not out


# ---------------------------------------------------------------------------------------------
# F-C6-5  H1 petrol guard cannot fire on the shipped data; diesel engines decode as petrol
# ---------------------------------------------------------------------------------------------
def test_f5_fuel_population():
    rows = _map_rows()
    fuels = collections.Counter(r["fuel_system_type"] for r in rows)
    ev = collections.Counter(r["brand"] for r in rows if r["brand"] in ("LIVEWIRE", "ZEEHO"))
    con = sqlite3.connect(DATA / "vref.db")
    vref_fuels = [f for (f,) in con.execute("select distinct fuel_delivery_type from engine_ref")]
    print(f"\nvds_engine_map fuel_system_type={dict(fuels)}; electric-brand rows={dict(ev)}; vref fuels={vref_fuels}")
    assert len(fuels) > 1, "every row is PORT_INJECTION: the CSV H1 scan can never match"


@pytest.mark.parametrize("vin,diesel_code", [
    ("WBA3E11009E123456", "N47D20C"),   # BMW N47 2.0 diesel
    ("KNAJE55107K123456", "D4EA-V"),    # Hyundai/Kia 2.0 CRDi
    ("VF1BB07C08A123456", "K9K A7"),    # Renault 1.5 dCi
])
def test_f5_diesel_engine_rejected(vin, diesel_code):
    """wiki 10.4: 'a non-petrol vehicle is rejected whichever source first reveals it'."""
    eng = L.DEC._resolve_engine(vin, L.DEC.wmi_index[vin[:3]]["brand"], [])
    assert eng and eng["engine_code"] == diesel_code
    with pytest.raises(L.VINDecodeError):
        print("\n" + L.summary(vin))
        L.decode(vin)


# ---------------------------------------------------------------------------------------------
# F-C6-6  WIDEBAND_AFR for every >=2001 injected car without a vref o2 hint
# ---------------------------------------------------------------------------------------------
def test_f6_upstream_o2_population():
    c = collections.Counter()
    for v in L.real_vins():
        try:
            d = L.decode(v)
        except L.VINDecodeError:
            continue
        c[(d.emissions.upstream_o2_type.value,
           "2001-2010" if d.model_year and 2001 <= d.model_year <= 2010 else
           ">2010" if d.model_year and d.model_year > 2010 else "<=2000/None")] += 1
    print("\n", dict(c))
    from vinlab.overlay.switches import derive_upstream_o2_type
    print("derive_upstream_o2_type(2003,'PORT_INJECTION','') =",
          derive_upstream_o2_type(2003, "PORT_INJECTION", "").value)
    import wired.composition as wc
    view = wc._build_obd_dna_view(L.decode("WVWZZZ1KZAP012480").to_json_payload())
    print("OBDLab view for corpus VIN WVWZZZ1KZAP012480:", view.upstream_o2_type)
    # COMLab wiki 04_horizon_eras.md: ADAPTIVE (Euro 3-4, ~2001-2011) = narrowband O2 closed-loop
    assert derive_upstream_o2_type(2003, "PORT_INJECTION", "").value == "NARROWBAND"


# ---------------------------------------------------------------------------------------------
# F-C6-7  checksum gate: bypass decided by country strings that do not match the set
# ---------------------------------------------------------------------------------------------
def test_f7_country_population():
    from vinlab.decoder import _EUROPEAN_COUNTRIES, _NON_NHTSA_COUNTRIES

    w = _wmi()
    c = collections.Counter(r["country"] for r in w.values()
                            if r["country"] not in _EUROPEAN_COUNTRIES | _NON_NHTSA_COUNTRIES)
    print("\ncountries that ENFORCE the NHTSA check digit:",
          {k: v for k, v in c.items() if k not in ("UNITED STATES (USA)", "CANADA", "MEXICO")})
    for k in ("1FA", "3VW", "XTA", "XTE", "MAT", "JHM", "NLH"):
        print(k, w[k]["brand"], repr(w[k]["country"]))


def test_f7_na_vin_with_bad_check_digit_rejected():
    good = L.with_check("1FAFP34P03W123456")
    bad = good[:8] + ("1" if good[8] != "1" else "2") + good[9:]
    good_m = L.with_check("1FMFP34P03W123456")
    bad_m = good_m[:8] + ("1" if good_m[8] != "1" else "2") + good_m[9:]
    honda_ok = "1HGCM82633A004352"
    honda_zero = "1HGCM82603A004352"  # true check digit is 3
    res = {}
    for v in (bad, bad_m, honda_ok, honda_zero):
        res[v] = L.DEC.validate_vin_checksum(v)
    print("\nindependent check digits:", good[8], good_m[8], L.check_digit(honda_zero))
    print(res)
    assert res[bad] is False and res[bad_m] is False and res[honda_zero] is False


@pytest.mark.parametrize("vin", ["XTE110216S0313054", "MAT6002719PL01425"])
def test_f7_real_non_na_vin_decodes(vin):
    """PRD: 'European VINs without a check digit still decode (data-driven bypass)'."""
    print("\n" + L.summary(vin))
    L.decode(vin)


# ---------------------------------------------------------------------------------------------
# F-C6-8  VINLab scope 1990-2020 / Euro 6 vs project scope 1990-2010 / Euro 1-5
# ---------------------------------------------------------------------------------------------
@pytest.mark.parametrize("vin", ["WBA4W9C5ZLYYYYYYY", "VF3WB5FR8CE025644", "JF1BJ4DL0EB023564"])
def test_f8_out_of_project_scope_rejected(vin):
    try:
        d = L.decode(vin)
    except L.VINDecodeError:
        return
    print("\n" + L.summary(vin))
    assert d.model_year is None or d.model_year <= 2010
    assert d.euro_emission_category.value not in ("EURO_6", "EURO_7")


# ---------------------------------------------------------------------------------------------
# F-C6-9  confidence grade: blank-brand WMI -> PARTIAL, not NONE; flags undocumented
# ---------------------------------------------------------------------------------------------
def test_f9_unknown_brand_and_engine_is_none():
    vin = "002ZZZZZ0Y1234567"[:17]
    d = L.decode(vin)
    print("\n" + L.summary(vin))
    blank = sum(1 for k, r in _wmi().items() if not r["brand"].strip())
    print("blank-brand WMIs:", blank)
    # VIN_VOCABULARY §4: engine_not_in_csv -> NONE; PRD: NONE (engine not in CSV)
    assert d.confidence.value == "NONE"


def test_f9_flags_documented():
    import re

    code = (ROOT / "labs/vinlab/vinlab/decoder.py").read_text()
    flags = set(re.findall(r'conf_flags\.append\("([a-z_]+)"\)', code)) | set(
        re.findall(r'"([a-z_]+)" not in conf_flags', code))
    flags |= {"era_hint_unrecognised"} if "era_hint_unrecognised" in code else set()
    vocab = (ROOT / "labs/vinlab/docs/VIN_VOCABULARY.md").read_text()
    missing = sorted(f for f in flags if f"`{f}`" not in vocab)
    print("\nflags in code:", sorted(flags), "missing from VIN_VOCABULARY §4:", missing)
    assert not missing


# ---------------------------------------------------------------------------------------------
# F-C6-10  Path B (pos_8_only) has no data
# ---------------------------------------------------------------------------------------------
def test_f10_pos8_path_has_rows():
    rows = _map_rows()
    n = sum(1 for r in rows if r.get("pos_8_only", "").strip() and not r.get("vds_full", "").strip())
    print(f"\npos_8_only-only rows: {n} of {len(rows)}; vds_pos8_index size={len(L.DEC.vds_pos8_index)}")
    assert n > 0


# ---------------------------------------------------------------------------------------------
# F-C6-11  SymptomLab: 18 vs 21 combinations
# ---------------------------------------------------------------------------------------------
def test_f11_combination_count_consistent():
    import re

    hits = []
    for p in sorted((ROOT / "labs/symptomlab").glob("docs/*.md")) + [
            ROOT / "labs/symptomlab/symptomlab/models.py"]:
        for i, ln in enumerate(p.read_text().splitlines(), 1):
            if re.search(r"\b18\b.*(combination|pair|allowed)|(combination|pair|allowed).*\b18\b", ln):
                hits.append(f"{p.relative_to(ROOT)}:{i}")
    from symptomlab import _get_validator, _DEFAULT_ALLOWED_PATH
    n = len(_get_validator(_DEFAULT_ALLOWED_PATH)._allowed)
    print(f"\ncatalog pairs={n}; lines still saying 18: {len(hits)}", hits[:12])
    assert not hits


# ---------------------------------------------------------------------------------------------
# F-C6-12  SymptomDNA.from_json silently defaults a missing load_state
# ---------------------------------------------------------------------------------------------
def test_f12_missing_load_state_raises():
    from symptomlab.models import SymptomDNA, SymptomValidationError
    from dnalab import build_vehicle_dna
    from dnalab.models import VehicleDNA

    t = dict(tier_1="lack_of_power_hesitation", tier_2="hesitation_throttle_tip_in",
             occurs_during="always", engine_state="running", load_state="transient_acceleration")
    p = build_vehicle_dna("VF7SA5FR8AW511081", t).to_json_payload()
    del p["symptom_dna"]["environmental_conditions"]["load_state"]
    print("\nschema_version:", p["schema_version"])
    try:
        back = VehicleDNA.from_json_payload(p)
    except SymptomValidationError as e:
        print("raised:", e)
        return
    print("accepted; load_state ->", back.symptom_dna.environmental_conditions.load_state)
    pytest.fail("missing required load_state accepted as idle")


# ---------------------------------------------------------------------------------------------
# F-C6-13  SymptomValidator: non-string tier -> TypeError, not SymptomValidationError
# ---------------------------------------------------------------------------------------------
@pytest.mark.parametrize("tier_1", [["rough_idle_shudder"], {"x": 1}])
def test_f13_unhashable_tier_is_validation_error(tier_1):
    from symptomlab import SymptomValidationError, resolve

    try:
        resolve(tier_1, "surging_hunting_idle", occurs_during="always", engine_state="running",
                load_state="idle")
    except SymptomValidationError:
        return
    except Exception as e:  # noqa: BLE001
        pytest.fail(f"{type(e).__name__}: {e}")


# ---------------------------------------------------------------------------------------------
# F-C6-14  vref lookup leaves sqlite connections open
# ---------------------------------------------------------------------------------------------
def test_f14_no_unclosed_connection():
    import gc
    import warnings

    from vinlab.db.tecdoc_query import lookup_engine_ref

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always", ResourceWarning)
        for _ in range(3):
            lookup_engine_ref(DATA / "vref.db", "5FR")
        gc.collect()
    rw = [str(x.message) for x in w if issubclass(x.category, ResourceWarning)]
    print("\n", rw)
    assert not rw


# ---------------------------------------------------------------------------------------------
# Negative controls (expected to PASS): input hygiene, determinism, round trip, isolation
# ---------------------------------------------------------------------------------------------
@pytest.mark.parametrize("raw,exc", [
    ("vf7sa5fr8aw511081", None), ("  VF7SA5FR8AW511081\t\n", None), ("VF7SA5FR8AW51108", "Chassis"),
    ("VF7SA5FR8AW5110811", "Chassis"), ("VF7SA5FR8AW51108Q", "VINDecode"), ("VF7SA5FR8AW 11081", "VINDecode"),
    ("VF7SA5FR8AW51I08O", None), ("", "Chassis"),
])
def test_control_input_hygiene(raw, exc):
    try:
        d = L.decode(raw)
        assert exc is None, f"accepted {raw!r} -> {d.vin}"
    except L.VINDecodeError as e:
        assert exc is not None and exc in type(e).__name__, f"{raw!r}: {type(e).__name__}"


@pytest.mark.parametrize("triage_patch", [
    {"tier_1": "Rough_Idle_Shudder"}, {"tier_2": "surging_hunting_idle "}, {"occurs_during": "Always"},
    {"engine_state": "wont_start"}, {"load_state": "cruise"}, {"tier_1": "rough_idle_shudder",
                                                               "tier_2": "black_smoke"},
    {"tier_1": None},
])
def test_control_symptom_rejects(triage_patch):
    from symptomlab import SymptomValidationError, resolve

    t = dict(tier_1="rough_idle_shudder", tier_2="surging_hunting_idle", occurs_during="always",
             engine_state="running", load_state="idle")
    t.update(triage_patch)
    with pytest.raises(SymptomValidationError):
        resolve(t["tier_1"], t["tier_2"], occurs_during=t["occurs_during"],
                engine_state=t["engine_state"], load_state=t["load_state"])


def test_control_dnalab_missing_and_bad_inputs():
    from dnalab import build_vehicle_dna
    from symptomlab import SymptomValidationError

    t = dict(tier_1="rough_idle_shudder", tier_2="surging_hunting_idle", occurs_during="always",
             engine_state="running", load_state="idle")
    with pytest.raises(SymptomValidationError):
        build_vehicle_dna("NOT-A-VIN", {k: v for k, v in t.items() if k != "load_state"})
    with pytest.raises(L.VINDecodeError):
        build_vehicle_dna("", t)
    with pytest.raises(SymptomValidationError):
        build_vehicle_dna("VF7SA5FR8AW511081", dict(t, tier_2="black_smoke"))
    a = build_vehicle_dna("VF7SA5FR8AW511081", t).to_json_payload()
    b = build_vehicle_dna("VF7SA5FR8AW511081", t).to_json_payload()
    for x in (a, b):
        x.pop("session_id"), x.pop("timestamp")
    assert a == b
