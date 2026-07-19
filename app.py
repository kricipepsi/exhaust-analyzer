"""Render entrypoint shim — delegates to the real UI at apps/ui/app.py.

Keeps the existing Render service contract (`streamlit run app.py` at repo
root) working against the 4DLabV2 layout. `apps/ui` is put on sys.path so the
UI's sibling import (`ui_payload`) resolves; `wired` + labs come from the
editable installs in requirements.txt.
"""
import runpy
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(_ROOT / "apps" / "ui"))

runpy.run_path(str(_ROOT / "apps" / "ui" / "app.py"), run_name="__main__")
