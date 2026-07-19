# T-COMV2-VPWR-GATE-1 — rail-health electrical pre-check (orphan-closer; default-off)

**Authored:** 2026-06-21 (architect, Cowork). **Stage:** 4. **Type:** orphan-closer consumer (mirror emitted field + wire its named reader → close anti-orphan).
**Blocked by:** `T-OBDV2-8` (OBD `control_module_voltage_v` emitter, **done**). **DEP-10 · proposal `EP-OBD-IN-04`** (`proposals.yaml`).
**Drill:** boot order → `PROGRESS.md` → **this file** → scope-confirm → code. **Load skills:** `comlab-python`, `comlab-verification-loop`, `comlab-code-review`, **`comlab-fusion-consumer`**.

> **One-line scope:** mirror OBD `control_module_voltage_v` and wire an electrical **pre-check** into `perception_contradiction.detect`, behind a default-off flag: when the rail is out of band, **down-weight / suppress** sensor-fault routing (a drifting rail mimics a lying sensor). Healthy rail and absent field are inert. Closes signal/noise for DEP-10.

### Context
A control-module rail outside `[12.0 V, 15.0 V]` can make a healthy O₂/MAF sensor read like a faulty one. The pre-check rules out a bad rail **before** `perception_contradiction` blames a sensor. Zero live COMLab reads today → orphan. Emit a **qualifier on the existing result**, never a new override.

### What to build
1. **`comlab/schemas/ingestion.py::OBDLiveDataPayload`** — add `control_module_voltage_v: float | None = None` (mirror emitter `labs/obdlab/obdlab/schemas/payload.py:111`; emitter default `14.0`, bounds `ge=0,le=18` — mirror as optional so absence stays inert). Comment the consumer.
2. **`comlab/core/perception_contradiction.py::detect`** (`:100`) — `detect()` is a **free function taking explicit scalars**, so add **two** keyword params: `control_module_voltage_v: float | None = None` and `enable_vpwr_gate: bool = False` (both default-inert, appended after the existing keyword args to keep callers compatible). When `enable_vpwr_gate` and `control_module_voltage_v` is present and **`< 12.0` or `> 15.0`**, attach a `QUALIFIER_RAIL_OUT_OF_BAND` to the result's existing `qualifiers` tuple (mirror the `QUALIFIER_MASKED_BY_DOWNSTREAM_TRIM` pattern, `:~28`) and down-weight / suppress the bias verdict. `# wiki: 02_lab_input_contract.md §2a CONCEPT_OBD_CONSUMER_BANDS "Control-module rail bands" (Low <12.0 V / High >15.0 V) + 13_proposals_register.md §line47 (EP-OBD-IN-04)`. Add the qualifier constant next to the existing ones.
3. **`comlab/core/lab_pipeline_aggregator.py` — the live path (required for anti-orphan).** `detect()`'s **only** production caller is `detect_perception_contradiction(...)` at **`:317`** (aliased import `:34–36`); `request.obd_live_data` is already in scope there (`:309` reads `.normalized_obd_lambda`). Two edits: (a) add `enable_vpwr_gate: bool = False` to `__init__` mirroring the existing `enable_delta` flag (`:96`), store it; (b) at the `:317` call, pass `control_module_voltage_v=(request.obd_live_data.control_module_voltage_v if request.obd_live_data is not None else None)` **and** `enable_vpwr_gate=self._enable_vpwr_gate`. Without this the new param is dead → the consumer-read gate fails. The flag stays **default-off**; flipping its default on is the separate live-activation follow-up.
4. Falsy short-circuits keep behaviour byte-identical: flag off · field `None`/in-band.

### Consumer (signal/noise)
`control_module_voltage_v` → `perception_contradiction.py::detect` rail-health qualifier, **reached via `lab_pipeline_aggregator.py:317`** (the live call site). Closes the DEP-10 orphan. Proposal `EP-OBD-IN-04` ships its consumer in this same change.

### Tests — `tests/` (ADD)
- `test_vpwr_inert_when_off`: low-rail input with `enable_vpwr_gate=False` and in-band rail with it on → result identical to baseline (no qualifier, unchanged verdict).
- `test_vpwr_low_rail_qualifies`: `control_module_voltage_v = 11.0`, gate on → `QUALIFIER_RAIL_OUT_OF_BAND` present + bias verdict suppressed/down-weighted.
- `test_vpwr_high_rail_qualifies`: `15.6` → same qualifier path.

### Success criteria (done = all)
- **Consumer-read gate (live path):** three greps — `control_module_voltage_v` read in `detect`, the `enable_vpwr_gate` branch, **and** the aggregator (`:317`) passing `control_module_voltage_v` into `detect_perception_contradiction(...)`. The third proves the read is reachable in production, not dead.
- Behaviour **byte-identical** with flag off / field absent / rail in-band (a full-pipeline test through the aggregator with the flag default-off must match baseline).
- `ruff check .` → `pyright comlab/` → `"$PY" -m pytest -x -q` clean (`PY=../../.sandbox-py/bin/python3.14`).
- Flip ledger row → `done`; fill both gate blocks in `progress_notes/T-COMV2-VPWR-GATE-1.md`. **STOP.**

### Files to touch
`comlab/schemas/ingestion.py` · `comlab/core/perception_contradiction.py` · `comlab/core/lab_pipeline_aggregator.py` (the live call site + the default-off flag) · `tests/` (**ADD**) · `tasks/PROGRESS.md` · `progress_notes/T-COMV2-VPWR-GATE-1.md`.

### Out of scope
**`ΔVPWR` alternator-AC-ripple node (`EP-FA-05`)** — needs a second-frame ΔVPWR and `EP-FA-05` is not in `proposals.yaml`; defer to a follow-up. **Flipping the `enable_vpwr_gate` default to on** (the aggregator gains the flag at default-off here; live activation is the separate follow-up); surfacing the qualifier into UI output; emitter changes; graphify.

### Verification
```bash
cd labs/comlab; PY=../../.sandbox-py/bin/python3.14
ruff check . && pyright comlab/ && "$PY" -m pytest -x -q
grep -nI "control_module_voltage_v" comlab/core/perception_contradiction.py   # read site
grep -nI "enable_vpwr_gate"          comlab/core/perception_contradiction.py   # the branch that reaches it
grep -nI "control_module_voltage_v\|enable_vpwr_gate" comlab/core/lab_pipeline_aggregator.py  # the live path (:317)
"$PY" -m pytest tests/ -q -k "vpwr"
```
