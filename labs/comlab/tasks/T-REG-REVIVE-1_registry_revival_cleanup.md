# T-REG-REVIVE-1 — Registry revival cleanup (run BEFORE T-COMV2-DELTA-2)

**Authored:** 2026-06-21 (architect, Cowork). **Stage:** 4 (COMLab). **Type:** cleanup / de-contamination of the revived v2 registry. **Blocks:** `T-COMV2-DELTA-2`.
**Basis:** `tasks/REGISTRY_REVIVAL_AUDIT_2026-06-20.md` (full findings). **Drill:** boot order → this file → scope-confirm before code.

> **One-line scope:** the v2 registry was moved out of `ARCHIVE/` into `labs/comlab/registry/`. Make that revived copy clean and unambiguous — purge stale bytecode, fix the `ignition_fault` orphan, relocate non-runtime docs out of the import root, and confirm the suite is `0 failed` on the mandated interpreter — so `T-COMV2-DELTA-2` builds on a trustworthy registry.

## ⚠ Read first — the registry is NOT absent (correct the record)

A prior session reported "registry absent, only `ARCHIVE/registry`." **That is stale.** The canonical, live copy is now:

```
labs/comlab/registry/        ← CANONICAL. Importable as `registry` (labs/comlab is on sys.path).
ARCHIVE/registry/            ← OLD snapshot. Do NOT import from or edit. Leave archived (archive-never-delete).
```

Confirm for yourself before anything else (mandated interpreter — see `tasks/COMLAB_PYTHON_ENV_SETUP.md`):
```bash
cd labs/comlab
$PY -c "import sys; sys.path.insert(0,'.'); from registry.integration_shim import route_case_with_diagnostics; print('OK')"
$PY -m pytest tests/unit/test_fault_atlas_router_v2.py -q     # expect: 4 passed (these were the 2 known reds)
```
If those pass, the DELTA-2 import blocker is already gone; this task is the cleanup, not a rescue.

## Steps

1. **Purge caches + stale bytecode** under `labs/comlab/registry/` — `__pycache__/`, `.pytest_cache/`, `.ruff_cache/`. They hold **30 `cpython-312` + 4 `cpython-313` `.pyc`** (repo is 3.14-only); stale bytecode can shadow a source edit.
   ```powershell
   Get-ChildItem -Recurse -Directory -Include __pycache__,.pytest_cache,.ruff_cache | Remove-Item -Recurse -Force
   ```
   (bash: `find labs/comlab/registry -type d \( -name __pycache__ -o -name .pytest_cache -o -name .ruff_cache \) -exec rm -rf {} +`)

2. **Resolve the `ignition_fault` empty-rule stub** (corrected scope — it is NOT vestigial). `ignition_fault` is a **live family**: spark-generation failure, pre-combustion (`comlab/schemas/vocabulary.py:234, lld §3.1`) — distinct from `misfire` (combustion event), separated by DTC (P0351 coil-driver vs P030x). It is wired into the KG (7 nodes in `comlab/config/kg/ignition_fault.json`), `schemas/{kg,response,vocabulary}.py`, `symptom_prior.yaml`, 3 registry corpus cases, and a live e2e (`tests/e2e/test_diagnostic_engine.py::test_e2e_ignition_fault_coil_driver` → `ERR-IF-001`, served via the v1/KG path). **DO NOT touch the enum, KG, or family.**
   The only defect: `registry/rules/ignition_fault.json` is an **empty stub** (`"rules": []` — the lone unauthored registry family) sitting on disk while correctly absent from `_EXPECTED_RULE_FILES`. Under glob-mode (tests) it loads as an empty family; under prod (fixed list) it doesn't — an inconsistency. **Cleanup action: delete the empty `registry/rules/ignition_fault.json`** (it is not loaded in prod and the suite already passes via the KG path → safe). Then rules-dir and manifest agree.
   Authoring the real v2-registry rule for spark-generation failure (IGNITION_MISFIRE + P0351 + positive trim → ERR-IF-001) is **separate deferred work → `REG-V2-AUTHOR-ignition_fault`**, validated against the 3 `expected_top_fault_family: ignition_fault` corpus cases. **Not in this cleanup.**

3. **Relocate non-runtime files out of the import root** (to `labs/comlab/registry/docs/` or `ARCHIVE/registry-docs/` — move, never delete). These are a parallel project's process docs and risk confusing the boot drill (note the duplicate `START_HERE`/`PROGRESS` inside a lab):
   `CHEMISTRY_COVERAGE.md`, `CORPUS_AUDIT.md`, `REGISTRY_AUDIT.md`, `REGISTRY_PROGRESS.md`, `REGISTRY_START_HERE.md`, `REGISTRY_START_HERE_AUDIT_RESPONSE.md`, `SCHEMA_V2_SPEC.md`, `Vol5.md`, `cvsgaps.md`, `registry_tasks/`, `_registry_skills/`.

4. **Review (decide + note in progress note):**
   - `pyrightconfig.json` (`{"extraPaths": [".."]}`) — duplicate of `pyproject [tool.pyright]`. Keep (helps standalone analysis) or fold into pyproject + remove. Either is fine; just record the choice.
   - `corpus_curated.csv` + `corpus_meta.json` + `tools/build_corpus.py` + `tests/test_build_corpus.py` — **not runtime** (the shim loads `rules/`, never the corpus). **Lean keep:** the corpus now has a named future consumer — the 3 `ignition_fault` cases validate `REG-V2-AUTHOR-ignition_fault`. Archive only if you also drop that authoring task.

## Success criteria (done = all)

- `registry` imports as `registry.integration_shim` from `labs/comlab`; **only one canonical copy is on the import path** (ARCHIVE copy not importable/edited).
- Empty `registry/rules/ignition_fault.json` stub **deleted**; enum/KG/family **untouched**; production and test rule sets now **agree** — assert this (a test that `_EXPECTED_RULE_FILES == sorted(p.name for p in rules_dir.glob("*.json"))`). Registry-rule authoring deferred to `REG-V2-AUTHOR-ignition_fault`.
- Non-runtime docs/tasks no longer sit at `registry/` import root.
- Full suite on the mandated interpreter: **`0 failed`** (`$PY -m pytest tests/ -q`); `ruff check .` clean; `$PY -m pyright --pythonpath $PY comlab/ registry/` clean.
- `VERIFICATION GATE` + `CODE REVIEW` filled in `progress_notes/T-REG-REVIVE-1.md`; flip the ledger row → `done`. Then **STOP** — DELTA-2 is now unblocked.

## Out of scope

- **No DELTA-2 work** (no v2 re-rank wiring, no `COMLab-DELTA-V2`). That is the next task, gated on this.
- No changes to `delta_engine.py` / DELTA-1 (done & green).
- No deleting `ARCHIVE/registry` (archive-never-delete); just stop using it.
- No rule *content* re-authoring beyond the `ignition_fault` decision; no corpus rebuild; no graphify/KG rebuild.

## Verification

```bash
cd labs/comlab
$PY -m ruff check .
$PY -m pyright --pythonpath $PY comlab/ registry/
$PY -m pytest tests/ -q                       # expect 0 failed
$PY -m pytest registry/tests/ -q              # registry's own rule + shim tests
grep -rn "ignition_fault\|IGNITION_FAULT" registry/   # consistent with your decision
find labs/comlab/registry -name "*.pyc" | sed -E 's/.*cpython-([0-9]+).*/\1/' | sort -u   # expect: 314 only
```
