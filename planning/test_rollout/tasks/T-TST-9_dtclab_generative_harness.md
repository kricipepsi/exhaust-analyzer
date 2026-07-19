# T-TST-9 — DTCLab generative harness: discrete combinatorial + fuzz

**Status:** `authored` (architect spec) — **ready for coder** ·
**Pack:** `planning/test_rollout/` · **Lab under test:** `labs/dtclab/` ·
**Mode:** STRICT (dual-gate: VERIFICATION GATE + CODE REVIEW before `done`)
**Author:** architect · **Date:** 2026-06-11
**Blocked by:** `T-TST-7` (done — supplies `fixtures/dtclab_cases.csv`). **Not** blocked by
the DTC hex-regex gap: that gap is COMLab-side (`T-FX-DTCHEX-1`) and gates the
*connected* rows only (T-TST-8W/T-TST-10). DTCLab's own `DTC_REGEX` is already
hex-correct (`^[BCPU][0-3][0-9A-F]{3}$`, `vocabulary.py` §2.3/§10).

**Load skills (session start):** read `TEST_ROLLOUT_START_HERE.md`, run the sandbox
Python 3.14 block (root `CLAUDE.md`), then load the mandatory pair —
`_skills/codingskills/pythonskill/python/SKILL.md` (language + inner loop
`ruff`→`pyright`→`pytest -x -q`) and
`_skills/codingskills/ecc-subset/verification-loop/SKILL.md`. On-demand for
this harness: `ecc-subset/{eval-harness,python-testing}` + `code-reviev`. (Do **not**
load the redirect stub `_skills/pythonskill/python/SKILL.md`.)

---

## 1. What this row builds (and the engine reality it must respect)

T-TST-9 is the rollout row "build dtclab generative harness (combinatorial + fuzz
only)". DTCLab is a **discrete** lab — its input space is DTC code sets + freeze-frame
context + MIL flags, not continuous numeric axes — so the ledger's generator matrix
already excludes boundary/noise/overlap (ε-boundary and Gaussian noise are
meaningless on discrete codes).

**Disk-verified engine constraint (the reason this spec pins a lab-local route).**
The shared engine in `harness/harness/` is a **gas pilot**, not yet lab-generic:

- `harness/harness/generators/combinatorial.py::CombinatorialGenerator` is hardcoded to
  `GAS_DIMS = ("gas_hc","gas_co","gas_co2","gas_o2","gas_nox")` and continuous
  min/max corners. For a DTCLab descriptor (no gas dimensions) it filters
  `box_dims = [d for d in GAS_DIMS if d in box.dimensions]` → empty → `continue` →
  **zero cases**. Importing it for DTCLab produces an empty suite.
- There is **no fuzz generator in the shared engine at all** — `generators/` holds
  only `boundary/combinatorial/noise/overlap`. Even gaslab's own
  `tests/generative/test_fuzz.py` is a skipped stub
  (`reason="Fuzz generator not implemented in shared engine"`).
- `START_HERE`/`TEMPLATE` cite `from harness.runner import run_generative_suite`; the
  runner actually exports **`run_suite`**. Use `run_suite` (the `run_generative_suite`
  name does not exist — logged FU-TST9-2).

**Resolution (owner-confirmed 2026-06-11 — "lab-local generators, keep runnable").**
T-TST-9 reuses the shared engine for `ModuleDescriptor`/`FieldRange`/`FaultBox` + the
`run_suite` CSV runner + the governance-column conventions, and implements the
**discrete combinatorial and fuzz generators as DTCLab-tailored test code** inside
`labs/dtclab/tests/generative/`. This matches the pack's governing model ("Tailored
per lab: … **which generators apply**", `TEST_ROLLOUT_PROGRESS.md`) and the gaslab
fuzz precedent. The engine generalization (a shared discrete-combinatorial mode + a
real fuzz generator) is **not** in this row — it is registered as a forward proposal
(§9 FU-TST9-1) so gaslab/obdlab/comlab can converge later, without blocking this row.

---

## 2. DTCLab entry points & oracle sources (pinned so the coder does not invent them)

**Process entry point (the descriptor's `entry_point`).** The full DTCLab pipeline is
`DataFusionSanitizer(dna_view).sanitize(...) -> DTCLabPayload`:

```
DataFusionSanitizer(dna_view: DtcLabDnaView | None).sanitize(
    raw_dtcs: dict[str, list[str]],        # keyed "$03"/"$07"/"$0A"
    raw_freeze_frame: dict[str, Any],      # bare PID name -> value (Mode $02)
    raw_mode06: dict[str, float],          # "MID_<HEX>_TID_<HEX>" -> margin_pct
    *, codes_cleared=False, active_mil=False, mil_flashing=False,
) -> DTCLabPayload   # source: dtclab/core/data_fusion_sanitizer.py
```

The pipeline's six steps and their **named oracle sources** (each box-bound / expected
cell must cite one of these in its `gt_source`):

| Sub-unit (live code path) | Oracle source (wiki) |
|---|---|
| `dtc_ingestion_gate.py::validate_dtc_list` (regex gate; raises `DTCFormatError`/`ValueError`) | DTC_VOCABULARY.md §2.3, §10 (`DTC_REGEX`), §3 (modes) |
| `routing_tag_mapper.py::RoutingTagMapper.map(confirmed_dtcs) -> list[DTCRoutingTag]` | §4 (code-range → tag), §4.1/§14 (DNA gates) |
| `freeze_frame_extractor.py::extract_freeze_frame` (raises `FreezeFrameIncompleteError`) | §11 (pipeline), context PIDs |
| `historical_context_classifier.py::classify_historical_context(ect, rpm, load)` | §9 (cold-start <60°C → idle rpm<1000 & load<25 → load rpm>2000 & load>45 → UNKNOWN) |
| `mode06_evaluator.py` (margin → `Mode06MonitorState`) | §7 (PASSED >15% / PENDING 1–15% / CRITICAL ≤0%) |
| `freeze_frame_extractor.py::_derive_open_loop(fuel_status)` | §8 (`FuelSystemStatus` CL/OL/OL_DRIVE/OL_FAULT) |

**Routing-tag table (the discrete "fault boxes").** The 19 `DTCRoutingTag` members in
`vocabulary.py` each carry a §4 code range, e.g. `LEAN_HISTORY`=P0171/P0174,
`RICH_HISTORY`=P0172/P0175, `MISFIRE_HISTORY`=P0300–P0312, `O2_HISTORY`=P0130–P0161,
`CATALYST_HISTORY`=P0420/P0430 (DNA-gated `has_catalyst`), `EGR_HISTORY`=P0400–P0409
(DNA-gated `egr_equipped`).
This member→code-range map **is** the combinatorial oracle.

**DNA gating (must be an explicit combinatorial axis).** `RoutingTagMapper._gate_allows`:
`dna_view=None` ≡ `VinConfidence.NONE` → emit unconditionally (§14.3); `PARTIAL` →
advisory-emit; `HIGH` → strict `has_catalyst`/`egr_equipped` presence
check (§4.1). The projection CSV path uses `dna_view=None` (T-TST-7 projected no DNA
columns); the combinatorial generator covers gating by constructing a `DtcLabDnaView`
with/without each gated capability and asserting the gated tag is dropped under HIGH
confidence and emitted under None/NONE.

**Error taxonomy (the fuzz oracle).** `DTCFormatError(ValueError)`,
`FreezeFrameIncompleteError(ValueError)`, and bare `ValueError` (malformed mode key /
empty-code). Fail-closed = one of these typed errors **or** a clean validated payload —
never an uncaught crash and never a silently mis-routed tag.

---

## 3. Files the coder will touch

- `labs/dtclab/tests/fixtures/descriptor.py` — replace the `NotImplementedError` stub
  with a real `build_dtclab_descriptor() -> ModuleDescriptor`. For a discrete lab:
  - `entry_point = DataFusionSanitizer(dna_view=None).sanitize` (the projection-CSV path);
  - `fields: list[FieldRange]` enumerating the **discrete** input axes — one exemplar
    DTC code per routing tag (`enum_values` from the §4 table), `fuel_status`
    (`enum_values=[e.value for e in FuelSystemStatus]`), the three freeze-frame context
    PIDs (`ff_ect`/`ff_rpm`/`ff_load` as the §9 bucket drivers), and the `active_mil`/
    `mil_flashing` bools;
  - `boxes` is left **empty** (`{}`) — continuous `FaultBox` geometry does not apply to
    discrete codes; the routing-tag→code-range oracle lives in the lab-local generator,
    not in gas-style boxes. Document this in a comment citing this spec §1.
  - `build_args(row)` / `extract_expected(row)` / `diff(actual, expected)` wired to the
    `dtclab_cases.csv` columns (T-TST-7: `dtcs`, `ff_dtcs`, `ff_ect`, `ff_rpm`, `ff_load`,
    `ff_map`, `ff_stft_b1`, `ff_ltft_b1`, `fuel_status` + the 3 empty expected cols).
- `labs/dtclab/tests/conftest.py` — fixtures building `sanitize(...)` inputs from a CSV
  row (parse the raw `dtcs`/`ff_dtcs` cells per T-TST-7's split-on-comma rule), plus the
  shared **discrete oracle helpers**: code→tag map (§4), §9 context classifier mirror,
  and the fail-closed predicate (single source of truth, imported by combinatorial+fuzz).
- `labs/dtclab/tests/generative/test_combinatorial.py` — replace the skipped stub with
  the lab-local discrete combinatorial suite (§4).
- `labs/dtclab/tests/generative/test_fuzz.py` — replace the skipped stub with the
  lab-local input-contract fuzz suite (§4).
- `labs/dtclab/tests/test_cases.py` — replace the skipped stub with a parameterised run
  over `fixtures/dtclab_cases.csv` (T-TST-7's 194 rows) as a **characterization net**
  (expected cols empty → `gt_method=characterization`; records `routing_tags` /
  `historical_context` / `freeze_frame_status`, asserts no crash + schema-valid payload).

**Consumes (does not author):** `fixtures/dtclab_cases.csv` from **T-TST-7**.
**No `dtclab/` source, no `comlab/` source, and no schema is edited.** No new schema
field is added (signal/noise: §6). The shared engine in `harness/harness/` is imported,
never copied (projection contract §2). The continuous-generator files
(`test_boundary/noise/overlap.py`) stay **absent** (T-TST-3 — discrete lab).

---

## 4. Generator semantics (lab-local, discrete)

**Combinatorial — exact-oracle, bounded.** Cartesian/pairwise coverage over the discrete
axes the descriptor declares:

- **routing axis:** one exemplar confirmed DTC per `DTCRoutingTag` (§4 table) → assert
  `RoutingTagMapper.map([code])` (via `sanitize`) yields exactly that tag;
- **DNA-gate axis** (for the 3 gated tags): `{dna_view=None, HIGH-with-hardware,
  HIGH-without-hardware}` → assert emit / emit / **drop** per §4.1/§14.3;
- **freeze-frame-context axis:** `ff_ect`/`ff_rpm`/`ff_load` set to one representative
  per `HistoricalFaultContext` bucket → assert `classify_historical_context` agreement
  (§9), including the cold-start priority-first rule;
- **MIL/fuel axis:** `active_mil`/`mil_flashing` × `FuelSystemStatus` representative →
  assert `_derive_open_loop` and the payload MIL fields round-trip.

The oracle is **deterministic** (the §4 map and §9 rules are exact), so combinatorial
asserts **exact agreement**, not a rate — do **not** invent a decision-rate floor (there
is no precedent number for DTCLab; T-TST-8's `FLOOR_STANDALONE=5%` is OBD-specific and
must not be copied here). Keep the case count bounded and printed (axis sizes × the
gated-tag fan-out), so coverage is auditable.

**Fuzz — fail-closed input-contract.** Mutate each `sanitize` input and assert the
fail-closed predicate (§2 taxonomy):

- DTC strings: bad prefix (`A0171`), wrong length, lowercase (`p0171`), out-of-range
  middle digit, hex-edge → `DTCFormatError`/`ValueError` or correct routing, never crash;
- freeze frame: missing required PIDs, garbage types → `FreezeFrameIncompleteError`;
- Mode $06: malformed `MID_*_TID_*` keys, non-numeric margins → `ValueError`.

Every fuzz case asserts: a **typed** exception from the §2 taxonomy *or* a schema-valid
`DTCLabPayload` — and never a silently wrong routing tag. (Use a small fixed seed if
randomised, and print the seed, so failures reproduce.)

---

## 5. Success criteria

1. `descriptor.py` builds a real `ModuleDescriptor` (no `NotImplementedError`);
   `entry_point` is `DataFusionSanitizer(...).sanitize`; every discrete axis value and
   every routing-tag oracle entry cites its `dtclab` source + DTC_VOCABULARY.md section
   in a comment.
2. Combinatorial runs green with **exact** tag/context oracles and **prints** its axis
   sizes + total case count (auditable coverage, not a curated list).
3. Fuzz runs green with the fail-closed predicate; the seed (if any) is printed; the
   valid hex DTC is exercised and routes (not rejected) — proving the harness
   does not re-import COMLab's decimal-only bug.
4. **Negative control (proof the harness can see a regression):** a temporary
   monkeypatch that forces `RoutingTagMapper.map` to return `[]` makes the combinatorial
   suite **fail**. Capture in the progress note; revert — it does not ship.
5. `test_cases.py` parameterises over all 194 `dtclab_cases.csv` rows as a
   characterization net (expected cols empty → `gt_method=characterization`); asserts no
   crash + schema-valid payload, and records the routing/context/ff-status it observes.
6. Inner loop clean: `ruff` / `pyright` / `pytest -x -q` on Windows `.venv-wired`
   (sandbox results are **not** the gate of record — `project_sandbox_mount_truncation`).
7. No change to the pass count of pre-existing
   `labs/dtclab/tests/{unit,integration,regression}`.

---

## 6. Signal/noise consumer (test-fixture variant)

The harness adds **no schema field**, so signal/noise applies to fixtures and oracles:
every routing-tag oracle entry in `descriptor.py`/`conftest.py` and every expected cell
traces to a **live `dtclab` source file + DTC_VOCABULARY.md section** in its `gt_source`;
uncited expecteds are `gt_method=characterization` (regression net, not correctness).
The **consumer of the harness itself** is the rollout acceptance gate + the DTC→COMLab
routing contract it protects: combinatorial and fuzz exist so that a future regression
that would starve COMLab fusion of routing tags (or silently mis-route a hex DTC) is
caught at the DTC seam, not downstream in the spine. Named live readers of the projected
columns are pinned in T-TST-7 (`RoutingTagMapper.map`, `historical_context_classifier`,
`freeze_frame_extractor`) — a column or oracle with no named reader does not ship.

---

## 7. Out of scope

- Authoring `dtclab_cases.csv` (T-TST-7) or the master relabel (`T-MASTER-RECON`).
- Any `dtclab/` or `comlab/` source change. A real DTC bug the harness exposes goes to
  **Unplanned follow-ups** (§9), not into this diff.
- The COMLab DTC hex-regex fix (`T-FX-DTCHEX-1`) — COMLab-side, connected-path only.
- **Generalizing the shared engine** (discrete combinatorial + a fuzz generator) — that
  is the forward proposal FU-TST9-1, a harness-pack (`T-TH-*`) concern, not this row.
- Re-running graphify / touching `graphify-out/` (HARD RULE).

---

## 8. Why this catches what the old suite missed (design rationale)

`tests/unit`/`integration` assert correctness on inputs the author chose. Discrete
combinatorial inverts that: it enumerates **every routing tag, every DNA-gate branch,
and every §9 context bucket** from the descriptor's declared axes and demands exact
agreement — so coverage is the lab's declared capability, not the author's optimism. The
fail-closed fuzz proves the ingestion gate rejects malformed codes with a *typed* error
rather than crashing or mis-routing. Together they make "a routing regression that
silently empties the tag set" a **red build**, by construction.

---

## 9. Unplanned follow-ups (logged, not fixed here) / proposals

| ID | Finding | Disposition |
|---|---|---|
| **FU-TST9-1** | The shared engine is gas-pilot only: `CombinatorialGenerator` is `GAS_DIMS`-hardcoded (yields 0 cases for discrete/PID labs) and **no fuzz generator exists** (gaslab's `test_fuzz.py` is a skipped stub). **Proposal:** add a discrete/enum combinatorial mode (keyed on `FieldRange.enum_values`) + a real fuzz generator to `harness/harness/generators/`, so gaslab/obdlab/dtclab/comlab converge on one engine. **Named consumer:** the four labs' `tests/generative/` suites (dtclab's lab-local generators from this row are the reference shape). Track as a `T-TH-*` harness-pack row. | proposal → harness pack |
| **FU-TST9-2** | `TEST_ROLLOUT_START_HERE.md` §1.3 + `TEMPLATE.md` cite `from harness.runner import run_generative_suite`; the runner exports **`run_suite`**. Doc drift — reconcile the two pack docs to the real symbol. | doc fix (pack docs) |
| **FU-TST9-3** | DTCLab payload fields `active_mil`/`mil_flashing`/`mode_06_monitors` have no master source column (carried over from FU-TST7-2); this row populates them only via characterization, not projection. | logged (no action) |

---

## VERIFICATION GATE (coder fills at implementation)

- [ ] Combinatorial green with exact tag/context oracles; axis sizes + case count printed.
- [ ] Fuzz green with the fail-closed predicate; seed printed; hex DTC routes (not rejected).
- [ ] Negative control: forced-empty `RoutingTagMapper.map` makes combinatorial **fail**
      (proof the harness sees a routing regression); monkeypatch reverted.
- [ ] `test_cases.py` runs all 194 rows as a characterization net; no crash, payloads valid.
- [ ] `ruff` / `pyright` / `pytest -x -q` clean on Windows `.venv-wired`.
- [ ] Pre-existing dtclab `unit/integration/regression` pass count unchanged.

## CODE REVIEW (coder fills at implementation)

- [ ] No `dtclab/` or `comlab/` source edited; no schema field added.
- [ ] Shared engine imported from `harness/harness/` (`ModuleDescriptor`, `run_suite`),
      not copied; discrete generators are lab-local (per §1 owner decision), not a copy
      of the gas generators.
- [ ] Every routing-tag oracle entry + expected cell carries a `gt_source` (live source +
      DTC_VOCABULARY.md section) or is tagged `gt_method=characterization`.
- [ ] Continuous-generator files (`test_boundary/noise/overlap.py`) remain absent.
- [ ] No graphify rebuild; `graphify-out/` untouched.
