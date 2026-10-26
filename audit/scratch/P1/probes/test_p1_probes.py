"""P1 probes: each CONFIRMED sweep record, shown running. Run from the repo root:
    python -m pytest -q audit/scratch/P1/probes/test_p1_probes.py
Each test PASSES when the defect is present (it asserts the defective behaviour).
"""
from __future__ import annotations

import ast
import os
import shutil
import sqlite3
import subprocess
import sys
import tomllib
import types
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(scope="module")
def clean_venv(tmp_path_factory):
    """Fresh Python 3.14 venv with nothing installed (uv; no network beyond PyPI)."""
    if not shutil.which("uv"):
        pytest.skip("uv not on PATH")
    d = tmp_path_factory.mktemp("venv")
    subprocess.run(["uv", "venv", "-q", "-p", "3.14", str(d / "v")], check=True)
    return d / "v" / "bin" / "python"


def _install(py: Path, src: Path, tmp: Path, extra: str = "") -> subprocess.CompletedProcess:
    copy = tmp / src.name
    shutil.copytree(src, copy, ignore=shutil.ignore_patterns("*.egg-info", "__pycache__", "tests", "graph",
                                                              "research", "wiki", "docs", "tasks"))
    return subprocess.run(["uv", "pip", "install", "--python", str(py), f"{copy}{extra}"],
                          capture_output=True, text=True)


# F-P1-1 — dnalab declares no dependencies but imports vinlab and symptomlab at module level.
def test_dnalab_manifest_omits_vinlab_symptomlab(clean_venv, tmp_path):
    meta = tomllib.loads((ROOT / "labs/dnalab/pyproject.toml").read_text())["project"]
    assert "dependencies" not in meta
    r = _install(clean_venv, ROOT / "labs/dnalab", tmp_path)
    assert r.returncode == 0, r.stderr
    imp = subprocess.run([str(clean_venv), "-c", "import dnalab"], capture_output=True, text=True)
    assert imp.returncode != 0
    assert "ModuleNotFoundError: No module named 'symptomlab'" in imp.stderr


# F-P1-2 — the tracing fallback tells the operator to install comlab's [tracing] extra, which does not exist.
def test_comlab_tracing_extra_missing(clean_venv, tmp_path):
    src = (ROOT / "labs/comlab/comlab/observability/_tracer.py").read_text()
    assert 'pip install -e ".[tracing]"' in src
    extras = tomllib.loads((ROOT / "labs/comlab/pyproject.toml").read_text())["project"]["optional-dependencies"]
    assert "tracing" not in extras
    r = _install(clean_venv, ROOT / "labs/comlab", tmp_path, "[tracing]")
    assert r.returncode == 0, r.stderr
    assert "does not have an extra named `tracing`" in r.stderr
    imp = subprocess.run([str(clean_venv), "-c", "import opentelemetry.sdk"], capture_output=True, text=True)
    assert "No module named 'opentelemetry'" in imp.stderr


# F-P1-3 — UI Mode $06 dictionary path resolves under apps/, so every monitor caption reads UNKNOWN.
def test_ui_mode06_dict_path_never_exists():
    app = ROOT / "apps/ui/app.py"
    tree = ast.parse(app.read_text())
    expr = next(n.value for n in tree.body if isinstance(n, ast.Assign)
                and getattr(n.targets[0], "id", "") == "DICT_PATH")
    dict_path = eval(compile(ast.Expression(expr), "app.py", "eval"), {"Path": Path, "__file__": str(app)})
    assert dict_path.resolve() == (ROOT / "apps/dtclab/dtclab/config/mode_06_hex_dictionary.json").resolve()
    assert not dict_path.exists()
    real = ROOT / "labs/dtclab/dtclab/config/mode_06_hex_dictionary.json"
    assert real.exists()
    # app.py:132-138 then leaves MODE06_DICT = {}; app.py:680 lookup for MID_01_TID_.. gives:
    mode06: dict = {}
    assert mode06.get("01", {}).get("name", "UNKNOWN") == "UNKNOWN"
    import json
    assert json.loads(real.read_text())["01"]["name"] == "O2 Sensor Response B1S1"


# F-P1-4 — VINLab offline builder splices the OPSI engine code into SQL without escaping.
def test_ktype_bridge_engine_code_unescaped(monkeypatch, tmp_path):
    monkeypatch.setenv("VEHICLE_DATA_ROOT", str(tmp_path))
    fake = types.ModuleType("mysql")
    fake.connector = types.ModuleType("mysql.connector")
    monkeypatch.setitem(sys.modules, "mysql", fake)
    monkeypatch.setitem(sys.modules, "mysql.connector", fake.connector)
    monkeypatch.syspath_prepend(str(ROOT / "labs/vinlab"))
    import importlib.util
    spec = importlib.util.spec_from_file_location("ktb", ROOT / "labs/vinlab/tools/tecdoc_ktype_bridge.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    sql = mod._build_layer_query("VW", 1600, 75, "AB'C")
    assert "REPLACE('AB'C', ' ', '')" in sql
    clause = "SELECT UPPER(REPLACE('AB'C', ' ', ''))"
    with pytest.raises(sqlite3.OperationalError):
        sqlite3.connect(":memory:").execute(clause)  # the same literal is not valid SQL
    inj = mod._build_layer_query("VW", 1600, 75, "X') OR ('1'='1")
    assert "= UPPER(REPLACE('X') OR ('1'='1', ' ', ''))" in inj  # the hint rewrites the WHERE clause
