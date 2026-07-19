## Plan

Scope confirm: `ff_fuel_spark_cut_at_crank` is emitted when the §12.1 freeze-frame PIDs show `fuel_system_status == OL_FAULT`, `vehicle_speed_kmh == 0`, and `engine_rpm <= 180`; the RPM boundary is pinned from wiki `10_nonstart_diagnostics.md` §10.3 (immobiliser cranking RPM 150-180, CKP/CMP RPM 0) and the computable fuel-status field comes from `DTC_VOCABULARY.md` §12.1/§12.3. This is a raw discriminator only, not a verdict. The CAN-era monitor-aborted gate is `EuroEmissionCategory` in `{EURO_4, EURO_5, EURO_6, EURO_7}`; wiki §10.1 places CAN/security in 2000-2010, while OBDLab Q6/Q8 says portable Mode $06 MID/TID is CAN/2008+ and pre-CAN is per-OEM, so `{EURO_1, EURO_2, EURO_3, UNKNOWN}` and absent DNA use the normal margin path. Named consumer remains COMLab `T-COMV2-NOSTART-1`, `comlab/comlab/core/fault_atlas_router.py` no-start branch, keyed on `MONITOR_ABORTED` plus `ff_fuel_spark_cut_at_crank`.

Implementation checklist:

- [x] Add `Mode06MonitorState.MONITOR_ABORTED`.
- [x] Gate `evaluate_monitor(..., monitor_incomplete=True)` to CAN-era `MID_A1_TID_53` only.
- [x] Add and compute `ff_fuel_spark_cut_at_crank`.
- [x] Add unit coverage for aborted classification, CAN gate, regression margin path, and FF-cut true/false.
- [x] Run verification gate.
- [x] Complete code review notes and update `tasks/PROGRESS.md`.

## VERIFICATION GATE

Commands run from `labs/dtclab` on 2026-06-16:

- `.\.venv\Scripts\ruff.exe check .` -> PASS (`All checks passed!`)
- `.\.venv\Scripts\pyright.exe --pythonpath .\.venv\Scripts\python.exe dtclab/` -> PASS (`0 errors, 0 warnings, 0 informations`)
- `.\.venv\Scripts\pytest.exe -x -q` -> PASS (`589 passed in 5.33s`)

Structural checks:

- `rg -n "MONITOR_ABORTED" dtclab\schemas\vocabulary.py` -> found enum member.
- `rg -n "PASSED|PENDING_FAIL_MARGINAL|CRITICAL_FAIL" dtclab\core\mode06_evaluator.py` -> margin tri-state branch present and unchanged in behavior.
- `rg -n "monitor_incomplete|euro_emission_category" dtclab\core\mode06_evaluator.py` -> evaluator gate present.
- `rg -n "ff_fuel_spark_cut_at_crank" dtclab\schemas\freeze_frame.py dtclab\core\freeze_frame_extractor.py` -> schema + extractor present.
- `rg -ni "security[_-]?lockout|mechanical[_-]?no[_-]?start" dtclab` -> PASS, no DTCLab verdict strings.
- `rg -n "from (gaslab|obdlab|comlab|dnalab)" dtclab` -> PASS, no cross-lab imports.

Note: `ruff`, `pyright`, and `pytest` were not available on PATH initially. Created local `labs/dtclab/.venv` and installed `.[dev]` from `pyproject.toml` to run the declared toolchain. The plain pyright wrapper did not resolve venv dependencies until invoked with `--pythonpath .\.venv\Scripts\python.exe`.

## CODE REVIEW

- Scope stayed emitter-only: DTCLab emits `MONITOR_ABORTED` and `ff_fuel_spark_cut_at_crank`; no security/mechanical no-start verdict is produced.
- `classify_margin` behavior remains the same; the aborted state bypasses it only for `monitor_incomplete=True`, `MID_A1_TID_53`, and CAN-portable `EuroEmissionCategory`.
- Pre-CAN, `UNKNOWN`, absent DNA, non-MID_A1/TID_53, and `monitor_incomplete=False` all take the existing margin path.
- The freeze-frame predicate is intentionally limited to §12.1 computable fields; lack of security-active, battery-voltage, or physical-cranking PIDs is recorded in the plan.
- Post-commit review found Deliverable #3 was incomplete because `ff_fuel_spark_cut_at_crank` had been computed by the extractor without a declared `FreezeFrameRecord` field; `T-DTCV2-NOSTART-1-FIX` closes that gap with the schema declaration and constructed-record round-trip coverage.
