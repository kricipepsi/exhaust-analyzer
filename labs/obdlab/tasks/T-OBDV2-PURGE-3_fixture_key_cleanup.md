# T-OBDV2-PURGE-3 — strip dead era/EGR keys from regression fixtures

**Status:** `pending (runnable)` · **Lab:** OBDLab (Stage 2) · **Mode:** STRICT
**Origin:** PURGE-2 follow-up — `OBDLAB_PURGE_AUDIT_2026-06-08.md` §3; closes the leftover after T-OBDV2-PURGE-2.
**Consumer (signal/noise):** N/A — removes dead data keys; adds nothing.

### Goal ###

PURGE-2 removed `emissions` and `resolved_horizon` from `ObdLabDnaView`, but five regression fixtures still
carry those now-dead keys. Pydantic silently ignores them (tests pass), so they are harmless but they are
schema drift — a fixture referencing a field the schema no longer has. Remove the dead keys so the fixtures
match the live contract.

### Success criteria ###

- `grep -rn 'emissions\|resolved_horizon\|HORIZON_' tests/regression/fixtures/` → **0 matches**.
- `pytest -x -q` stays green (same pass count as after PURGE-2; behaviour unchanged — the keys were ignored).

### Context ###

The dead keys sit at the `dna_view_json` block of each fixture. Affected files (verified by grep), with the two
keys to delete in each (`"emissions": { "egr_equipped": ... }` and `"resolved_horizon": "..."`):

- `tests/regression/fixtures/case_01_stabilised_idle_healthy.json`
- `tests/regression/fixtures/case_02_lean_vacuum_leak.json`
- `tests/regression/fixtures/case_04_stress_idle_clinical.json`
- `tests/regression/fixtures/case_05_maf_only_backcalc.json`
- `tests/regression/fixtures/case_06_partial_dna_confidence.json`

`case_03_cold_engine_frozen.json` has no such keys (dna_view is null/absent) — do not touch it. Keep each JSON
valid: when you delete the `emissions` and `resolved_horizon` lines, ensure the preceding line's trailing comma
is correct (no dangling comma, no missing comma).

### Deliverables ###

1. The five fixtures above — remove the `emissions` and `resolved_horizon` keys; keep JSON valid.

### Files to touch ###

- `tests/regression/fixtures/case_01_stabilised_idle_healthy.json` (MODIFY)
- `tests/regression/fixtures/case_02_lean_vacuum_leak.json` (MODIFY)
- `tests/regression/fixtures/case_04_stress_idle_clinical.json` (MODIFY)
- `tests/regression/fixtures/case_05_maf_only_backcalc.json` (MODIFY)
- `tests/regression/fixtures/case_06_partial_dna_confidence.json` (MODIFY)

### Out of scope ###

Do not touch `case_03`. Do not alter any non-`dna_view` field, expected output, or the schema/code. Do not add
new fixtures. **Do NOT run `graphify` or rebuild any graph** — the verified graph is canonical; this task
changes test data only. Surgical-change rule: only the `emissions`/`resolved_horizon` keys come out.

### Verification ###

```bash
cd /path/to/4DLab/labs/obdlab
# Dead keys gone from fixtures
grep -rnE 'emissions|resolved_horizon|HORIZON_' tests/regression/fixtures/ \
  && { echo "FAIL: dead key survives"; exit 1; } || echo "OK keys gone"
# JSON still valid
for f in tests/regression/fixtures/case_0{1,2,4,5,6}*.json; do python3.14 -m json.tool "$f" >/dev/null || { echo "FAIL invalid json: $f"; exit 1; }; done
# Suite green, unchanged behaviour
pytest -x -q
```

All steps must pass. **Do not run graphify.**

### Progress hook ###

`tasks/progress_notes/T-OBDV2-PURGE-3.md` opens with the confirmed `## Plan`, then `VERIFICATION GATE` +
`CODE REVIEW`. End the session by **emitting the PowerShell commit block** (explicit paths, one per line,
backtick-continued; do not stage `graphify-out/` or caches).
