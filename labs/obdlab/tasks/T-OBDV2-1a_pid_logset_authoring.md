# T-OBDV2-1a — author the PID log set + signal-map (data half of the un-quarantine proof)

**Status:** `pending (next)` — **coder-runnable** · **Lab:** OBDLab (Stage 2) · **Mode:** STRICT
**Origin:** `HANDOFF_T-OBDV2-1_pid_logset_wiring_gate.md` · authoring spec `wiki/PID_LOGSET_RESEARCH_PROMPT.md`
**Blocked by:** — (T-OBDV2-0 done = revive; PURGE-1/2/3 done = final DNA contract pinned)
**Consumer (signal/noise):** the live `translate()` pipeline via **T-OBDV2-1b** (the wiring-gate test). This task adds **no schema field** — it produces test data (fixtures + a signal-map) that exercises the existing `OBDLivePayload` channels. No new contract surface.

### Goal ###

Produce the PID-bearing fixture corpus that proves OBDLab is no longer starved of input. Author **~30 JSON
fixtures** (target 25–40) spanning the 8-cell coverage matrix in `PID_LOGSET_RESEARCH_PROMPT.md`, each
designed to drive `translate()` to a **discriminating, non-`NO_FAULT`/non-default** channel value, plus a
**signal-map** table (`case_id → the single OBDLab channel it is designed to move`). Done when the corpus
covers every matrix cell + every in-scope fault family, every non-obvious numeric is sourced, and the fixtures
load against the **real** `translate()` input contract (verified structurally — the *behavioural* assertion is
T-OBDV2-1b).

### Success criteria ###

- `tests/pid_logset/logset.json` — a JSON array of ~25–40 cases in the `PID_LOGSET_RESEARCH_PROMPT.md` §"Output format" shape (`case_id`, `description`, `fault_family`, `vehicle`, `dna_view`, `raw_pids`, `expected_obd_signature` | `expected_rejection`, `sources`).
- **Coverage:** ≥1 case per matrix cell (VE branches ×3, O2 types ×3, lambda outcomes ×4 incl. `O2_CHANNEL_FAULT`, trim outcomes ×3, VE-validity faults ×3, RPM/thermal ×4, trim-gates ×5, boundary/rejection ×≥6) and ≥1 case per fault family (`lean_condition`, `rich_condition`, `catalyst_failure`, `misfire`/ignition, `sensor_fault`, `mechanical_wear`, `no_fault`).
- `tests/pid_logset/signal_map.md` — table mapping each `case_id` to the **single** channel it moves (e.g. `total_trim_correction_delta`, `normalized_obd_lambda`, `ve_validity`, `o2_failure_mode`, `trim_analytics_gate`) or, for rejection cases, the typed error expected.
- **Sourcing:** every non-obvious numeric cites SAE J1979 / ISO 15031-5 PID defs, a service manual, or a reputable diagnostic reference. Estimated values carry `"estimated": true` + reasoning and live in a **separate** `tests/pid_logset/estimated/` file — they are **excluded from the gate set** (T-OBDV2-1b runs only the sourced set).
- **Structural load check** (this task's gate, not the behavioural one): every sourced case's `dna_view` parses into `ObdLabDnaView` and every `raw_pids` is accepted by the validator without raising (except the rejection cases, which must parse as inputs but are *flagged* for 1b to assert the error).

### Context — PIN these contract facts (do not copy the stale prompt verbatim) ###

The prompt's **Part B is stale post-PURGE.** The real `obdlab/schemas/dna_view.py::ObdLabDnaView` has **exactly
eight** fields: `engine_displacement_liters`, `cylinder_count`, `rated_rpm`, `stress_idle_rpm_target`,
`air_metering_strategy`, `upstream_o2_type`, `induction_type`, `confidence`. Therefore:

- **DROP `emissions.egr_equipped` and `number_of_banks`** from every `dna_view` — they are **not** fields on
  `ObdLabDnaView` (PURGE-2 removed `ObdEmissionsView`/`emissions`; there is no `number_of_banks` here). Do not
  add `resolved_horizon` either.
- **Bank-2 is expressed in `raw_pids`, not the DNA view:** a V-engine case carries `shrtft2`/`longft2` (and
  `cylinder_count` ≥ 6/8 in the DNA view); a single-bank case omits them. The matrix-item-8 "bank-2
  null-contract violation" rejection case is a 4-cyl engine that *wrongly* carries `shrtft2`/`longft2`.
- `translate(raw_user_inputs: dict, dna_view: ObdLabDnaView | None = None)` is the entry point; `dna_view=None`
  defaults to `DUAL_MAF_MAP_CROSSCHECK` + confidence `NONE`.
- **Trim realism:** real STFT/LTFT range is **−100…+99 %**; `±127` is a saturation **sentinel**, not a reading
  (the CSV fixes this). Use realistic trims everywhere **except** the explicit saturation rejection case.
- **CSV is reference-only:** read `research/obd2-pid-table-service-01.csv` to keep raw PID values in real
  J1979 ranges. **Do not** build a J1979 decoder — that is out of scope.
- **`fault_family` is an organizing label, not an emitted field.** `translate()` emits **channels**, never a
  fault-family verdict (OBDLab is the emitter; COMLab judges). The `fault_family` key groups cases for sourcing
  and coverage; T-OBDV2-1b must **not** assert `translate()` returns it.

### Deliverables ###

1. `tests/pid_logset/logset.json` — the sourced fixture corpus.
2. `tests/pid_logset/signal_map.md` — `case_id → channel moved` (+ rejection error per rejection case).
3. `tests/pid_logset/estimated/logset_estimated.json` — any case with an estimated numeric (excluded from the gate).
4. `tests/pid_logset/README.md` — one paragraph: what the set proves, the post-PURGE DNA-contract pins above, and that 1b is the gate.

### Files to touch ###

- `tests/pid_logset/logset.json` (NEW)
- `tests/pid_logset/signal_map.md` (NEW)
- `tests/pid_logset/estimated/logset_estimated.json` (NEW)
- `tests/pid_logset/README.md` (NEW)
- (reference-only, do not modify: `research/obd2-pid-table-service-01.csv`, `obdlab/schemas/{dna_view,payload}.py`, the 6 `tests/regression/fixtures/case_0*.json` for shape)

### Out of scope ###

No code, no test logic (that is T-OBDV2-1b). No new schema field; no edit to `translate()`, schemas, or
analytics. No J1979 decoder. Do not extend the regression fixtures (`tests/regression/fixtures/`) — the
un-quarantine set is **distinct**. Off-scope finds → `PROGRESS.md` "Unplanned follow-ups".

### Verification ###

```bash
cd <repo>/labs/obdlab
ruff check tests/ 2>/dev/null || true   # data task; ruff applies only if a .py helper is added (avoid)
# JSON well-formed
python3.14 -c "import json,glob; [json.load(open(f)) for f in glob.glob('tests/pid_logset/**/*.json',recursive=True)]; print('json OK')"
# Structural load: every sourced dna_view parses; every sourced raw_pids validates (rejection cases flagged, not run here)
python3.14 - <<'PY'
import json, pathlib
from obdlab.schemas.dna_view import ObdLabDnaView
cases = json.load(open("tests/pid_logset/logset.json"))
cells = set()
for c in cases:
    assert "case_id" in c and "signal" not in c.get("dna_view", {}), c["case_id"]
    if "expected_rejection" not in c:
        ObdLabDnaView(**c["dna_view"])          # must not raise for non-rejection cases
        # forbid stale fields
        assert "emissions" not in c["dna_view"] and "number_of_banks" not in c["dna_view"], c["case_id"]
print(f"OK {len(cases)} cases parse against post-PURGE ObdLabDnaView")
PY
```

All steps pass; coverage + sourcing reviewed against `PID_LOGSET_RESEARCH_PROMPT.md` §"Coverage matrix".

### Progress hook ###

`tasks/progress_notes/T-OBDV2-1a.md` opens with the confirmed `## Plan` (naming the corpus size, the cells, and
the channel each case moves), then `VERIFICATION GATE` + `CODE REVIEW`. PROGRESS.md `T-OBDV2-1a`: Status=done,
Files changed=N, Verification="~30 sourced cases across 8 matrix cells + 7 families; post-PURGE DNA contract
(no emissions/number_of_banks); estimated cases quarantined; all parse".
