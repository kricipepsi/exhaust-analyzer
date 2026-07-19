# SCHEMA V2 SPEC — 4DLab Registry Rule Schema

**Generated:** 2026-05-27
**Source task:** REG-V2-SCHEMA
**Authoritative model:** `registry/schema_v2.py`
**Audience:** Rule authors (REG-V2-AUTHOR-{family}) and integration engineer (REG-V2-INTEGRATE)

---

## 1. What Changed from v1

The v1 architecture (`COMLab/comlab/config/global_fault_registry.json`) gates every
rule on a single hard-coded `gas_lab_state` field. Only 11 of 32 GASLab chemistry
states appear across 53 rules. The two most common chemistry signatures in failing
traces — `TIMING_RETARDED` (64 curated cases) and `SAMPLE_INVALID` (17 cases) —
have zero matching rules, guaranteeing 100% prune for ~32% of the curated corpus
before evaluation begins (AUDIT-REG §1, CHEMISTRY_COVERAGE §1).

v2 decouples evidence from gating:

| v1 | v2 |
|---|---|
| One chemistry gate key per rule | List of chemistry states, each weighted (Evidence Tier) |
| DTC `REQUIRE_MATCH` / `REQUIRE_DTC` prune | DTC presence is evidence, not a gate |
| OBD constraints as a block | Each PID constraint individually weighted |
| Single-winner scoring | Competition groups — multiple rules fire, highest score wins |
| No confidence bounds | Confidence ceilings enforce "no solo survivor" discipline |
| Rules in one monolithic JSON | One JSON file per fault family under `rules/` |

---

## 2. Evidence Tier Model

Every piece of evidence (chemistry, OBD, DTC) carries exactly one tier. The
router accumulates evidence weights during scoring.

### 2.1 `DEFINITIVE`

Strong signal — alone nearly confirms the fault. A chemistry state that is
pathognomonic for the fault family. Example: `LEAN_MIXTURE` for `lean_condition`.

**Router behaviour:** Full weight multiplier applied. A DEFINITIVE chemistry
match alone can push a rule above the threshold.

### 2.2 `SUGGESTIVE`

Consistent with the fault but not diagnostic alone. Example: `TIMING_RETARDED`
for `lean_condition` — many lean conditions retard timing as a secondary effect,
but retarded timing also appears in cam_timing, catalyst_failure, and ecu_fault.

**Router behaviour:** Partial weight multiplier. A SUGGESTIVE match contributes
additively but cannot carry a rule to threshold on its own.

### 2.3 `GATING`

Must be present for the rule to evaluate at all. This is the v1 prune analogue,
but scoped narrowly. Use sparingly — overuse reproduces v1's prune problem.

**Router behaviour:** If any GATING evidence is absent, the rule is pruned
before scoring. If all GATING evidence is present, the rule proceeds to full
evaluation. GATING evidence does NOT contribute to the score — it only controls
whether the rule fires.

**Authoring rule:** A rule may have at most 1 GATING chemistry evidence item.
GATING on DTCs is discouraged (reproduces v1's DTC-dependence problem) — prefer
SUGGESTIVE DTC evidence combined with chemistry GATING.

---

## 3. Rule Structure

Each rule is a JSON object conforming to the Pydantic `Rule` model in
`schema_v2.py`. One JSON file per fault family under `registry/rules/`.

### 3.1 Required Fields

| Field | Type | Description |
|---|---|---|
| `rule_id` | `str` | Unique within the family, e.g. `"LC-001"` |
| `fault_family` | `FaultFamily` | One of 16 enum values |
| `description` | `str` | One sentence describing what this rule detects |
| `competition_group` | `str` | Rules in the same group compete by score (typically the family name) |
| `passes_cases` | `list[str]` | At least one curated case ID this rule must PASS |
| `base_weight` | `float` (0.0–1.0) | Starting confidence weight; default 0.70 |

### 3.2 Optional Fields

| Field | Type | Description |
|---|---|---|
| `chemistry_evidence` | `list[ChemistryEvidence]` | Chemistry states with evidence tiers |
| `obd_evidence` | `list[OBDEvidence]` | OBD PID constraints with evidence tiers |
| `dtc_evidence` | `list[DTCEvidence]` | DTC patterns with evidence tiers |
| `confidence_ceiling` | `float` (0.0–1.0) or `null` | Max confidence when rule is solo in its competition group |
| `perception_flag` | `str` or `null` | Truth-vs-perception hint, e.g. `"perception_only"` |
| `precondition` | `str` or `null` | Free-text precondition, e.g. `"vvt_equipped: true"` |
| `source_wiki_refs` | `list[str]` | Wiki sources for this rule's thresholds |

### 3.3 ChemistryEvidence

```json
{
  "state": "LEAN_MIXTURE",
  "tier": "DEFINITIVE",
  "wiki_ref": "GAS_VOCABULARY §3"
}
```

| Field | Type | Description |
|---|---|---|
| `state` | `ChemistryState` | One of 34 enum values |
| `tier` | `EvidenceTier` | `DEFINITIVE`, `SUGGESTIVE`, or `GATING` |
| `wiki_ref` | `str` or `null` | Citation for the chemistry→family mapping |

### 3.4 OBDEvidence

```json
{
  "pid": "longft1",
  "operator": "ge",
  "value": 10.0,
  "tier": "SUGGESTIVE",
  "units": "%",
  "wiki_ref": "GAS_VOCABULARY §2"
}
```

Operators: `lt`, `le`, `gt`, `ge`, `eq`, `in_range`.

For `in_range`, provide `range_low` and `range_high` instead of `value`.
Ranges must satisfy `range_low < range_high`.

### 3.5 DTCEvidence

```json
{
  "dtc_codes": ["P0171", "P0174"],
  "strategy": "any_match",
  "tier": "SUGGESTIVE",
  "wiki_ref": "DTC_VOCABULARY §4"
}
```

Strategies:
- `any_match` — at least one DTC in the list is present (default)
- `all_match` — every DTC in the list must be present
- `none_present` — rule gains weight when none of the listed DTCs are present

---

## 4. Competition Groups

A competition group is a named pool of rules that compete by score. The router
scores every rule in the group and selects the highest-scoring rule as the
winner for that group.

**Default:** Each fault family is its own competition group (group name matches
family name). Cross-family competition groups are possible but not needed in the
initial authoring pass.

**Authoring rule:** Every rule in a competition group must differentiate itself
from peers — two rules with identical evidence profiles but different `rule_id`
values is an authoring defect.

---

## 5. Confidence Ceilings (No Solo Survivor)

The "no solo survivor" discipline: if only one rule in a competition group fires
(no competing rule survived gating), the winning rule's confidence is capped at a
documented ceiling. This prevents spurious high-confidence diagnoses from single
rules with no competitive validation.

**Rule:** A fault family file with exactly 1 rule must set `confidence_ceiling`
on that rule. The `RuleSet` model enforces this at validation time (hard error).

**Recommended ceiling:** 0.70 for solo rules. A two-rule family with both rules
firing is always preferred.

**Invariant:** `confidence_ceiling <= base_weight`. A solo rule's ceiling should
never exceed its base weight.

---

## 6. Vocabulary Enums

### 6.1 ChemistryState (34 values)

Mirror of GASLab `ChemicalSignature` enum (`GASLab/gaslab/contracts.py`).
Full list in `schema_v2.py:35-73`. Key states referenced in authoring:

**Tier A** (v1-accessible, 11 states): `NORMAL_OPERATION`, `RICH_MIXTURE`,
`LEAN_MIXTURE`, `IGNITION_MISFIRE`, `LEAN_MISFIRE`, `RICH_MISFIRE`,
`EXHAUST_AIR_LEAK`, `CATALYST_NOT_LIGHTING_OFF`, `CATALYST_OVERWHELMED`,
`INCOMPLETE_COMBUSTION`, `POA_SIGNATURE`.

**Tier B** (missing from v1, high priority): `TIMING_RETARDED` (64 curated
cases), `SAMPLE_INVALID` (17 curated cases).

### 6.2 FaultFamily (16 values)

`lean_condition`, `misfire`, `ecu_fault`, `rich_mixture`, `catalyst_failure`,
`sensor_fault`, `no_fault`, `mechanical_wear`, `cam_timing`, `exhaust_leak`,
`non_starter`, `ignition_fault`, `invalid_input`, `vacuum_leak` (new),
`overheating` (new), `charging_system` (new).

### 6.3 DTCRoutingTag (20 values)

Mirror of DTCLab `DTCRoutingTag` enum (`DTCLab/code/dtclab/schemas/vocabulary.py`).
Includes `CYLINDER_FLUID_MISFIRE` (needed for FIX-ENUM-1 misfire routing gap)
and `UNKNOWN_FORMAT` (sentinel for malformed DTC strings per FIX-DTC-1).

### 6.4 EvidenceTier (3 values)

`DEFINITIVE`, `SUGGESTIVE`, `GATING`.

---

## 7. Worked Example — lean_condition Family

Two competing rules for `lean_condition`, illustrating the evidence-tier model:

### Rule LC-001 — Lean mixture confirmed (classic air leak)

```json
{
  "rule_id": "LC-001",
  "fault_family": "lean_condition",
  "description": "Lean mixture confirmed by Brettschneider lambda > 1.03",
  "chemistry_evidence": [
    {
      "state": "LEAN_MIXTURE",
      "tier": "DEFINITIVE",
      "wiki_ref": "GAS_VOCABULARY §3"
    }
  ],
  "obd_evidence": [
    {
      "pid": "longft1",
      "operator": "ge",
      "value": 12.0,
      "tier": "SUGGESTIVE",
      "units": "%",
      "wiki_ref": "OBD_VOCABULARY §2"
    },
    {
      "pid": "shrtft1",
      "operator": "ge",
      "value": 8.0,
      "tier": "SUGGESTIVE",
      "units": "%",
      "wiki_ref": "OBD_VOCABULARY §2"
    }
  ],
  "dtc_evidence": [
    {
      "dtc_codes": ["P0171", "P0174"],
      "strategy": "any_match",
      "tier": "SUGGESTIVE",
      "wiki_ref": "DTC_VOCABULARY §4"
    }
  ],
  "base_weight": 0.85,
  "competition_group": "lean_condition",
  "passes_cases": ["CSV-016", "CSV-068", "CSV-109", "CSV-201"],
  "source_wiki_refs": ["GAS_VOCABULARY §3", "OBD_VOCABULARY §2"]
}
```

**Why this works:** `LEAN_MIXTURE` is definitive for this family. The OBD
evidence (positive fuel trims) and DTC evidence (P0171/P0174) are suggestive
reinforcement, not gates. A case with `LEAN_MIXTURE` chemistry but no P0171
still scores well because the DEFINITIVE chemistry evidence carries the rule.

### Rule LC-002 — Lean mixture from vacuum leak (trims correct at 2500 RPM)

```json
{
  "rule_id": "LC-002",
  "fault_family": "lean_condition",
  "description": "Lean mixture from vacuum leak — fuel trims correct at elevated RPM",
  "chemistry_evidence": [
    {
      "state": "LEAN_MIXTURE",
      "tier": "DEFINITIVE",
      "wiki_ref": "GAS_VOCABULARY §3"
    },
    {
      "state": "TIMING_RETARDED",
      "tier": "SUGGESTIVE",
      "wiki_ref": "GAS_VOCABULARY §3"
    }
  ],
  "obd_evidence": [
    {
      "pid": "longft1",
      "operator": "lt",
      "value": 8.0,
      "tier": "GATING",
      "units": "%",
      "wiki_ref": "OBD_VOCABULARY §2"
    },
    {
      "pid": "map_kpa",
      "operator": "lt",
      "value": 35.0,
      "tier": "SUGGESTIVE",
      "units": "kPa",
      "wiki_ref": "OBD_VOCABULARY §3"
    }
  ],
  "base_weight": 0.80,
  "competition_group": "lean_condition",
  "passes_cases": ["CSV-100", "CSV-113", "CSV-201"],
  "source_wiki_refs": ["GAS_VOCABULARY §3", "OBD_VOCABULARY §2"]
}
```

**Why this differs from LC-001:** The GATING OBD constraint (`longft1 < 8.0`)
differentiates this from the classic air-leak pattern. A vacuum leak typically
shows trims that correct at 2500 RPM, so the long-term trim may be modest at
idle. The `TIMING_RETARDED` chemistry evidence is SUGGESTIVE — many vacuum
leaks cause the ECU to retard timing as a knock-avoidance response, but retarded
timing also appears in other families. This rule competes with LC-001: a case
with `LEAN_MIXTURE` chemistry will fire both rules, and the router selects the
higher-scoring one.

---

## 8. Authoring Checklist (for REG-V2-AUTHOR-{family} tasks)

Before marking a rule file complete, verify:

- [ ] The JSON file is at `registry/rules/{family_name}.json`
- [ ] It validates against `RuleSet` (`python -c "from registry.schema_v2 import RuleSet; ..."`)
- [ ] Every rule has `passes_cases` with at least one curated case ID
- [ ] Every `passes_cases` entry resolves to a row in `registry/corpus_curated.csv`
- [ ] Every numeric threshold carries a `wiki_ref` citation (no bare magic numbers)
- [ ] No invented enum values — chemistry states, fault families, evidence tiers,
      and DTC routing tags all match the schema vocabulary
- [ ] The fault family has >= 2 competing rules OR the solo rule has a
      `confidence_ceiling` set
- [ ] Every chemistry state in `TIMING_RETARDED` and `SAMPLE_INVALID` (Tier B
      gaps) used in at least one rule across the family's evidence lists
- [ ] Inner loop ran clean: JSON parse -> schema validate -> case-ID resolve

---

## 9. Integration Notes (for REG-V2-INTEGRATE)

The `schema_v2.py` model is the contract between the registry and the COMLab
router. The router reads `registry/rules/{family}.json` files, deserializes
them into `RuleSet` objects via Pydantic, and consumes:

- `ChemistryEvidence` → maps to GASLab's `ChemicalSignature` output
- `OBDEvidence` → maps to OBDLab's PID payload fields
- `DTCEvidence` → maps to DTCLab's `routing_tags` set
- `base_weight` → initial score before evidence modifiers
- `competition_group` → router scoring pool
- `confidence_ceiling` → post-score cap for solo rules

The router is responsible for implementing the evidence-tier scoring algorithm.
The registry provides the data and the contract — it does not define the scoring
function.

---

## 10. Maintenance

**Vocabulary sync:** The `ChemistryState` and `DTCRoutingTag` enums in
`schema_v2.py` are manual mirrors of their source-of-truth enums in GASLab
and DTCLab. When those source enums change, update `schema_v2.py` to match.
The `test_chemistry_state_count` and `test_dtc_routing_tag_count` tests will
catch drift in enum cardinality but not in naming.

**Schema evolution:** The `model_config = {"extra": "forbid"}` setting on all
models means new fields cannot be added to rule JSON without first updating
`schema_v2.py`. This is intentional — rule files are the data contract, and
the schema is the single source of truth.
