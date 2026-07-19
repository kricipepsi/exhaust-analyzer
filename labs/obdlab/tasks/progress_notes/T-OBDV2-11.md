# T-OBDV2-11 — progress note

## Plan

We will add optional per-cell LTFT load-cell vector manual input to OBDLab:
- **Field Addition:** Add `ltft_cell_vector: dict[int, float] | None = Field(default=None)` to [payload.py](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/obdlab/obdlab/schemas/payload.py) under `OBDLivePayload`.
- **Validation bounds/type check:** Add verification of the field type and contents in `PIDIngestionValidator` to ensure it is a dictionary mapping integer cell indices to float LTFT % values, or `None`. Cell keys must be non-negative integers (>= 0), and LTFT values must be floats or ints between -127 and 127. Validated in [pid_ingestion_validator.py](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/obdlab/obdlab/core/pid_ingestion_validator.py) (gated with `# wiki: research/chunks/fuel-trim/13` comments).
- **Signal Translator Logic:** Update [sensor_signal_translator.py](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/obdlab/obdlab/core/sensor_signal_translator.py) to accept, validate, and ferry the new field with a default of `None` if not provided.
- **Proposals Registration:** Register `EP-OBD-12` in [proposals.yaml](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/comlab/comlab/config/proposals/proposals.yaml).
- **Forward-registered Consumer:** Register `T-COMV2-LTFT-CELL-1` in COMLab's [PROGRESS.md](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/comlab/tasks/PROGRESS.md).
- **Schema Doc Update:** Update the schema table and field count in [OBDLab_KG_Wiki.md](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/obdlab/wiki/OBDLab_KG_Wiki.md).
- **Tests:** Write unit test verifying type/value validation, payload emission, and default `None` (no cell PIDs) fallback.

## VERIFICATION GATE

- [x] `ltft_cell_vector` defined in `OBDLivePayload`.
- [x] type/bounds check for `ltft_cell_vector` enforced by `PIDIngestionValidator` (must be `dict[int, float]` or `None`, cell indices >= 0, values between -127 and 127).
- [x] `ltft_cell_vector` defaults to `None` when absent (graceful degradation path).
- [x] `EP-OBD-12` registered in `proposals.yaml` with named consumer and NEW-wiki cite.
- [x] `T-COMV2-LTFT-CELL-1` row forward-registered in `comlab/tasks/PROGRESS.md`.
- [x] `OBDLab_KG_Wiki.md` schema table updated to list `ltft_cell_vector` and the field count updated.
- [x] `pytest` unit test suite passes cleanly.

## CODE REVIEW

- [x] strict emitter discipline: only fields are emitted, no diagnostic/localisation verdicts in OBDLab.
- [x] all `pyright` checks are clean (0 errors, 0 warnings).
- [x] all `ruff` lint checks pass.
