## Plan

Task scope is intentionally narrow: close the parent task's schema-contract gap by declaring `FreezeFrameRecord.ff_fuel_spark_cut_at_crank` as a real Pydantic field, keep the existing extractor predicate unchanged, and prove the extractor-populated value survives as a declared field in `model_dump()`.

Implementation checklist:

- [x] Confirm graph locations for `FreezeFrameRecord`, `extract_freeze_frame`, and `tests/unit/test_freeze_frame_extractor.py`.
- [x] Keep the existing extractor predicate and CAN-era Mode $06 logic untouched.
- [x] Ensure the schema field carries the pinned `10_nonstart_diagnostics.md §10.3` wiki cite.
- [x] Add a constructed-record round-trip test through `FreezeFrameRecord.model_fields` and `model_dump()`.
- [x] Run verification gate.
- [x] Complete code review notes and update `tasks/PROGRESS.md` plus the parent progress note.

## VERIFICATION GATE

Commands run from `labs/dtclab` on 2026-06-16:

- `.\.venv\Scripts\ruff.exe check .` -> PASS (`All checks passed!`)
- `.\.venv\Scripts\pyright.exe --pythonpath .\.venv\Scripts\python.exe dtclab/` -> PASS (`0 errors, 0 warnings, 0 informations`)
- `.\.venv\Scripts\pytest.exe -x -q` -> PASS (`590 passed in 3.87s`)

Structural checks:

- `rg -n "ff_fuel_spark_cut_at_crank" dtclab/schemas/freeze_frame.py` -> PASS, declared field found at `dtclab/schemas/freeze_frame.py:95`.
- `.\.venv\Scripts\python.exe -c "from dtclab.schemas.freeze_frame import FreezeFrameRecord; assert 'ff_fuel_spark_cut_at_crank' in FreezeFrameRecord.model_fields, 'not a declared field'"` -> PASS.
- `rg -rniE "security[_-]?lockout|mechanical[_-]?no[_-]?start" dtclab/` -> PASS, no DTCLab verdict strings.
- `rg -rnE "from (gaslab|obdlab|comlab|dnalab)" dtclab/` -> PASS, no cross-lab imports.
- `rg -n "classify_margin" dtclab/core/mode06_evaluator.py` -> PASS, symbol still present; this task did not edit `mode06_evaluator.py`.

## CODE REVIEW

- Scope stayed pinned to the schema contract and constructed-record coverage. The extractor predicate, CAN-era gate, `mode06_evaluator.py`, and `vocabulary.py` were not changed.
- `ff_fuel_spark_cut_at_crank` is now a declared `FreezeFrameRecord` field and appears in `model_dump()`, so downstream COMLab S4 code can rely on the schema contract rather than an undeclared runtime attribute.
- The parent progress record has been corrected back to `done`, with the post-commit schema gap and this fix recorded in the parent progress note.
