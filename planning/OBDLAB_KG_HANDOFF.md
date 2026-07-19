# OBDLab → KG Readiness — HANDOFF (context reset)

**Date:** 2026-06-09 · **Purpose:** ingest the **full obdlab module — production code + test code —
into the KG**, as **two separate graphs**. This doc is self-contained: a fresh session continues from
here without re-deriving anything.

---

## Locked decisions (do not re-litigate)

1. **Two graphs, never merged.** `graph/v2_code/` = production code (`obdlab/obdlab/`, architecture
   navigation). `graph/v2_tests/` = test code (`obdlab/tests/`, coverage/traceability). Merging them
   buries every "what calls X" query under ~760 test nodes — a signal/noise breach. Mirrors the existing
   wiki-KG vs code-KG split.
2. **Freeze is done.** All obdlab audit-backlog fixes (`FIX-1..7`, `ARCH-1`, `ARCH-2`) are `done` — gates
   clean, progress notes present. Production source is stable.
3. **Ingest the code map now; the test map after the harness.** They don't block each other.
4. **The test harness = the decision-rate "bounce" gate** (`T-TST-8`): fail if obdlab returns default/
   NO_FAULT shape on signal-bearing cases. Standalone now; COMLab-connected (`T-TST-8W`) after COMLab S4.

## State now

| Item | Status |
|---|---|
| obdlab freeze (FIX-1..7, ARCH-1/2) | **done** |
| `T-KG-OBD-1` wiki KG (`v2_wiki/`) | **done** |
| **`T-KG-OBD-2` production code map (`v2_code/`)** | **READY — run now** (freeze done) |
| `T-KG-OBD-3` test map (`v2_tests/`) | authored · blocked on the harness |
| `T-TST-8` bounce harness (standalone) | authored · blocked on `T-TST-6` |
| `T-TST-6` obdlab_cases.csv | authored · blocked on `T-MASTER-RECON` |
| `T-MASTER-RECON` master relabel (keystone) | authored · **owner decisions pending** |

## Optimal sequence

1. **NOW (coder, 1 session):** run `T-KG-OBD-2` → production code in `graph/v2_code/`.
   Command: scoped **`/graphify obdlab/obdlab`** only. **Never** `graphify update .` from root (HARD RULE).
2. **OWNER:** answer the 3 `T-MASTER-RECON` decisions (canonical `expected_top_fault` vocabulary;
   perception-gap row handling; malformed-row disposition). See that task file §Decisions.
3. **Coder:** run `T-MASTER-RECON` (reconcile the master) → then `T-TST-6` (obdlab_cases.csv).
4. **Coder:** build `T-TST-8` (descriptor + generative + bounce gate) → obdlab test code complete.
5. **Coder:** run `T-KG-OBD-3` → test code in `graph/v2_tests/` (scoped `/graphify obdlab/tests`).
6. **Result:** full obdlab module (code + tests) in the KG, as two clean graphs.
7. **Deferred:** `T-TST-8W` (COMLab-connected bounce gate) until COMLab Stage-4 readers are live.

Critical path to "code in KG" = step 1 (today). Critical path to "tests in KG" = steps 2→5
(gated on the owner vocabulary decision at step 2).

## File pointers

- KG tasks: `labs/obdlab/tasks/T-KG-OBD-2_*.md` (code), `T-KG-OBD-3_*.md` (tests); ledger `labs/obdlab/tasks/PROGRESS.md`.
- Test harness: `planning/test_rollout/` (START_HERE + PROGRESS + `tasks/T-TST-6/8`).
- Keystone: `harness/tasks/T-MASTER-RECON_master_relabel.md`; ledger `harness/HARNESS_PROGRESS.md`.
- Skills (local): `_skills/codingskills/…` (load via each pack's START_HERE).

## Bootstrap for the fresh session

- KG ingest work → `labs/obdlab/tasks/OBDLAB_TASKS_START_HERE.md`.
- Test-harness work → `planning/test_rollout/TEST_ROLLOUT_START_HERE.md`.
- Master relabel → `harness/HARNESS_START_HERE.md`.
One task per session; pick the first row whose blockers are all `done`.

## Open owner decisions (the only thing blocking the test track)

`T-MASTER-RECON` §Decisions — canonical label vocabulary, perception-gap class, malformed-row disposition.
Nothing downstream (`T-TST-6/8`, `T-KG-OBD-3`) can proceed until these are answered.
