# Re-extraction Spec — chunk-1 pass to make graph faithful to wiki

**Purpose:** close the two garbage-in gaps surfaced in `GRAPH_REPORT_ANSWERS.md` §6 items 1 and 2. Anything outside those two items is out of scope for this pass.

**Input:** `docs/wiki/GAS_WIKI.md` v1.0, `docs/wiki/GAS_VOCABULARY.md` v1.0 (unchanged).

**Output:** updated `graphify-out/graph.json`, regenerated communities, regenerated `GRAPH_REPORT.md`, regenerated per-community wiki files under `graphify-out/wiki/`.

---

## 1. Cache invalidation

The two semantic-cache files are SHA-keyed on **(prompt × content)**. If the prompt is changed and the content is unchanged, the cache files will not regenerate unless either (a) deleted, or (b) the prompt-version is bumped so the SHA changes.

Action: bump the prompt-version constant in the graphify config (preferred — keeps cache as audit trail), or `rm graphify-out/cache/semantic/*.json` (acceptable — current cache is one-of-a-kind, no other consumers).

---

## 2. Augmented extraction prompt — content (paste into the existing semantic-extraction prompt template)

### 2.1 Additional cross-reference patterns to look for in §7 fault atlas

When extracting from a §7.X subsection, scan the prose for these literal patterns and emit an edge for each:

| Phrase pattern (in prose) | Emit edge | Relation |
|---|---|---|
| "route to `X`" / "routes to `X`" / "see §7.X (X)" | current_node → X | `escalates_to` |
| "same gas pattern as `X`" / "tailpipe signature identical to §7.X" | current_node → X | `tailpipe_signature_identical_to` |
| "Distinct from §7.X in that …" | current_node → X | `differential_diagnosis_of` |
| "differentiator …" / "Key differentiator …" | current_node → (next-mentioned node) | `differentiated_by` (and attach the differentiator text as edge property) |
| "Disambiguate with `X`" / "disambiguated by `X`" | current_node → X | `disambiguated_by` |
| "sub-mode" within a table of sub-modes | row_node → table_owner_node | `sub_mode_of` |
| "override any `X` verdict" | rule_node → X | `overrides` |
| "suppresses `X` / `Y` / `Z`" (§9.5 SAI) | suppressor_node → each suppressed | `suppresses` |
| "must be true" / "DNA gate: `X`" | current_node → X | `gated_by` |
| "Confirmed by `X` (test/check)" | current_node → X | `confirmed_by` |
| "Mirror of `X` §Y" / "single source of truth: `X` §Y" | current_node → X | `mirrors_contract_in` |

### 2.2 Specific edges the current graph is missing (proof-set — re-extraction MUST recover these)

The coder can use this as a green/red test after the run. Every edge below is sourced to an explicit line in the wiki:

| Source → Target | Relation | Wiki anchor |
|---|---|---|
| `LEAN_MIXTURE` → `LEAN_MISFIRE` | `escalates_to` | §7.3 line 464 ("If HC rises significantly, route to LEAN_MISFIRE") |
| `RICH_MISFIRE` → `EXHAUST_AIR_LEAK` | `disambiguated_by` (Triangle) | §7.6 line 492 ("sum > 16 % → ingress; sum ≈ 15.5 % → rich misfire") |
| `EGR_STUCK_CLOSED` → `HIGH_COMBUSTION_TEMP` | `tailpipe_signature_identical_to` | §7.25 line 668 ("Same gas pattern as HIGH_COMBUSTION_TEMP") |
| `TIMING_OVER_ADVANCED` → `HIGH_COMBUSTION_TEMP` | `differential_diagnosis_of` | §7.12 line 536 ("Distinct from §7.8 in that NOₓ is very high while the other four gases remain near normal") |
| `GDI_HPFP_INTERNAL_SEAL_LEAK` → `VACUUM_REGULATOR_DIAPHRAGM_RUPTURE` | `tailpipe_signature_identical_to` | §7.20 line 606 ("Tailpipe signature identical to §7.19; differentiator is crankcase evidence") |
| `WORN_VALVE_SEALS` → `POA_SIGNATURE` | `sub_mode_of` | §7.23 line 642 (POA sub-mode table row 1) |
| `WORN_PISTON_RINGS` → `POA_SIGNATURE` | `sub_mode_of` | §7.23 line 643 (POA sub-mode table row 2) |
| `Masking Rule` → `LEAN_MIXTURE` | `overrides` | §8.4 line 773 ("override any LEAN verdict") |
| `Masking Rule` → `LEAN_MISFIRE` | `overrides` | §8.4 line 773 (same) |
| `SAI` → `IGNITION_MISFIRE` | `suppresses` | §9.5 line 856 ("suppresses verdicts: IGNITION_MISFIRE, LEAN_MISFIRE, LEAN_MIXTURE") |
| `SAI` → `LEAN_MISFIRE` | `suppresses` | §9.5 line 856 (same) |
| `SAI` → `LEAN_MIXTURE` | `suppresses` | §9.5 line 856 (same) |
| `IGNITION_MISFIRE` → `cylinder_count (DNA)` | `gated_by` | §7.4 line 472 ("Cylinder count from DNA gives the misfire count") |
| `GDI_INTAKE_VALVE_CARBON` → `STRESS_IDLE` | `confirmed_by` (RPM-differential) | §7.18 line 586 ("clears substantially at 2500 RPM") |
| `WORN_VALVE_SEALS` → `STRESS_IDLE` | `confirmed_by` | §7.21 (RPM-differential matrix) |
| `WORN_PISTON_RINGS` → `STRESS_IDLE` | `confirmed_by` | §7.22 (RPM-differential matrix) |
| `FLAT_CAMSHAFT` → `Cylinder-Contribution Test` | `confirmed_by` | §7.17 line 576 |
| `NORMAL_OPERATION` → `Lambda (λ)` | `references` | §7.1 line 446 (λ = 0.995–1.005) |
| `NORMAL_OPERATION` → `Three-Way Catalyst (TWC)` | `references` | §7.1 line 448 ("Catalyst lit") |
| `NORMAL_OPERATION` → `Exhaust Gas Triangle (Rule of 16)` | `references` | §7.1 line 448 ("triangle valid") |
| `ChemicalSignature Enum` → each of the 28 CS values | `enumerates` | VOCAB §3 lines 79–106 |
| `EngineStateBucket Enum` → `STABILIZED_IDLE` / `REGULATORY_HIGH_IDLE` / `STRESS_IDLE` / `COLD_OPEN_LOOP_INVALID` | `enumerates` | VOCAB §7 lines 232–244 |
| `CatalystStatus Enum` → `Three-Way Catalyst (TWC)` | `evaluates_state_of` | VOCAB §9 lines 270–278 |
| `GasBehavior Enum` → `Collision Rule` | `used_by` | VOCAB §8 line 264 |
| `SEMANTIC_CONTRACT.md (COMLab)` → `GasLabPayload` | `defines` | VOCAB §12 line 397 |

Minimum proof bar: of the 25 edges above, at least 22 must be present in the regenerated graph. If fewer, the augmented prompt is not biting and the run should be re-tried with the patterns more aggressively stated.

### 2.3 Relation-type vocabulary — REPLACE `semantically_similar_to` for the 8 existing INFERRED edges

The current `semantically_similar_to` is too coarse. The extractor should choose from this richer set when inferring relations between two §7 fault rows:

| New relation | Use when… |
|---|---|
| `tailpipe_signature_identical_to` | Two faults produce the same five-gas pattern, differentiated only by non-gas evidence |
| `differential_diagnosis_of` | One fault is explicitly the "distinct from X" clarification of another |
| `escalates_to` | The wiki uses "route to" / "if X rises further" language |
| `disambiguated_by` | One node is the test that splits two others (e.g. Triangle splits rich-misfire from ingress) |
| `sub_mode_of` | The node is one row in a sub-mode table inside a parent fault |
| `paired_under_<parent>` | Two siblings of a parent concept (e.g. WORN_VALVE_SEALS / WORN_PISTON_RINGS under POA) |
| `mistaken_for_via_<rule>` | Two nodes that the named-override rule exists to disentangle (e.g. IGNITION_MISFIRE vs LEAN_MIXTURE via masking rule) |

`semantically_similar_to` should remain available but only as the fallback when none of the above apply.

### 2.4 Specific INFERRED-edge relabellings (deterministic, do not re-infer)

If the coder wants a fast path (no re-inference), the existing 8 INFERRED edges can be relabelled deterministically:

| Old (current) | New |
|---|---|
| `Dilution Screen --semantically_similar_to--> Exhaust Gas Triangle` | `simplification_of` |
| `RICH_MISFIRE --semantically_similar_to--> RICH_MIXTURE` | `differential_diagnosis_of` |
| `IGNITION_MISFIRE --semantically_similar_to--> LEAN_MIXTURE` | `mistaken_for_via_masking_rule` |
| `LEAN_MISFIRE --semantically_similar_to--> LEAN_MIXTURE` | `escalates_to` (direction: LEAN_MIXTURE → LEAN_MISFIRE, reverse the current edge) |
| `EGR_STUCK_CLOSED --semantically_similar_to--> HIGH_COMBUSTION_TEMP` | `tailpipe_signature_identical_to` |
| `TIMING_OVER_ADVANCED --semantically_similar_to--> HIGH_COMBUSTION_TEMP` | `differential_diagnosis_of` |
| `VACUUM_REGULATOR_DIAPHRAGM_RUPTURE --semantically_similar_to--> GDI_HPFP_INTERNAL_SEAL_LEAK` | `tailpipe_signature_identical_to` |
| `WORN_VALVE_SEALS --semantically_similar_to--> WORN_PISTON_RINGS` | `paired_under_POA_signature` |

Each relabel is justified verbatim in `GRAPH_REPORT_ANSWERS.md` §5.

---

## 3. Success criteria — loop until ALL pass

The coder reruns until all six checks pass against the regenerated `graph.json` + `GRAPH_REPORT.md`. Any failure means another pass.

1. **Bridge preservation (amended 2026-05-19, re-amended same day)** — `Exhaust Gas Triangle (Rule of 16)` retains betweenness centrality ≥ 0.15 AND bridges ≥ 3 communities. `Rule Engine Priority Levels` retains bridges ≥ 3 communities; its betweenness is permitted to drop below 0.15 when direct rule→signature edges are present, because in that topology Priority Levels is correctly a reference table (VOCAB §14) rather than a path-bearing bridge. `ChemicalSignature Enum` is permitted to dominate as a new hub — that is the direct mathematical consequence of the 28 enumerates edges added in §2.2 of this spec.
2. **Proof-set recovery** — at least 22 of the 25 edges in §2.2 above are present in the new graph (exact source/target/relation).
3. **No `semantically_similar_to` between two §7 fault rows** — `grep` the edges; this relation between two CS values is the failure marker. Allowed only between non-CS concept pairs.
4. **Isolated-node count (amended 2026-05-19)** — non-leaf, non-Category-C isolated nodes < 5. Leaf vocabulary nodes (`EngineStateBucket` members, `ChemicalSignature` members reached only via the `enumerates` edge, single-purpose enums) are excluded from the count. Category C singletons from `GRAPH_REPORT_ANSWERS.md` §3 (`Stoichiometry`, `SAI`, `SAMPLE_INVALID`, `FLAT_CAMSHAFT`, `VACUUM_REGULATOR_DIAPHRAGM_RUPTURE` / `GDI_HPFP_INTERNAL_SEAL_LEAK` as a pair, `EGR_STUCK_CLOSED`, `TIMING_RETARDED`, `VVT_FAILURE`, `EVAP_CANISTER_SATURATED`) are excluded — they are sparse by design.
5. **`NORMAL_OPERATION` has degree ≥ 3** — currently 0. After §2.2 it should hit Lambda, TWC, Triangle at minimum.
6. **Hyperedge participation is counted in the isolated-node metric** in the regenerated `GRAPH_REPORT.md`. The "27" should become "21 true + 6 hyperedge-only".

---

## 4. Out of scope for this pass — do NOT do

- Do not edit `GAS_WIKI.md` or `GAS_VOCABULARY.md`. They are the source of truth; the graph is downstream.
- Do not change the 28-value `ChemicalSignature` enum or any threshold table.
- Do not change community-detection parameters (Leiden/Louvain resolution etc.) — communities must shift only as a consequence of the new edges, not by tuning.
- Do not add INFERRED edges with confidence < 0.85. The pass is to capture EXTRACTED prose, not to invent new inferences.
- Do not deep-read `library/` during extraction — it's a second-opinion vault, not extraction input, per `GRAPH_REPORT_ANSWERS.md` §8.

---

## 5. Tradeoffs surfaced

- **Cost:** ~ same as the first pass (chunks unchanged, prompt richer ≈ +10–15% input tokens). User said tokens are not the constraint.
- **Cache audit trail:** bumping prompt-version preserves the v1 cache; `rm`ing it loses provenance. Recommend prompt-version bump.
- **Relation-vocabulary expansion:** introducing 7 new relation types raises the bar for downstream consumers (e.g. graphify-lookup must know what `tailpipe_signature_identical_to` means). The alternative — sticking to a tiny set and using edge properties for nuance — is uglier to query. Recommend accept the expansion; it matches how the wiki reasons.
- **Risk of over-extraction:** richer prompt can hallucinate edges. Mitigation: success criterion #2 is positive (≥ 22/25), but also spot-check 10 random new edges against the wiki line they cite. Refuse to ingest if > 1 fails.

---

## 6. Handoff

When all six success criteria pass, mark GASLab bootstrap Step 1 complete and proceed to Step 2 (`_gaslab_skills/gaslab-python/SKILL.md`). If any criterion fails after two passes, escalate to the user — likely the prompt template needs structural change, not a third re-run.
