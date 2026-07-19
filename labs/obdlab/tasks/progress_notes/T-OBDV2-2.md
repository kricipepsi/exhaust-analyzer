# T-OBDV2-2 — progress note

## Plan

We will record the VE-as-independent-evidence bound in the inter-lab contract and forward-register the Stage 4 consumer.
- **Files to create/modify:**
  - [comlab/tasks/PROGRESS.md](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/comlab/tasks/PROGRESS.md): Change `T-OBDV2-2` status from pending to done in the "Blocked by" column of the pre-registered `T-COMV2-VE-GATE-1` row.
  - [comlab/docs/wiki/SEMANTIC_CONTRACT.md](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/comlab/docs/wiki/SEMANTIC_CONTRACT.md) and [semantic/vocabul/SEMANTIC_CONTRACT.md](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/semantic/vocabul/SEMANTIC_CONTRACT.md): Insert section 6.7 documenting the Volumetric Efficiency Gating (DEP-6) boundary contract details.
  - [v2-restructure/CROSS_LAB_DEPENDENCIES.md](file:///C:/Users/muto/claude/4DApp/4DLab/v2-restructure/CROSS_LAB_DEPENDENCIES.md): Update the status of `DEP-6` to show the OBD half is done.
  - [obdlab/tasks/PROGRESS.md](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/obdlab/tasks/PROGRESS.md): Update `T-OBDV2-2` status to done and list the file changes and follow-ups.
- **Bound Details:** A Volumetric Efficiency (VE) fault verdict (`ve_validity ∈ {FAULT_VE_IDLE_COLLAPSE, FAULT_MAF_CONTAMINATION, FAULT_VE_SENSOR_SKEW}`) counts as independent sensor-diagnosis evidence *only* when `air_metering_strategy == DUAL_MAF_MAP_CROSSCHECK`. Under single-sensor configurations (`MAP_ONLY_SPEED_DENSITY` or `MAF_ONLY`), the channel is circular and the consumer (`T-COMV2-VE-GATE-1`) must suppress VE-based verdicts and route to the **P0068 rationality cross-check (MAF/MAP/TPS) + IAC/idle-MAP** fallback.
- **Emitter-only stance:** OBDLab emits only the raw signals and provenance; no verdict or classification is performed within `compute_ve`.

## VERIFICATION GATE

- [x] Confirmed OBDLab already emits all required gating signals:
  - `air_metering_strategy` on [dna_view.py](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/obdlab/obdlab/schemas/dna_view.py#L69).
  - `maf_status`, `map_status`, `ve_pct`, `ve_validity` on [payload.py](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/obdlab/obdlab/schemas/payload.py#L77-L90).
- [x] Confirmed emitter-discipline compliance:
  - Zero references to `FaultFamily`, `fault_family`, `ve_verdict`, or `sensor_fault` in [ve_engine.py](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/obdlab/obdlab/core/ve_engine.py).
- [x] Local test suite ran clean:
  - Ruff linting checks passed.
  - Pyright static typing checks passed with `0 errors, 0 warnings`.
  - Pytest runs for `obdlab` and `comlab` are completely green.
    - `obdlab`: `373 passed, 6 skipped in 0.54s`
    - `comlab`: `336 passed, 6 skipped in 1.44s`

## CODE REVIEW

- **Contract Registration:** The `T-COMV2-VE-GATE-1` consumer row in [comlab/tasks/PROGRESS.md](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/comlab/tasks/PROGRESS.md) is updated.
- **Boundary Contract updated:** The boundary rules for `DEP-6` (VE-as-evidence gate) are frozen into the `SEMANTIC_CONTRACT.md` copies, ensuring the Stage 4 consumer implementation matches this pinned specification.
- **No functional code changes:** Verified that no source files under `obdlab/obdlab/**` were modified (confirming clean division of responsibilities between emitter and consumer).
