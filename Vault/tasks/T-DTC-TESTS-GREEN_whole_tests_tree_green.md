---
node_type: task
task_id: T-DTC-TESTS-GREEN
status: done
pack: VAULT
lab: dtclab
mode: coder lane
blocked_by: []
consumers:
- drift-guards.base — coverage view
- graph/v2_tests — AST test graph
tags:
- task
- vault
- dtclab
---


# T-DTC-TESTS-GREEN — Whole `tests/` tree green and meaningful

**Status:** `done` · **Pack:** VAULT (DTCLab) · **Mode:** coder lane (inner loop)
**Origin:** pipeline guide §3·1B (test corpus green before it becomes a graph) · **Blocked by:** —
**Consumer (signal/noise):** **Adds no schema field.** The `tests/` tree becomes its own graph
(`graph/v2_tests/`, built in `T-DTC-GRAPH-AST`). Green, behaviour-asserting tests are what produce the
`VERIFIES` / `drift_guards` edges the vault reads for `drift-guards.base`. A skipped or vacuous test
yields a dead edge — so the consumer is the drift-guard spine of the vault.

### Scope ###

- `labs/dtclab/tests/` — 16 test files across `unit/`, `integration/`, `regression/`, `generative/`,
  plus `fixtures/`, `conftest.py`, `test_cases.py`, `scripts/`.
- Confirm the whole tree runs and **asserts behaviour** (maps to real schema/rules), not just imports.

### What to verify is actually covered (maps to shipped behaviour) ###

- DTC ingestion gate: regex accept/reject, fail-on-first, unknown-mode `ValueError`.
- Freeze-frame: 12 mandatory PIDs, 6 derived flags at boundary, `FreezeFrameIncompleteError`, coercion.
- Historical context: priority order, `ECT == 60` exclusive boundary, both-conditions-required.
- Mode $06: margin tri-state boundaries, valid/invalid keys, component lookup, LRU-cache ≤ 1 open.
- Routing mapper: fan-out, DNA gates HIGH/PARTIAL/NONE, gpf_combined matrix, POA never emitted.
- **Phase-2 scorer** (`ranking.py`): `test_rank_candidates.py` + `test_classify_top3.py` — weight
  selection, DNA factor (1.0/0.7/0.5), unit-interval clamp, dedup, top-3 ordering.
- **Family map** (`family_map.py`): `test_family_map.py` — tag→family, `None` handling, dedup/order.
- Cross-field step 5b: `COOLANT_SYSTEM_MALFUNCTION` / `CYLINDER_FLUID_MISFIRE` in pipeline/regression.
- Isolation: `test_dna_view.py` import audit (no `gaslab`/`obdlab`/`comlab`/`dnalab`).

### Success criteria ###

1. `pytest -q` green across the whole `tests/` tree (note any intentional `slow`/`generative` markers
   and the decision to run or skip them — record in the Plan).
2. No vacuous tests (every test file asserts behaviour, not just that an import succeeds); fixtures
   resolve; `conftest.py` wiring loads.
3. Test↔code mapping is real: each unit test names the module/rule it guards, so the `v2_tests` graph
   can form `VERIFIES` edges to the package symbols.
4. Inner loop clean (`ruff`/`pyright` on `tests/` too).

### Out of scope ###

- The package code-clean (→ `T-DTC-CODE-CLEAN`) · running graphify (→ `T-DTC-GRAPH-AST`).
- Adding new behaviour/tests for the `EP-DTC-NOSTART-1` proposal (it is not shipped — proposal only).

### Files to touch ###

- `labs/dtclab/tests/**` — only fixes needed to make the tree green and meaningful (wiring, markers,
  vacuous-test hardening). No production-code change here (that is CODE-CLEAN).

### Verification ###

```bash
cd <repo>/labs/dtclab
pytest -q
ruff check tests/ && pyright tests/
pytest -q tests/unit/test_rank_candidates.py tests/unit/test_classify_top3.py tests/unit/test_family_map.py
```

### Progress hook ###

`Vault/tasks/progress_notes/T-DTC-TESTS-GREEN.md` opens with the confirmed `## Plan` (slow/generative
decision, any wiring fixes); the run session fills `VERIFICATION GATE` (tree green, no vacuous tests,
mapping real) + `CODE REVIEW` (coverage maps to shipped rules). Ledger row → `done` only when both clean.
If the tree is already green with no edits needed, record that and the row may note "folds into CODE-CLEAN".
