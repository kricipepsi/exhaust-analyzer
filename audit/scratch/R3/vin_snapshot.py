"""R3 snapshot: decode the real-VIN corpus with the VINLab of tree ROOT and dump deterministic JSON.

Usage: python audit/scratch/R3/vin_snapshot.py <tree-root> <corpus-root> > out.json
The corpus is audit/scratch/C6/c6_lib.py::real_vins re-implemented here (17-char VIN tokens in
<corpus-root>/labs/vinlab/*.md|*.csv, first char a letter) so both trees decode the same population.
Also: for each vds_engine_map row of the tree, the vref.db row lookup_engine_ref returns and its brand.
"""
from __future__ import annotations
import csv, glob, json, logging, re, sys
from pathlib import Path

root, corpus = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(root / "labs/vinlab"))
logging.disable(logging.WARNING)
import vinlab  # noqa: E402
from vinlab import VINDecodeError, _get_decoder  # noqa: E402
from vinlab.db.tecdoc_query import lookup_engine_ref  # noqa: E402
assert Path(vinlab.__file__).resolve().is_relative_to(root), vinlab.__file__

DEC = _get_decoder(vinlab._DEFAULT_DATA_DIR)
vins: set[str] = set()
for f in sorted(glob.glob(str(corpus / "labs/vinlab/*.md")) + glob.glob(str(corpus / "labs/vinlab/*.csv"))):
    vins |= set(re.findall(r"\b[A-HJ-NPR-Z0-9]{17}\b", open(f, errors="ignore").read()))
vins = {v for v in vins if re.match(r"^[A-Z]", v)}

def fold(s: str | None) -> str:
    return re.sub(r"[^A-Z]", "", (s or "").upper())

out: dict = {"vins": {}, "map_xbrand": []}
for vin in sorted(vins):
    try:
        d = DEC.decode_vin_payload(vin)
    except VINDecodeError as e:
        out["vins"][vin] = {"error": str(e)}
        continue
    eng = DEC._resolve_engine(d.vin, d.make, [])
    code = eng and eng.get("engine_code")
    row = lookup_engine_ref(DEC.db_path, code) if code else None
    out["vins"][vin] = {
        "make": d.make, "year": d.model_year, "engine": code,
        "disp": d.engine_displacement_liters, "cyl": d.cylinder_count,
        "fuel": d.fuel_delivery_type.value, "ind": d.induction_type.value,
        "euro": d.euro_emission_category.value, "o2": d.emissions.upstream_o2_type.value,
        "conf": d.confidence.value,
        "vref": None if row is None else [row["engine_code"], row["brand"], row["my_start"], row["my_end"]],
    }
mp = root / "labs/vinlab/vinlab/data/vds_engine_map.csv"
seen = set()
for r in csv.DictReader(open(mp, newline="", encoding="utf-8")):
    key = (r["brand"], r["engine_code"])
    if key in seen or not r["engine_code"]:
        continue
    seen.add(key)
    row = lookup_engine_ref(DEC.db_path, r["engine_code"])
    if row is not None and fold(row["brand"]) != fold(r["brand"]):
        out["map_xbrand"].append([r["brand"], r["engine_code"], row["engine_code"], row["brand"]])
out["map_xbrand"].sort()
print(json.dumps(out, indent=0, sort_keys=True))
