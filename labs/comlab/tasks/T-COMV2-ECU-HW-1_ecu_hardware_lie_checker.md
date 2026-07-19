# T-COMV2-ECU-HW-1 — ECU-hardware digital-lie checker (orphan-closer; default-off)

**Authored:** 2026-06-21 (architect, Cowork). **Stage:** 4. **Type:** orphan-closer consumer (flesh out the named stub + mirror emitted fields + wire the reader → close anti-orphan).
**Blocked by:** `T-OBDV2-7` (OBD `intake_air_temp_c` + `throttle_pos_pct` emitter, **done**) · `T-OBDV2-ECU-PERCEPT-1` (**done**). **DEP-9 · proposals `EP-OBD-IN-08`/`EP-OBD-IN-05` (`proposals.yaml:80`/`:73`) + `EP-COM-04` (`:15`).**
**Drill:** boot order (`COMLAB_TASKS_START_HERE.md`) → `PROGRESS.md` → **this file** → scope-confirm → code. **Load skills:** `comlab-python`, `comlab-verification-loop`, `comlab-code-review`, **`comlab-fusion-consumer`**.

> **One-line scope:** flesh out the empty `ECUHardwareChecker` stub into a checker that reads the **Mode-4 digital-lie signature** — `intake_air_temp_c` and `coolant_temp_c` both pinned at the −40 °C sensor floor with `throttle_pos_pct` at 100 %, corroborated by railed, **bank-symmetric** trim — and routes it to the **`ecu_fault`** family (internal-ECU / wiring fault, not a real mixture fault). Wire it into the router behind a default-off flag; absent/normal inputs are inert. Closes signal/noise for DEP-9.

### Context
`comlab/core/ecu_hardware_checker.py::ECUHardwareChecker` is a **stub** (`class ECUHardwareChecker: pass`) — the named consumer in `proposals.yaml` (`EP-COM-04`/`EP-OBD-IN-08`/`EP-OBD-IN-05`) that the OBD input-fields `intake_air_temp_c`/`throttle_pos_pct` were registered for, but it reads **nothing** → those fields are orphaned at the ECU-hardware reader. A failed/stuck ECU or a chewed sensor harness produces a **physically impossible coherent lie**: IAT and ECT both at −40 °C (the sensor-floor / open-circuit value) while TPS rails to 100 %, and fuel trim saturates on **both** banks together (global, symmetric — not bank-localised). That coherent pattern is an internal-ECU/hardware fault (`ecu_fault`, `ERR-EF-001` family, P06XX), and naming it stops the engine mis-routing the railed trim into a real lean/rich verdict. `coolant_temp_c` is already mirrored (`ingestion.py:371`); `bank-symmetric` here means `per_bank_trim_delta` is small (|Δ| ≤ ±5 %, the BANK-FUSE bound) while total trim is railed — the complement of BANK-FUSE's asymmetric case.

### What to build
1. **`comlab/schemas/ingestion.py::OBDLiveDataPayload`** — add `intake_air_temp_c: float | None = None` and `throttle_pos_pct: float | None = None`, mirroring the emitter (`labs/obdlab/obdlab/schemas/payload.py:105`/`:108`; bounds `ge=-40,le=140` / `ge=0,le=100` — mirror as **optional default-None** so absence is inert). `coolant_temp_c` already present (`:371`). Comment the consumer (`# consumer: ecu_hardware_checker.ECUHardwareChecker — T-COMV2-ECU-HW-1`).
2. **`comlab/core/ecu_hardware_checker.py`** — replace the `pass` stub with a small pure checker (no I/O, no cross-lab import):
   ```
   @dataclass(frozen=True)
   class ECUHardwareVerdict:
       is_ecu_hardware_fault: bool
       confidence: float

   class ECUHardwareChecker:
       def check(self, intake_air_temp_c, coolant_temp_c, throttle_pos_pct,
                 total_trim_correction_delta, per_bank_trim_delta) -> ECUHardwareVerdict:
           # digital-lie AND-gate (any None -> inert, is_ecu_hardware_fault=False):
           #   IAT <= _ECU_HW_TEMP_FLOOR_C (-40) AND ECT <= _ECU_HW_TEMP_FLOOR_C (-40)
           #   AND throttle_pos_pct >= _ECU_HW_TPS_RAIL_PCT (100)
           #   AND |total_trim_correction_delta| >= _ECU_HW_RAILED_TRIM_PCT (25)   # >±25% saturated, ERR-EF-001
           #   AND bank-symmetric: per_bank_trim_delta is None OR |per_bank_trim_delta| <= 5.0  # global, not bank-local
   ```
   Constants carry cites: `# wiki: 02_lab_input_contract.md §2a CONCEPT_OBD_CONSUMER_BANDS "ECU-hardware digital-lie signature" (IAT/ECT −40 floor + TPS 100 rail + railed symmetric trim) + §2 line70 (>±25 % saturated → ERR-EF-001) + 06_fault_atlas_families.md §CONCEPT_FAM_ECU + 13_proposals_register.md B-row (EP-COM-04 / EP-OBD-IN-08 / -05)`. **The §2a "ECU-hardware digital-lie signature" band is added by the architect out-of-band** (recorded in `PROGRESS.md`) so the checker cites COMLab-local thresholds, never `obdlab/research/`.
3. **`comlab/core/fault_atlas_router.py`** — add `enable_ecu_hw: bool = False` to the constructor (mirror `enable_ctxmod` `:375`; store `self._enable_ecu_hw`). Instantiate one `ECUHardwareChecker()` at `__init__` (cheap, stateless). In `execute_triage_loop` Phase 5, behind `self._enable_ecu_hw and obd_live_data is not None`, call `self._ecu_hw_checker.check(...)` with the mirrored fields + `obd_live_data.total_trim_correction_delta` + `obd_live_data.per_bank_trim_delta`; when `is_ecu_hardware_fault`, **promote** scored rows whose KG `fault_family == "ecu_fault"` as conflict-aware evidence (`max(score_val, verdict.confidence)`, mirror BANK-FUSE `:928–954`). Emit an `ecu_hardware_fault_applied` span event. (`ecu_fault` family + `ERR-EF-001` confirmed in `comlab/config/kg/ecu_fault.json`.)
4. Falsy short-circuits keep behaviour byte-identical: flag off · any input `None` · signature not met.

### Consumer (signal/noise)
`intake_air_temp_c` + `throttle_pos_pct` (+ existing `coolant_temp_c`, `total_trim_correction_delta`, `per_bank_trim_delta`) → `ecu_hardware_checker.ECUHardwareChecker.check`, reached from `fault_atlas_router.py::execute_triage_loop` Phase 5. Closes the DEP-9 ECU-hardware orphan and turns the `ECUHardwareChecker` stub into a live reader. Proposals `EP-COM-04`/`EP-OBD-IN-08`/`EP-OBD-IN-05` ship their consumer in this change.

### Tests — `tests/` (ADD)
- `test_ecu_hw_checker_unit`: direct `ECUHardwareChecker().check(...)` — the full digital-lie tuple returns `is_ecu_hardware_fault=True`; flipping any one input out of band (e.g. IAT=20) returns `False`; any `None` returns `False`.
- `test_ecu_hw_inert_when_off`: the full digital-lie request with `enable_ecu_hw=False` → `OrchestratorFinalUIOutput` identical to baseline.
- `test_ecu_hw_promotes_ecu_fault`: digital-lie request with `enable_ecu_hw=True` raises an `ecu_fault` row + fires `ecu_hardware_fault_applied`; a bank-**asymmetric** railed-trim request (|per_bank_trim_delta| > 5) does **not** (that is BANK-FUSE's case).

### Success criteria (done = all)
- **Consumer-read gate:** two greps — read site (`intake_air_temp_c`/`throttle_pos_pct` in `ecu_hardware_checker.py`) **and** the `enable_ecu_hw` branch in `fault_atlas_router.py` — prove the fields are read in a reachable path (the stub is no longer empty).
- Single-point **byte-identical** with flag off / any input absent / signature not met.
- `ruff check .` → `pyright comlab/` → `"$PY" -m pytest -x -q` clean (`PY=../../.sandbox-py/bin/python3.14`).
- Flip ledger row → `done`; fill `VERIFICATION GATE` + `CODE REVIEW` in `progress_notes/T-COMV2-ECU-HW-1.md`. **STOP.**

### Files to touch
`comlab/schemas/ingestion.py` · `comlab/core/ecu_hardware_checker.py` · `comlab/core/fault_atlas_router.py` · `tests/` (**ADD**) · `tasks/PROGRESS.md` (flip row) · `progress_notes/T-COMV2-ECU-HW-1.md`.

### Out of scope
The **idle-leak / idle-MAP corroboration** sub-channel named in DEP-9 (`EP-OBD-IN-05` second half — needs idle-MAP context not in scope here; defer to a follow-up); **flipping `enable_ecu_hw` default to on** (live activation is a separate follow-up); consuming `total_trim_correction_delta_b2` directly (that twin-trim input belongs to `T-COMV2-ECU-FUSE-1`; this task uses the already-mirrored `per_bank_trim_delta` for the symmetry check); new KG nodes beyond the existing `ecu_fault` family; emitter changes; graphify.

### Verification
```bash
cd labs/comlab; PY=../../.sandbox-py/bin/python3.14
ruff check . && pyright comlab/ && "$PY" -m pytest -x -q
grep -nI "intake_air_temp_c\|throttle_pos_pct" comlab/core/ecu_hardware_checker.py   # read site
grep -nI "enable_ecu_hw\|ECUHardwareChecker" comlab/core/fault_atlas_router.py        # the branch that reaches it
"$PY" -m pytest tests/ -q -k "ecu_hw"
```
