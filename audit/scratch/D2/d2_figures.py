"""D2 probe — figures stated in the COMLab design chain vs each other and vs code/data.

Run from the repo root (venv active):
    python audit/scratch/D2/d2_figures.py
Each row: CLAIM <doc:line> "<quoted text>"  ->  ACTUAL <value> (<how computed>).
Read-only.
"""
from __future__ import annotations

import collections
import glob
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
COM = ROOT / "labs/comlab"
sys.path.insert(0, str(COM))

from comlab.schemas import lab_dna_views as views  # noqa: E402
from comlab.schemas.ingestion import FreezeFrameRecord  # noqa: E402
from comlab.schemas.vocabulary import ChemicalSignature, DTCRoutingTag, FaultFamily  # noqa: E402

DOCS = sorted(glob.glob(str(COM / "docs/**/*.md"), recursive=True))


def claims(pattern: str):
    rx = re.compile(pattern)
    for d in DOCS:
        for n, ln in enumerate(Path(d).read_text(encoding="utf-8").splitlines(), 1):
            if rx.search(ln):
                yield f"{Path(d).relative_to(ROOT)}:{n}", ln.strip()[:170]


def show(title: str, pattern: str, actual: str):
    print(f"\n## {title}\nACTUAL: {actual}")
    for anchor, text in claims(pattern):
        print(f"  CLAIM {anchor} \"{text}\"")


kg_files = sorted(Path(f).stem for f in glob.glob(str(COM / "comlab/config/kg/*.json"))
                  if not Path(f).name.startswith("_"))
kg_nodes = {}
for f in glob.glob(str(COM / "comlab/config/kg/*.json")):
    if not Path(f).name.startswith("_"):
        kg_nodes.update(json.load(open(f))["nodes"])
v1 = json.load(open(COM / "comlab/config/global_fault_registry.json"))
v1_rows = v1["registry"]
v2_rules = [r for f in glob.glob(str(COM / "registry/rules/*.json")) for r in json.load(open(f))["rules"]]
v2_fams = sorted({r["fault_family"] for r in v2_rules})
cfg_bytes = sum(p.stat().st_size for p in (COM / "comlab/config").rglob("*") if p.is_file())
ff_flags = [f for f in FreezeFrameRecord.model_fields if f.startswith("ff_")]
router_src = (COM / "comlab/core/fault_atlas_router.py").read_text().splitlines()
shim_line = next(i for i, l in enumerate(router_src, 1) if "from registry.integration_shim import" in l)

show("KG family-file count / family set",
     r"13 per-family|Twelve files|12 FaultFamily|13 files|\(13 files\)",
     f"{len(kg_files)} family files {kg_files}; FaultFamily enum {len(list(FaultFamily))}; "
     f"extra file(s) vs enum: {sorted(set(kg_files) - {m.value for m in FaultFamily})}")
show("Registry rule-row count", r"120 rule|~120 rows|rules_evaluated\": +\d+",
     f"v1 global_fault_registry.json rows={len(v1_rows)} (unique ids "
     f"{len({r['fault_id'] for r in v1_rows})}); REG-V2 (production default) rules={len(v2_rules)} "
     f"in {len(v2_fams)} families")
show("Config footprint", r"2\.5 MB|2\.78 MB|0\.22 MB|2\.40 MB",
     f"du-equivalent comlab/config = {cfg_bytes} bytes = {cfg_bytes/1e6:.3f} MB; "
     f"DLD §2.2 own breakdown sums to 2.78 MB > the 2.5 MB limit it states")
show("LabDnaView field counts", r"15 / 10 / 11",
     f"Gas={len(views.GasLabDnaView.model_fields)} Obd={len(views.ObdLabDnaView.model_fields)} "
     f"Dtc={len(views.DtcLabDnaView.model_fields)}")
show("DTCRoutingTag cardinality", r"19-value|19 routing|16 values today|All 17 `DTCRoutingTag",
     f"comlab DTCRoutingTag={len(list(DTCRoutingTag))}")
show("ChemicalSignature cardinality", r"34 values|34-value|\*\*34", f"{len(list(ChemicalSignature))}")
show("FreezeFrame derived flags", r"6 derived|6 bool fields",
     f"{len(ff_flags)} ff_* flags: {ff_flags}")
show("registry shim import line", r"~L1845", f"fault_atlas_router.py:{shim_line}")
show("Reference interpreter", r"Python 3\.10", f"running {sys.version.split()[0]}")
print("\nv1 duplicate fault_ids:",
      sorted(k for k, c in collections.Counter(r["fault_id"] for r in v1_rows).items() if c > 1))
print("v1 top-level keys:", list(v1)[:6], "(LLD §8.1 requires 'schema_version')")
print("v1 fallback_strategy values:", sorted({str(r.get('fallback_strategy')) for r in v1_rows}),
      "(LLD §8.1 enum: REQUIRE_MATCH | PROCEED_ON_MATCH_OR_EMPTY | PROCEED)")
print("v1 rows carrying fault_name:", sum('fault_name' in r for r in v1_rows),
      "ui_diagnostic_string:", sum('ui_diagnostic_string' in r for r in v1_rows),
      "preconditions:", sum('preconditions' in r for r in v1_rows), "of", len(v1_rows))
print("REG-V2 families not in FaultFamily enum:", sorted(set(v2_fams) - {m.value for m in FaultFamily}))
