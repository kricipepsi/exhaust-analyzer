# T-TST-8 — OBDLab decision-rate ("bounce") harness: standalone + COMLab-connected

**Status:** `authored` (architect spec) — **implementation blocked** (see §8) ·
**Pack:** `planning/test_rollout/` · **Lab under test:** `labs/obdlab/` ·
**Mode:** STRICT (dual-gate: VERIFICATION GATE + CODE REVIEW before `done`)
**Author:** architect · **Date:** 2026-06-09
**Load skills (session start):** read `TEST_ROLLOUT_START_HERE.md`, run the sandbox
Python 3.14 block (root `CLAUDE.md`), then load the mandatory pair —
`_skills/codingskills/pythonskill/python/SKILL.md` (language + inner loop
`ruff`→`pyright`→`pytest -x -q`) and
`_skills/codingskills/ecc-subset/verification-loop/SKILL.md`. On-demand for
this harness: `ecc-subset/{eval-harness,python-testing,ai-regression-testing}` +
`code-reviev`. (Do **not** load the redirect stub `_skills/pythonskill/python/SKILL.md`.)

This is the full authoring of the rollout row T-TST-8 ("build obdlab generative
harness"), **re-scoped around its real acceptance criterion**: a *decision-rate
floor* that fails when OBDLab silently abstains (returns default/`NO_FAULT` shape)
on cases that carry decidable signal. It is the harness that would have flashed
red at the ">95% NO_FAULT" collapse the legacy `TestSuite/OBD` suite could not see.

---

## 1. Problem statement — what the "97% bounce" actually was

`OBDLab` was quarantined when it returned `NO_FAULT`-shaped output on **>95%** of
`cases_petrol_master_v6.csv`. The owner-ratified root cause (`labs/obdlab/tasks/
T-OBDV2-0_revive_emitter_decision.md`, 2026-06-08) is that the corpus is
**PID-less**: the master rows carry gas chemistry, not OBD PIDs, so abstaining
was *correct*, not a code defect. The resolution: **revive OBDLab as a typed
perception-channel emitter** that feeds COMLab fusion and emits **no** standalone
fault verdict.

Two structural blind spots let the collapse hide:

1. **No decision-rate gate.** The legacy `TestSuite/OBD` suite (64 curated rows)
   and the current `tests/unit` + `tests/integration` only assert that
   `translate()` does not throw and returns expected fields on happy-path inputs.
   Nothing measures *what fraction of a signal-bearing corpus moves a channel* —
   the one metric that goes to ~3% when the lab silently NO_FAULTs everything.
2. **No COMLab-connected test.** Since revive, OBDLab's output only becomes a
   verdict **inside COMLab**. A 97%-default emitter passes every standalone test
   and still makes the fusion spine useless. Nothing exercises OBD→COMLab end to end.

The embryo of the fix already exists: `labs/obdlab/tests/pid_logset/
test_pid_logset_wiring_gate.py::test_coverage_matrix_and_aggregate_rate` asserts
`default_pct < 5.0`. But it runs only on **38 hand-authored** PID-bearing cases,
**standalone**, with a "default shape" definition bound to four fields that the
pending audit patches will move (§8). T-TST-8 **generalises that one assertion**
to (a) the master-derived projection + the generative corpus, and (b) a
COMLab-connected mode.

---

## 2. Gate semantics — decision-rate floor (owner-locked 2026-06-09)

The gate **fails below a decision-rate floor**. The crux is separating a *correct
abstention* from a *bounce*: PID-less / cold / out-of-bounds inputs **should**
yield `NO_FAULT`/rejection and must **not** count against the lab.

**Denominator — "decidable, signal-bearing" cases only.** A case enters the
bounce denominator iff it both (a) passes ingestion (warmed engine, in-bounds
PIDs) — i.e. is not a typed rejection — **and** (b) carries at least one
non-nominal input a channel is supposed to move on. Excluded and tallied
separately (never counted as bounce):
- PID-less rows (no trims, no O2, no MAF/MAP) → correct `NO_FAULT`.
- Cold / open-loop / out-of-bounds → `COLD_OPEN_LOOP_INVALID` or a typed
  `PIDValidationError`/`SemanticConsistencyError`.

**Numerator — "bounce".** A decidable, signal-bearing case whose payload is
**default/`NO_FAULT` shape**: *every* discriminating channel sits at its default.
The channel set must be re-pinned against the **frozen post-backlog** emitter
contract (§8); as of this writing the discriminating channels are
`o2_failure_mode`, `ve_validity`/`ve_pct`, `total_trim_correction_delta`,
`total_trim_correction_delta_b2`/`per_bank_trim_delta`, `lambda_perception_delta`,
`w_theo`/`sensor_error_delta`, and the `WIDEBAND_OFFSET_CANDIDATE` finding.

**Two run modes (one gate, two harnesses):**

- **Mode A — standalone emitter (this lab).** Two assertions:
  - **A1 (projection CSV):** over `fixtures/obdlab_cases.csv` (T-TST-6,
    master-derived), `bounce_rate < FLOOR_STANDALONE` on the signal-bearing
    subset.
  - **A2 (generative interior):** for every point the `ModuleDescriptor` samples
    **inside a fault-signature box** (boundary/combinatorial; noise/overlap/fuzz
    as resilience), the emitter must move that box's channel on
    `≥ (100 − FLOOR_STANDALONE)%` of points. This is the assertion that cannot be
    satisfied by a lab that silently abstains — a 97% collapse drops it to ~3%.
- **Mode B — COMLab-connected (wired layer).** Over the master corpus run through
  OBD→COMLab fusion (`apps/wired/harness/run_cases.py`), the **actionable-verdict
  rate on OBD-decidable rows** must be `≥ FLOOR_CONNECTED`, where "actionable"
  means COMLab emits a non-default verdict **that consumed an OBD channel**
  (trace the OBD channel into the fusion decision — not merely "COMLab returned
  something"). Mode B is forward-registered as **T-TST-8W** and is additionally
  blocked on COMLab Stage-4 (§8).

**Floors.** `FLOOR_STANDALONE = 5%` (default-shape ceiling), anchored to the
existing `test_pid_logset_wiring_gate` precedent — do **not** invent a new number.
`FLOOR_CONNECTED` is **to be pinned from a first characterization run** when COMLab
Stage-4 fusion readers are live; until then it is `TBD` and Mode B stays
`pending (characterization)`, never green-by-default. Both gates are **fail-closed**:
an empty signal-bearing denominator is a gate failure, not a pass.

---

## 3. Files the coder will touch (Mode A)

- `labs/obdlab/tests/fixtures/descriptor.py` — replace the `NotImplementedError`
  stub with the real `ModuleDescriptor`: input schema ranges from
  `obdlab/schemas/{payload,dna_view,vocabulary}.py`, the OBD fault-signature box
  table (per-channel interior/boundary), and `process = SensorSignalTranslator().translate`.
- `labs/obdlab/tests/conftest.py` — fixtures building `OBDLivePayload` inputs +
  `ObdLabDnaView` from a CSV row; the signal-bearing predicate; the default-shape
  detector (single source of truth, imported by both A1 and A2).
- `labs/obdlab/tests/generative/test_{boundary,combinatorial,noise,overlap,fuzz}.py`
  — replace the skipped stubs; import the shared engine
  (`from harness.descriptor import ModuleDescriptor`, `from harness.runner import
  run_generative_suite`). A2 lives here.
- `labs/obdlab/tests/test_cases.py` — parameterised over `fixtures/obdlab_cases.csv`;
  A1 lives here (or a dedicated `test_decision_rate.py` if cleaner).
- **Consumes (does not author):** `fixtures/obdlab_cases.csv` from **T-TST-6**.

**Mode B (T-TST-8W), separate session/home:** `apps/wired/tests/test_obd_comlab_decision_rate.py`
driving `apps/wired/harness/run_cases.py` over `apps/wired/harness/data/cases_petrol_master_v6.csv`.

**No `obdlab/` source, no `comlab/` source, and no schema is edited by this task.**
No new schema field is added (signal/noise: §6). The shared engine in
`harness/harness/` is imported, never copied (projection contract §2).

---

## 4. Success criteria

1. `descriptor.py` builds a real `ModuleDescriptor` (no `NotImplementedError`);
   every fault box maps to exactly one discriminating channel and cites its
   `obdlab` source + wiki section in a comment.
2. A1 + A2 run green with `FLOOR_STANDALONE = 5%`, and each **prints the measured
   rate and the signal-bearing/abstention/rejection split** so a future drift is
   visible, not silent.
3. **Negative control (must fail-closed):** a temporary monkeypatched emitter that
   always returns default shape makes A1 **and** A2 **fail**. Capture this in the
   progress note — it is the proof the harness can see a 97% bounce. (Revert the
   monkeypatch; it does not ship.)
4. The default-shape detector's channel list matches the **frozen post-backlog**
   emitter surface (re-grep after FIX-2..7 + ARCH-2 land); no channel removed by
   ARCH-2 is referenced, and FIX-2's re-animated `WIDEBAND_OFFSET_CANDIDATE` is
   included.
5. Inner loop clean: `ruff` / `pyright` / `pytest -x -q` (coder runs the loop after
   every meaningful edit; sandbox results are not the gate of record — Windows
   `.venv-wired` is truth, per `project_sandbox_mount_truncation`).
6. No change to the pass count of pre-existing `labs/obdlab/tests/{unit,integration,
   regression,pid_logset}`.

---

## 5. Out of scope

- Authoring `obdlab_cases.csv` (T-TST-6) or the master relabel (T-MASTER-RECON).
- Any `obdlab/` or `comlab/` source change. If the harness exposes a real OBD bug,
  it goes to **Unplanned follow-ups** (§9), not into this diff.
- Building Mode B's assertions in full — its floor and channel-trace are pinned
  only when COMLab Stage-4 readers exist (T-TST-8W, forward-registered).
- Re-running graphify / touching `graphify-out/` (HARD RULE).

---

## 6. Signal/noise consumer (test-fixture variant)

The harness adds **no schema field**, so the signal/noise rule applies to fixtures:
every expected-output cell in `obdlab_cases.csv` and every fault-box bound in
`descriptor.py` must trace to a **live `obdlab` source file + wiki section** in its
`gt_source`; uncited expecteds are `gt_method=characterization` (regression net,
not correctness). The **consumer of the harness itself** is the rollout
acceptance gate + the OBD→COMLab fusion contract it protects: A2 and Mode B exist
precisely so that a future emitter regression that would starve COMLab fusion is
caught at the OBD seam instead of silently degrading the whole spine.

---

## 7. Why this catches what the old suite missed (design rationale)

The legacy suite asserts *correctness on inputs it chose*. A lab can pass every
such assertion and still abstain on everything it was not handed. A2 inverts the
question: it samples the **descriptor's** fault-box interiors (not a curated list)
and demands a channel move — so coverage is defined by the lab's declared
capability, not by the test author's optimism. Mode B then proves the moved
channel actually reaches a COMLab verdict. Together they make "97% silent NO_FAULT"
a **red build**, by construction.

---

## 8. Blockers — the answer to "wait until the patches finish?"

**Yes, the *implementation* should wait; authoring this spec now does not.** The
decision-rate gate binds to the emitter's output distribution, exception taxonomy,
vocabulary/schema surface, and call-determinism — all of which the pending
`labs/obdlab/tasks/audit_backlog` patches still move. Building the harness now
would bind the default-shape detector and the descriptor to a surface that is
about to change, forcing a re-baseline. This is the **same code-freeze gate that
already blocks `T-KG-OBD-2`** (the AST code-map), for the same reason ("source in
flux … captures soon-to-be-deleted symbols").

Implementation **Blocked-by**:

| Blocker | Why it moves the harness contract |
|---|---|
| `T-OBDV2-FIX-2` (wideband offset re-animated) | changes how often a channel moves → changes the bounce numerator and the default-shape channel list |
| `T-OBDV2-FIX-3` (de-state MAF linearity) | removes order-dependent instance state → without it, generative call-order changes results (A2 non-deterministic) |
| `T-OBDV2-FIX-4` (`number_of_banks` default) | changes bank-2 field population → affects default-shape detection |
| `T-OBDV2-FIX-5` (exception taxonomy) | changes which typed errors cross `translate()` → changes the rejection/abstention split |
| `T-OBDV2-ARCH-2` (orphan members prune/proposal) | changes the vocab/schema surface (e.g. `O2FailureMode.DEAD`) the descriptor enumerates |
| `T-OBDV2-FIX-6`, `T-OBDV2-FIX-7` | behaviour-preserving, but bundle into the same freeze so the surface is re-gripped once, not twice (matches T-KG-OBD-2's gate) |
| `T-TST-6` | supplies `fixtures/obdlab_cases.csv` (itself blocked on `T-MASTER-RECON`) |

Already cleared (do **not** re-block on these): `T-OBDV2-0` revive (resolved
2026-06-08), `T-OBDV2-FIX-1` (done, Option B), `T-OBDV2-ARCH-1` (done, excised
`ranking.py`/`family_map.py`).

**Mode B / T-TST-8W additionally blocked-by:** COMLab Stage-4 fusion readers
live (the forward-registered `T-COMV2-*` set: `VE-GATE-1`, `O2OFFSET-1`,
`BANK-FUSE-1`, `ECU-FUSE-1`, …). Until then the OBD channels are pre-frozen
contract surface with no live reader, so an end-to-end "actionable verdict" cannot
be measured honestly.

**Recommended unblock order:** close `audit_backlog` FIX-2..7 + ARCH-2 → author
`T-TST-6` (needs `T-MASTER-RECON`) → implement T-TST-8 Mode A → at COMLab Stage-4,
pin `FLOOR_CONNECTED` and implement T-TST-8W.

---

## 9. Unplanned follow-ups (logged, not fixed here)

| ID | Finding | Status |
|---|---|---|
| FU-TST8-1 | Rollout ledger (2026-06-07) states obdlab harness is "blocked on the revive-vs-quarantine decision"; that decision **resolved `revive` 2026-06-08**. Corrected in this task's ledger update. | fixed in ledger |
| FU-TST8-2 | `descriptor.py` for OBD must encode per-channel fault boxes that the shared engine's continuous generators can sample; confirm the engine's `ModuleDescriptor` supports multi-channel (not single-verdict) emitters before T-TST-8 starts — GASLab's descriptor is single-verdict. | open (engine pre-check for the coder) |

---

## VERIFICATION GATE (coder fills at implementation)

- [ ] A1 + A2 green at `FLOOR_STANDALONE = 5%`; measured rates + splits printed.
- [ ] Negative control: forced-default emitter makes A1 **and** A2 fail (proof the
      harness can see a 97% bounce); monkeypatch reverted.
- [ ] Default-shape channel list re-gripped against the post-backlog emitter surface.
- [ ] `ruff` / `pyright` / `pytest -x -q` clean on Windows `.venv-wired`.
- [ ] Pre-existing obdlab test pass count unchanged.

## CODE REVIEW (coder fills at implementation)

- [ ] No `obdlab/` or `comlab/` source edited; no schema field added.
- [ ] Shared engine imported from `harness/harness/`, not copied.
- [ ] Every fault-box bound + expected cell carries a `gt_source` (live source +
      wiki) or is tagged `gt_method=characterization`.
- [ ] No graphify rebuild; `graphify-out/` untouched.
