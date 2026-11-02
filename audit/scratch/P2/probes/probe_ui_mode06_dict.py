"""Probe: the UI's Mode $06 component-name dictionary is never loaded.

apps/ui/app.py:132 builds DICT_PATH from apps/ui/ -> parent -> "dtclab/dtclab/config/...". This re-executes
that expression and the lookup at app.py:675-680 for a well-formed Monitor ID.
Run (repo root): python audit/scratch/P2/probes/probe_ui_mode06_dict.py
"""
import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
app = ROOT / "apps/ui/app.py"
tree = ast.parse(app.read_text())
expr = next(n.value for n in tree.body if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", "") == "DICT_PATH")
dict_path = eval(compile(ast.Expression(expr), "app.py", "eval"), {"Path": Path, "__file__": str(app)})
print("DICT_PATH      :", dict_path.relative_to(ROOT), "exists =", dict_path.exists())
MODE06_DICT = json.loads(dict_path.read_text()) if dict_path.exists() else {}
real = ROOT / "labs/dtclab/dtclab/config/mode_06_hex_dictionary.json"
REAL = json.loads(real.read_text())
mon_id = "MID_01_TID_80"
mid_hex = mon_id.split("_")[1]
print("UI caption     : Component:", MODE06_DICT.get(mid_hex, {}).get("name", "UNKNOWN"))
print("shipped dict   : Component:", REAL.get(mid_hex, {}).get("name", "UNKNOWN"), f"({real.relative_to(ROOT)})")
print("MIDs resolvable: UI", sum(1 for k in MODE06_DICT if not k.startswith("_")), "of", sum(1 for k in REAL if not k.startswith("_")))
