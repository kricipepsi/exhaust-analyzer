# T-OIL-1 — Add `oil_consumption` 7th tier_1 + 3 tier_2 markers (validator cap 18→21)

Pack: `planning/oil_consumption/` (see START_HERE + PROGRESS).
Supersedes the deferred `T-DNA-9` row in `labs/dnalab/tasks/PROGRESS.md`.
Owner decision (2026-06-12): **Option A** — a 7th first-class `tier_1` category, raising
the catalog invariant to 21 pairs (clean 7×3 grid), *not* a tier_2 under an existing
category.

### Why this exists ###

`oil_consumption` is one of the most common petrol-engine complaints and the operator-
facing entry point for the five oil-burning fault cases in the dossier
(`planning/OilburnCases.md`, P_NEW_09…13). The live symptom catalog
(`symptomlab/data/allowed_combinations.yaml`) has **6** tier_1 categories × 3 tier_2 = 18
pairs and **no** oil-consumption category. The three new markers are the operator
presentations that let COMLab's symptom prior bias toward the oil fault-families before
gas chemistry confirms which one.

### Scope confirmation (1 paragraph) ###

Add one tier_1 (`oil_consumption`) with exactly three tier_2 markers to
`allowed_combinations.yaml`; bump the validator's pair-count invariant from 18 to 21 and
every "18" literal that travels with it (validator guard + message, the test class/assert,
the YAML fixtures); add the three markers as routing keys so they have a live consumer.
**Files:** `symptomlab/data/allowed_combinations.yaml`, `symptomlab/validator.py`,
`tests/unit/test_validator.py`, `tests/fixtures/allowed_combinations.good18.yaml`
(→ `good21`), `tests/conftest.py` (fixture path), and the COMLab proposal/prior config
(consumer). **Signal/noise consumer:** COMLab `fault_atlas_router` Phase-5 symptom prior —
the marker→family rows in `symptom_prior.yaml`, registered via proposal COMLab-A. **No
new schema field on `SymptomDNA`** — `tier_1`/`tier_2` are open-vocabulary `str`, so this
is a catalog + invariant change, not a model change.

### Target — the new `oil_consumption` block ###

Append to `combinations:` in `allowed_combinations.yaml`:

```yaml
  oil_consumption:
    - blue_smoke_on_cold_start_clears   # valve-stem seals: cold-start cloud that clears on driving (P_NEW_10)
    - blue_smoke_under_acceleration     # piston rings / turbo seal: worsens under load (P_NEW_09, P_NEW_13)
    - oil_loss_no_visible_smoke         # PCV stuck-open / slow consumption: oil loss without obvious smoke (P_NEW_11)
```

Marker rationale (operator-observable, maps to the dossier's distinguishing tests):

```
 cold-start cloud, clears        -> valve-stem seals   (HC high at L1, cleans up at L2)
 blue smoke worse on accel       -> piston rings/turbo (HC/CO worsen L1->L2)
 oil disappears, little/no smoke -> PCV stuck-open      (rich L1, drops at L2) / turbo post-cat
```

Head-gasket (P_NEW_12) is **already covered** by the existing
`visible_exhaust_smoke.white_sweet_smell` marker → "Engine Mechanical (Head Gasket)";
do **not** add an oil_consumption marker for it.

### Validator change (the cap) ###

`symptomlab/validator.py` currently hard-checks `len(self._allowed) != 18`. Change the
literal to **21** and update the error string ("must define exactly 21 pairs"). The
invariant is a **pair count**, not a per-category count — 7×3 = 21 keeps it clean.

```
- if len(self._allowed) != 18:
+ if len(self._allowed) != 21:   # 7 tier_1 × 3 tier_2 — oil_consumption added (T-OIL-1)
```

### Named signal/noise consumer (mandatory) ###

A marker that no code reads is an orphan. These three markers become live consumers via
**two** registrations, both in this task's diff (the consumer ships *with* the field, per
the v2-rework default):

1. **Proposal COMLab-A extension** — `labs/comlab/comlab/config/proposals/entries.yaml`:
   add three `oil_consumption.*` rows with their `fault_family` targets (Piston Rings,
   Valve Stem Seals, PCV/Crankcase — the last two reuse/extend existing families; see pack
   PROGRESS "Named cross-lab consumers"). Config registration only — **no COMLab code.**
2. **Symptom-prior rows** — `labs/comlab/comlab/config/symptom_prior.yaml`: the live table
   read by `fault_atlas_router.execute_triage_loop` Phase 5. The marker→family rows here
   are the **code path** that reads the vocabulary (`csv_symptom in self._prior_table`).

> If the owner prefers the COMLab config to land in the COMLab session (T-OIL-4) rather
> than this symptomlab diff, this task still names the consumer and code path (above), so
> the field is **forward-registered**, not orphaned — acceptable under the Stage-4
> anti-orphan rule. State which split is used in the progress note.

### Success criteria ###

- `allowed_combinations.yaml` holds **21** pairs (7 categories × 3); `grep -c "^    - "` == 21.
- `SymptomValidator(Path('symptomlab/data/allowed_combinations.yaml'))` constructs without
  raising (21-pair invariant passes).
- `symptomlab.resolve("oil_consumption", "blue_smoke_on_cold_start_clears",
  occurs_during=..., engine_state=..., load_state=...)` returns a valid `SymptomDNA`.
- An invalid pair under the new category (e.g. `("oil_consumption", "black_smoke")`) raises
  `SymptomValidationError` with the "Valid tier_2 for 'oil_consumption'" message.
- `tests/unit/test_validator.py`: the `TestAll18Combinations` class + `match="exactly 18
  pairs"` assertion are updated to 21; good fixture renamed `good21`; bad fixture still
  rejects (wrong count). `tests/conftest.py` fixture path updated.
- Anti-orphan: each of the 3 markers appears as a key in **either** `symptom_prior.yaml`
  **or** COMLab-A `entries.yaml` (named consumer); confirm by grep before flipping `done`.
- Inner loop clean on every edited file: `ruff` → `pyright` → `pytest -x -q` from the
  symptomlab root, then re-run the DNALab suite (it builds the validator transitively):
  `cd ../dnalab && pytest tests -x -q`.

### Files to touch ###

- `labs/symptomlab/symptomlab/data/allowed_combinations.yaml` (MODIFY — +oil_consumption block, 18→21)
- `labs/symptomlab/symptomlab/validator.py` (MODIFY — invariant 18→21 + message)
- `labs/symptomlab/tests/unit/test_validator.py` (MODIFY — count 18→21, class/assert text)
- `labs/symptomlab/tests/fixtures/allowed_combinations.good18.yaml` (RENAME → `good21.yaml`, +3 pairs)
- `labs/symptomlab/tests/conftest.py` (MODIFY — fixture path good18→good21)
- `labs/comlab/comlab/config/proposals/entries.yaml` (ADJUST — COMLab-A +3 marker rows) *or defer to T-OIL-4 (state which)*
- `labs/comlab/comlab/config/symptom_prior.yaml` (ADJUST — +3 marker→family rows) *or defer to T-OIL-4*

### Out of scope ###

The 2 new GASLab signatures (T-OIL-2), the 5 KG fault nodes + new families (T-OIL-3), the
routing rules / delta discriminator / turbo perception trigger (T-OIL-4), and the doc/wiki
refresh (T-OIL-5). Do **not** touch `models.py` field shapes. Do **not** retire the
existing `visible_exhaust_smoke.blue_oily_smell` here (overlap decision is U-OIL-1).

### Ledger-integrity step (mandatory) ###

This task supersedes the deferred `T-DNA-9`. In `progress_notes/T-OIL-1.md` note that
T-DNA-9's symptom add is delivered here under Option A. Leave the cross-referenced
T-DNA-9 row as-is (history); the pack PROGRESS is now authoritative for the symptom add.

### Verification ###

```bash
cd $HOME/mnt/4DLab/labs/symptomlab
ruff check symptomlab/ && pyright symptomlab/
python3.14 -c "from symptomlab.validator import SymptomValidator; from pathlib import Path; SymptomValidator(Path('symptomlab/data/allowed_combinations.yaml')); print('21-pair invariant OK')"
pytest tests/ -x -q --tb=short
grep -c "^    - " symptomlab/data/allowed_combinations.yaml   # must print 21
# anti-orphan: each new marker must be read somewhere live
for m in blue_smoke_on_cold_start_clears blue_smoke_under_acceleration oil_loss_no_visible_smoke; do
  grep -rq "$m" ../comlab/comlab/config/ && echo "$m: consumer OK" || echo "$m: ORPHAN"; done
cd ../dnalab && pytest tests -x -q --tb=short                 # transitive validator build
```

### On completion ###

Both VERIFICATION GATE and CODE REVIEW blocks clean in `progress_notes/T-OIL-1.md`; flip
T-OIL-1 → `done` in the pack PROGRESS. Then STOP — one task per session. T-OIL-2…5 each
need their own architect authoring pass first (see pack START_HERE §3).
