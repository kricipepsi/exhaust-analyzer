### Goal ###
Recover the **133 SURFACE_DEFECT** cases — the rows that already route to the correct family +
state and fail only on the answer-key *format* — by re-pinning the oracle per the investigated
**Option B** dispositions, with **zero engine change**. Two columns in
`apps/wired/v7/data/cases_petrol_v7.csv` change for **named-fault rows only**:
`expected_fault_code` -> short form (`MF-001`, not `ERR-MF-001`), and `expected_confidence_*`
-> the live scorer's per-family bands. Abort rows (`ERR-ABORT-*`), `OPTIMAL_HEALTH`, and
`no_fault` bands are **kept as-is**. Done when re-scoring shows the SURFACE_DEFECT `fault_code`
and `confidence` dimensions pass for the named-fault rows, family/state routing is unchanged,
and the change is captured as a **new yardstick** (not an edit of the frozen one).

### Success criteria ###
- After the re-pin, `score_v3_yardstick.py score --results <existing run JSON>` shows
  `fault_code` PASS for the named-fault SURFACE_DEFECT rows (was 0/294) and `confidence` PASS
  for those rows, with **`fault_family` and `state` counts unchanged** (still 141 / 275).
- A guard test `test_oracle_repin.py::test_abort_rows_untouched` confirms no `ERR-ABORT-*`,
  `OPTIMAL_HEALTH`, or `no_fault` row's expected_* changed (a blanket `s/^ERR-//` would corrupt
  abort rows — this test forbids that).
- `v3/reports/V3_ORACLE_REPIN_2026-06-30.md` records: rows changed (count + ids), the exact
  per-family confidence bands applied, the new CSV SHA-256, and an explicit note that this mints
  `V3_YARDSTICK` and leaves `FL_YARDSTICK_2026-06-30` frozen.
- The corpus still `--validate`s against `FaultAtlasKG` (no vocabulary/KG violation introduced).

### Context ###
Phase 2 of `v3/V3_PLAN.md` (section 4). The two dispositions are already investigated and
recommended (Option B) — implement them, do not re-investigate:
- `fault_code` namespace: `apps/wired/v7_tasks/reports/V7_CODE_NS_DECISION_2026-06-30.md` —
  the v2 default path emits the short `rule_id`; no live consumer needs the `ERR-` prefix;
  re-pin `expected_fault_code` to short for **named-fault rows only**, KEEP `ERR-ABORT-*` and
  `OPTIMAL_HEALTH`.
- `confidence` semantics: `apps/wired/v7_tasks/reports/V7_CONF_DECISION_2026-06-30.md` —
  `confidence_score` is a bounded additive evidence score, not a calibrated posterior; re-pin
  `expected_confidence_min/max` to the live scorer's **per-family distribution** from run
  `20260630_163900`, named-fault rows only; KEEP abort / `OPTIMAL_HEALTH` / `no_fault` bands.
The SURFACE_DEFECT set (133 rows, ids) is enumerated in
`apps/wired/fl_tasks/reports/FL_LOCALIZATION_2026-06-30.md` (per-case table, `mode=SURFACE_DEFECT`).
The scorer dimensions are `apps/wired/v7/run_suite.py::score_case` (fault_code at line ~154-ish
region; confidence band check). The per-family confidence distribution is computable from the
existing run JSON `apps/wired/v7/runs/20260630_163900/results.json` — derive the band per family
(e.g. observed min..max or a tight window around the modal score), do not hand-wave a number.

**Owner sign-off gate:** both memos are marked "awaiting owner sign-off". Confirm the owner has
signed off on Option B before editing the CSV. If not yet signed off, stop and surface it — do
not guess the disposition.

### Consumer (signal/noise) ###
- **Consumer:** the scorer's `fault_code` and `confidence` dimensions
  (`run_suite.py::score_case`) and the v3 acceptance gate.
- **Code path:** `apps/wired/v7/run_suite.py::score_case` reads `expected_fault_code` and
  `expected_confidence_min/max` from the CSV row and compares to the verdict. No engine/schema
  change — only oracle data values move.

### Deliverables ###
1. `apps/wired/v7/data/cases_petrol_v7.csv` — MODIFY (oracle columns only, named-fault rows
   only). Mints a new yardstick; does not touch the frozen one.
2. `apps/wired/.../tests/test_oracle_repin.py` — CREATE. Guards abort/no_fault rows untouched.
3. `v3/reports/V3_ORACLE_REPIN_2026-06-30.md` — CREATE. What changed, new hash, yardstick note.

### Files to touch ###
- `apps/wired/v7/data/cases_petrol_v7.csv` (MODIFY — oracle columns only)
- `apps/wired/.../tests/test_oracle_repin.py` (CREATE)
- `v3/reports/V3_ORACLE_REPIN_2026-06-30.md` (CREATE)

### Out of scope ###
No engine change of any kind — this is an answer-key data re-pin only. Do not touch
`fault_family`/`state`/`perception_gap`/`demotion_note` expected columns. Do not re-pin the 10
`mechanical_wear -> misfire` ORACLE_SUSPECT rows here — that is the separate
`FL-V3-ORACLE-MW-MISFIRE` decision. Do not overwrite or re-hash `FL_YARDSTICK_2026-06-30`. Do
**not** run a blanket regex over the code column (it would corrupt `ERR-ABORT-*`). Surgical
change only. GRAPH GUARDRAIL: no `graphify`/rebuild. No `Vault/` edits.

### Verification ###
```bash
cd /agent_workspace
# Corpus still valid against the KG/vocabulary:
/agent_workspace/.venv-wired/bin/python apps/wired/v7/load_corpus.py --validate
# Guard test: abort / no_fault / OPTIMAL_HEALTH rows untouched:
/agent_workspace/.venv-wired/bin/python -m pytest -x -q apps/wired -k oracle_repin
# Re-score the existing run JSON against the re-pinned oracle:
/agent_workspace/.venv-wired/bin/python apps/wired/fl_tasks/score_v3_yardstick.py score \
  --results apps/wired/v7/runs/20260630_163900/results.json
# family+state counts MUST be unchanged (141 / 275); fault_code now passes for named-fault rows
```
All steps must pass; family/state routing counts must be identical to the frozen baseline.

### Progress hook ###
PROGRESS.md `T-V3-2`: Status=done, Files changed=3, Verification="Option B re-pin (named-faults-only); 133 SURFACE_DEFECT surface dims pass; family/state unchanged; abort rows guarded"
