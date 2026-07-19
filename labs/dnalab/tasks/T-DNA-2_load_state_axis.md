# T-DNA-2 — Add `load_state` environmental axis

### Goal ###

Add a third environmental axis, `load_state`, to `SymptomDNA.environmental_conditions`
(`docs/research/DNAresearch.md` §"Expanding Environmental Context Axes" + §"Conclusions"
rec 1). The two legacy axes (`occurs_during`, `engine_state`) capture thermal/temporal
behaviour but not mechanical load. `load_state` lets the engine separate static
air-metering faults (prominent at idle, high manifold vacuum) from transient load
failures (ignition coil dielectric breakdown under acceleration, low vacuum).

Values (transcribe verbatim): `idle`, `steady_cruise`, `transient_acceleration`,
`coasting_deceleration`. Source: SAE J2944 (cited in research).

### Named signal/noise consumer ###

COMLab context-modifier prior (**proposal COMLab-B**). The research §"Context-Modifier
Shifts" table uses `load_state` to promote/demote fault families (e.g.
`transient_acceleration` → promote ignition-coil + fuel-pump, demote minor vacuum
leak). COMLab-B also enforces the **65% trust-ceiling cap** on the symptom prior
(research §"Real-World Rates…": ~35% misleading-report floor). Register `load_state`
in `proposals/entries.yaml` naming the context-modifier code path; the axis and its
COMLab-B consumer ship as a pair.

### Success criteria ###

- New `LoadState(StrEnum)` in `symptomlab/models.py` with the four values.
- `EnvironmentalConditions` gains `load_state: LoadState`; `to_json()` emits it;
  `SymptomDNA.from_json()` parses it. Deserialization of a payload **missing**
  `load_state` is handled deterministically (default `idle` with a documented reason,
  or raise) — pick one and cover it with a test; this couples to the schema_version
  bump in T-DNA-7.
- `SymptomValidator.validate()` accepts a `load_state` arg and raises
  `SymptomValidationError` on an out-of-vocabulary value.
- `tests/test_models.py` / `test_validator.py` / `test_symptomdna_from_json.py`
  cover round-trip, validation, and the missing-field path.
- Proposal COMLab-B entry exists naming the context-modifier consumer + the 65% cap.
- Draft `SEMANTIC_CONTRACT.md` §4.2 amendment in the progress note (the
  `environmental_conditions` block gains `load_state`) — flagged for COMLab sign-off.
- Inner loop clean on every edited file.

### Files to touch ###

- `labs/symptomlab/symptomlab/models.py` (MODIFY — `LoadState`, `EnvironmentalConditions`)
- `labs/symptomlab/symptomlab/validator.py` (MODIFY — accept/validate `load_state`)
- `labs/symptomlab/tests/` (MODIFY — the three test modules above)
- `labs/comlab/comlab/config/proposals/entries.yaml` (ADD proposal COMLab-B)

### Out of scope ###

The context-modifier weights and the 65% cap arithmetic (COMLab-B owns them). The
`dnalab` assembly wiring that passes `load_state` from triage → that is T-DNA-7. The
symptom catalog strings (T-DNA-1).

### On completion ###

Both gates clean in `progress_notes/T-DNA-2.md`; flip T-DNA-2 → `done`. STOP.

### Verification ###

```bash
cd $HOME/mnt/4DLab/labs/symptomlab
ruff check symptomlab/ && pyright symptomlab/
pytest tests/ -x -q --tb=short
grep -rn "load_state" symptomlab/   # defined in models + read in validator (not only defined)
```
