# T-DTCV2-NOSTART-1-FIX — declare `ff_fuel_spark_cut_at_crank` on `FreezeFrameRecord`

**Status:** `pending` (authored 2026-06-16 · coder-runnable) · **Lab:** DTCLab · **Stage:** 3 · **Mode:** STRICT
**Parent:** `T-DTCV2-NOSTART-1` (committed `240f3c5`) · **Blocked by:** —
**Consumer (signal/noise):** same as parent — COMLab `T-COMV2-NOSTART-1` (S4) reads
`FreezeFrameRecord.ff_fuel_spark_cut_at_crank` in the `fault_atlas` no-start branch.

## Why this exists

Post-commit review of `240f3c5` found the parent task's **Deliverable #3 incomplete**.
`ff_fuel_spark_cut_at_crank` is computed in `core/freeze_frame_extractor.py` (with a `§10.3` wiki cite)
but is **not declared as a field on `FreezeFrameRecord`** — `schemas/freeze_frame.py` still carries only
the original six §12.3 flags (`ff_open_loop_at_fault` … `ff_codes_cleared_invalidated`). The value
survives only as an **undeclared runtime attribute** set during record construction, so it is *not* part
of the schema contract: invisible to pyright, not guaranteed in `model_dump()`, and not a field the
COMLab consumer can rely on. (This is why the parent's `ruff`/`pyright`/`pytest` all passed despite the
gap.) The parent progress note's gate line — *"ff_fuel_spark_cut_at_crank → schema + extractor present"*
— is inaccurate for the schema half.

## Scope (PINNED — one declaration, no behaviour change)

1. Add to the §12.3 derived-flags block of `dtclab/schemas/freeze_frame.py`, beside the existing six:
   ```python
   ff_fuel_spark_cut_at_crank: bool = False
   # wiki: 10_nonstart_diagnostics.md §10.3 — OL_FAULT in a stationary no-run snapshot
   ```
2. **No change** to the predicate, `freeze_frame_extractor.py` derivation, the CAN-era gate,
   `mode06_evaluator.py`, or `vocabulary.py` — those parts of the parent are verified correct. The
   extractor already supplies the value; this only makes it a declared field so it lands and serializes.
3. Confirm the extractor's computed value now reaches the **declared** field on the constructed record
   (not just a stray attribute).

## Success criteria

- `ff_fuel_spark_cut_at_crank` is a **declared field** on `FreezeFrameRecord` — present in
  `FreezeFrameRecord.model_fields`.
- A unit test asserts the value on the **constructed record** (round-trips through the schema), e.g.
  `extract_freeze_frame(<OL_FAULT, vehicle_speed_kmh=0, engine_rpm=0>).ff_fuel_spark_cut_at_crank is True`
  and `False` for a normal running snapshot — not merely the helper's return value.
- The parent spec's own verification grep now passes:
  `rg -n "ff_fuel_spark_cut_at_crank" dtclab/schemas/freeze_frame.py` returns the field.
- Inner loop green: `ruff check .` → `pyright dtclab/` → `pytest -x -q` (via the local `.venv` per the
  parent's note: `.\.venv\Scripts\pyright.exe --pythonpath .\.venv\Scripts\python.exe dtclab/`).
- The parent's full verification block re-runs green (emitter-only; no cross-lab imports;
  `classify_margin` unchanged) — no regression.

## Deliverables

1. `dtclab/dtclab/schemas/freeze_frame.py` — the field declaration (+ wiki cite).
2. `dtclab/tests/unit/test_freeze_frame_extractor.py` — assert the flag on the constructed record (add if absent).
3. `tasks/progress_notes/T-DTCV2-NOSTART-1-FIX.md` — `## Plan`, `VERIFICATION GATE`, `CODE REVIEW`.
4. **Correct the parent record:** in `tasks/PROGRESS.md` flip `T-DTCV2-NOSTART-1` back to `done` only once
   this lands, and amend `progress_notes/T-DTCV2-NOSTART-1.md` CODE REVIEW to record that the schema gap
   was found post-commit and closed here.

## Files to touch

- `dtclab/dtclab/schemas/freeze_frame.py`
- `dtclab/tests/unit/test_freeze_frame_extractor.py`
- `tasks/progress_notes/T-DTCV2-NOSTART-1-FIX.md`
- `tasks/PROGRESS.md` + `tasks/progress_notes/T-DTCV2-NOSTART-1.md` (status correction only)

## Out of scope

- The FF-cut predicate, the CAN-era gate, `MONITOR_ABORTED`, `mode06_evaluator.py`, `vocabulary.py` — all
  verified correct; do not touch.
- Any COMLab (S4) work. No graph rebuild. No cross-lab imports. No new field beyond the one declaration.

## Verification

```bash
cd <repo>/labs/dtclab
# 1. now a real declared field
rg -n "ff_fuel_spark_cut_at_crank" dtclab/schemas/freeze_frame.py            # MUST return the field
python -c "from dtclab.schemas.freeze_frame import FreezeFrameRecord; assert 'ff_fuel_spark_cut_at_crank' in FreezeFrameRecord.model_fields, 'not a declared field'"
# 2. inner loop + parent contract intact
ruff check . && pyright dtclab/ && pytest -x -q
! rg -rniE "security[_-]?lockout|mechanical[_-]?no[_-]?start" dtclab/ && echo "OK emitter-only"
! rg -rnE "from (gaslab|obdlab|comlab|dnalab)" dtclab/ && echo "OK no cross-lab imports"
```

All green: the flag is a declared field, the extractor's value reaches it on the constructed record, and
the parent task is now complete to contract.

## Progress hook

Open `progress_notes/T-DTCV2-NOSTART-1-FIX.md` with the `## Plan`, then `VERIFICATION GATE` +
`CODE REVIEW`. On completion flip the FIX row to `done` and restore the parent `T-DTCV2-NOSTART-1` row to
`done` (now genuinely complete to contract).
