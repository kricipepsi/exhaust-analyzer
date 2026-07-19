# T-GV2-10 — O2-Sensor-Bias Calibration Consumer (`upstream_o2_type`)

### Goal ###

Wire the orphan DNA field `upstream_o2_type` (`GASLab/gaslab/dna_view.py` L34 —
read in **0** code paths today) to its wiki-named consumer (§1.4 L84:
"calibrates sensor-bias signatures"): calibrate the `O2_SENSOR_BIASED_LOW` /
`O2_SENSOR_BIASED_HIGH` signature gates by sensor type (narrowband vs
wideband/UEGO), per `GAS_WIKI §7.14` / §7.15.

`family_map.py` L42-43 already classes both as `sensor_fault`; this task makes
the **detection** sensor-type-aware.

### Steps ###

1. Add `upstream_o2_type` calibration to the `O2_SENSOR_BIASED_*` discrimination
   (`resolution.py` / `rule_engine.py`): the sensor type adjusts the
   bias-detection bounds (a wideband/UEGO reports differently from a narrowband
   switching sensor). The coder **pins the exact bounds from §7.14/§7.15** in
   scope confirmation and cites them inline (`# wiki:
   docs/GASLab/wikiNEW/GAS_WIKI.md §7.14`). **Do not invent numbers.**
2. Tests per criteria.

### Success criteria ###

- `test_o2_bias_calibrated_by_sensor_type` — the same reading classifies as
  `O2_SENSOR_BIASED_*` for one sensor type but not another, per §7.14/§7.15.
- `test_o2_bias_default_when_type_absent`.
- All existing GASLab tests pass.

### Files to touch ###

- `GASLab/gaslab/resolution.py` **or** `rule_engine.py` (MODIFY — coder pins)
- `GASLab/tests/test_rule_engine.py` (MODIFY)

### Signal/noise consumer ###

`upstream_o2_type` → `O2_SENSOR_BIASED_LOW`/`_HIGH` calibration (`family_map`
`sensor_fault`; §7.14/§7.15). **Anti-orphan gate:** `grep upstream_o2_type` must
show a live read after this task.

### Out of scope ###

- Timing / lean / catalyst / oil families. No new field or enum value.
