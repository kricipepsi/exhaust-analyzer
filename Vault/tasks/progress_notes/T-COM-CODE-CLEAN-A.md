## Plan

Task: `T-COM-CODE-CLEAN-A` — codingskills audit + AST-legibility pass for the COMLab atlas routing spine.

Target files:
- `labs/comlab/comlab/core/fault_atlas_router.py`
- `labs/comlab/comlab/core/fault_atlas_kg.py`

Skills/passes loaded:
- `comlab-python`
- `comlab-verification-loop`
- `comlab-code-review`
- `improve-codebase-architecture`
- `uncle-bob-craft`
- `code-simplifier`
- `code-review-excellence`
- `pythonskill`

Scope guard:
- No behavior change.
- No schema field or enum additions.
- No graphify / graph rebuild.
- No cross-lab Python imports.
- Only scoped legibility fixes in the router/KG files, plus this progress note and VAULT ledger update if gates pass.

Target symbols confirmed from `labs/comlab/graph/v2_current/graph.json`:
- `FaultAtlasRouter`
- `FaultAtlasKG`
- `OBDConstraint`
- `DTCLabStatusRule`
- `CrossDomainMatrix`
- `ConfidenceScoring`
- `RegistryRow`
- `RegistryFile`
- `TriageVerdict`

VERIFICATION GATE — T-COM-CODE-CLEAN-A
======================================
Interpreter note: the mandated `../../.sandbox-py/bin/python3.14` is a Linux ELF binary on this Windows host; WSL has no installed distributions, so it cannot be executed here. Final gate used the lab-local executable Python 3.14.6 at `.venv-comlab/Scripts/python.exe`. A separate Windows `C:\Python314\python.exe` run was rejected for final gate because its environment lacked optional OpenTelemetry packages and produced pyright import errors.

Phase 1 Syntax/import:  PASS
- `python -m py_compile comlab/core/fault_atlas_router.py comlab/core/fault_atlas_kg.py`
- `import comlab.core.fault_atlas_router; import comlab.core.fault_atlas_kg` → `IMPORT_PASS`

Phase 2 Type check:     PASS
- `.venv-comlab/Scripts/python.exe -m pyright --pythonpath .venv-comlab/Scripts/python.exe comlab/`
- Result: `0 errors, 0 warnings, 0 informations`

Phase 3 Lint:           PASS
- `.venv-comlab/Scripts/python.exe -m ruff check .`
- Result: `All checks passed!`

Phase 4 pytest:         PASS
- `.venv-comlab/Scripts/python.exe -m pytest -x -q`
- Result: `509 passed, 4 skipped`

Phase 5 Wiki/orphan:    PASS
- No schema fields, enums, or faults added; anti-orphan check not applicable.
- Final diff numeric additions are named constants with inline `# wiki:` citations.
- `rg "import \*"` on scoped files: `OK no star-import`.
- `rg "from (gaslab|obdlab|dtclab|dnalab|vinlab|symptomlab)"` on scoped files: `OK isolated`.

Phase 6 Diff review:    PASS
- Scoped files only: `fault_atlas_router.py`, `fault_atlas_kg.py`, this progress note, and VAULT ledger/task status.
- No graphify / graph rebuild run.
- No behavior change: explicit `__all__`, named constants replacing identical literals, a private return annotation, and equivalent readability simplifications.

comlab-python checklist items applied:
- 1 Type hints: checked; `_sentinel_echo_audit` return annotation added.
- 2 Docstrings: public module/class/function docstrings checked.
- 3 No mutable defaults: checked.
- 4 No bare except: checked scoped files for `except:`.
- 5 No magic numbers: repeated thresholds named and wiki-cited.
- 6 f-strings: existing style preserved; no `%`/`.format()` introduced.
- 7 Pathlib: existing `Path` usage preserved.
- 8 Context managers: no new file/session handling introduced.
- 9 `is None`: checked; no `== None` introduced.
- 10 Sorted imports: ruff clean.

Status: DONE — flipping VAULT ledger row to done.

CODE REVIEW — T-COM-CODE-CLEAN-A
================================
1. Design rules:        PASS — no cross-lab import, no raw-sensor/DTC/chemistry re-derivation added, no signal/noise surface added.
2. Scope compliance:    PASS — scoped router/KG source files plus required progress/ledger metadata only.
3. Contracts:           PASS — no schema or public method signature contract changed; module export surfaces are now explicit.
4. Docstrings:          PASS — public symbols remain documented; no undocumented public function/class introduced.
5. Wiki provenance:     PASS — new numeric constants carry inline wiki citations.
6. Immediate Checklist: PASS — no mutable defaults, bare excepts, prints, or `None` comparison issues introduced.
7. Test coverage:       PASS — existing router/KG and full COMLab tests passed; no behavior branch added requiring new tests.
8. Structural craft:    PASS with notes — `FaultAtlasRouter` remains intentionally large and decision-heavy; this task reduced opacity by naming repeated thresholds and declaring public surfaces. A deeper Phase-5 evidence adapter split remains a future architecture candidate, not a safe code-clean change here.

Verdict: CLEAN
Blockers: none
