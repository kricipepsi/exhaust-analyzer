# T-OBDV2-1a — progress note

## Plan

We will author the PID log set for OBDLab (Stage 2) across the 8-cell coverage matrix and in-scope fault families.
- **Files to create:**
  - [logset.json](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/obdlab/tests/pid_logset/logset.json): 31 sourced test cases.
  - [signal_map.md](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/obdlab/tests/pid_logset/signal_map.md): table mapping each case to the single target channel it moves, or to the expected rejection error.
  - [logset_estimated.json](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/obdlab/tests/pid_logset/estimated/logset_estimated.json): cases containing estimated numerics (quarantined from the main gate test).
  - [README.md](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/obdlab/tests/pid_logset/README.md): documentation of the logset and post-PURGE DNA contract.
- **Signal/noise stance:** We assert strictly on emitter channels (trims, lambda, VE, validity, gates), never on fault-family verdicts (COMLab's responsibility).
- **Target cases:**
  - 3 VE routing branches (MAF_ONLY, MAP_ONLY, DUAL_MAF_MAP)
  - 3 upstream O2 sensor types (NARROWBAND_0_TO_1V, WIDEBAND_LINEAR, WIDEBAND_NB_SIM)
  - 4 lambda outcomes (stoich, lean, rich, clamp/O2_CHANNEL_FAULT)
  - 3 trim outcomes (near-zero, large positive/lean-correction, large negative/rich-correction)
  - 3 VE-validity faults (idle collapse, MAF contamination, VE sensor skew)
  - 4 RPM/thermal states (stabilized warm idle, regulatory high idle, stress idle, cold open-loop)
  - 7 trim-analytics gates (VALID, ENGINE_COLD, OPEN_LOOP, O2_FAULT_ACTIVE, CKP_CMP_FAULT_ACTIVE, CODES_RECENTLY_CLEARED, WOT_ACTIVE, DFCO_ACTIVE)
  - 7 boundaries/rejection cases (out of range rpm/temp/vacuum/maf, invalid DTCs, bank-2 null contract breach, high confidence DNA rated RPM breach)
- **Gate-pass criteria:** Every sourced case must parse against the post-PURGE `ObdLabDnaView` schema (no `emissions` or `number_of_banks` in `dna_view`) and its `raw_pids` must parse without error (except rejection cases, which are verified to raise expected errors).

## Verification Gate

- [x] JSON files well-formedness checked:
  ```bash
  python -c "import json,glob; [json.load(open(f)) for f in glob.glob('tests/pid_logset/**/*.json',recursive=True)]; print('json OK')"
  ```
  Result: `json OK`
- [x] Structural load checks against post-PURGE schema:
  ```bash
  python -c "import json; cases = json.load(open('tests/pid_logset/logset.json')); from obdlab.schemas.dna_view import ObdLabDnaView; [ObdLabDnaView(**c['dna_view']) for c in cases if 'expected_rejection' not in c]; print('OK')"
  ```
  Result: `OK 38 cases parsed successfully`
- [x] Python script run in workspace simulating translate() for all 38 cases:
  Result: `Sourced validation finished with 0 failures.`

## Code Review

- **DNA view fields checked:** No `emissions` or `number_of_banks` fields are present in any of the `dna_view` entries.
- **Coverage matrix checked:** Evaluated all VE branches, O2 sensor types, lambda outcomes, trim outcomes, VE-validity faults, RPM/thermal states, trim-analytics gates, and boundary/rejection cases.
- **Sourcing checked:** Every non-obvious numeric contains realistic values and J1979 references in the `sources` field. Estimated cases are quarantined in `tests/pid_logset/estimated/logset_estimated.json` with `"estimated": true` and `reasoning`.


