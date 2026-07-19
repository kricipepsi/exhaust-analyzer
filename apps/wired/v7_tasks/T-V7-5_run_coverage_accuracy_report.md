# T-V7-5 — Run the v7 suite + coverage/accuracy + error-taxonomy report

**Authored by:** architect (Cowork), 2026-06-30 · **Status:** `deferred` (→ `pending` when T-V7-4 is `done`) · **Blocked by:** T-V7-4
**Mode:** STRICT — runs the suite + writes one report; **no source edits**. · **Scope owner:** wired-v7.
**Load skills:** wired-python, wired-verification-loop, wired-code-review.

## Objective
Run the full v7 corpus and turn the results into the pack's headline deliverable: a
**coverage + per-family accuracy report** plus a **per-error-dimension failure
taxonomy** and the **wiki↔engine disagreement list** — the actionable signal. The
report shows not just *how many* cases pass but *which error classes* the engine
produces. Optionally trace the failures so the phase-of-failure is readable.

## Signal/noise
Adds no domain field or fault. The **named consumer** is the architect's regression
gate / next-pack triage — `apps/wired/v7_tasks/reports/V7_ACCURACY_<date>.md` is what
that consumer reads. Each failure becomes a candidate follow-up (wiki fix, engine bug,
or oracle correction), logged — not fixed here.

## Pinned facts (verified at authoring)
- Driver `apps/wired/v7/run_suite.py` (T-V7-4); corpus + oracle
  `apps/wired/v7/data/cases_petrol_v7.csv`.
- Optional trace: Jaeger from `apps/wired/test_tasks/T-WTEST-3` + `apps/wired/trace/`;
  `--trace` mode in `run_suite.py`; router phase spans `phase.prune`/`phase.rank`
  carry `router.candidates_in/out`, `router.winner_id`, `router.threshold_miss`
  (observed in T-WTEST-5).
- Accuracy `%` is over **`accuracy`-tagged** cases only; characterization reports
  no-crash rate separately.

## Scope
**IN:**
- Run `run_suite.py` over the full corpus; capture aggregate + per-case results.
- Write `apps/wired/v7_tasks/reports/V7_ACCURACY_<date>.md`:
  - **headline:** overall accuracy (over `accuracy` cases), characterization no-crash
    rate, crash count, total cases / families covered / families with zero cases (the
    coverage blind spots from T-V7-1).
  - **coverage table:** every reachable family × cases × pass × accuracy %; mark
    families with no case as blind spots.
  - **error taxonomy:** counts per failure dimension — wrong family, wrong code, wrong
    state, confidence out of band, perception-gap mismatch, demotion-note mismatch,
    crash, bad-input mishandled. This is the "catch all errors" view.
  - **disagreement list:** each FAIL with `case_id`, `wiki_ref` (expected), the live
    verdict (predicted), the failing dimension(s), and a one-line hypothesis tag —
    *wiki-fix* / *engine-bug* / *oracle-correction* (marked hypothesis, not verdict).
  - cross-links to the corpus (T-V7-2), oracle + triage (T-V7-3), research (T-V7-1),
    and the green baseline (T-WTEST-1).
- **Optional** (Jaeger up): re-run FAIL cases with `--trace`; per fail record the trace
  id + the phase where routing diverged (lab boundary vs COMLab prune/rank).
- Log each failure as a row under "Unplanned follow-ups" in `V7_PROGRESS.md`
  (ID + one-liner + `open`).

**OUT:** fixing any failure (wiki/engine/oracle) — measure and report only; any source
edit; committing run/trace JSON or the Jaeger binary; `graphify`; `Vault/`.

## Steps
1. Run `run_suite.py` over the full corpus; capture aggregate + per-case.
2. Write `V7_ACCURACY_<date>.md` (headline, coverage table, error taxonomy,
   disagreement list, cross-links).
3. Optional: `--trace` the FAIL cases; add the phase-of-divergence per fail.
4. Log each failure in `V7_PROGRESS.md` "Unplanned follow-ups".
5. Fill `v7_tasks/progress_notes/T-V7-5.md` gates; STOP.

## Success criteria
- Report exists, `.md`, with: headline (accuracy over `accuracy` cases + no-crash rate
  + crash count + coverage blind spots); the coverage table; the per-error-dimension
  taxonomy; the disagreement list with `case_id` + `wiki_ref` + failing dimension(s) +
  hypothesis tag.
- Accuracy `%` is computed over `accuracy`-tagged cases only — stated explicitly.
- Every failure is an `open` follow-up in `V7_PROGRESS.md`; none fixed here.
- If `--trace` was used, each FAIL has a trace id + the divergence phase.
- `git status` shows only new files under `apps/wired/v7_tasks/` (+ ledger edit); no
  run/trace JSON or binary staged; no source edits.

## VERIFICATION GATE — T-V7-5
Complete in `v7_tasks/progress_notes/T-V7-5.md`: the `run_suite.py` aggregate output;
the report path; the per-dimension failure counts; the disagreement count; (if traced)
the FAIL trace ids + phases.

## CODE REVIEW — T-V7-5
Complete in `v7_tasks/progress_notes/T-V7-5.md`: measure-and-report only (no fixes);
accuracy denominator is `accuracy`-tagged cases; failures logged as follow-ups, not
patched; no run/trace artefacts staged; `graphify` not run.

## Commit (owner, explicit paths)
```bash
cd /agent_workspace
git add \
  apps/wired/v7_tasks/reports/V7_ACCURACY_<date>.md \
  apps/wired/v7_tasks/progress_notes/T-V7-5.md \
  apps/wired/v7_tasks/V7_PROGRESS.md
git commit -m "T-V7-5: run v7 suite + coverage/accuracy + error-taxonomy report"
```
