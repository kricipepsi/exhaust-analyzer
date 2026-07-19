# REG-V2-CHEMSIG-34 — reconcile registry `ChemistryState` to GASLab's 34-value surface (FU-1 / DEP-1)

### Goal ###

Bring the registry's local `ChemistryState` enum up to the same 34-value surface
GASLab now emits, so the registry's chemistry vocabulary matches the emitter and
the COMLab mirror. GASLab split the single `WRONG_VALVE_TIMING` state into three
cam-timing states (`CAM_TIMING_ADVANCED`, `CAM_TIMING_RETARDED_MAF`,
`CAM_TIMING_RETARDED_MAP`); the registry is still at 32 and still carries the
retired `WRONG_VALVE_TIMING`. Drop the retired value, add the three new ones
(verbatim from the GAS contract), re-point every rule that referenced the old
state, and keep the rule-validation + manifest guards green. **Pair-land with
`T-GV2-2`** (the COMLab mirror) so the cross-package consistency guard agrees on
both ends. Done when registry `ChemistryState` has 34 members identical to
GASLab's and the registry suite is green.

### Success criteria ###

Tests-first:

- `schema_v2.ChemistryState` has 34 members; `WRONG_VALVE_TIMING` is absent and
  `{CAM_TIMING_ADVANCED, CAM_TIMING_RETARDED_MAF, CAM_TIMING_RETARDED_MAP}` are
  present, names verbatim from `gaslab/gaslab/contracts.py::ChemicalSignature`
  (= `GAS_VOCABULARY §3`).
- No rule references `WRONG_VALVE_TIMING`; every `cam_timing.json` rule that used
  it resolves to a replacement state, chosen per the GAS split semantics, and its
  `passes_cases` still resolve against the curated corpus.
- The registry rule-load / manifest==glob guard and the chemistry-state validation
  pass (`test_shim_loads_all_*_rule_files`, schema tests). Full registry suite green
  before and after.
- Inner loop clean on every edited file.

### Context ###

`schema_v2.ChemistryState` (`registry/schema_v2.py:35`) lists `WRONG_VALVE_TIMING`
at `:65`. The only rule data referencing it is `registry/rules/cam_timing.json`
(CT-001, `:11`, the non-VVT mechanical base-timing rule — "elevated HC + CO with
depressed CO2", no MAP in the curated corpus). The other cam_timing rules use
`TIMING_RETARDED` / `VVT_FAILURE` / `INCOMPLETE_COMBUSTION`, which are **unchanged**.

The split is owned by the **emitter** — the source of truth for which replacement
state(s) CT-001 maps to is `gaslab/gaslab/contracts.py::ChemicalSignature` +
`GAS_VOCABULARY §3` (the advanced vs retarded and MAF vs MAP air-metering
distinction). **Step 1: read that mapping**, then re-point CT-001 to the
replacement state the corpus cam_timing cases actually carry (with no MAP in the
curated corpus, the retarded case is the MAF-metered variant; advanced is its own
state). If one CT rule must become two (advanced vs retarded) to keep
`passes_cases` resolving, that is in scope — re-point, don't invent unrelated rules.

This is a **value re-point**, not a net-new field — the `cam_timing` family route
pre-exists. Per `no-cross-lab-imports`, the registry declares `ChemistryState`
**locally** (mirror); copy the names verbatim, do not import GASLab.

**Coordination:** the COMLab-side mirror is `T-GV2-2` (COMLab `ChemicalSignature`
32→34). The cross-package consistency guard checks the registry enum set against
the COMLab enum set, so these two must land together — if the guard fails because
one side still lists `WRONG_VALVE_TIMING`, that is the expected interlock, not a
defect: coordinate the pair, do not unilaterally diverge.

Load skills: the registry bundle (`registry/docs/_registry_skills/_INDEX.md` —
`registry-python`, `registry-verification-loop`, `registry-code-review`); env per
`REGISTRY_START_HERE.md`.

### Deliverables ###

1. `registry/schema_v2.py` — `ChemistryState`: remove `WRONG_VALVE_TIMING`; add the
   three `CAM_TIMING_*` members (same order as `GAS_VOCABULARY §3`); update the
   "32" count in the class docstring → 34.
2. `registry/rules/cam_timing.json` — re-point CT-001 (and any other
   `WRONG_VALVE_TIMING` reference) to the replacement state(s) per the GAS split;
   keep `competition_group` and `passes_cases` intact and resolving.
3. `registry/tests/` — extend the schema test for the 34-value set + a parity
   assertion vs the GAS-emitted names; update any cam_timing rule test that pinned
   `WRONG_VALVE_TIMING`.

### Files to touch ###

- `registry/schema_v2.py` (MODIFY)
- `registry/rules/cam_timing.json` (MODIFY)
- `registry/tests/test_schema_v2.py` + `registry/tests/test_cam_timing_rules.py` (MODIFY)
- `registry/docs/REGISTRY_PROGRESS.md` (flip row)
- `registry/docs/registry_tasks/progress_notes/REG-V2-CHEMSIG-34.md` (gates)

### Out of scope ###

Does **not** edit `comlab/schemas/vocabulary.py` (that is `T-GV2-2`, the COMLab
mirror — land as the coordinated pair, not from here). Does **not** edit
`OBD_VOCABULARY.md §17` (FU-2 — doc-sync, separate). Does **not** add new cam_timing
*coverage* beyond re-pointing the existing rule(s) (EXP-N023 stays a logged
follow-up). No new families, no confidence-layer changes. Surgical-change rule:
adjacent issues → Unplanned follow-ups.

### Verification ###

```bash
cd labs/comlab/registry   # env per REGISTRY_START_HERE.md
# Structural / parity
python -c "from registry.schema_v2 import ChemistryState as C; v={m.value for m in C}; assert len(C)==34, len(C); assert 'WRONG_VALVE_TIMING' not in v; assert {'CAM_TIMING_ADVANCED','CAM_TIMING_RETARDED_MAF','CAM_TIMING_RETARDED_MAP'} <= v; print('registry chemsig OK', len(C))"
grep -rnI "WRONG_VALVE_TIMING" registry/schema_v2.py registry/rules/   # expect: none
# Functional
python -m pytest registry/tests/ -q
python -m pytest registry/tests/test_schema_v2.py registry/tests/test_cam_timing_rules.py -q
```

If the cross-package consistency guard fails because the COMLab mirror (`T-GV2-2`)
has not landed, **STOP and coordinate the pair** — do not edit COMLab from here.

### Progress hook ###

`REGISTRY_PROGRESS.md` `REG-V2-CHEMSIG-34`: Status=done, Files changed={COUNT},
Verification="registry ChemistryState 34-value, parity with GASLab; WRONG_VALVE_TIMING re-pointed in cam_timing.json; guard + N registry tests green; paired with T-GV2-2".
