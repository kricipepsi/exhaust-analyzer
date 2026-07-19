# T-TST-5 — Wired integration test folder + master-CSV home

**Status:** completed · **Blocked by:** T-TST-0 · **Pack:** `planning/test_rollout/`

## Goal

Make the wired layer the unambiguous home of the **full-pipeline** integration
test: confirm/scaffold `apps/wired/tests/` against the template and establish a
data home for the master corpus so the wired harness stops reading it by a brittle
root-relative path.

## Context (disk state)

`apps/wired/harness/` already runs the full L1→L5 chain (`run_cases.py`,
`case_mapper.py`, `scoring.py`) and `apps/wired/tests/` has real tests
(`test_composition.py`, `test_harness.py`, …). `run_cases.py` reads
`TestSuite/cases_petrol_master_v6.csv` and a `smoke_cases.csv` by root-relative
string (migration map §0/§4). The master is the **wired/COMLab** integration gate
(`T-TH-12`), not a per-lab fixture.

## Success criteria

1. A data home exists for the integration corpus: `apps/wired/harness/data/`
   (or equivalent named in T-TST-0), and `run_cases.py` reads the master from a
   single resolved path constant, not an ad-hoc root-relative string.
2. The master CSV location is **pinned** (migrated copy or a documented pointer) —
   exactly one canonical path, recorded in the wired README/harness docstring.
3. `smoke_cases.csv` is located and either co-homed or documented; no silent
   missing-file fallback.
4. `apps/wired/tests/` reflects the template's split: unit vs the master-driven
   integration test (the `T-TH-12` end-to-end gate slot is named, even if that
   gate itself stays blocked).

## Out of scope

- Implementing/activating the `T-TH-12` end-to-end gate (still blocked on master
  recon + a runnable seam).
- Editing the master CSV contents (owner-adjudicated under `T-MASTER-RECON`).
- Per-lab folders (T-TST-1..4).

## Signal/noise consumer

`apps/wired/harness/run_cases.py` + `apps/wired/tests/` — the named integration
consumer of the full master corpus.

## Files to touch

- `apps/wired/harness/run_cases.py` (path constant only), `apps/wired/harness/data/`
  (new home or pointer), `apps/wired/tests/` (template alignment), wired README note

## Verification

`run_cases.py` resolves the master from the single pinned path on a clean checkout
(no CWD assumption); `pytest -q apps/wired` unchanged; `ruff`/`pyright` clean; grep
shows no remaining `TestSuite/cases_petrol_master_v6.csv` root-relative literal in
wired code.
