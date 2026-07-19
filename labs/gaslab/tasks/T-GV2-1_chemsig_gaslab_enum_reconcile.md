# T-GV2-1 — Reconcile GASLab `ChemicalSignature` to the v2 wiki (34-value), emitter side

### Goal ###

Bring the GASLab-emitted `ChemicalSignature` contract up to the v2 wiki's
**34-value** surface by retiring `WRONG_VALVE_TIMING` and minting the three
system-specific cam-timing states `CAM_TIMING_RETARDED_MAP`,
`CAM_TIMING_RETARDED_MAF`, and `CAM_TIMING_ADVANCED`, then rebinding the single
`wrong_valve_timing_rule` so the rule engine emits the correct one of the three
per the v2 fault atlas. Done when `gaslab.contracts.ChemicalSignature` has
exactly 34 members matching `GAS_VOCABULARY §3`, no member or string named
`WRONG_VALVE_TIMING` remains in `gaslab/` (outside an intentional retirement
comment), and the GASLab test suite is green.

### Success criteria ###

Tests-first. Write these failing, then make them pass:

- `tests/test_contracts.py::test_chemical_signature_is_34_value` — asserts
  `len(ChemicalSignature) == 34`, `"WRONG_VALVE_TIMING" not in {m.value for m in
  ChemicalSignature}`, and the three `CAM_TIMING_*` values are present.
- `tests/unit/test_rule_engine_reachability.py` — the cam-timing rule path is
  reachable and emits a `CAM_TIMING_*` value (not `WRONG_VALVE_TIMING`); all
  34 signatures remain reachable from the synthetic grid + edge probes.
- `tests/test_rule_engine.py` and `tests/test_validators.py` — existing WVT
  assertions updated to the new states; whole GASLab suite green before and
  after.
- Inner loop clean on every edited file: `ruff` → `pyright` → `pytest`.

### Context ###

The `ChemicalSignature` contract disagrees with itself across three artefacts —
**32** in GASLab code, **34** in the v2 wiki, **28**/**31** in COMLab's stale
mirror docstrings. The user has ruled (GASLabV2 kickoff) that **the v2 wiki is
canonical** and code reconciles *up to* it. This task fixes the **emitter**
(GASLab); T-GV2-2 fixes the consumers. This is the blocker that must clear
before any v2 payload-shape / confidence-layer work.

The exact 32 → 34 delta is authored in
`docs/GASLab/wikiNEW/CHANGE_v2.1_timing_taxonomy.md`: `WRONG_VALVE_TIMING` is
retired and replaced by three states. The full 34-member enum (with order — the
order is normative for stable JSON round-trips) is in
`docs/GASLab/wikiNEW/GAS_VOCABULARY.md §3`; the three new fault records and their
idle + 2500-RPM 5-gas vectors are in
`docs/GASLab/wikiNEW/06b_fault_atlas_valvetrain_egr_combustion.md` (the WVT
record is replaced by the three `CAM_TIMING_*` records). The rule rebind uses the
**gas-direction discriminator the wiki already specifies** (Speed-Density / MAP →
rich branch; MAF → lean branch; advanced → both) — transcribe the gas vectors
**verbatim** from 06B; do not invent thresholds.

**Named signal/noise consumer (required to ship these values):**
`gaslab/family_map.py::SIGNATURE_TO_FAMILY` already routes the retired
`WRONG_VALVE_TIMING → "cam_timing"`; each of the three new states routes to the
same `"cam_timing"` family, which COMLab fault-atlas routing consumes via
`chemical_state` (06B). This is a *re-pointing* of an existing routed value, not
a net-new orphan field — the consumer and code path both pre-exist.

**Match class:** per `CHANGE_v2.1_timing_taxonomy.md`, the three states are
`match_class: SPECIFIC` (not DEFINITIVE) — tailpipe gas cannot prove cam phase;
that needs CKP/CMP correlation downstream. Preserve that classification.
**DNA gate:** `none` on all three (no MAF-vs-MAP DNA field exists; inventing one
would violate signal/noise). The MAP/MAF split rides the gas-direction
discriminator, not a DNA gate.

**Load skills:** `gaslab-python`, `gaslab-verification-loop`,
`gaslab-code-review` (mandatory), `gaslab-wiki-provenance` (enum + rule edits).
Optionally `graphify-lookup` if you need the §-to-§ map for 06B. Do **not** load
the rest of the bundle.

### Deliverables ###

1. `GASLab/gaslab/contracts.py` — `ChemicalSignature`: remove
   `WRONG_VALVE_TIMING`; add the three `CAM_TIMING_*` members in the position
   `GAS_VOCABULARY §3` lists them (between `POA_SIGNATURE` and `EGR_STUCK_CLOSED`);
   update the class docstring count to 34; cite `# vocab: GAS_VOCABULARY §3`.
2. `GASLab/gaslab/family_map.py` — replace the `WRONG_VALVE_TIMING: "cam_timing"`
   row with three rows mapping each `CAM_TIMING_*` → `"cam_timing"`, each citing
   its 06B / GAS_WIKI §7 anchor.
3. `GASLab/gaslab/rule_engine.py` — rebind the `wrong_valve_timing_rule` branch
   (lines ~213–218) to emit the correct `CAM_TIMING_*` via the 06B gas-direction
   discriminator instead of `WRONG_VALVE_TIMING`.
4. `GASLab/gaslab/data/gas_lab_ontology.yaml` — replace the
   `wrong_valve_timing_rule` grammar block and the `WRONG_VALVE_TIMING:` fault
   record (~line 422) with the three cam-timing rule/record entries; gas vectors
   transcribed verbatim from 06B; citations updated.
5. `GASLab/tests/test_contracts.py` — add `test_chemical_signature_is_34_value`.
6. `GASLab/tests/test_rule_engine.py`, `GASLab/tests/test_validators.py`,
   `GASLab/tests/unit/test_rule_engine_reachability.py` — update WVT fixtures and
   assertions to the three new states; keep full-suite green.

### Files to touch ###

- `GASLab/gaslab/contracts.py` (MODIFY)
- `GASLab/gaslab/family_map.py` (MODIFY)
- `GASLab/gaslab/rule_engine.py` (MODIFY)
- `GASLab/gaslab/data/gas_lab_ontology.yaml` (MODIFY)
- `GASLab/tests/test_contracts.py` (MODIFY/CREATE test)
- `GASLab/tests/test_rule_engine.py` (MODIFY)
- `GASLab/tests/test_validators.py` (MODIFY)
- `GASLab/tests/unit/test_rule_engine_reachability.py` (MODIFY)

### Out of scope ###

This task does **not** touch any consumer of the wire value — COMLab
`vocabulary.py` / `ingestion.py`, COMLab tests, or `registry/schema_v2.py`. Those
are T-GV2-2 and FU-1. It does **not** edit any wiki/doc under `docs/GASLab/` or
`COMLab/docs/wiki/OBD_VOCABULARY.md §17` (FU-2, doc-sync owned). It does **not**
rename the `RULE_WVT` rule id / `wrong_valve_timing_rule` key beyond what is
needed to emit the new states if a rename would ripple into consumers — if a
clean in-place rebind is possible, prefer it and note any deferred rename as an
Unplanned follow-up. No new DNA field. No confidence/uncertainty layer (that is
post-reconciliation v2 work). Surgical-change rule: every changed line traces to
a Deliverable above; adjacent improvements go to `PROGRESS.md`
"Unplanned follow-ups", not into this diff.

### Verification ###

```bash
cd /sessions/<vm>/mnt/4DLab/GASLab   # or C:\Users\muto\claude\4DApp\4DLab\GASLab on Windows
# (restore sandbox Python 3.14 first — see 4DLab/CLAUDE.md § Sandbox Python)

# Inner loop on each edited file
ruff check gaslab/contracts.py gaslab/family_map.py gaslab/rule_engine.py
pyright gaslab/contracts.py gaslab/family_map.py gaslab/rule_engine.py

# Structural checks
python3.14 -c "from gaslab.contracts import ChemicalSignature as C; vals={m.value for m in C}; assert len(C)==34, len(C); assert 'WRONG_VALVE_TIMING' not in vals; assert {'CAM_TIMING_RETARDED_MAP','CAM_TIMING_RETARDED_MAF','CAM_TIMING_ADVANCED'} <= vals; print('enum OK', len(C))"
grep -rn "WRONG_VALVE_TIMING" gaslab/ | grep -v "# retired"   # expect: no live references
python3.14 -c "import yaml,sys; d=yaml.safe_load(open('gaslab/data/gas_lab_ontology.yaml')); assert 'WRONG_VALVE_TIMING' not in d.get('faults',{}), 'stale fault record'"

# Functional / test checks
pytest tests/ -x -q --tb=short
```

All steps must pass. Confirm (FU-3) via the graph that no DTC/KG node still
routes *to* `WRONG_VALVE_TIMING` before deleting its record.

### Progress hook ###

`PROGRESS.md` `T-GV2-1`: Status=done, Files changed={COUNT},
Verification="ChemicalSignature 34-value; WVT retired → 3× CAM_TIMING_*; N GASLab tests green".
