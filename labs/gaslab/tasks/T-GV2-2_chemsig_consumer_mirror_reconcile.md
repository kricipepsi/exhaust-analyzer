# T-GV2-2 — Mirror the 34-value `ChemicalSignature` into COMLab (consumer side)

### Goal ###

Bring COMLab's local mirror of `ChemicalSignature` up to the same 34-value
surface GASLab now emits (after T-GV2-1), so the GASLab → COMLab JSON boundary
round-trips the three `CAM_TIMING_*` states and rejects nothing GASLab can now
produce. Retire `WRONG_VALVE_TIMING` from the COMLab mirror, add the three
`CAM_TIMING_*` values, and correct the two stale count docstrings (28 and 31) to
34. Done when COMLab's `ChemicalSignature` has 34 members identical to GASLab's,
the registry consistency guard passes, and the COMLab suite is green.

### Success criteria ###

Tests-first:

- `COMLab/tests/e2e/test_kg_registry_consistency.py::TestChemicalSignatureGuard`
  passes with the new value set (`valid = {m.value for m in ChemicalSignature}`
  now includes the three `CAM_TIMING_*` and excludes `WRONG_VALVE_TIMING`); no
  registry `gas_lab_state` is left unregistered.
- A contract-parity check (add to the same e2e file): the COMLab
  `ChemicalSignature` value set equals the GASLab-emitted set as documented in
  `docs/GASLab/wikiNEW/GAS_VOCABULARY.md §3` (34 values, names verbatim).
- `COMLab/tests/e2e/test_diagnostic_engine.py` and
  `COMLab/tests/fixtures/mock_gas_lab.py` — WVT fixtures updated to a
  `CAM_TIMING_*` state; full COMLab suite green before and after.
- Inner loop clean on every edited file.

### Context ###

T-GV2-1 made GASLab emit `CAM_TIMING_RETARDED_MAP` / `CAM_TIMING_RETARDED_MAF` /
`CAM_TIMING_ADVANCED` and stop emitting `WRONG_VALVE_TIMING`. Until this task
lands, the wire is intentionally divergent — COMLab's mirror
(`comlab/schemas/vocabulary.py:276`) still has `WRONG_VALVE_TIMING` and lacks the
three new values, so a real `CAM_TIMING_*` payload would fail the consistency
guard / ingestion. This task closes that gap. Per `no-cross-lab-imports`, COMLab
declares the enum **locally** (mirror), it does not import GASLab — keep it that
way; copy the 34 names verbatim from `GAS_VOCABULARY §3`, do not import.

The two stale docstrings are the "28"/"31" half of the original three-way drift:
`comlab/schemas/ingestion.py:166` ("28-value canonical fault label") and
`comlab/schemas/vocabulary.py:241` ("31 canonical chemical fingerprints"). Both
become 34. These are *count* corrections in docstrings, not new schema fields, so
they carry no signal/noise obligation of their own.

**Named signal/noise consumer:** the three `CAM_TIMING_*` values are consumed by
the registry consistency guard (`valid = {m.value for m in ChemicalSignature}`)
and by fault-atlas routing on `chemical_state` (same `"cam_timing"` family the
retired value used). Both code paths pre-exist — this is a value re-point, not a
net-new field.

**Load skills:** COMLab's mandatory inner-loop / verification / code-review
skills (`COMLab/_comlab_skills/_INDEX.md` — load `comlab-python`,
`comlab-verification-loop`, `comlab-code-review`), plus `comlab-vocabulary`
**only because this task edits `vocabulary.py` enum values**. Do not load the
rest of the COMLab bundle.

### Deliverables ###

1. `COMLab/comlab/schemas/vocabulary.py` — `ChemicalSignature`: remove
   `WRONG_VALVE_TIMING`; add the three `CAM_TIMING_*` members (same order as
   `GAS_VOCABULARY §3`); fix the class docstring "31 canonical…" → "34 canonical…";
   keep the existing per-member inline comments style.
2. `COMLab/comlab/schemas/ingestion.py` — line ~166 docstring "28-value
   canonical fault label" → "34-value canonical fault label (ChemicalSignature)".
3. `COMLab/tests/e2e/test_kg_registry_consistency.py` — extend the guard /
   add the GASLab-parity assertion (34 values, no `WRONG_VALVE_TIMING`).
4. `COMLab/tests/e2e/test_diagnostic_engine.py`,
   `COMLab/tests/fixtures/mock_gas_lab.py` — update WVT fixtures to a
   `CAM_TIMING_*` state.

### Files to touch ###

- `COMLab/comlab/schemas/vocabulary.py` (MODIFY)
- `COMLab/comlab/schemas/ingestion.py` (MODIFY)
- `COMLab/tests/e2e/test_kg_registry_consistency.py` (MODIFY)
- `COMLab/tests/e2e/test_diagnostic_engine.py` (MODIFY)
- `COMLab/tests/fixtures/mock_gas_lab.py` (MODIFY)

### Out of scope ###

Does **not** touch `registry/schema_v2.py` (FU-1 — registry owns its own ledger;
reconcile there as a REG-V2 row, coordinated after this task so the guard's
registry/enum sets agree). Does **not** edit `COMLab/docs/wiki/OBD_VOCABULARY.md
§17` (FU-2 — doc-sync owned; it is still 32-value upstream and the wiki flags the
mirror update as pending). Does **not** add fault-atlas *rules* for the new
states beyond what already routes the `"cam_timing"` family — the values inherit
the existing family route. No new fields, no confidence layer. Surgical-change
rule applies: adjacent issues → "Unplanned follow-ups".

### Verification ###

```bash
cd /sessions/<vm>/mnt/4DLab/COMLab   # or C:\Users\muto\claude\4DApp\4DLab\COMLab on Windows
# (restore sandbox Python 3.14 first — see 4DLab/CLAUDE.md § Sandbox Python)

# Inner loop
ruff check comlab/schemas/vocabulary.py comlab/schemas/ingestion.py
pyright comlab/schemas/vocabulary.py comlab/schemas/ingestion.py

# Structural / parity checks
python3.14 -c "from comlab.schemas.vocabulary import ChemicalSignature as C; vals={m.value for m in C}; assert len(C)==34, len(C); assert 'WRONG_VALVE_TIMING' not in vals; assert {'CAM_TIMING_RETARDED_MAP','CAM_TIMING_RETARDED_MAF','CAM_TIMING_ADVANCED'} <= vals; print('mirror OK', len(C))"
grep -n "28-value\|31 canonical\|WRONG_VALVE_TIMING" comlab/schemas/   # expect: none live

# Functional / test checks
pytest tests/ -x -q --tb=short
# the registry consistency guard specifically:
pytest tests/e2e/test_kg_registry_consistency.py -q
```

All steps must pass. If the registry guard fails because `registry/schema_v2.py`
still lists `WRONG_VALVE_TIMING` (FU-1), STOP and coordinate the registry row —
do not edit registry from this task.

### Progress hook ###

`PROGRESS.md` `T-GV2-2`: Status=done, Files changed={COUNT},
Verification="COMLab mirror 34-value, parity with GASLab; docstrings 28/31→34; guard + N COMLab tests green".
