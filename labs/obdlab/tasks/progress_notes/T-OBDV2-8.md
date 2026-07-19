# T-OBDV2-8 — progress note

## Plan

We will add control module voltage (VPWR) manual input to OBDLab:
- **Field Addition:** Add `control_module_voltage_v: float` to [payload.py](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/obdlab/obdlab/schemas/payload.py) under `OBDLivePayload`.
- **Validation Bounds:** Update [physical_sensor_bounds.json](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/obdlab/obdlab/config/physical_sensor_bounds.json) with `control_module_voltage_v` range `[0.0, 18.0]` V with a wiki cite (`ecu-diagnosis/09` / `OBDLab_KG_Wiki.md §3.1`).
- **Signal Translator Logic:** Update [sensor_signal_translator.py](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/obdlab/obdlab/core/sensor_signal_translator.py) to populate the new field with a default of `14.0` V.
- **Proposals Registration:** Register `EP-OBD-IN-04` in [proposals.yaml](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/comlab/comlab/config/proposals/proposals.yaml).
- **Forward-registered Consumer:** Mark `T-OBDV2-8` as done in the `T-COMV2-VPWR-GATE-1` status row in COMLab's [PROGRESS.md](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/comlab/tasks/PROGRESS.md).
- **Tests:** Write unit test verifying bounds validation and payload emission.

## VERIFICATION GATE

- [x] `control_module_voltage_v` defined in `OBDLivePayload`.
- [x] boundary rules defined in `physical_sensor_bounds.json` and validated by `PIDIngestionValidator`.
- [x] `control_module_voltage_v` validated up to 18.0 V and rejects values out of bounds (e.g. -0.1 V or 18.1 V).
- [x] a low-rail input (e.g. `11.0 V`) carries through the translator without raising OBD verdicts.
- [x] `EP-OBD-IN-04` registered in `proposals.yaml`.
- [x] `T-COMV2-VPWR-GATE-1` row dependencies updated in `comlab/tasks/PROGRESS.md`.
- [x] `pytest` unit test suite passes cleanly.

## CODE REVIEW

- [x] strict emitter discipline: only fields are emitted, no diagnostic/electrical verdicts in OBDLab.
- [x] all `pyright` checks are clean (0 errors, 0 warnings).
- [x] all `ruff` lint checks pass.
