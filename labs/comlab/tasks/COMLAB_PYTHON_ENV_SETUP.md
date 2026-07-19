# COMLab — Python environment setup (per-runtime adapted interpreter)

**Written:** 2026-06-20 (architect, Cowork). **Why:** the `T-COMV2-DELTA-2` session stalled because it tried to run the mandated `.sandbox-py` interpreter under native Windows PowerShell. `.sandbox-py` is a **Linux ELF binary** (a Python compiled for Linux) — it cannot execute as a native Windows program. The interpreter is fine; the mismatch is *where it was run*.

> **Core rule:** the toolchain target is **Python 3.14.x + pydantic 2.13.x + pytest 9.1.x + ruff + pyright**. *How* you get a 3.14 interpreter depends on your runtime. Each runtime uses its **own adapted interpreter** — they are not interchangeable binaries.
>
> **Manager note:** fold this into the parent `4DLab\CLAUDE.md` (the single source of truth for venv/sandbox ritual). This file is a coder-facing clarification, not a competing infra spec.

## Pick the row that matches how you were launched

```
runtime                         interpreter to use                         notes
──────────────────────────────  ─────────────────────────────────────────  ──────────────────────────────
Sandboxed agent (Cowork/Linux)  .sandbox-py/bin/python3.14                  ELF runs natively here. ✅ works.
Host coder in WSL / bash        .sandbox-py/bin/python3.14  (via WSL)       same ELF, Linux userland present.
Host coder in native PowerShell native Windows venv, py 3.14 (see below)    ELF can't run; build a PE-native venv.
```

The earlier fallback to **DTCLab's venv** (`C:\Workspace\labs\dtclab\.venv`) was wrong — it is a different lab's environment and gave misleading results. Do not use it for COMLab.

## A. Sandboxed / WSL / bash coder — use the mandated interpreter

```bash
PY="$REPO/.sandbox-py/bin/python3.14"      # $REPO = .../C/Workspace
cd labs/comlab
$PY -m pip install -e .                      # editable-install so imports resolve
$PY -m ruff check .
$PY -m pyright --pythonpath "$PY" comlab/    # --pythonpath = resolve pydantic et al.
$PY -m pytest -x -q
```
If on Windows-with-WSL, the coder's earlier `wsl.exe --cd /mnt/c/Workspace/labs/comlab .../python3.14 ...` form is correct **once a WSL distro is installed** (`wsl --install -d Ubuntu`). The previous failure was "no WSL distribution," not a Python problem.

## B. Native PowerShell coder — build a Windows-native 3.14 venv

The `.sandbox-py` ELF will never run here. Create a matching native interpreter once:

```powershell
# 1. Install CPython 3.14 for Windows (python.org or winget: `winget install Python.Python.3.14`)
# 2. Create + activate a COMLab-local venv
py -3.14 -m venv C:\Workspace\labs\comlab\.venv-comlab
C:\Workspace\labs\comlab\.venv-comlab\Scripts\Activate.ps1
# 3. Mirror the toolchain (versions from .sandbox-py: pydantic 2.13.4, pytest 9.1.0)
python -m pip install -e .
python -m pip install "pydantic==2.13.*" "pytest==9.1.*" ruff pyright jsonschema
# 4. Inner loop (venv activated → pyright resolves packages without --pythonpath)
ruff check .
pyright comlab\
pytest -x -q
```
This is a **sanctioned per-host adaptation**, not a divergence from canon: same 3.14 language level, same pinned deps. Keep its versions in step with `.sandbox-py`; drift between the two is the thing to watch.

## Known-red baseline (every environment)

Two tests fail everywhere because the `registry` module is absent from this checkout (same family as the missing `v2-restructure/`):

```
tests/unit/test_fault_atlas_router_v2.py::test_v1_when_explicit_false
tests/unit/test_fault_atlas_router_v2.py::test_v2_when_explicit_true   → ModuleNotFoundError: No module named 'registry'
```
These are **pre-existing and not yours.** A green run = `2 failed, 370 passed` with both failures being exactly these. (Verified 2026-06-20 on the mandated interpreter — see `progress_notes/DELTA_ENV_VERIFICATION_2026-06-20.md`.)

## pyright gotcha (the "12 errors" that weren't)

Running bare `pyright` with no environment reports phantom `reportMissingImports` for `pydantic`/`opentelemetry` and pins them on your diff. Always run pyright **from the activated venv** or with **`--pythonpath <interpreter>`**. `pyproject.toml [tool.pyright]` now pins `pythonVersion = "3.14"` but cannot know your interpreter path — that is yours to supply.
