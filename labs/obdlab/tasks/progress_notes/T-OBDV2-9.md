# T-OBDV2-9 — progress note

## Plan

We will add optional per-cylinder misfire counts manual input to OBDLab:
- **Field Addition:** Add `per_cylinder_misfire_counts: dict[int, int] | None = Field(default=None)` to [payload.py](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/obdlab/obdlab/schemas/payload.py) under `OBDLivePayload`.
- **Validation bounds/type check:** Add verification of the field type and contents in `PIDIngestionValidator` to ensure it is a dictionary mapping integer cylinder numbers to integer misfire counts, or `None`. Since this is a dictionary type and not a scalar numeric sensor value, we will validate it in python logic inside [pid_ingestion_validator.py](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/obdlab/obdlab/core/pid_ingestion_validator.py) rather than `physical_sensor_bounds.json`.
- **Signal Translator Logic:** Update [sensor_signal_translator.py](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/obdlab/obdlab/core/sensor_signal_translator.py) to accept, validate, and ferry the new field with a default of `None` if not provided.
- **Proposals Registration:** Register `EP-OBD-IN-07` in [proposals.yaml](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/comlab/comlab/config/proposals/proposals.yaml).
- **Forward-registered Consumer:** Register `T-COMV2-MISFIRE-LOC-1` in COMLab's [PROGRESS.md](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/comlab/tasks/PROGRESS.md).
- **Schema Doc Update:** Update the schema table and field count in [OBDLab_KG_Wiki.md](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/obdlab/wiki/OBDLab_KG_Wiki.md).
- **Tests:** Write unit test verifying type/value validation, payload emission, and default `None` (pre-CAN) fallback.

## VERIFICATION GATE

- [x] `per_cylinder_misfire_counts` defined in `OBDLivePayload`.
- [x] type/bounds check for `per_cylinder_misfire_counts` enforced by `PIDIngestionValidator` (must be `dict[int, int]` or `None`, counts >= 0, cylinder indices >= 1).
- [x] `per_cylinder_misfire_counts` defaults to `None` when absent (pre-CAN graceful path).
- [x] `EP-OBD-IN-07` registered in `proposals.yaml` with named consumer and NEW-wiki cite.
- [x] `T-COMV2-MISFIRE-LOC-1` row forward-registered in `comlab/tasks/PROGRESS.md`.
- [x] `OBDLab_KG_Wiki.md` schema table updated to list `per_cylinder_misfire_counts` and the field count updated.
- [x] `pytest` unit test suite passes cleanly.

## CODE REVIEW

- [x] strict emitter discipline: only fields are emitted, no diagnostic/misfire/localisation verdicts in OBDLab.
- [x] all `pyright` checks are clean (0 errors, 0 warnings).
- [x] all `ruff` lint checks pass.
