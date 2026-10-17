"""C3 negative-result sweep: range edges and order stability that held (evidence for
'Approaches that found nothing'). Run from the repo root: python audit/scratch/C3/edge_sweep.py"""
import itertools, logging, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
logging.disable(logging.WARNING)
from test_c3_probes import tr, dna, sanitize, dtc_view  # noqa: E402
from dtclab.ranking import rank_candidates, classify_top3  # noqa: E402

def outcome(**kw):
    try:
        tr(**kw); return "ok"
    except Exception as e:  # noqa: BLE001
        return type(e).__name__
edges = [("engine_rpm", 6825, 6826), ("coolant_temp_c", 140.0, 140.01), ("coolant_temp_c", -40.0, -40.01),
         ("mass_airflow_gps", 655.35, 655.36), ("manifold_vacuum_kpa", 255.0, 255.01),
         ("shrtft1", 127.0, 127.01), ("longft1", -127.0, -127.01), ("intake_air_temp_c", 140.0, 140.01),
         ("throttle_pos_pct", 100.0, 100.01), ("control_module_voltage_v", 18.0, 18.01),
         ("calculated_engine_load_pct", 100.0, 100.01)]
for f, ok, bad in edges:
    print(f"{f}: {ok} -> {outcome(**{f: ok})} | {bad} -> {outcome(**{f: bad})}")
print("rpm 8001 no-DNA-HIGH:", outcome(d=dna(confidence=__import__('obdlab.schemas.dna_view', fromlist=['VinConfidence']).VinConfidence.NONE), engine_rpm=8001))
print("banks=2 without bank-2 trims:", outcome(number_of_banks=2))
print("banks=1 with shrtft2=0.0:", outcome(shrtft2=0.0))
for f in ("_f", "_psi", "_inhg", "_lbmin"):
    pass
p = tr(drop=("coolant_temp_c",), coolant_temp_f=194.0); print("194 F ->", p.coolant_temp_c)
p = tr(drop=("mass_airflow_gps",), mass_airflow_lbmin=1.0); print("1 lb/min ->", p.mass_airflow_gps)
p = tr(coolant_temp_f=32.0); print("both _f and _c present -> canonical kept:", p.coolant_temp_c)
# ranking order stability over every permutation of a 5-code input
codes = ["P0171", "P0300", "P0420", "P0131", "P0011"]
outs = set()
for perm in itertools.permutations(codes):
    p = sanitize({"$03": list(perm)}, dtc_view())
    outs.add((tuple(t.value for t in p.routing_tags), tuple((c.family, c.raw_confidence) for c in rank_candidates(p, dna_view=dtc_view())), tuple(classify_top3(p, dna_view=dtc_view()))))
print("permutations:", 120, "distinct (tags, rank, top3) outputs:", len(outs))
for conf in ("HIGH", "PARTIAL", "NONE"):
    from dtclab.schemas.dna_view import VinConfidence as C
    v = dtc_view(has_catalyst=False, egr=False, conf=C(conf))
    print(conf, "P0420+P0401 tags:", [t.value for t in sanitize({"$03": ["P0420", "P0401"]}, v).routing_tags])
for code in ("P1171", "P2171", "P3000", "B0001", "C0035", "U0100", "P0700"):
    p = sanitize({"$03": [code]}); print(code, "accepted, tags:", [t.value for t in p.routing_tags], "rank:", rank_candidates(p))
for code in ("p0171", "P01a1", "P4000", "D0001", "P017", "P01711", " P0171"):
    try:
        sanitize({"$03": [code]}); print(repr(code), "accepted")
    except Exception as e:  # noqa: BLE001
        print(repr(code), "->", type(e).__name__)
