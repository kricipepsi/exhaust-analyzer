# T-OBDV2-6 — progress note

## Plan

We will add a fuel-system-status manual input (Closed/Open-Loop dropdown) to OBDLab:
- **Enum Mirror:** Mirror DTCLab's `FuelSystemStatus` enum locally in [vocabulary.py](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/obdlab/obdlab/schemas/vocabulary.py) without cross-lab imports.
- **Dropdown Field:** Add `fuel_system_status` to [payload.py](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/obdlab/obdlab/schemas/payload.py).
- **Migration Mapping & Ingestion:** Update [pid_ingestion_validator.py](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/obdlab/obdlab/core/pid_ingestion_validator.py) to accept, validate, and convert the input value, mapping legacy strings `"Closed_Loop"` -> `CL` and `"Open_Loop_Cold"` -> `OL`.
- **Internal Consumers:** Migrate string checks to the enum in [analytics_preconditions.py](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/obdlab/obdlab/core/analytics_preconditions.py) and [semantic_consistency_checker.py](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/obdlab/obdlab/core/semantic_consistency_checker.py).
- **Forward-registered Consumer:** Register proposal `EP-OBD-IN-03` in [proposals.yaml](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/comlab/comlab/config/proposals/proposals.yaml) and verify its consumer `T-COMV2-FUELSYS-GATE-1` in the progress ledger.

## VERIFICATION GATE

- [x] local `FuelSystemStatus` enum (CL/OL/OL_DRIVE/OL_FAULT) exists in `vocabulary.py` with no cross-lab imports.
- [x] `fuel_system_status` accepted as manual input and validated.
- [x] two internal consumers migrated to the enum with behavior preserved.
- [x] `EP-OBD-IN-03` registered in `proposals.yaml`.
- [x] `T-COMV2-FUELSYS-GATE-1` confirmed in `comlab/tasks/PROGRESS.md`.
- [x] `pytest` tests pass successfully.

## CODE REVIEW

- [x] strict emitter discipline: no fuel-system verdict emitted.
- [x] type checking via pyright and lint checking via ruff are clean.
