# T-OBDV2-1b — wiring-gate test: prove discriminating output (code half)

**Status:** `pending` — **coder-runnable after T-OBDV2-1a** · **Lab:** OBDLab (Stage 2) · **Mode:** STRICT
**Origin:** `HANDOFF_T-OBDV2-1_pid_logset_wiring_gate.md` §4 · **Blocked by:** `T-OBDV2-1a`
**Consumer (signal/noise):** the test **is** the consumer — it drives the live `translate()` pipeline against the T-OBDV2-1a corpus and asserts the designed channels move. Adds **no schema field**. This is the artefact that converts the revive decision from ratified *intent* into demonstrated *capability*.

### Goal ###

Author the wiring-gate test that loads the T-OBDV2-1a log set, runs `SensorSignalTranslator.translate()` on
each case, and asserts the **OBDLab channel each case is designed to move actually moved** (per the
signal-map) — and that the rejection cases raise their typed error instead of crashing. Done when the gate is
green on the sourced corpus and red if a case collapses to the all-default / `NO_FAULT` shape.

### Success criteria — PINNED gate-pass criteria ###

The gate is **green** iff **all** of the following hold (the corpus is the sourced set only; estimated cases
are excluded):

1. **Coverage realised:** every one of the 8 coverage-matrix cells is exercised by ≥1 passing case, and every
   in-scope fault family by ≥1 case (asserted by reading the signal-map / `fault_family` labels — coverage,
   not verdict).
2. **Discrimination, per case:** for each sourced non-rejection case, the single channel named in
   `signal_map.md` is emitted by `translate()` at a **non-default / non-`NO_FAULT`** value consistent with the
   case's `expected_obd_signature` (within the case's stated tolerance; comparison rules below). **Required
   pass rate: 100 % of the sourced gate set.** A case that fails to move its channel is either a bad fixture
   (fix it or move it to `estimated/`) or a real defect (file it in "Unplanned follow-ups") — it does not get
   silently tolerated. *(Owner may ratify a lower rate; default is 100 % of sourced cases.)*
3. **Rejection, per case:** every `expected_rejection` case raises exactly its named typed error
   (`PIDValidationError` / `SemanticConsistencyError`) — `pytest.raises` — with **zero** unhandled
   exceptions/crashes.
4. **Aggregate anti-regression:** strictly **fewer than 5 %** of the sourced non-rejection cases come back as
   the all-default/`NO_FAULT`/`ve_pct==0.0`/`ve_validity==UNKNOWN` shape — the inverse of the >95 % that
   quarantined the module. (With criterion 2 at 100 %, this is automatically satisfied; it is stated
   explicitly as the un-quarantine headline metric.)

### Context — assert on CHANNELS, never on a verdict ###

OBDLab is the **emitter**, COMLab the **judge** (`KGtopic.md` division of labour; `T-OBDV2-0`). Therefore the
gate asserts only on `OBDLivePayload` channels — `o2_failure_mode`, `normalized_obd_lambda`,
`ve_pct`/`ve_validity`, `trim_analytics_gate`, `total_trim_correction_delta(_b2)`, `maf_status`/`map_status`,
`rpm_state_bucket`. It must **never** assert a `fault_family` verdict or a top-3 list — `translate()` does not
emit one, and the `fault_family` key in the fixtures is an organizing label only.

Comparison rules for `expected_obd_signature` (the corpus uses these forms): exact match for enum channels
(`ve_validity`, `trim_analytics_gate`, `o2_failure_mode`, `rpm_state_bucket`, `maf_status`, `map_status`);
threshold strings like `">+15"` / `"<50"` parsed and asserted as inequalities for numeric channels
(`total_trim_correction_delta`, `ve_pct`); tolerance band (default ±0.02) for `normalized_obd_lambda`. The
`o2_channel_fault: true` cases assert the O2 clamp path (`O2_CHANNEL_FAULT` / clamped lambda + flagged
payload), not a crash.

The entry point is `translate(raw_user_inputs, dna_view=ObdLabDnaView(**case["dna_view"]))`; build the
`dna_view` from each case, pass `raw_pids` as `raw_user_inputs`. Mirror the load pattern of the 6
`tests/regression/fixtures/case_0*.json` cases.

### Deliverables ###

1. `tests/pid_logset/test_pid_logset_wiring_gate.py` — parameterised over `logset.json`: one assertion path for `expected_obd_signature` cases (channel moved), one for `expected_rejection` cases (`pytest.raises`), plus the coverage + <5 %-default aggregate checks.
2. A small loader/helper in the test module (no production code) to parse the threshold-string comparison rules.

### Files to touch ###

- `tests/pid_logset/test_pid_logset_wiring_gate.py` (NEW)
- (reads, does not modify: `tests/pid_logset/logset.json`, `signal_map.md`; `obdlab/core/sensor_signal_translator.py`; `obdlab/schemas/{dna_view,payload}.py`; `obdlab/core/exceptions.py` for the typed errors)

### Out of scope ###

No production-code change — if `translate()` genuinely cannot move a channel a sourced case says it should,
that is a **finding** (Unplanned follow-ups), not a licence to edit the emitter in this task. No new schema
field. No assertion on fault-family/verdict. Do not touch the regression suite. Do not run `graphify` / rebuild
the KG.

### Verification ###

```bash
cd <repo>/labs/obdlab
ruff check obdlab/ tests/
pyright obdlab/ tests/
# the gate itself
pytest -x -q tests/pid_logset/test_pid_logset_wiring_gate.py
# emitter discipline: the gate must NOT assert a fault-family verdict (must return nothing)
grep -nE 'fault_family|top3|top_3|LabResult|LabCandidate' tests/pid_logset/test_pid_logset_wiring_gate.py \
  && { echo "FAIL: gate asserts a verdict — OBDLab is an emitter"; exit 1; } || echo "OK channels-only"
# full suite still green
pytest -x -q
```

All steps pass; the un-quarantine headline (<5 % default-shape) is recorded in the note.

### Progress hook ###

`tasks/progress_notes/T-OBDV2-1b.md` opens with the confirmed `## Plan`, then `VERIFICATION GATE` (record:
cells covered, sourced-case pass rate, default-shape %) + `CODE REVIEW`. PROGRESS.md `T-OBDV2-1b`: Status=done,
Files changed=1, Verification="gate green: all 8 cells exercised, 100 % sourced cases moved their channel,
rejections raise typed errors, <5 % default-shape — OBDLab un-quarantined as an emitter". **When 1b is done,
revive is demonstrated capability, not just intent.**
