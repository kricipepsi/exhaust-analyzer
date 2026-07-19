# T-OBDV2-FIX-2 — Wideband offset detector is dead (enum vs wire-string) (🔴 correctness)

**Status:** `done` — coder-runnable · **Lab:** OBDLab (Stage 2) · **Mode:** STRICT
**Origin:** OBDLab skills-audit 2026-06-08 — finding **CR-2** (`audit/AUDIT_03_code-review.md`);
also absorbs **UB-3** (fuel-status DRY).
**Blocked by:** — (independent; pairs with the single-source helper below)
**Consumer (signal/noise):** `o2_failure_mode == WIDEBAND_OFFSET_CANDIDATE` →
COMLab **`T-COMV2-O2OFFSET-1`** (Stage 4, already forward-registered by T-OBDV2-4). This
fix *re-animates* that already-named consumer; it does not add a field.

## Why this exists (root cause is precise)

`O2Normalizer._wideband_passthrough` gates the `WIDEBAND_OFFSET_CANDIDATE` finding on
`is_closed_loop = fuel_status == "Closed_Loop"` (`core/o2_normalizer.py` L185). **T-OBDV2-4**
added this detector; **T-OBDV2-6** then migrated `fuel_sys_status` from the wire string to a
`FuelSystemStatus` enum (value `"CL"`) and migrated *two* consumers
(`analytics_preconditions`, `semantic_consistency_checker`) — **but missed
`o2_normalizer`.** In the live pipeline the validator hands O2 normalisation a
`FuelSystemStatus` enum, so `FuelSystemStatus.CL == "Closed_Loop"` is `False`,
`is_closed_loop` is always `False`, and the branch (L189-191) never runs. The documented
`WIDEBAND_OFFSET_CANDIDATE` fault is unreachable in production.

**Why the test missed it:** `tests/unit/test_o2_normalizer.py::test_wideband_offset_candidate_trigger`
(L315-328) passes `"fuel_sys_status": "Closed_Loop"` as a **raw string directly** to
`O2Normalizer.normalize`, bypassing the validator — so the unit test exercises the pre-migration
shape and stays green. Classic same-author blind spot (`audit/AUDIT_05` E-2).

## Scope (pinned)

1. In `_wideband_passthrough`, coerce/compare against `FuelSystemStatus.CL`, not the literal
   `"Closed_Loop"`. Use the **single-source helper** (item 2) so the comparison accepts both
   the enum and any legacy wire string.
2. **Single-source the fuel-status coercion (absorbs UB-3).** Add
   `FuelSystemStatus.from_wire(value) -> FuelSystemStatus | None` (or `coerce_fuel_status`)
   in `schemas/vocabulary.py`; replace the three duplicated maps in
   `pid_ingestion_validator.py` (L166-175), `semantic_consistency_checker.py` (L233-242),
   `analytics_preconditions.py` (L75-84), and use it in `o2_normalizer`.
3. Update `test_wideband_offset_candidate_trigger` (and the other offset cases) so the input
   goes through the validator (or passes the enum), proving the **live** shape triggers.

## Success criteria

- A warm / closed-loop / not-WOT / not-DFCO `WIDEBAND_LINEAR` reading with persistent
  `|λ−1| > 0.05` yields `O2FailureMode.WIDEBAND_OFFSET_CANDIDATE` **through `translate()`**
  (not only via a raw-string unit call). The updated test fails on today's code, passes after.
- One definition of the fuel-status wire→enum map; the three duplicates removed.
- Regression + pid_logset gate stay green; inner loop clean (Windows `.venv-wired`).

## Files to touch

- `core/o2_normalizer.py` · `schemas/vocabulary.py` · `core/pid_ingestion_validator.py` ·
  `core/semantic_consistency_checker.py` · `core/analytics_preconditions.py` ·
  `tests/unit/test_o2_normalizer.py`

## Out of scope

No new O2 failure mode. No gas/λ_chem comparison (Stage-4 COMLab). Test-infra build deferred.

## Verification

```bash
cd <repo>/labs/obdlab
ruff check obdlab/ tests/ && pyright obdlab/
# only one fuel-status map remains:
grep -rcn '"Closed_Loop": FuelSystemStatus.CL' obdlab/obdlab   # expect a single hit (the helper)
pytest -x -q
```

## Progress hook

`tasks/progress_notes/T-OBDV2-FIX-2.md`: `## Plan` → `VERIFICATION GATE` → `CODE REVIEW`
(note the through-`translate()` trigger proof). PROGRESS.md row → `done` with Files changed.
