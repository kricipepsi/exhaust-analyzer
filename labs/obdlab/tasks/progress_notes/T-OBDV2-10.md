# T-OBDV2-10 — progress note

## Plan

We will add the MAF linearity and speed-density theoretical-airflow calculation:
- **Field Addition:** Add `w_theo: float | None = Field(default=None)` and `sensor_error_delta: float | None = Field(default=None)` to [payload.py](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/obdlab/obdlab/schemas/payload.py) under `OBDLivePayload`.
- **Calculation Logic:** Implement the ideal-gas-based speed-density theoretical airflow $W_{\text{theo}}$ and the two-point non-linearity delta calculations in a new helper [maf_linearity.py](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/obdlab/obdlab/core/maf_linearity.py).
- **Signal Translator Wiring:** Update [sensor_signal_translator.py](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/obdlab/obdlab/core/sensor_signal_translator.py) to cache the latest `(maf, w_theo)` values for `STABILIZED_IDLE` and `STRESS_IDLE` bands. The scalars will be computed and emitted only under the two-point guard when both bands have been successfully captured and the strategy is `DUAL_MAF_MAP_CROSSCHECK`.
- **Proposals Registration:** Register `EP-OBD-11` in [proposals.yaml](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/comlab/comlab/config/proposals/proposals.yaml).
- **Forward-registered Consumer:** Register `T-COMV2-MAF-LIN-1` in COMLab's [PROGRESS.md](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/comlab/tasks/PROGRESS.md).
- **Schema Doc Update:** Update the schema table and field count in [OBDLab_KG_Wiki.md](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/obdlab/wiki/OBDLab_KG_Wiki.md).
- **Tests:** Write unit tests verifying the calculations, cached two-band logic, fallback behavior when a band is missing, and strict emitter discipline.

## VERIFICATION GATE

- [x] `w_theo` and `sensor_error_delta` defined in `OBDLivePayload`.
- [x] Calculations of `w_theo` and `sensor_error_delta` match formula specifications.
- [x] Both fields are cached and emitted only when both `STABILIZED_IDLE` and `STRESS_IDLE` bands are captured.
- [x] Both fields default to `None` if any band is missing or strategy is not `DUAL_MAF_MAP_CROSSCHECK`.
- [x] `EP-OBD-11` registered in `proposals.yaml` with named consumer and NEW-wiki cite.
- [x] `T-COMV2-MAF-LIN-1` row forward-registered in `comlab/tasks/PROGRESS.md`.
- [x] `OBDLab_KG_Wiki.md` schema table updated to list the new fields and the field count updated.
- [x] `pytest` unit test suite passes cleanly.

## CODE REVIEW

- [x] strict emitter discipline: only fields are emitted, no diagnostic/fault verdicts in OBDLab.
- [x] all `pyright` checks are clean (0 errors, 0 warnings).
- [x] all `ruff` lint checks pass.
