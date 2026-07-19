# DTCLab v2 — Progress Ledger (Stage 3)

**Lab:** DTCLab · **Build stage:** 3.
**Cross-lab forward registry:** `v2-restructure/CROSS_LAB_DEPENDENCIES.md`.
**Mode:** STRICT.

## Task log — Stage-3 DTCLab tasks

| ID | Task file | Status | Blocked by | Consumes / Emits | Notes |
|---|---|---|---|---|---|
| **T-DTCV2-NOSTART-1** | `T-DTCV2-NOSTART-1_mode06_monitor_aborted_emit.md` | `done` | `progress_notes/T-DTCV2-NOSTART-1.md` | MONITOR_ABORTED + ff_fuel_spark_cut_at_crank; CAN-era gated; classify_margin unchanged; emitter-only. | **DEP-8 · proposal `EP-DTC-NOSTART-1`.** Committed `240f3c5`. **Post-commit review:** schema gap found after commit and closed by `T-DTCV2-NOSTART-1-FIX`; `ff_fuel_spark_cut_at_crank` is now declared on `FreezeFrameRecord` and round-trips through `model_dump()`. `MONITOR_ABORTED`, CAN-era gate (`euro_emission_category`), emitter-only otherwise verified. |
| **T-DTCV2-NOSTART-1-FIX** | `T-DTCV2-NOSTART-1-FIX_freeze_frame_schema_field.md` | `done` | — | Declares `FreezeFrameRecord.ff_fuel_spark_cut_at_crank` (§12.3) — the field the parent's S4 consumer reads | Schema field + constructed-record round-trip test complete; parent Deliverable #3 closed. |
