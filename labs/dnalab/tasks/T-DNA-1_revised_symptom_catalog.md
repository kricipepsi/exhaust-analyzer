# T-DNA-1 — Revised symptom catalog (6×3 reworked pairs)

### Goal ###

Replace the legacy 18-pair symptom catalog with the research-revised catalog
(`docs/research/DNAresearch.md` §"Revised Driveability Symptom Catalog" + §"Symptom
Questionnaire Changelog"). Two tier_1 categories are renamed and several tier_2
sub-filters are reworked; the catalog stays **exactly 18 pairs** (6 tier_1 × 3
tier_2), so the validator's hard invariant holds.

The rework removes dimensional overlap: legacy tier_2 values that duplicated the
`occurs_during` axis (`cold_engine_only`, `hot_engine_only`, `only_when_hot`) and the
load axis (`only_high_rpm_highway`, `right_after_fillup`) are dropped, and gaps
(surging idle, prolonged crank, tip-in hesitation, knock, backfire) are filled.

### Revised catalog — transcribe verbatim ###

```yaml
combinations:
  vehicle_starting_issues:       # was vehicle_wont_start
    - no_crank_silent
    - fast_crank_whining
    - prolonged_crank_hard_start # was normal_crank_zero_rpm (REWORD)
  rough_idle_shudder:
    - constant_vibration_shudder # was constant_shudder (REWORD)
    - surging_hunting_idle        # ADD
    - stalls_on_cold_start        # ADD
  lack_of_power_hesitation:
    - flat_sluggish_always
    - hesitation_throttle_tip_in  # ADD
    - sudden_jerk_stumble
  poor_economy_fuel_odor_sound:  # was poor_economy_fuel_odor
    - just_poor_mpg
    - strong_fuel_smell
    - knock_pinging_under_load    # ADD
  engine_dies_or_stalls:
    - when_coasting_to_stop
    - intermittent_random_cutout  # was intermittent_random (REWORD)
    - backfire_loud_pop           # ADD
  visible_exhaust_smoke:
    - black_smoke
    - blue_oily_smell
    - white_sweet_smell
```

Each pair's mapped fault family + rationale + source link is in the research catalog
table — copy them into the proposal entry (below), one row per pair.

### Named signal/noise consumer ###

COMLab `fault_atlas_router` symptom→fault-family prior. The tier_1/tier_2 strings are
the routing keys; the revised strings have **no live consumer yet**, so this ships as
**proposal COMLab-A**: register every (tier_1, tier_2) → fault_family mapping in
`labs/comlab/comlab/config/proposals/entries.yaml` naming the
`fault_atlas_router` code path. The DNA-side vocabulary and the COMLab-A routing map
ship as a pair; until COMLab-A is live the new strings are proposed, not orphaned.

### Success criteria ###

- `allowed_combinations.yaml` holds the revised 18 pairs above; `SymptomValidator`
  still loads and its `len(...) == 18` invariant passes.
- `labs/vinlab/VehicleDNA.md` "Complete Universal Triage & Diagnostic Mapping Diagram"
  (the contract-declared enum source, §4.2) is updated to the revised strings.
- `tests/test_validator.py` / `tests/test_models.py` updated: every revised pair
  validates; every dropped legacy pair now raises `SymptomValidationError`.
- Proposal COMLab-A entry exists with all 18 family mappings + source links.
- Draft `SEMANTIC_CONTRACT.md` §4.2 amendment text in the progress note (the example
  payload uses revised strings) — flagged for COMLab/semantic sign-off, not edited
  unilaterally.
- Inner loop clean on every edited file: `ruff` → `pyright` → `pytest -x -q`.

### Files to touch ###

- `labs/symptomlab/symptomlab/data/allowed_combinations.yaml` (MODIFY)
- `labs/vinlab/VehicleDNA.md` (MODIFY — mapping diagram only)
- `labs/symptomlab/tests/test_validator.py`, `tests/test_models.py` (MODIFY)
- `labs/comlab/comlab/config/proposals/entries.yaml` (ADD proposal COMLab-A — config
  registration only, no COMLab code)

### Out of scope ###

The COMLab routing code (COMLab-A implementation), the prior probability numbers
(research §"Per-Tier 1 Diagnostic Prior Strengths" — COMLab owns those), and
`load_state` (→ T-DNA-2). Do not touch `models.py` field shapes here — strings only.

### On completion ###

Both gates clean in `progress_notes/T-DNA-1.md`; flip T-DNA-1 → `done`. This unblocks
T-DNA-2. Then STOP — one task per session.

### Verification ###

```bash
cd $HOME/mnt/4DLab/labs/symptomlab
ruff check symptomlab/ && pyright symptomlab/
python3.14 -c "from symptomlab.validator import SymptomValidator; from pathlib import Path; SymptomValidator(Path('symptomlab/data/allowed_combinations.yaml'))"  # 18-pair invariant
pytest tests/ -x -q --tb=short
grep -c ":" symptomlab/data/allowed_combinations.yaml   # sanity on pair count
```
