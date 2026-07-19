### Goal ###
For every `PRODUCER_GAP` case (25 in the frozen run), decide the **resolvability fork**:
`CLASSIFIER_FIXABLE` (the required upstream state IS reachable from the row's actual input values,
but GASLab/OBDLab binned it elsewhere — fixable now) vs `SIGNAL_REQUIRED` (the discriminating
quantity is physically absent from the input — needs a Phase-4 measurement). Output
`v3/reports/V3_PRODUCER_GAP_SPLIT_2026-06-30.md` (+ `.json`): per case — expected code, required
gating state, emitted state, the verdict, the specific state/threshold involved, and (for
`SIGNAL_REQUIRED`) which research cluster it maps to. This is the task that says exactly how many
of the 25 are cheap classifier wins vs genuine research. Read-only / query-only on the labs.

### Success criteria ###
- All 25 PRODUCER_GAP case_ids labelled `CLASSIFIER_FIXABLE` or `SIGNAL_REQUIRED` with cited
  evidence (the gating threshold compared against the row's input values).
- `v3/producer_gap_split.py` regenerates the report by **replaying each case's raw inputs through
  the GASLab/OBDLab classifier in query mode** and inspecting the required state's gating
  condition vs the input; exits 0, writes `.md` + `.json`, no network.
- For each `SIGNAL_REQUIRED` case, the report names the missing physical quantity and maps it to
  one of the research clusters in `v3/research/` (e.g. cam-timing → Cluster 7).
- `py_compile` + `ruff` clean.

### Context ###
The single most scope-decisive diagnostic for `v3/V3_PLAN.md` Phase 4. The localization labels
these 25 `PRODUCER_GAP` and already records, per dead-family case, the **required gating state vs
the emitted state** in `apps/wired/fl_tasks/reports/FL_UPSTREAM_2026-06-30.json` (keys
`required_gating_states_by_dead_family`, `dead_family_records[*].required_gating_state_for_expected_code`
and `.gas_chemistry_states`). What is missing is the fork: was the required state *reachable* from
the input? Reuse the existing replay harness pattern in
`apps/wired/fl_tasks/capture_upstream_evidence.py` (it puts `labs/gaslab`, `labs/obdlab` on
`sys.path` and calls `_run_gaslab` / `_run_obdlab` / `diagnose` via `wired.composition`, mapping a
row with `v7.load_corpus.row_to_raw_inputs`). For each case, compare the required state's gating
thresholds (from the lab's state definition) against the row's actual 5-gas / OBD values: if the
input *could* satisfy the state's condition, it is `CLASSIFIER_FIXABLE`; if the condition needs a
quantity the row does not contain, it is `SIGNAL_REQUIRED`.

### Consumer (signal/noise) ###
N/A — no new field/enum/fault. Query-only analysis. Output consumed by Phase-4 scoping (which of
the 25 become signal-research tasks) and by any GASLab/OBDLab classifier-fix task (the
`CLASSIFIER_FIXABLE` list is its work list).

### Deliverables ###
1. `v3/producer_gap_split.py` — CREATE. Replays cases through the labs (query mode) + emits the split.
2. `v3/reports/V3_PRODUCER_GAP_SPLIT_2026-06-30.md` — CREATE.
3. `v3/reports/V3_PRODUCER_GAP_SPLIT_2026-06-30.json` — CREATE.

### Files to touch ###
- `v3/producer_gap_split.py` (CREATE)
- `v3/reports/V3_PRODUCER_GAP_SPLIT_2026-06-30.md` (CREATE)
- `v3/reports/V3_PRODUCER_GAP_SPLIT_2026-06-30.json` (CREATE)

### Out of scope ###
No engine/lab/classifier edits — this task *classifies* the gap, it does not fix it. No oracle/CSV
edits. **GRAPH GUARDRAIL (critical here):** querying the labs and building a fresh offline index is
fine, but do **not** re-run `graphify` or rebuild any frozen graph. No `Vault/` edits. Surgical:
every line traces to a deliverable.

### Verification ###
```bash
cd /agent_workspace
/agent_workspace/.venv-wired/bin/python -m py_compile v3/producer_gap_split.py
ruff check v3/producer_gap_split.py
/agent_workspace/.venv-wired/bin/python v3/producer_gap_split.py
# All 25 labelled; both labels reconcile to 25:
grep -iE 'CLASSIFIER_FIXABLE|SIGNAL_REQUIRED|25' v3/reports/V3_PRODUCER_GAP_SPLIT_2026-06-30.md
```
All steps must pass; the two labels must reconcile to 25 and every SIGNAL_REQUIRED case must name a
research cluster.

### Progress hook ###
PROGRESS.md `T-V3-D2`: Status=done, Files changed=3, Verification="25 PRODUCER_GAP split CLASSIFIER_FIXABLE vs SIGNAL_REQUIRED with cited gating evidence; signal cases mapped to research clusters"
