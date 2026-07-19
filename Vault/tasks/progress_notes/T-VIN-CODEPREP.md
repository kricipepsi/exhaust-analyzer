# T-VIN-CODEPREP - progress note

**Status:** `done` - package audit/fixes complete; ledger row closed.
Task spec: `Vault/tasks/T-VIN-CODEPREP_*.md` - Pack ledger: `Vault/tasks/VIN_VAULT_TASKS_START_HERE.md`

## Plan

Scope: `labs/vinlab/vinlab/**/*.py` only; tests/wiki/data excluded. Consumer is the future AST code graph
`graph/v2_code`, feeding vault module/source frontmatter and the design-code-test spine. No schema fields,
no behavior changes, and no graphify run in this task.

## 4dlab-code-ingest: vinlab/vinlab / audit report

Pre-check:
- `python -m pytest -q` passed: `177 passed, 11 skipped`.
- The 11 skips are expected environment-gated fixture/data skips under the corrected spec: build artifact
  tests look under `tests/vinlab/data`, external sample VINs are absent, OPSI CSV is absent, and one
  parametrized fixture is empty. They are recorded, not charged to this task.
- Package data files required by `vinlab/data/` exist: `wmi.csv`, `vds_engine_map.csv`, `years.csv`, `vref.db`.

Machine-checkable audit:

| file:line | rule | found | fix |
|---|---|---|---|
| `vinlab/decoder.py:36` | A | public decoder surface lacked module `__all__` | added `ChassisNumberError`, `RobustVINDecoder`, `VINDecodeError`, `pre_clean_vin` |
| `vinlab/models.py:17` | A | model/schema surface lacked module `__all__` | added public enum/dataclass export list |
| `vinlab/db/__init__.py:3` | A | package marker had no explicit export surface | added empty typed `__all__` |
| `vinlab/db/tecdoc_query.py:13` | A | DB helper surface lacked module `__all__` | added `lookup_engine_ref`, `open_vref_readonly` |
| `vinlab/overlay/__init__.py:3` | A | package marker had no explicit export surface | added empty typed `__all__` |
| `vinlab/overlay/air_metering.py:13` | A | public classifier surface lacked module `__all__` | added `AirMeteringClassification`, `classify_air_metering` |
| `vinlab/overlay/cylinder_heuristic.py:15` | A | public cylinder fallback surface lacked module `__all__` | added `CylinderHint`, `infer_cylinder` |
| `vinlab/overlay/horizon.py:7` | A | public horizon mapper lacked module `__all__` | added `euro_to_horizon` |
| `vinlab/overlay/stress_rpm.py:12` | A | public stress-RPM mapper lacked module `__all__` | added `stress_idle_rpm` |
| `vinlab/overlay/switches.py:7` | A | public O2 switch mapper lacked module `__all__` | added `derive_upstream_o2_type` |

Rule summary:
- I: no `import *` found.
- A: fixed all missing public export surfaces in package, DB, decoder, models, and overlays.
- T: AST scan found no missing annotations on public module functions or public class methods.
- C: one static dispatch table remains in `cylinder_heuristic.py`; it is intentional brand-rule dispatch,
  uses statically named local handlers, and is not changed.
- E: domain states are real `StrEnum`s in `models.py`.
- R/D: source already carries rationale/source comments and docstrings for the non-obvious gates checked in scope.

Probe note:
- The VIN pack says graphify is sanctioned only inside `T-VIN-GRAPH-AST`; no graphify command was run here.

## VERIFICATION GATE

- `python -m pytest -q` before prep: passed, `177 passed, 11 skipped`, zero failures.
- Audit fixes applied only under `labs/vinlab/vinlab/`.
- `python -m ruff check .`: passed.
- `python -m pyright vinlab tests`: passed, `0 errors`.
- `python -m pyright`: failed on out-of-scope build/temp/tool scripts with missing `mysql.connector`/`pyngrok`
  imports and one existing tool-script type issue; this is logged in `VIN_VAULT_TASKS_START_HERE.md` section 6
  and is not charged to this package-scoped task.
- `python -m pytest -x -q`: passed, `177 passed, 11 skipped`, zero failures.
- Star import check: `OK no star-import`.
- `graphify` not run, per VIN pack non-negotiable.

Gate status: clean for the corrected package-scoped task.

## CODE REVIEW

Explicit `__all__` declarations were added across decoder, models, DB, and overlay modules. The lists include
the public symbols used by the decoder and downstream package imports: `RobustVINDecoder`, `pre_clean_vin`,
`classify_air_metering`, `infer_cylinder`, `euro_to_horizon`, `stress_idle_rpm`, and
`derive_upstream_o2_type`.

Review result: legibility-only structural change. No decoder behavior, model fields, schema shape, data files,
tests, or graph directories changed. Signal/noise is N/A: this adds no schema field and only improves AST export
surface clarity for `graph/v2_code`.
