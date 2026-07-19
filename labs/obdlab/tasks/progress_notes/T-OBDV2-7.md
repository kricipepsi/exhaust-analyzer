# T-OBDV2-7 — progress note

## Plan

We will add intake air temperature (IAT) and throttle position sensor (TPS) manual inputs to OBDLab:
- **Field Addition:** Add `intake_air_temp_c` (-40..140 °C) and `throttle_pos_pct` (0..100 %) to [payload.py](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/obdlab/obdlab/schemas/payload.py) under `OBDLivePayload`.
- **Validation Bounds:** Update [physical_sensor_bounds.json](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/obdlab/obdlab/config/physical_sensor_bounds.json) and [pid_ingestion_validator.py](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/obdlab/obdlab/core/pid_ingestion_validator.py) boundary cases to include both fields. Widen `intake_air_temp_c` max limit to 140 °C to match the task spec and coolant limits.
- **Signal Translator Logic:** Update [sensor_signal_translator.py](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/obdlab/obdlab/core/sensor_signal_translator.py) to populate the new fields in `OBDLivePayload`.
- **VE Math Integration:** Verify that IAT propagates correctly into [ve_engine.py](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/obdlab/obdlab/core/ve_engine.py).
- **Proposals Registration:** Register `EP-OBD-IN-08` (IAT) and `EP-OBD-IN-05` (TPS) in [proposals.yaml](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/comlab/comlab/config/proposals/proposals.yaml).
- **Forward-registered Consumer:** Mark `T-OBDV2-7` as done in the `T-COMV2-ECU-HW-1` status row in COMLab's [PROGRESS.md](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/comlab/tasks/PROGRESS.md).
- **Documentation Update:** Update [OBDLab_KG_Wiki.md](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/obdlab/wiki/OBDLab_KG_Wiki.md) and [LLD_OBDLab.md](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/obdlab/wiki/LLD_OBDLab.md) to document the updated bounds.

## VERIFICATION GATE

- [x] `intake_air_temp_c` and `throttle_pos_pct` defined in `OBDLivePayload`.
- [x] boundaries defined in `physical_sensor_bounds.json` and validated by `PIDIngestionValidator`.
- [x] IAT validated up to 140 °C; TPS validated up to 100 %.
- [x] changing IAT successfully alters computed VE in unit tests, proving live-consumer math propagation.
- [x] ground-trace digital-lie pattern (IAT/ECT/TPS = -40 / -40 / 100) passes through translator without raising OBD verdicts.
- [x] `EP-OBD-IN-05` and `EP-OBD-IN-08` registered in `proposals.yaml`.
- [x] `T-COMV2-ECU-HW-1` row dependencies updated in `comlab/tasks/PROGRESS.md`.
- [x] `pytest` unit test suite passes cleanly (all 390 tests green).

## CODE REVIEW

- [x] strict emitter discipline: only fields are emitted, no diagnostic verdicts in OBDLab.
- [x] all `pyright` checks are clean (0 errors, 0 warnings).
- [x] all `ruff` lint checks pass.
