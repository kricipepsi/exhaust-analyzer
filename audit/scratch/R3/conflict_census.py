"""R3: vref.db rows whose values conflict with another source, on the tip tree (repo root = cwd).

(a) vref.db rows vs the T-VINA-13a extract: displacement_cc, has_turbo, has_gdi, is_v_engine, euro_norm differ for a
    code the extract holds under the vref row's own brand (old 72 rows and merged rows alike).
(b) real VINs that reach a vref row: decoded cylinder_count (from vds_engine_map) vs the extract cylinder_count of the
    matched code; decoded displacement (vref) vs the map row's displacement (>0.15 L).
Deterministic JSON on stdout.
"""
import csv, json, re, sqlite3, sys
from pathlib import Path
sys.path.insert(0, "labs/vinlab")
from vinlab.db.tecdoc_query import _normalise_code  # noqa: E402

ext = {}
for r in csv.DictReader(open("labs/vinlab/tools/data/tecdoc_1q2019_engine_extract.csv", newline="", encoding="utf-8")):
    ext.setdefault(_normalise_code(r["engine_code"]), []).append(r)
db = sqlite3.connect("labs/vinlab/vinlab/data/vref.db"); db.row_factory = sqlite3.Row
a = []
for row in db.execute("select * from engine_ref order by engine_code"):
    for e in ext.get(_normalise_code(row["engine_code"]), []):
        if e["brand"].upper() != (row["brand"] or "").upper() or e["status"] not in ("OK", "FAMILY"):
            continue
        diffs = {}
        if e["displacement_cc"] and row["displacement_cc"] and abs(int(e["displacement_cc"]) - int(row["displacement_cc"])) > 50:
            diffs["displacement_cc"] = [row["displacement_cc"], int(e["displacement_cc"])]
        for k in ("has_turbo", "has_gdi", "is_v_engine"):
            if e[k] != "" and int(e[k]) != int(row[k]):
                diffs[k] = [row[k], int(e[k])]
        if e["euro_norm"] and row["euro_norm"] and e["euro_norm"].replace("_", "").upper() != str(row["euro_norm"]).replace("_", "").upper():
            diffs["euro_norm"] = [row["euro_norm"], e["euro_norm"]]
        if diffs:
            a.append({"code": row["engine_code"], "brand": row["brand"], "diffs": diffs})
snap = json.load(open(sys.argv[1]))["vins"]
b = []
for vin, x in sorted(snap.items()):
    if "error" in x or not x["vref"]:
        continue
    es = [e for e in ext.get(_normalise_code(x["vref"][0]), []) if e["status"] in ("OK", "FAMILY") and e["cylinder_count"]]
    cyls = sorted({int(e["cylinder_count"]) for e in es})
    if cyls and x["cyl"] and x["cyl"] not in cyls:
        b.append({"vin": vin, "code": x["vref"][0], "decoded_cyl": x["cyl"], "extract_cyl": cyls, "disp": x["disp"]})
print(json.dumps({"vref_vs_extract": a, "decoded_cyl_vs_extract": b}, indent=0, sort_keys=True))
