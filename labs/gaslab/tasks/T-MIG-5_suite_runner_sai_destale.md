# T-MIG-5 — De-stale `gaslab_suite_runner.py` (remove purged SAI fields)

**Authored by:** architect · **Status:** `pending` (runnable) · **Blocked by:** — (independent of T-MIG-4)
**Mode:** STRICT · **Scope owner:** TestSuite (register in `TestSuite/TESTSUITE_*` ledger when run).
**Surfaced by:** T-MIG-4 step 5 · **Root cause:** T-GV2-11 SAI purge (SAI moved to DTCLab).

## Objective

Bring `TestSuite/gaslab_suite_runner.py` back in line with the **post-T-GV2-11 GASLab contract** by
removing the **purged SAI fields** it still passes, so the runner executes clean against the forked
`gaslab` (`labs/gaslab`). This is a **pre-existing** bug (the runner was broken against v1 too);
it is not introduced by the migration.

## Signal/noise

This **removes** stale fields; it adds nothing. The purged fields have **no GASLab consumer** (T-GV2-11:
"no `secondary_air_equipped` consumer to build"). Removing the runner's dead references restores
contract alignment — no new field/enum ships.

## Pinned facts (verified 2026-06-05)

`GasLabContext` has **no** `secondary_air_injection_active`; `GasLabDnaView` has **no**
`secondary_air_equipped`. The runner still references both:

- `gaslab_suite_runner.py:45` — `"secondary_air_equipped": False,` (default row dict)
- `gaslab_suite_runner.py:97` — `secondary_air_equipped=_parse_bool(row["dna_secondary_air_equipped"])` (→ `GasLabDnaView`)
- `gaslab_suite_runner.py:113` — `secondary_air_injection_active=False,` (→ `GasLabContext`)
- `gaslab_suite_runner.py:120-121` — `secondary_air_injection_active=_parse_bool(row.get("ctx_secondary_air_injection_active", "") or "False")` (→ `GasLabContext`)

## Scope

**IN:** remove the four SAI references above (and any now-dead CSV columns they read —
`dna_secondary_air_equipped`, `ctx_secondary_air_injection_active` — plus their parse helpers if they
become unused). Run the runner clean against the forked `gaslab`.
**OUT:** re-adding SAI to GASLab (forbidden — T-GV2-11); any DTCLab SAI work; changing `gaslab` code or
the CSV corpus schema beyond dropping the two dead columns; any rule/threshold change.

## Steps
1. Read `TestSuite/TESTSUITE_START_HERE.md`, register this row in its ledger (atomic), restore sandbox 3.14.
2. Delete the four SAI references; drop the two dead CSV columns from any sample/fixture the runner reads;
   remove now-unused parse helpers.
3. Run the runner end-to-end against `labs/gaslab` (editable `gaslab` already repointed by T-MIG-4):
   it must complete without the SAI `TypeError`.
4. Inner loop on touched files: `ruff` → `pyright` → `pytest -x -q` (any runner unit tests).

## Success criteria
`gaslab_suite_runner.py` runs to completion against the fork; no reference to `secondary_air_*` remains
(`grep -n 'secondary_air' TestSuite/gaslab_suite_runner.py` → empty); ruff/pyright clean.

## VERIFICATION GATE — T-MIG-5
_(coder fills)_

## CODE REVIEW — T-MIG-5
_(coder fills: SAI fully removed; no GASLab change; no new field; runner green)_

## Commit (owner, explicit paths)
```powershell
cd C:\Users\muto\claude\4DApp\4DLab
git add `
  TestSuite/gaslab_suite_runner.py `
  planning/sprints/stage1_gaslab/tasks/T-MIG-5_suite_runner_sai_destale.md `
  planning/sprints/stage1_gaslab/tasks/progress_notes/T-MIG-5.md
git commit -m "T-MIG-5: de-stale gaslab_suite_runner SAI fields (post T-GV2-11)"
```
