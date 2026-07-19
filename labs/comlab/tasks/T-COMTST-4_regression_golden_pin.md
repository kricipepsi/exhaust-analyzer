# T-COMTST-4 — COMLab regression suite (pinned golden-master verdicts)

**Authored:** 2026-06-20 (architect, Cowork). **Stage:** 4 (COMLab, LAST). **Type:** test-suite harness infra (no `comlab/` source change).
**Pack:** `T-COMTST-*`. **Blocked by:** T-COMTST-2 (reuses the row→request builder).
**Drill:** `START_HERE.md` → `ROADMAP.md` → `AGENTS.md` (five rules) → **this file**, then post the scope-confirm before any code.

> **One-line scope:** add `labs/comlab/tests/regression/` — a small set of pinned JSON fixtures (canonical assembled-verdict scenarios) plus `test_comlab_regression.py` that runs each through `LabPipelineAggregator.process()` and asserts the **current** verdict (top fault, family, degradation mode, confidence) is **byte-stable** against the committed golden value. This is a change-detector, not an accuracy claim: it catches *unintended* verdict drift between sessions.

---

### ⚠ Read first — golden-master, not ground-truth

The pinned values are **whatever COMLab emits today**, captured once and frozen — they are *characterization* goldens, not externally-validated correct answers. A future task that *intentionally* changes a verdict updates the golden in the same diff (and says so in its progress note). A verdict that changes **without** such a task is a regression this suite exists to surface. This mirrors `labs/dtclab/tests/regression/` and `labs/obdlab/tests/regression/`. Do not conflate these goldens with the F1/GATE_DATA accuracy harness (`wiki/12_corpus_eval_discipline.md`) — that one measures correctness against re-audited labels and is a separate, later pack.

### Goal ###

Pin COMLab's current behaviour on ~5–7 canonical scenarios so silent regressions are caught. Each `regression/fixtures/case_*.json` holds one fully-assembled `OrchestratorInboundRequest` payload + an `expected` block of the verdict fields observed today. `test_comlab_regression.py` loads each fixture, runs the aggregator, and asserts the observed verdict equals `expected`. Proof it's done: `pytest tests/regression/ -q` passes; deliberately perturbing one golden makes exactly that case fail.

### Success criteria ###

- `tests/regression/fixtures/` contains 5–7 `case_*.json` files spanning: healthy/`no_fault` (`FULL_FUSION`), a legacy no-OBD `GAS_DOMINANT`, a `FATAL_INCOMPLETE` invalid-input, and ≥3 fault families COMLab actually routes (e.g. `catalyst_failure`, `ignition_fault`/`misfire`, `cam_timing` or `mechanical_wear`).
- `tests/regression/test_comlab_regression.py` is parametrized over the fixtures and asserts the observed verdict equals each fixture's pinned `expected` block (top fault / family / degradation mode / confidence).
- Each fixture's `expected` block was captured from the **actual** current `LabPipelineAggregator` output (not hand-guessed); a comment/field records the capture date + commit.
- Negative control: perturbing any single golden value flips exactly that one case to fail (state this was checked in the progress note).
- Inner loop clean: `ruff check tests/regression/` → `pyright tests/regression/` → `pytest tests/regression/ -q`; whole suite stays green.

### Context ###

**Load skills:** `_comlab_skills/comlab-python`, `_comlab_skills/comlab-verification-loop`, `_comlab_skills/comlab-code-review` — the three COMLab mandatory skills (per `_comlab_skills/_INDEX.md`), loaded at session start before any code. No on-demand skill applies: this is a `tests/` task, not a `registry/` task, so the registry bundle is not loaded.

Templates: `labs/dtclab/tests/regression/test_dtclab_regression.py` + `labs/dtclab/tests/regression/fixtures/case_*.json` (and the obdlab equivalent) — copy the load-fixture / parametrize / assert-equal structure and the `__init__.py`. Build the request payloads from the same mock-builder scenarios used in T-COMTST-1 and the `_make_request` assembly in `tests/e2e/test_pipeline_round_trip.py` (lines 29–50). Capture goldens by running the aggregator once locally and copying its output verdict fields into each fixture's `expected` block. Verdict field names: `comlab/schemas/response.py::DiagnosticVerdict` (line 87) + `ExecutionMeta` (line 67; degradation/confidence). **READ-NARROW:** read the dtclab regression template and the `DiagnosticVerdict` block by line range only.

### Consumer (signal/noise) ###

`N/A — no new field/enum/fault.` Test-only; pins the existing `OrchestratorFinalUIOutput` contract. No production schema surface added.

### Deliverables ###

1. `labs/comlab/tests/regression/__init__.py` — CREATE.
2. `labs/comlab/tests/regression/fixtures/case_*.json` — CREATE; 5–7 pinned scenarios with `expected` verdict blocks.
3. `labs/comlab/tests/regression/test_comlab_regression.py` — CREATE; parametrized golden-master assertions.

### Files to touch ###

- `labs/comlab/tests/regression/__init__.py` (CREATE)
- `labs/comlab/tests/regression/fixtures/case_*.json` (CREATE)
- `labs/comlab/tests/regression/test_comlab_regression.py` (CREATE)

### Out of scope ###

Do **not** treat goldens as ground truth or add accuracy/scoring metrics (F1/GATE_DATA pack). Do **not** re-derive verdicts by hand — capture from live output. Do **not** touch `test_cases.py` (T-COMTST-2), the generative layer (T-COMTST-3), the descriptor/CSV (T-COMTST-1), or any `comlab/` source. If capturing a golden surfaces a COMLab bug, log it to PROGRESS.md "Unplanned follow-ups" — do not fix it in this diff. Surgical-change rule applies. **GRAPH GUARDRAIL:** no `graphify` / graph rebuild.

### Verification ###

```bash
cd labs/comlab
# Python 3.14 ONLY — no 3.10/3.12/3.13 mixing. Pin every python/pytest call to the repo sandbox interpreter:
PY=../../.sandbox-py/bin/python3.14
"$PY" --version                          # must print Python 3.14.x — stop if not
ruff check tests/regression/
pyright tests/regression/                # pyrightconfig must pin pythonVersion 3.14
# all golden-master cases pass:
"$PY" -m pytest tests/regression/ -q
# whole suite still green:
"$PY" -m pytest -x -q
```

All steps must pass.

### Progress hook ###

PROGRESS.md `T-COMTST-4`: Status=done, Files changed=>=5, Verification="regression golden-master pinned (N cases) and green; negative-control verified; suite green"
