# COMLab — Graphify Re-extraction Spec

**Module:** COMLab  
**Wiki root:** `C:\Users\muto\claude\4DApp\4DLab\COMLab\wiki\`  
**graphify-out root:** `C:\Users\muto\claude\4DApp\4DLab\COMLab\graphify-out\`  
**Spec version:** 1.0 — 2026-05-21  
**Author:** Architect (kricipepsi)

---

## §1 — Purpose

This spec governs the T-PREP-1 graphify extraction of the COMLab wiki into
`graphify-out/graph.json`. The coder must read this spec end-to-end before
invoking any graph-build command. The verified graph is a navigation artefact;
the primary source for KG JSON population is the YAML frontmatter in each wiki
`.md` file (direct parse, not graph traversal).

**What the graph IS used for:**
- Entity inventory: confirm all 30 fault nodes + OPTIMAL_HEALTH are extracted
- Relationship map: differential siblings, family membership, horizon assignments
- Cross-file coherence check: wiki files cross-reference each other via `differential_siblings`

**What the graph is NOT used for:**
- Populating `comlab/config/kg/*.json` — that is done by T-P2-1 via direct YAML parse
- Determining the KGNode field schema — that comes from `COMLab_LLD.md §3.4`

---

## §2 — Wiki file inventory

42 files in `COMLab/wiki/`:

**Fault profiles (30 files):**
- ERR-RM-001 through ERR-RM-007 (rich_mixture)
- ERR-LC-001 through ERR-LC-007 (lean_condition)
- ERR-MF-001 through ERR-MF-007 (misfire)
- ERR-SF-001 through ERR-SF-006 (sensor_fault)
- ERR-EF-001, ERR-EF-002 (ecu_fault)
- OPTIMAL_HEALTH (no_fault)

**Cluster docs (6 files):**
Rich_Mixture_Family.md, Lean_Condition_Family.md, Misfire_Family.md,
Sensor_Fault_Family.md, ECU_Fault_Family.md, No_Fault_Family.md

**Foundation docs (6 files):**
index.md, COMLab_Fault_Taxonomy.md, COMLab_Diagnostic_Logic.md,
COMLab_Lab_Input_Reference.md, COMLab_Horizon_Eras.md, COMLab_DNA_Architecture.md

**Truncation canary:** File `ERR-SF-006_Downstream_O2_Contaminated.md` is the last
alphabetically in the sensor_fault group. If no nodes appear from that file,
truncation occurred.

---

## §3 — Extraction criteria (C1–C6)

All six must PASS before declaring T-PREP complete.

| # | Criterion | Threshold | What to check |
|---|---|---|---|
| C1 | Fault node coverage | ≥ 28/30 fault IDs present as nodes | `fault_id` YAML field value appears as a node label |
| C2 | Family cluster nodes | 6/6 family names present | `rich_mixture`, `lean_condition`, `misfire`, `sensor_fault`, `ecu_fault`, `no_fault` |
| C3 | Differential sibling edges | ≥ 20 sibling edges | `differential_diagnosis_of` or `has_differential_sibling` relation between fault nodes |
| C4 | No generic fallback relations between domain nodes | 0 bad relations | `semantically_similar_to`, `conceptually_related_to` must be absent between fault nodes |
| C5 | Legacy alias links | 3/3 legacy aliases linked | `ERR-E1-M032 → ERR-LC-005`, `ERR-E2-I104 → ERR-MF-001`, `ERR-E3-F501 → ERR-RM-005` |
| C6 | Cross-file coherence | ≥ 10 cross-file edges | Edges whose source_file ≠ target node's source_file |

**Proof-set recovery threshold: ≥ 18/25 edges (see §4).**

---

## §4 — Proof-set (25 required edges)

These specific edges must appear in graph.json. Missing ones → Option 3 patch.

| Source → Target | Relation | Wiki anchor |
|---|---|---|
| `ERR-RM-001` → `ERR-RM-002` | `has_differential_sibling` | ERR-RM-001 §Differential Siblings |
| `ERR-RM-002` → `ERR-MF-006` | `has_differential_sibling` | ERR-RM-002 §Differential Siblings |
| `ERR-RM-003` → `ERR-RM-007` | `has_differential_sibling` | ERR-RM-003 §Differential Siblings |
| `ERR-RM-005` → `ERR-E3-F501` | `maps_to` | ERR-RM-005 YAML legacy_aliases |
| `ERR-RM-006` → `ERR-SF-005` | `has_differential_sibling` | ERR-RM-006 §Differential Siblings |
| `ERR-LC-001` → `ERR-LC-002` | `has_differential_sibling` | ERR-LC-001 §Differential Siblings |
| `ERR-LC-003` → `ERR-LC-004` | `has_differential_sibling` | ERR-LC-003 §Differential Siblings |
| `ERR-LC-005` → `ERR-E1-M032` | `maps_to` | ERR-LC-005 YAML legacy_aliases |
| `ERR-LC-006` → `ERR-SF-001` | `has_differential_sibling` | ERR-LC-006 §Differential Siblings |
| `ERR-MF-001` → `ERR-E2-I104` | `maps_to` | ERR-MF-001 YAML legacy_aliases |
| `ERR-MF-001` → `ERR-MF-004` | `has_differential_sibling` | ERR-MF-001 §Differential Siblings |
| `ERR-MF-002` → `ERR-MF-003` | `has_differential_sibling` | ERR-MF-002 §Differential Siblings |
| `ERR-MF-004` → `ERR-MF-005` | `has_differential_sibling` | ERR-MF-004 §Differential Siblings |
| `ERR-MF-006` → `ERR-RM-002` | `has_differential_sibling` | ERR-MF-006 §Differential Siblings |
| `ERR-MF-007` → `ERR-LC-001` | `has_differential_sibling` | ERR-MF-007 §Differential Siblings |
| `ERR-SF-001` → `ERR-SF-002` | `has_differential_sibling` | ERR-SF-001 §Differential Siblings |
| `ERR-SF-001` → `ERR-LC-006` | `has_differential_sibling` | ERR-SF-001 §Differential Siblings |
| `ERR-SF-002` → `ERR-EF-002` | `has_differential_sibling` | ERR-SF-002 §Differential Siblings |
| `ERR-SF-003` → `ERR-LC-001` | `has_differential_sibling` | ERR-SF-003 §Differential Siblings |
| `ERR-SF-004` → `ERR-SF-003` | `has_differential_sibling` | ERR-SF-004 §Differential Siblings |
| `ERR-SF-005` → `ERR-RM-006` | `has_differential_sibling` | ERR-SF-005 §Differential Siblings |
| `ERR-SF-006` → `ERR-SF-001` | `has_differential_sibling` | ERR-SF-006 §Differential Siblings |
| `ERR-EF-001` → `ERR-EF-002` | `has_differential_sibling` | ERR-EF-001 §Differential Siblings |
| `OPTIMAL_HEALTH` → `no_fault` | `belongs_to_family` | OPTIMAL_HEALTH YAML fault_family |
| `rich_mixture` → `ERR-RM-001` | `enumerates` | Rich_Mixture_Family.md §Fault Map |

---

## §5 — Augmented extraction prompt rules

Prepend to any graphify extraction prompt for this module:

```
COMLAB AUGMENTED EXTRACTION RULES:

1. YAML FRONTMATTER → NODE/EDGE RULE:
   For every .md file with a YAML frontmatter block (between --- markers):
   - `fault_id` → create a node with that ID as label
   - `fault_family` → create a belongs_to_family edge: fault_id → fault_family value
   - `differential_siblings` list → for each sibling ID: create a has_differential_sibling edge
   - `legacy_aliases` list → for each alias: create a maps_to edge: fault_id → alias_id
   - `target_horizons` → for each horizon: create a targets_horizon edge

2. RELATION VOCABULARY — prefer these:
   has_differential_sibling, belongs_to_family, maps_to, targets_horizon,
   enumerates, confirmed_by, gated_by, describes
   Use conceptually_related_to ONLY as last resort.
   NEVER use semantically_similar_to between two fault nodes.

3. LEGACY ALIAS ENTITIES:
   ERR-E1-M032, ERR-E2-I104, ERR-E3-F501 are legacy fault IDs.
   Create nodes for each. Link via maps_to from the new ERR-* ID.

4. TRUNCATION CANARY:
   The file ERR-SF-006_Downstream_O2_Contaminated.md must produce a node.
   If extraction ends without seeing ERR-SF-006, extraction was truncated — report it.

5. SECTION COVERAGE:
   All 30 fault_id values in wiki YAML frontmatter must appear as nodes.
   If count < 28, extraction is incomplete.
```

---

## §6 — Escalation rule

If C1/C3 still fail AFTER augmented chunked extraction AND Option 3 patch:
**STOP. Do not run a third extraction.** Surface the failing cache file to the
architect. Mark T-PREP-1 as `blocked`.

---

## §7 — Post-extraction

After all criteria pass:
1. Run `graphify rebuild graphify-out/` to regenerate communities
2. Write `graphify-out/STEP1_VERIFICATION_LOG.md` (use 4dlab-graph `log` operation)
3. Mark T-PREP-1 done in `COMLAB_PROGRESS.md`
