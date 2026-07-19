---
name: wired-composition-contract
description: >
  On-demand domain skill for the `wired` composition app. Load when a task builds
  or modifies the lab->COMLab payload mapping, the `diagnose()` entry point, or
  the single-case runner that consumes its verdict. Covers the COMLab inbound
  contract, each lab's CURRENT public surface (verified 2026-06-28), the per-lab
  mapping work, the high-idle gas forwarding the oil case depends on, and the
  signal/noise consumer rule. Gates T-WIRE-1, T-WIRE-2, T-WIRE-3.
status: BUILT
---
# wired-composition-contract — the lab->COMLab payload contract

`apps/wired/wired/composition.py` exposes one entry point,
`diagnose(raw_inputs) -> OrchestratorFinalUIOutput`. Its job: run each lab, map
each lab's typed output into a COMLab payload, build one
`OrchestratorInboundRequest`, and call `LabPipelineAggregator.process()`.

**Reference implementations to adapt (READ-NARROW, do NOT copy):**
`ARCHIVE/wiredV2/wiredv2/composition.py` (634 lines, 2026-06-21 — the most recent
prior wiring, ~80% correct for the current tree) and the older
`ARCHIVE/4DLabWired/wired/composition.py`. Both are bound to stale surfaces and
live under `ARCHIVE/` — never import them. Grep them for a pattern, adapt it,
verify every type against the live source below.

## 1. The COMLab inbound contract (verified 2026-06-28)
`OrchestratorInboundRequest` lives at `labs/comlab/comlab/schemas/ingestion.py:488`.
It is the single inbound type COMLab accepts and carries:

| Field | COMLab payload type | Authority (ingestion.py) |
|---|---|---|
| `metadata` | `SessionMetadata` | line 151 |
| `gas_lab_output` | `GasLabPayload` | line 165 |
| `obd_live_data` | `OBDLiveDataPayload \| None` | line 324 |
| `dtc_lab_output` | `DTCLabPayload \| None` | line 289 |
| `symptom_dna` | `dict` | — |
| `downstream_trim_role`, `has_catalyst` | enum / bool | line 488+ |

These are **mirrors** — COMLab re-declares the types it needs locally; it never
imports a lab. `ingestion.py` is authoritative for field names, types, and
`Field(...)` constraints. `grep -n` the exact class before writing a mapper; do
not trust a remembered field list. Output type: `OrchestratorFinalUIOutput`
(`labs/comlab/comlab/schemas/response.py:132`); the verdict the runner asserts on
is its `diagnostic_verdict.fault_code`.

> **Chem-mirror prerequisite.** `GasLabPayload.chemical_state` mirrors GASLab's
> 34-value `ChemicalSignature`. Until gaslab `T-GV2-2` lands, that mirror is at
> 28/32 (docstring `ingestion.py:168` still says "28-value"). `T-WIRE-1` is
> blocked on `T-GV2-2` for exactly this reason — see `WIRING_PREP.md` Section A.

## 2. Lab public surfaces (CURRENT — verified by live import)
| Lab | Import | Entry point | Output type |
|---|---|---|---|
| GASLab | `from gaslab import process, GasLabContext, GasReading` | `process(GasReading, GasLabContext) -> GasLabPayload` | `GasLabPayload` |
| OBDLab | `from obdlab import SensorSignalTranslator` | `.translate(raw_user_inputs: dict, dna_view: ObdLabDnaView \| None, accumulator=None)` | `OBDLivePayload` |
| DTCLab | `from dtclab import DataFusionSanitizer` | `.sanitize(raw_dtcs, raw_freeze_frame, raw_mode06, *, codes_cleared=False, active_mil=False, mil_flashing=False)` | `DTCLabPayload` |
| DNALab | `from dnalab import build_vehicle_dna` | `build_vehicle_dna(vin: str, triage: dict) -> VehicleDNA` | `VehicleDNA` |
| VINLab | `from vinlab import decode, VINDecodeError` | `decode(vin) -> VinDNA`; `VINDecodeError` for no-VIN fallback | `VinDNA` |
| COMLab | `from comlab.core.lab_pipeline_aggregator import LabPipelineAggregator` | `.process(OrchestratorInboundRequest, fault_code=None)` | `OrchestratorFinalUIOutput` |

`apps/wired/wired/` is the **only** package that may hold these imports together.
No lab imports another lab; no lab imports `wired/`. The mapper between a lab
output and a COMLab payload lives **here** — never in a lab, never in COMLab.

`LabPipelineAggregator.__init__` flags (default-off unless a task says
otherwise): `enable_delta`, `enable_delta_v2`, `enable_vpwr_gate`,
`enable_fatal_gates`. The baseline `diagnose()` constructs it with defaults;
`enable_fatal_gates` is threaded only in `T-WIRE-4`.

## 3. Per-lab mapping work (current reality)
- **DNALab -> metadata + VIN/symptom dicts:** `build_vehicle_dna(vin, triage)`
  -> `vehicle_dna.to_json_payload()` -> `vin_dna` + `symptom_dna` dicts. On
  `VINDecodeError`, use the no-VIN fallback (MODERN horizon, NONE confidence).
  Build `SessionMetadata` including the optional `air_metering_strategy` token
  (the VE gate reads it).
- **GASLab -> `GasLabPayload`:** build a low-idle `GasReading`, and when the case
  carries high-idle (`*_high`) values, a second `GasReading` passed as
  `GasLabContext.reading_high`. Map the snapshot fields straight across **and
  forward the high-idle fields onto the payload** (the oil case depends on this;
  the prior wiring dropped it).
- **OBDLab -> `OBDLiveDataPayload`:** map the rich field set (`engine_warmed`,
  `total_trim_correction_delta`(+`_b2`), `ve_pct`/`ve_validity`,
  `rpm_state_bucket`, `o2_failure_mode`, `maf_status`/`map_status`,
  `normalized_obd_lambda`, `per_bank_trim_delta`, `lambda_perception_delta`,
  `fuel_system_status`, `freeze_frame_pids`). New optional fields default to
  `None`. OBD is optional — absent -> `obd_live_data=None`.
- **DTCLab -> `DTCLabPayload`:** cross-package boundary via
  `dtc_payload.model_dump(mode="json")` -> `DTCLabPayload(**dtc_dict)` (Pydantic
  re-coerces enums/nested models). DTC is optional — absent -> `None`.

Two mechanical vocab translations live here (no lab logic): `_map_o2_sensor_type`
(VINLab `WIDEBAND_AFR`/`NARROWBAND` -> OBDLab `WIDEBAND_LINEAR`/`NARROWBAND_0_TO_1V`)
and `_derive_horizon` (fallback only — DNALab now emits `resolved_horizon`).

## 4. The signal/noise consumer rule
Every field mapped from a lab output into a COMLab payload carries an inline
comment naming the COMLab consumer that reads it:
```python
ve_pct=obd.ve_pct,  # consumer: fault_atlas_router VE-evidence gate (T-COMV2-VE-GATE-1)
```
If you cannot name a COMLab reader for a field, **do not map it** — that is the
signal/noise rule at the boundary.
