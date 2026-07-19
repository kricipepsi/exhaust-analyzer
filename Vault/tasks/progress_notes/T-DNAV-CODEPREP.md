# T-DNAV-CODEPREP — Progress Notes

## Plan

`4dlab-code-prep` probe→audit→report on `labs/dnalab/dnalab/` (3 files: `__init__.py`, `assembly.py`, `models.py`). Composition-layer package — domain-enum lever waived. Pre-check pytest green (27 passed), probe confirms R/D rules active (E waived), audit flags rationale gaps + docstring gaps only, coder applies fixes under inner loop.

## VERIFICATION GATE

### Pre-prep suite green
```
27 passed in 0.07s
```
No skips, no failures. `test_real_pipeline_smoke` passed (sibling labs available).

### Probe results (throwaway sample, graphify 0.8.13)
- E (enum sub-nodes): **NO** → waived from audit (composition layer, no domain enums)
- R (rationale from `# WHY:`): **YES** → in scope
- D (rationale from docstrings): **YES** → in scope

### Audit results (rules I, A, T, C, S, R, D)
| Rule | Result |
|------|--------|
| I — Star imports | PASS — none found |
| A — `__all__` | PASS — `["build_vehicle_dna", "VehicleDNA"]` matches shipped symbols |
| T — Type hints | PASS — all 5 public signatures fully typed; dataclass fields annotated |
| C — Dynamic dispatch | PASS — no `getattr`/`importlib`/dispatch dicts |
| S — Runtime symbols | PASS — no `type()` constructions |
| E — Explicit enums | WAIVED (probe=no + DNALab composition layer — START_HERE §0.2) |
| R — Rationale tags | **3 gaps fixed** |
| D — Docstrings | **2 gaps fixed** |

### Fixes applied (4 edits, 2 files)
1. `models.py:18` — `SCHEMA_VERSION = "1.2"` + `# WHY:` cite to SEMANTIC_CONTRACT.md §4.3
2. `models.py:94` — `# WHY:` on schema_version mismatch strict-match gate
3. `assembly.py:33` — `# WHY:` on required triage keys guard
4. `models.py:36` — docstring for `VehicleDNA.new()` (session_id/timestamp auto-generation)
5. `models.py:77` — docstring for `VehicleDNA.to_json()`

### Inner loop post-fix
```
ruff check .   — All checks passed!
pyright        — 0 errors, 0 warnings, 0 informations
pytest -x -q   — 27 passed in 0.07s
```

### Confirmations
- No `import *` anywhere
- `__all__` matches shipped symbols
- All public signatures typed
- No domain-enum lever expected (composition layer — noted, not flagged)
- No behaviour change — comments + docstrings only
- `to_json_payload` keys unchanged: session_id, timestamp, schema_version, vin_dna, symptom_dna
- No graphify run performed
- No schema field added/removed

## CODE REVIEW

**Violations found:** 5 (3 missing `# WHY:` rationale tags + 2 missing docstrings)
**Violations fixed:** 5 (all in-scope)
**No behaviour change:** confirmed — only comments and docstrings added; all 27 tests pass unchanged; wire shape byte-identical
**Out of scope (correctly waived):** E (enum sub-nodes — probe returned no + DNALab has no domain enums); TESTPREP (separate task); graphify run (separate task)
