# T-KG-OBD-2-PREP - Code-prep `obdlab` source for code-map ingest

## Plan

Scope: production package `labs/obdlab/obdlab/` only. No tests, research, `graph/*`,
canonical `graphify-out/`, or real code-map build were touched.

Applied `4dlab-code-prep` as a manual audit/fix/report pass:

1. Probe the local graphify extraction engine because the package version changed.
2. Audit machine-checkable rules I/A/T/C/S plus kept R/D.
3. Apply only behavior-neutral edits tied to a named Pass-1 consumer.
4. Run the OBDLab inner loop and graph-collateral guards.

Probe answers, `graphifyy` package `0.8.35`:

| Probe | Answer | Scope result |
|---|---:|---|
| Enum member `STABILIZED_IDLE` present as its own node | NO | Rule E dropped |
| `# WHY:` comment emitted as `file_type: rationale` | YES | Rule R kept |
| Formula docstring emitted as `file_type: rationale` | YES | Rule D kept |

The only graphify invocation was the permitted throwaway probe in
`C:\tmp\gfx_probe`; it wrote only `C:\tmp\gfx_probe\graphify-out`.

## Audit Fix Plan

Before counts:

| Rule | Count | Finding | Fix |
|---|---:|---|---|
| I | 0 | No star imports in `obdlab` | None |
| A | 2 | `obdlab/core/__init__.py`, `obdlab/schemas/__init__.py` lacked `__all__` | Add public package exports |
| T | 1 | `obdlab/core/pid_ingestion_validator.py:36` constructor lacked return annotation | Add `-> None` |
| C | 1 advisory | `obdlab/core/state_bucketing.py:110` uses `getattr` for a config-selected DNA field | Report only; legitimate live indirection |
| S | 0 | No runtime-generated query symbols found | None |
| R | 0 | Existing non-obvious gates already carry wiki/rationale comments | None |
| D | 0 | Formula/validation candidates already have docstrings | None |

Applied edits and consumers:

| File | Rule | Consumer |
|---|---|---|
| `obdlab/core/__init__.py` | A | God-node ranking + package entry-point nodes |
| `obdlab/schemas/__init__.py` | A | God-node ranking + package entry-point nodes |
| `obdlab/core/pid_ingestion_validator.py` | T | Type-reference edges for public constructor signature |

After counts:

| Rule | Count |
|---|---:|
| I star imports | 0 |
| A package `__init__.py` missing `__all__` | 0 |
| T public signature annotation gaps | 0 |
| C forced edits | 0 |
| S runtime-generated query symbols | 0 |
| R/D forced edits | 0 |

Remaining C advisory: `state_bucketing.py:110` resolves the whitelisted
`stress_idle_rpm_target` DNA field from configuration. Replacing it would be a
logic change and is out of scope for this prep task.

## VERIFICATION GATE

Commands run from `C:\Users\muto\claude\4DApp\4DLab\4DLabV2\labs\obdlab`:

```powershell
Select-String -Path 'obdlab\*.py','obdlab\*\*.py' -Pattern 'from\s+\S+\s+import\s+\*'
Get-ChildItem -Path 'obdlab' -Recurse -Filter '__init__.py' | ForEach-Object { if (-not (Select-String -LiteralPath $_.FullName -Pattern '__all__' -Quiet)) { $_.FullName } }
C:\Users\muto\claude\4DApp\4DLab\.venv-wired\Scripts\ruff.exe check obdlab
C:\Users\muto\claude\4DApp\4DLab\.venv-wired\Scripts\pyright.exe obdlab
C:\Users\muto\claude\4DApp\4DLab\.venv-wired\Scripts\python.exe -m pytest -x -q
git status --porcelain -- '4DLab/4DLabV2/labs/obdlab/graph'
```

Results:

- Star imports: PASS, no matches.
- `__all__`: PASS, no package `__init__.py` missing `__all__`.
- Public signature annotation gaps: PASS, 0.
- Ruff: PASS, `All checks passed!`.
- Pyright: PASS, `0 errors, 0 warnings, 0 informations`.
- Pytest: PASS, `384 passed, 6 skipped in 0.54s`.
- `graph/*` collateral: PASS, no changed files.
- Canonical `graphify-out` collateral: PASS by mtime/status review. The repo already had untracked `4DLabV2/graphify-out/` and `labs/obdlab/graphify-out/`; both predate this task and were not touched.

Pythonskill checklist:

1. Type hints - applied to the one missing public constructor return.
2. Docstrings - package `__init__.py` modules now document their public entry-point role.
3. No mutable defaults - checked; no edit introduced any.
4. No bare except - checked; no edit introduced any.
5. No magic numbers - checked; no numeric literals added.
6. f-strings - not applicable.
7. Pathlib - no file-operation code added.
8. Context managers - no resource-management code added.
9. `is None` - no comparison code added.
10. Sorted imports - ruff verified.

## CODE REVIEW

PASS. Diff is limited to kept-rule code-prep edits:

- Rule A: explicit `__all__` package surfaces for `core` and `schemas`.
- Rule T: `PIDIngestionValidator.__init__` return annotation.

No behavior logic changed, no schema fields/channels were added, no cross-lab imports were introduced,
and no real OBDLab code graph was built.
