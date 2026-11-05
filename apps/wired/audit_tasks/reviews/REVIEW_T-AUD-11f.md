# REVIEW T-AUD-11f — ACCEPT, score 94 (Windows Cowork, 2026-11-05 22:27 CET)

Facts first: commit `42327ec` on `fix/T-AUD-11f` (after spec `3d84b0d`) changes only
`audit/drift/2026-11-05_DRIFT_REPORT_obdlab.md`. Cowork re-run of `check_report.py`: `sections 8/8, findings 33,
refs ok 63/63`, `REPORT OK` (exit 0). Porcelain: note and RESULT only. Headless run 21:14:08-21:21:22 UTC, exit 0.
Docs row: no second-model review.

## Findings re-derived (33, none rejected)
Checked by Cowork:
- Frozen engine: `sensor_signal_translator.py:149-151` sets `normalized_lambda = None` ("no made-up λ"); PRD:207,
  HLD:106, LLD:303, BDD:48 say 1.0; PRD:127 and DLD:172 type the field as plain `float` (`payload.py:74` allows None).
- `ve_engine.py:95` raises a bare `ValueError`, while `core/exceptions.py:4` defines `ObdLabError` and ADR-0005 /
  PRD:107 promise the one family. **A code defect against the lab's own contract.**
- `HIGH_IDLE_LOAD` occurs once in `obdlab/`: the YAML note `obd_translation_rules.yaml:40` "Supersedes former …".
  True against the token-scan criterion (PRD, HLD, LLD, DLD, BDD: 6 bullets), but a one-word comment fix.
- Cold cutoff 75 °C (`semantic_consistency_checker.py:21`, YAML `value: 75.0`) vs VOCAB:151, 748 at 70 °C. Note:
  T-AUD-4h set the registry's freeze-frame trim cutoff at 70 °C, so the app now holds two cutoffs.
- README:4 "masking": `grep -rniE mask labs/obdlab/obdlab` is empty.
- `composition.py:572-573` falls back to `MAP_ONLY_SPEED_DENSITY` when the VIN gives no strategy (HLD:52 undocumented).
- The rest (VOCAB ranges, enum members, `fuel_trim_invalid`, euro switch, `ObdEmissionsView` still defined, the
  `iat or 25.0` defaults, `freeze_frame_pids` never filled by the composition) rest on their quoted lines or ABSENT commands.

## Drift groups (for the fix row)
1. Frozen-λ wording 1.0 → None, and the `float | None` type (PRD, HLD, LLD, DLD, BDD).
2. **Code:** `ve_engine.py:95` `ValueError` → an `ObdLabError` subclass (ADR-0005).
3. **Ruling:** the cold cutoff, 70 or 75 °C, across OBDLab and the registry freeze-frame rule (T-AUD-4h).
4. **Ruling:** silent defaults (`iat or 25.0`, translator 0.0 fills) vs the wiki-citation and degraded-mode rules.
5. Composition facts: `freeze_frame_pids` never populated; MAP_ONLY fallback; Mode $06 and trim pass-through fields.
6. Vocabulary: euro switch, `fuel_trim_invalid`, `O2_CHANNEL_FAULT`, VE and trim ranges, STRESS_IDLE band, ECT bands.
7. Small: the YAML comment token; `ObdEmissionsView` still defined; README masking.

## Score
100 − 3 (six bullets for one comment token inflate the count) − 3 (`## Time` one phase) = 94.

## Follow-up
T-AUD-17 (OBDLab docs drift fixes, plus the `ValueError` code fix); rulings first on groups 3 and 4.

Measured: OBDLab (129 KB docs, 2,055 code lines) → 33 findings in 7 min on Sonnet medium.
