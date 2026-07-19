# CHI-1 — Wire `co_high_idle` to its consumer (closes the T-GV2-4 orphan)

### Goal ###

Give the `co_high_idle` DNA field a real, live consumer so T-GV2-4 can reach a
legitimate `done`. Today `co_high_idle` is defined in `gaslab/dna_view.py:39`
and read **nowhere** (`grep` confirms 0 code paths); `resolution.py` gates every
2500-RPM rich-CO judgment with fixed literals. Per the v2 wiki the per-vehicle
`co_high_idle` is the mild-rich CO ceiling at 2500 RPM and **overrides** the
generic literal when vehicle confidence is HIGH.

Decision (owner, 2026-06-04): **wire it, do not prune.**

### Success criteria ###

Tests-first. Write failing, then pass:

- `tests/test_resolution.py::test_co_high_idle_overrides_literal_when_high_conf`
  — with `dna.confidence == HIGH` and `dna.co_high_idle` populated, the 2500-RPM
  rich-CO ceiling used in the catalyst / CAM_TIMING rich branches is
  `dna.co_high_idle`, not the hard-coded literal. A `reading_high.co` just under
  the per-vehicle ceiling passes; just over it is rejected.
- `tests/test_resolution.py::test_co_high_idle_falls_back_to_literal`
  — with `co_high_idle is None` **or** confidence != HIGH, behaviour is
  byte-identical to today (literal ceiling). Regression guard.
- The existing catalyst dual-idle and CAM_TIMING tests (T-GV2-4/5) stay green.
- Inner loop clean on every edited file: `ruff` → `pyright` → `pytest -x -q`.

### Context ###

`co_high_idle` was added on credit in T-GV2-3 with its consumer scheduled for
T-GV2-4. T-GV2-4 instead implemented the 2500-RPM signal via a full second
`reading_high: GasReading` and left `co_high_idle` unconsumed (audit 2026-06-04,
follow-up **CHI-1**, Process-breach log). This task supplies the missing
consumer: the per-vehicle ceiling becomes the override for the rich-CO bound that
`reading_high.co` is tested against.

**Named signal/noise consumer (now satisfied):** `co_high_idle` →
`resolution.apply_differentiators`, rich-CO ceiling in the catalyst-dead /
CAM_TIMING_RETARDED_MAP branches (the rich 2500-RPM checks). Override applies
only when `dna.confidence == HIGH` and `co_high_idle is not None`
(`GAS_VOCABULARY` L425); literal is the fallback (L431).

**Wiki provenance:** transcribe the ceiling rule verbatim — `co_high_idle` =
`mild_rich.max` at 2500 RPM (`GAS_VOCABULARY` L431); per-vehicle override gate
HIGH-confidence (L425). Every changed numeric/branch carries the inline cite.

### Files to touch ###

- `GASLab/gaslab/resolution.py` (MODIFY — replace the literal rich-CO ceiling in
  the relevant 2500-RPM branches with a `co_high_idle`-or-literal helper, gated
  on confidence)
- `GASLab/tests/test_resolution.py` (CREATE/MODIFY — the two tests above)

### Out of scope ###

No new schema field. Do **not** touch `reading_high` plumbing, the lean/CAM
lambda checks, `dna_view.py`, or the wired mapper. Do **not** alter the literal
values themselves — only make `co_high_idle` able to override them. Surgical:
every changed line traces to a Deliverable; adjacent issues → "Unplanned
follow-ups".

### On completion ###

When both gates are clean in `progress_notes/CHI-1.md`: flip **CHI-1** to `done`
**and** flip **T-GV2-4** from `in_progress` to `done` (its contracted consumer is
now met). Close follow-up CHI-1 in the table. Then STOP — one task per session.

### Verification ###

```bash
# restore sandbox Python 3.14 first (4DLab/CLAUDE.md § Sandbox Python)
cd /sessions/<vm>/mnt/4DLab/GASLab
ruff check gaslab/resolution.py
pyright gaslab/resolution.py
grep -rn "co_high_idle" gaslab/        # expect: read in resolution.py, not only defined
pytest tests/ -x -q --tb=short         # T-GV2-4/5 tests stay green
```
