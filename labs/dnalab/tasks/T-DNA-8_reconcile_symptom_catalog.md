# T-DNA-8 — Reconcile symptom catalog to the revised 18-pair set (close T-DNA-1 gap)

### Why this exists ###

The 2026-06-11 doc-audit found that T-DNA-1 is marked `done` and its progress note
claims "YAML has 6 tier_1 categories and 18 total pairs", but the **live**
`symptomlab/data/allowed_combinations.yaml` is **17 pairs** (mtime 2026-05-22, never
edited): `visible_exhaust_smoke` lists only `black_smoke`, `blue_oily` — missing the
third entry and still using the legacy `blue_oily` string.

`SymptomValidator.__init__` hard-requires exactly 18 pairs, so the live catalog raises a
`ValueError` at construction. Because `symptomlab.resolve()` and
`dnalab.build_vehicle_dna()` both build a validator, the whole symptom path is broken
against the live file — and now that **T-DNA-2 landed `load_state`** (a required
`validate()` arg + a required `EnvironmentalConditions` field), every SymptomLab and
DNALab test that constructs the validator is affected.

This is a stale-ledger + unmet-deliverable condition. T-DNA-8 reconciles the live
catalog to the T-DNA-1 revised spec and re-verifies the invariant end-to-end.

### Verify first (the task may be a no-op reconcile) ###

```bash
cd $HOME/mnt/4DLab/labs/symptomlab
grep -c "^    - " symptomlab/data/allowed_combinations.yaml     # expect 18; live shows 17
sed -n '/visible_exhaust_smoke:/,$p' symptomlab/data/allowed_combinations.yaml
```

If the live file is already the revised 18-pair set, T-DNA-8 reduces to a ledger
reconcile: confirm, record in the progress note, and move on. If it is 17/legacy (as the
audit found), complete it below.

### Target — the T-DNA-1 revised `visible_exhaust_smoke` block ###

```yaml
  visible_exhaust_smoke:
    - black_smoke
    - blue_oily_smell      # was blue_oily (REWORD)
    - white_sweet_smell    # ADD (missing third pair)
```

The other five tier_1 categories already match the revised T-DNA-1 catalog
(`prolonged_crank_hard_start`, `surging_hunting_idle`, `stalls_on_cold_start`,
`hesitation_throttle_tip_in`, `knock_pinging_under_load`, `intermittent_random_cutout`
are present). Only `visible_exhaust_smoke` is short.

### Named signal/noise consumer ###

COMLab `fault_atlas_router` symptom→family prior — **proposal COMLab-A** (already
registered by T-DNA-1 in `comlab/comlab/config/proposals/entries.yaml` with 18 mappings).
The two reworked strings (`blue_oily_smell`, `white_sweet_smell`) must match the keys in
COMLab-A's mapping exactly: if COMLab-A already names them, the catalog catches up to it;
if COMLab-A also carries the legacy `blue_oily`, fix both sides so the anti-orphan
set-equality (`YAML pairs == COMLab-A keys`) holds at 18.

### Success criteria ###

- `allowed_combinations.yaml` holds the revised **18** pairs; `grep -c "^    - "` == 18.
- `SymptomValidator(Path('symptomlab/data/allowed_combinations.yaml'))` constructs without
  raising (18-pair invariant passes).
- `symptomlab.resolve("visible_exhaust_smoke", "white_sweet_smell", occurs_during=...,
  engine_state=..., load_state=...)` returns a valid `SymptomDNA` (confirms the new pair
  and the T-DNA-2 `load_state` arg coexist).
- `tests/test_validator.py` / `test_models.py`: the two reworked pairs validate; the
  dropped legacy `blue_oily` now raises `SymptomValidationError`.
- Anti-orphan: live YAML pairs == COMLab-A proposal keys as sets (18 == 18). If COMLab-A
  needs a key rename, draft it in the progress note for COMLab sign-off (do not edit
  COMLab routing code).
- `labs/vinlab/VehicleDNA.md` triage diagram shows `blue_oily_smell` / `white_sweet_smell`
  (the contract-declared §4.2 enum source) — update if it still shows legacy strings.
- Inner loop clean on every edited file: `ruff` → `pyright` → `pytest -x -q`, run from
  the symptomlab root. Then re-run the DNALab suite (it constructs the validator
  transitively): `cd ../dnalab && pytest tests -x -q`.

### Ledger-integrity step (mandatory) ###

T-DNA-1 is `done` but its deliverable was unmet on the live file. In the T-DNA-8 progress
note, record the discrepancy (T-DNA-1 note claimed 18 pairs; live file was 17, mtime
2026-05-22) and the reconciliation. Do **not** retro-edit the T-DNA-1 note. Leave
T-DNA-1 `done` only if T-DNA-8 brings the live file to the state T-DNA-1 contracted;
T-DNA-8's `done` is what certifies the 18-pair catalog is actually live.

### Files to touch ###

- `labs/symptomlab/symptomlab/data/allowed_combinations.yaml` (MODIFY — to 18 pairs)
- `labs/symptomlab/tests/test_validator.py`, `tests/test_models.py` (MODIFY — assert the
  two reworked pairs; assert legacy `blue_oily` rejects)
- `labs/vinlab/VehicleDNA.md` (MODIFY — mapping diagram only, if still legacy)
- `labs/comlab/comlab/config/proposals/entries.yaml` (ADJUST COMLab-A keys only if they
  carry the legacy string — config registration, no COMLab code)

### Out of scope ###

The COMLab routing implementation (COMLab-A code), the prior probability numbers, the
`load_state` axis itself (T-DNA-2, already landed), and any new symptom such as
`oil_consumption` (→ T-DNA-9, deferred). Do not touch `models.py` field shapes — this is
a catalog-string + test reconcile only.

### On completion ###

Both gates clean in `progress_notes/T-DNA-8.md`; flip T-DNA-8 → `done`. This unblocks the
symptom path for T-DNA-7's round-trip gate. Then STOP — one task per session.

### Verification ###

```bash
cd $HOME/mnt/4DLab/labs/symptomlab
ruff check symptomlab/ && pyright symptomlab/
python3.14 -c "from symptomlab.validator import SymptomValidator; from pathlib import Path; SymptomValidator(Path('symptomlab/data/allowed_combinations.yaml')); print('18-pair invariant OK')"
pytest tests/ -x -q --tb=short
grep -c "^    - " symptomlab/data/allowed_combinations.yaml   # must print 18
cd ../dnalab && pytest tests -x -q --tb=short                 # transitive validator build
```
