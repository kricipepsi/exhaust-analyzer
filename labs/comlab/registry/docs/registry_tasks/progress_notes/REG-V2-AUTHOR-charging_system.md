# REG-V2-AUTHOR-charging_system — Progress Note

## Summary

Authored 2 rules (CS-001, CS-002) for the new `charging_system` fault family
— the last of three new cvsgaps.md families and the final REG-V2-AUTHOR-*
task before REG-V2-INTEGRATE. Family ships with 2 rules instead of the
initially-planned 3 because `DTC_VOCABULARY §15` does not list the
generator/regulator code range P0620–P0626; the only charging-system DTCs
in the wiki are P0562 (system voltage low) and P0563 (system voltage high).
The dropped CS-002 (alternator regulator) was redesigned: NEW-charging_system-02
was reassigned from "alternator regulator failure" to "overcharging" (P0563)
and covered by CS-001.

CS-002 (the ghost-misfire rule, renumbered from the earlier CS-003 draft) is
the **first rule in the registry to gate on `NORMAL_OPERATION` chemistry**
— a positive evidence-of-absence pattern used to discriminate from
`misfire.json` MF-004. Verified via grep across `registry/rules/*.json`:
chemistry-GATING is widespread (15 instances across 6 rule files), but every
existing use gates on an **anomalous** state. CS-002 is the first
`NORMAL_OPERATION`-as-GATING.

The pattern requires the COMLab router to treat missing chemistry as
"rule does not fire" (hard-absence), not "default to NORMAL" (imputation).
Logged as a verification gate at REG-V2-INTEGRATE; see follow-ups below.

## VERIFICATION GATE — REG-V2-AUTHOR-charging_system

| Phase | Check | Result | Detail |
|---|---|---|---|
| 1 | ruff lint + JSON parse | PASS | `ruff check registry/ --fix` → "All checks passed!"; all 13 JSON rule files parse |
| 2 | pyright | PASS | 0 errors, 0 warnings, 0 informations |
| 3 | unit tests | PASS | 380 passed (was 359 baseline + 21 new charging_system tests) |
| 4 | task verification | PASS | All commands in spec `### Verification ###` block exit 0; `Validated: 2 rules in family charging_system`; `All 3 case refs resolve OK`; `DTCRoutingTag mirror intact: 20 members`; `All DTC codes wiki-grounded: ['P0300', 'P0562', 'P0563']` |
| 5a | rule schema validity | PASS | 60 rules validate across 13 rule files (charging_system added 2) |
| 5b | case-ID resolution | PASS | 189 case refs across all rule files resolve in `corpus_curated.csv` (was 186 + 3 new = 189) |
| 5c | harness side-by-side | N/A | Integration shim does not yet exist — belongs to REG-V2-INTEGRATE |
| 6 | scope check | PASS | Exactly the 4 files in the spec's `### Files to touch ###` modified; no out-of-scope edits; no new lab/COMLab/4DLabWired imports; no new `DTCRoutingTag` enum values |

**Overall: PASS**

## CODE REVIEW — REG-V2-AUTHOR-charging_system

| Section | Item | Result | Note |
|---|---|---|---|
| A | No lab / COMLab / 4DLabWired imports | PASS | New test imports only from `registry.schema_v2`; rule file is JSON data |
| A | No ARCHIVE / v2 / v6 imports | PASS | — |
| A | Rules-as-data discipline | PASS | All rule content in JSON; only new Python is the test file |
| A | No diagnostic logic in Python escape hatches | PASS | `NORMAL_OPERATION` at tier `GATING` is a schema-supported field (`EvidenceTier.GATING` on `ChemistryEvidence`); not a code escape. **First-of-kind use of `NORMAL_OPERATION`-as-GATING** — documented in spec Context; previous 15 chemistry-GATING usages all gate on anomalous states |
| B | Every rule has passes_cases list | PASS | CS-001: 2 cases; CS-002: 1 case |
| B | Every passes_cases ID resolves in corpus_curated.csv | PASS | All 3 refs resolve (Phase 5b) |
| B | Every numeric threshold has wiki citation | PASS | No numeric thresholds in this family — all evidence is DTC-list-based with `wiki_ref: "DTC_VOCABULARY §15"` or chemistry-state-based with `wiki_ref: "GAS_VOCABULARY §3"` |
| B | No invented enum values | PASS | All `ChemistryState` and `EvidenceTier` values match schema_v2.py vocabulary; no `DTCRoutingTag` enum values added (mirror intact at 20 members per `test_no_routing_tag_added`) |
| B | No solo-survivor rules (≥2 competing rules per family) | PASS | 2 rules in `charging_system` competition group; both carry `confidence_ceiling` (CS-001: 0.85; CS-002: 0.75) |
| C | All lines trace to Deliverables | PASS | Each of the 4 modified files corresponds to a numbered Deliverable in the spec |
| C | No scope creep | PASS | `rules/misfire.json` MF-004 unmodified; competition handled entirely on CS-002 side (double-GATING + ceiling 0.75 > MF-004's 0.70). `DTCRoutingTag` unchanged. `OBDEvidence` unchanged (battery_voltage_v deferred per spec Out-of-scope) |
| D | Public functions have tests | PASS | The new file is a JSON rule + test pair; no new public functions in registry tooling |
| D | Every changed rule covered by ≥1 passing case | PASS | CS-001 covers NEW-charging_system-01, NEW-charging_system-02; CS-002 covers NEW-charging_system-03 |

**Blocking findings:** none

**Follow-up rows added to REGISTRY_PROGRESS.md:**
1. `CS-002-router-assumption` — CS-002 NORMAL_OPERATION-GATING assumes router uses hard-absence semantics for missing chemistry. Verify at REG-V2-INTEGRATE.
2. `charging-system-alternator-gap` — Alternator/regulator field-circuit faults (P0620–P0626) not covered: `DTC_VOCABULARY §15` does not list these codes. Requires a wiki-update task before a REG-V2-AUTHOR-charging_system-v2 can ship.

## Design notes

### Why 2 rules instead of 3

First-draft spec proposed 3 rules including a `CS-002` citing
`["P0620", "P0621", "P0622", "P0625", "P0626"]` as generator/regulator
codes. Verification against `DTCLab/docs/wiki/DTC_VOCABULARY.md §15`
(lines 528–531) showed the wiki lists **only** P0562 and P0563 in the
charging cluster (both routed to `ECU_INTERNAL_HISTORY`). P0641–P0643
are documented as sensor-reference voltage, also under
`ECU_INTERNAL_HISTORY`. P0620–P0626 are not in the wiki at all.

Per the registry's "every literal carries a wiki citation" discipline,
shipping a rule citing wiki-uncited DTC codes was not an option. The
alternator rule was dropped; NEW-charging_system-02 was reframed as
overcharging (P0563) and folded into CS-001. The coverage gap is logged
as a follow-up.

### Why no `ELECTRICAL_HISTORY` routing tag

Two reasons, confirmed before spec sign-off:

1. `Rule.dtc_evidence` is a list of `DTCEvidence` objects carrying
   `dtc_codes: list[str]` directly. `DTCRoutingTag` is referenced
   nowhere in `Rule` or its evidence classes; the rules don't consume
   it during evaluation. VL-002 in `rules/vacuum_leak.json` is the
   canonical pattern (raw P-codes with `any_match`, no routing-tag
   indirection).
2. `ECU_INTERNAL_HISTORY` already covers `P0600–P0699` (per
   `DTC_VOCABULARY §15` line 529, which routes P0562/P0563 there).
   Adding `ELECTRICAL_HISTORY` would create two valid routes for the
   same DTC bucket. The only coordinated enum precedent
   (`CYLINDER_FLUID_MISFIRE`) was added via FIX-ENUM-1 with explicit
   COMLab/DTCLab coordination; a unilateral mirror-drift add would
   break the schema_v2.py L7–8 invariant.

### Competition with MF-004 (the discriminator)

MF-004 in `registry/rules/misfire.json`:

- chemistry: `NORMAL_OPERATION` **DEFINITIVE**
- dtc: `P0300–P0304` SUGGESTIVE
- ceiling: 0.70
- GATING entries: zero

CS-002 in this task:

- chemistry: `NORMAL_OPERATION` **GATING**
- dtc: `["P0562", "P0563"]` GATING; `["P0300"]` SUGGESTIVE
- ceiling: 0.75
- GATING entries: two

On NEW-charging_system-03 (P0300 + P0562 + NORMAL chemistry), both fire,
but CS-002 has strictly stronger gating discipline (two GATING entries
vs MF-004's zero) and is one ceiling notch higher. Pinned by
`test_cs_002_ceiling_dominates_mf_004` which reads MF-004's rule_id
explicitly (catches a silent failure if MF-004 is renumbered).

On a real ghost misfire **without** a charging DTC, CS-002 does not
fire (charging-DTC GATING unsatisfied); only MF-004 fires. Clean
separation.

### Ceiling matches OV-002 precedent

CS-001 ships at confidence_ceiling **0.85**. This matches `OV-002` in
`rules/overheating.json` — the same archetype: single specific DTC,
DTC-pathognomonic, single-fault diagnosis. Pinned by
`test_cs_001_ceiling_matches_overheating_precedent`.

### Two precedent-claim mistakes during spec authoring

Two claims in earlier drafts of the spec did not survive `grep`:

1. "MF-001..006 will not fire DEFINITIVE on NORMAL chemistry" — false;
   MF-004 fires DEFINITIVE on NORMAL chemistry by design.
2. "No other rule in the registry uses chemistry as GATING" — false;
   15 instances across 6 files use chemistry-GATING on anomalous states.

Both caught by architect review before any code was written. The
verification-before-claim discipline (`grep` the actual files; quote
the result in the Context section as a table) is the right standing
rule.

## Files touched

| File | Change | Lines |
|---|---|---|
| `registry/rules/charging_system.json` | CREATE | 56 |
| `registry/tests/test_charging_system_rules.py` | CREATE | 287 |
| `registry/corpus_curated.csv` | MODIFY (3 rows) | NEW-charging_system-01/02/03 populated |
| `registry/corpus_meta.json` | MODIFY (3 notes) | NEW-charging_system-01/02/03 notes updated |
| `registry/registry_tasks/REG-V2-AUTHOR-charging_system.md` | CREATE (spec) | per spec-authoring rule |

## Test count

- Before: 359 passing
- After: 380 passing (21 new charging_system tests)
- pyright: 0 errors (unchanged)
- ruff: clean (unchanged)
- Phase 5a: 60 rules validate (was 58 + 2 new)
- Phase 5b: 189 case refs resolve (was 186 + 3 new)
