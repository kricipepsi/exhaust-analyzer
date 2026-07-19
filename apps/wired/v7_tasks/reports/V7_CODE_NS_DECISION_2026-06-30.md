# V7_CODE_NS_DECISION — canonical `fault_code` contract (F-V7-CODE-NS)

**Task:** [[T-V7-7]] · **Author:** GLM (omp coder, READ-ONLY) · **Date:** 2026-06-30
**Status:** Memo delivered — **recommendation awaiting owner sign-off.** No source/oracle/wiki
edited by this task.

---

## TL;DR — recommendation

**Option B: the v2 short `rule_id` (e.g. `MF-001`) is the intended public verdict
`fault_code`. The v7 oracle column is over-qualified; re-pin
`expected_fault_code` from `ERR-MF-001` → `MF-001` (named-fault rows only).**

- **Zero engine change.** The live default path already emits short ids.
- **Zero consumer impact.** No live reader of `diagnostic_verdict.fault_code`
  depends on the `ERR-` prefix (enumerated below).
- **Safe:** the 73 v2 `rule_id`s are globally unique across all families
  (collision check: 0 duplicates); the `ERR-` prefix is cosmetic on the v2 path.
- **One caveat that gates the fix:** `ERR-ABORT-00x` fatal-gate codes are a
  *separate* id space (Stage-A aborts, emitted on **both** v1 and v2 paths) and
  are **already `ERR-`-prefixed** in the engine. The oracle's `ERR-ABORT-*` rows
  for fatal-incomplete cases are correct as-pinned and must NOT be re-pinned. The
  eventual fix splits the oracle column by verdict class: short for named faults,
  `ERR-ABORT-*` kept for aborts.

---

## 1. The two coexisting id conventions (the root cause)

The engine gates `fault_code` form on `USE_V2_REGISTRY` (resolved in
`comlab/core/lab_pipeline_aggregator.py:120-121`; constructor flag at
`fault_atlas_router.py:580`):

| Path | Gate | `fault_code` source | Form | KG used? |
|---|---|---|---|---|
| **v2 (DEFAULT, `USE_V2_REGISTRY=1`)** | `route()` L1898-2080 | `rule.rule_id` (`integration_shim.py:788`) | **short** `MF-001` | **No** — passthrough-default enrichment (shim L822+) |
| v1 (`USE_V2_REGISTRY=0`) | `route()` L2130-2208 | `winner.fault_id` (`global_fault_registry.json`) | `ERR-MF-001` | Yes — `FaultAtlasKG.resolve()` |

**The T-V7-5 run (`20260630_163900`) used the v2 default** → emitted short ids
(`MF-001`, `LC-001`, `CF-001`, `RM-001`, `SF-002`, `NF-001`, `SF-001`, `LC-002`,
`EF-004`, `CT-007`, `CT-008`, `MF-002`) plus `ERR-ABORT-001` (14 fatal-gate
aborts) and `OPTIMAL_HEALTH` (no-fault). The oracle (T-V7-3) pinned the `ERR-`
KG form for named faults → 294/294 `fault_code` FAIL.

> **Note on the START_HERE claim.** `WIRED_V7_START_HERE.md` states "There is no
> `use_v2_registry` arg." That is incorrect against the live engine — the arg
> exists and the v2 path is the default. The v7 suite nonetheless treats the v2
> default as *the* engine contract (the v1 path exists only as T-V7-9's runnable
> proxy), so the START_HERE intent — "score the v2 default" — holds; only the
> wording is loose. This memo does not edit the START_HERE.

## 2. The short→`ERR-` resolution path: does it exist? (Success criterion 3)

**No.** There is no short→`ERR-` resolution anywhere on the v2 path:

- `FaultAtlasKG.resolve()` (`comlab/core/fault_atlas_kg.py:58-82`) keys on
  `ERR-` ids; its `_ALIAS_MAP` (L32-36) maps only **`ERR-`→`ERR-`** legacy
  aliases (`ERR-E1-M032→ERR-LC-005`, `ERR-E2-I104→ERR-MF-001`,
  `ERR-E3-F501→ERR-RM-005`). No short→`ERR-` entry.
- The v2 shim never calls `kg.resolve()`. It returns its own passthrough-default
  `fault_enrichment` (`integration_shim.py:822-834`: `component_group="engine"`,
  empty `impacted_subsystems`, generic remediation) and the router reconstructs
  the full `OrchestratorFinalUIOutput(**v2_output)` at `fault_atlas_router.py:2080`
  — bypassing `LabPipelineAggregator._stage_c_enrich()` entirely.
- `_stage_c_enrich(fault_code)` (`lab_pipeline_aggregator.py:142-164`, which
  calls `self._kg.resolve(fault_code)`) is reached **only** on the v1 path and
  the `fault_code=` test-hook override path — never on the live v2 verdict path.

**Consequence for the decision:** Option A (engine emits `ERR-`) is *not*
"surface an already-resolved id" — it is **build new resolution + change the
verdict contract for every v2 consumer**. Option B (oracle emits short) is a
one-column CSV edit with zero engine change.

## 3. Short-id uniqueness across families (Success criterion 2)

73 v2 rules in `registry/rules/*.json`. Collision check (all `rule_id`s):

```
total rule_ids : 73
duplicates     : []   (0)
family prefixes: LC×3 NF×2 CT×8 EF×5 OV×4 NS×4 RM×4 CS×2 EL×3 IF×3
                 MW×9 SF×8 II×2 VL×3 CF×7 MF×6
```

Family-coded prefixes make the short ids **globally unique**, not just
"unique within the family" as `SCHEMA_V2_SPEC.md:79` minimally promises. Option
B is unambiguous: every `MF-001` maps to exactly one fault. The `ERR-` prefix is
cosmetic on the v2 path (the KG it indexes is not consumed there).

`OPTIMAL_HEALTH` (no-fault) and `ERR-ABORT-00x` (fatal gates) are separate id
spaces (see §4) and are already consistent engine↔oracle.

## 4. Consumer-surface enumeration (Success criterion 1)

Every reader of `diagnostic_verdict.fault_code`, with the id form each expects:

| Consumer | Location | Expects | Re-pin impact (short oracle) |
|---|---|---|---|
| **v7 scorer** | `run_suite.py:158` (`actual_code.lower()==expected_code.lower()`) | compares engine↔oracle | **FIXED** — currently 294/294 FAIL because oracle=`ERR-`, engine=short; re-pin→short makes them match |
| **wired composition** | `apps/wired/wired/composition.py` forwards `diagnostic_verdict` to UI unchanged; does not parse the id form | indifferent | none |
| **UI verdict card** | PRD §5.2 (`COMLab_PRD.md:262`) — "small, monospace, for service-record cross-reference" | no prefix mandated | none (short is a valid service-record ref) |
| COMLab Stage-C enrichment (v1 path) | `lab_pipeline_aggregator.py:150` `self._kg.resolve(fault_code)` | `ERR-` (v1 only) | none — not reached on v2 path |
| Engine v1-path tests | `tests/e2e/test_real_routing.py`, `test_diagnostic_engine.py`, `test_pipeline_round_trip.py` (all `use_v2_registry=False`) | `ERR-EL-001`, `ERR-CF-001`, `ERR-MW-001`, … | none — engine tests, not suite tests; gated on v1 path |
| Engine v2-path / registry tests | `registry/tests/test_oil_live_verdicts.py`, `test_pcv_rule.py`, `test_turbo_rule.py`, `test_integration_shim.py` | **short** `MW-001`, `MW-008`, `MW-009`, `CS-002`, `MW-SYN-1` | none — already assert short; re-pin aligns the suite with them |
| Delta-router wiring tests | `tests/e2e/test_delta_router_wiring.py` | **both** forms, path-gated (L279-280 `ERR-`; L294/324/352/386/402 short) | none |
| Regression fixtures | `tests/fixtures/descriptor.py:162`, `tests/regression/test_comlab_regression.py:53,74` | echo engine output verbatim (`expected_top_fault = actual...fault_code`) | none — self-echo, form-agnostic |
| Fatal-gate aborts | `lab_pipeline_aggregator.py:282` (`fault_code=abort.error_code`); codes `ERR-ABORT-001/002/004/005` (`:329-358`) | **`ERR-ABORT-*`** on BOTH paths | **none — keep `ERR-ABORT-*` in oracle** (see §5 caveat) |

**No live consumer depends on the `ERR-` prefix for named-fault verdicts.** The
only `ERR-`-form readers are (a) v1-path-only engine internals and (b) the
fatal-gate abort codes, which are a separate id space the fix must preserve.

## 5. The abort-code caveat (gates the fix task)

`ERR-ABORT-00x` is **not** a v1/v2 convention split — it is the Stage-A fatal-gate
abort code, emitted by `LabPipelineAggregator` *before* routing, on **both**
paths (`lab_pipeline_aggregator.py:282`, `:329-358`). The run emitted
`ERR-ABORT-001` (14 cases). The oracle's `ERR-ABORT-*` rows for the
fatal-incomplete cases (`CASE-043`, `RULE-NOx-1`, `YAML-PDF_HI_007` and any
`expected_fault_code=ERR-ABORT-*` rows) are **already correct** — engine and
oracle agree.

**Therefore the eventual fix task must split the oracle re-pin by verdict class:**
- named-fault rows: `ERR-MF-001` → `MF-001` (re-pin to short)
- abort rows: `ERR-ABORT-001` → keep `ERR-ABORT-001` (do NOT re-pin)
- no-fault rows: `OPTIMAL_HEALTH` → keep (already consistent)

A blanket `s/^ERR-//` on `expected_fault_code` would corrupt the abort rows and
re-introduce a FAIL. The fix task's verification must assert the abort rows are
unchanged.

## 6. Decision — Option B (oracle-side re-pin)

**Recommendation:** Re-pin the v7 oracle `expected_fault_code` to the short
`rule_id` form for **named-fault rows only**, preserving `ERR-ABORT-*` abort
rows and `OPTIMAL_HEALTH` no-fault rows. This makes the v7 suite a faithful v2
ruler: it scores the contract the default engine actually emits.

**Why not Option A (engine resolves to `ERR-`):**
- It requires *building* a short→`ERR-` resolution (none exists today, §2) and
  re-wiring the v2 verdict to surface the resolved id — a contract change for
  **every** v2 consumer, not a one-line fix.
- It would diverge the v2 verdict from the v2 registry's own schema-canonical
  `rule_id` (`SCHEMA_V2_SPEC.md:79`) — the very id the registry tests already
  assert. The v2 registry is the designated replacement ("v1 is frozen; v2
  replaces it at cutover", per `REG-V2-AUTHOR-*.md`).
- It would also require re-wiring KG enrichment onto the v2 path (currently
  passthrough-default) to make the `ERR-` keys meaningful — a larger, separate
  piece of work.

**Exact file+symbol the eventual fix task would touch (Option B):**
- `apps/wired/v7/data/cases_petrol_v7.csv` — column `expected_fault_code`:
  strip the `ERR-` prefix on **named-fault rows only** (leave `ERR-ABORT-*` and
  `OPTIMAL_HEALTH` rows untouched).
- `apps/wired/v7_tasks/reports/ORACLE_TRIAGE_2026-06-30.md` — update the
  pinned-form note from "canonical `ERR-`" to "v2 short `rule_id` (named faults)
  / `ERR-ABORT-*` (aborts) / `OPTIMAL_HEALTH` (no-fault)".
- No engine, KG, registry, wiki, or test edit. (This memo recommends; it does
  not implement — READ-ONLY.)

## 7. Separate defect surfaced (not in scope — for the architect to triage)

The v2 path returns **passthrough-default `fault_enrichment`** and never consults
the KG (`integration_shim.py:822-834`; router `:2080`). So the curated
`component_group` / `impacted_subsystems` / `ui_remediation_steps` /
`differential_siblings` from `config/kg/*.json` are **orphaned on the v2 path**
— the verdict card gets `component_group="engine"`, empty subsystems, generic
remediation. This is a real enrichment-quality defect, but it is **separate**
from the fault_code namespace and does **not** gate the accuracy %. Suggest the
architect log it as `F-V7-ENRICH-ORPHAN` rather than folding it into the
`F-V7-CODE-NS` fix.

---

## Evidence index (grep/file citations)

- Verdict construction, v2 path: `comlab/core/fault_atlas_router.py:1898-2080`
  (delegates to shim; returns `OrchestratorFinalUIOutput(**v2_output)` at L2080)
- Verdict construction, v1 path: `comlab/core/fault_atlas_router.py:2130-2208`
  (`fault_id = winner.fault_id` L2131; `fault_code=fault_id` L2201)
- Shim emits short: `registry/integration_shim.py:788` (`"fault_code": rule.rule_id`)
- Shim passthrough enrichment: `registry/integration_shim.py:822-834`
- KG resolve (ERR- keyed, no short→ERR-): `comlab/core/fault_atlas_kg.py:58-82`,
  alias map L32-36
- v1/v2 gate: `comlab/core/lab_pipeline_aggregator.py:120-121`; router flag
  `fault_atlas_router.py:580`
- Registry rule_ids (73, 0 dups): `registry/rules/*.json`
- KG node keys (108, all `ERR-`): `comlab/config/kg/*.json`
- v1 registry fault_ids (104, all `ERR-`): `comlab/config/global_fault_registry.json`
- Fatal-gate abort codes: `lab_pipeline_aggregator.py:282,329-358`
  (`ERR-ABORT-001/002/004/005`)
- v7 scorer equality: `apps/wired/v7/run_suite.py:158`
- Run JSON (emitted short + `ERR-ABORT-001`):
  `apps/wired/v7/runs/20260630_163900/results.json`
- Schema doc: `registry/docs/SCHEMA_V2_SPEC.md:79` (`rule_id` canonical)
- PRD consumer: `labs/comlab/docs/COMLab_PRD.md:262`
