# REG-V2-AUTHOR-ignition_fault — author the v2-registry rule for spark-generation failure

**Authored:** 2026-06-21 (architect, Cowork). **Stage:** 4 (COMLab / registry). **Type:** v2-registry rule authoring (diagnostic content). **Status:** **deferred — does NOT block `T-COMV2-DELTA-2`.**
**Origin:** the `ignition_fault` gap surfaced in `REGISTRY_REVIVAL_AUDIT_2026-06-20.md` — `ignition_fault` is the only fault family with an **empty** v2 rule file (`T-REG-REVIVE-1` deletes that empty stub). The family is fully live elsewhere (KG, schema, corpus, e2e via the v1/KG path); this task gives the **v2 registry** its missing rule so the v2 path can diagnose it too.
**Drill:** boot order → `tasks/COMLAB_PYTHON_ENV_SETUP.md` → this file → scope-confirm before code.
**Load skills:** this task works inside `registry/`, so load the **registry** bundle — `registry/docs/_registry_skills/registry-python`, `registry/docs/_registry_skills/registry-verification-loop`, `registry/docs/_registry_skills/registry-code-review` (per `registry/docs/_registry_skills/_INDEX.md`) — at session start before any code, not the `_comlab_skills/` trio.

> **One-line scope:** create `registry/rules/ignition_fault.json` (RuleSet, ≥3 competing rules) for **spark-generation failure, pre-combustion** (`vocabulary.py:234, lld §3.1`), add `"ignition_fault.json"` to `_EXPECTED_RULE_FILES`, and prove it against the 3 curated cases that currently mispredict. Mirror the structure of `registry/rules/misfire.json` and the existing `REG-V2-AUTHOR-*` pattern.

## ⚠ Domain decision required (bring thresholds to the owner)

The rule *shape* is specced below, but the **numeric evidence thresholds** (HC ppm, O₂ %, trim %, which DTC ranges count) are a domain call. Propose values in the scope-confirm with a `wiki_ref` for each, and get owner sign-off before finalising — do not invent bare magic numbers (house rule: every numeric literal carries a `# wiki:`/`wiki_ref` citation).

## The discrimination problem (why this rule must exist)

`ignition_fault` = the spark **hardware** failing (coil / driver / secondary / CKP), distinct from `misfire` = the combustion event missing. The system separates them **by DTC**: P035x (coil) → ignition_fault; P030x (misfire) → misfire. The live e2e proves the target behaviour:

```
IGNITION_MISFIRE chemistry + P0351 (coil driver) + short_term_ft1 = +20  →  ERR-IF-001 (ignition_fault)
   (uses P0351 not P030x so the misfire family is excluded by the DTC gate)
```

Two boundaries the rules must respect (signal/noise):
- **vs misfire:** `misfire.json` already has IGNITION_MISFIRE-gated rules — do NOT cannibalise misfire cases. Gate ignition_fault rules on the **coil/CKP DTC families** (P0351–P0358, P0335–P0340), and use `competition_group` so they compete cleanly.
- **vs rich_mixture / no_fault:** the 3 validation cases below currently mispredict as `rich_mixture`/`no_fault`. The new rule must **out-compete** those for exactly those cases — that is the success signal.

## KG nodes to cover (the family catalogue — `comlab/config/kg/ignition_fault.json`, codes ERR-IF-001..007)

`ignition_coil_driver_fault` · `ignition_coil_secondary_breakdown` · `ignition_weak_spark_partial_combustion` · `ignition_switch_voltage_drop` · `ckp_sensor_intermittent_dropout` · `ignition_failure_no_combustion_no_start` (boundary with `non_starter`) · `ignition_fault_intermittent_not_active`.

## Deliverables

1. **`registry/rules/ignition_fault.json`** (CREATE) — RuleSet with ≥3 rules, e.g.:
   - **IF-001 coil-driver fault** — `IGNITION_MISFIRE` DEFINITIVE + coil DTC (P0351–P0358) SUGGESTIVE + positive STFT OBD evidence → `ERR-IF-001`. Must reproduce the e2e.
   - **IF-002 weak spark / secondary breakdown** — `IGNITION_MISFIRE` DEFINITIVE + high-HC OBD evidence, **no** coil DTC required (partial-combustion signature) → `ERR-IF-002`/`-005`.
   - **IF-003 CKP intermittent dropout** — CKP DTC (P0335–P0340) SUGGESTIVE + intermittent pattern → `ERR-IF-006`; coordinate the no-combustion/no-start node with the `non_starter` family so they don't both fire.
   - Add a `SAMPLE_INVALID` GATING rule if any validation case needs it.
   Each rule: unique `rule_id`, `competition_group: "ignition_fault"`, `base_weight`, `passes_cases` listing real curated IDs, `wiki_ref` on every threshold. Mirror `misfire.json` field-for-field.
2. **Add `"ignition_fault.json"` to `_EXPECTED_RULE_FILES`** in `registry/integration_shim.py` (so prod loads it; keeps manifest == `rules/` glob — the assertion `T-REG-REVIVE-1` adds).
3. **`registry/tests/test_ignition_fault_rules.py`** (CREATE) — validates the RuleSet against `schema_v2.RuleSet`, asserts `IGNITION_MISFIRE` DEFINITIVE present, coil-DTC evidence present, and case-ID resolution; follow `test_lean_condition_rules.py`.

## Success criteria (done = all)

- `registry/rules/ignition_fault.json` parses, validates against `schema_v2.RuleSet`, ≥3 unique `rule_id`s.
- `"ignition_fault.json"` in `_EXPECTED_RULE_FILES`; the REVIVE-1 manifest==glob assertion still passes.
- The **3 validation cases flip to `ignition_fault`** on the v2 path: `EXP-N026`, `CASE-035`, `case_036` (today → `rich_mixture`/`no_fault`). These are the named consumer for this rule.
- The live e2e `tests/e2e/test_diagnostic_engine.py::test_e2e_ignition_fault_coil_driver` (ERR-IF-001) still passes; `misfire` cases unaffected (no cannibalisation).
- Mandated interpreter: `ruff` clean · `pyright --pythonpath $PY` clean · `pytest tests/ registry/tests/ -q` → `0 failed`.
- `VERIFICATION GATE` + `CODE REVIEW` in `progress_notes/REG-V2-AUTHOR-ignition_fault.md`; flip ledger row → `done`.

## Out of scope

- Any other fault family (each has its own `REG-V2-AUTHOR-*`).
- DELTA-2 / delta wiring; KG, schema, or enum changes (the family already exists — author the **rule** only).
- Corpus rebuild / graphify.
