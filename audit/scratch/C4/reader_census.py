"""C4 probe: where (if anywhere) is each COMLab inbound OBD/GAS field read on the production path?

Run from repo root: python audit/scratch/C4/reader_census.py
Production path = LabPipelineAggregator default (USE_V2_REGISTRY unset -> "1"): FaultAtlasRouter.route()
returns the registry-v2 result before execute_triage_loop() (v1) runs. A field read only inside
execute_triage_loop (or a helper only it calls) has no production reader.
"""
import ast
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "labs/comlab"))
import comlab.schemas.ingestion as ci  # noqa: E402

router = (ROOT / "labs/comlab/comlab/core/fault_atlas_router.py").read_text().splitlines()
tree = ast.parse("\n".join(router))
loop = next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == "execute_triage_loop")
route = next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == "route")
v2_if = next(n for n in ast.walk(route) if isinstance(n, ast.If) and "_use_v2_registry" in ast.unparse(n.test))
v2_return = v2_if.end_lineno
# helpers called from execute_triage_loop (module-level functions / methods)
called = {n.func.id if isinstance(n.func, ast.Name) else n.func.attr
          for n in ast.walk(loop) if isinstance(n, ast.Call) and isinstance(n.func, (ast.Name, ast.Attribute))}
v1_only_ranges = [(loop.lineno, loop.end_lineno), (v2_return + 1, route.end_lineno)]
for n in ast.walk(tree):
    if isinstance(n, ast.FunctionDef) and n.name in called and n.name.startswith("_"):
        v1_only_ranges.append((n.lineno, n.end_lineno))

other = [p for p in (ROOT / "labs/comlab").rglob("*.py")
         if "/tests/" not in str(p) and "/schemas/" not in str(p) and "/graph/" not in str(p)
         and p.name != "fault_atlas_router.py"]

print(f"route(): v2 result returned at line {v2_return}; execute_triage_loop lines {loop.lineno}-{loop.end_lineno}")
for model in (ci.OBDLiveDataPayload, ci.GasLabPayload):
    print(f"\n== {model.__name__}")
    for f in model.model_fields:
        pat = re.compile(rf"\b{f}\b")
        r_lines = [i + 1 for i, l in enumerate(router) if pat.search(l)]
        prod_router = [i for i in r_lines if not any(a <= i <= b for a, b in v1_only_ranges)]
        v1 = [i for i in r_lines if i not in prod_router]
        others = sorted({str(p.relative_to(ROOT)) for p in other if pat.search(p.read_text(errors="ignore"))})
        tag = "NO PRODUCTION READER" if not prod_router and not others else ""
        where = sorted({fn.name for fn in ast.walk(tree) if isinstance(fn, ast.FunctionDef)
                        and any(fn.lineno <= i <= fn.end_lineno for i in v1) and fn.name != route.name})
        print(f"  {f:38s} router_prod={prod_router[:4]} router_v1_only={len(v1)} other={others[:3]} {tag}"
              + (f"  v1 sites in {where}" if tag else ""))
