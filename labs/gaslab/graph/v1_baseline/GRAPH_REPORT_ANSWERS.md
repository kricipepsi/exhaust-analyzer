# Graph Report — Open Questions Answered (pre-ingestion vet)

**Source of truth used:** `docs/wiki/GAS_WIKI.md` v1.0 (2026-05-19) and `docs/wiki/GAS_VOCABULARY.md` v1.0 (2026-05-19). Library at `C:\Users\muto\claude\4DApp\4DLab\library` was inventoried but not deep-read — the wiki+vocab answer all three questions self-consistently. Library hooks are listed in §6 as second-opinion sources if any claim is challenged during ingestion.

Purpose: confirm what the graph is telling us against the source docs, so we don't ingest "garbage" (extractor artefacts) as facts.

---

## Q1 — Why does `Exhaust Gas Triangle (Rule of 16)` bridge Payload-Schema, Gas-Chemistry, and Rich/Hot-Fault clusters? (betweenness 0.368)

**Answer:** because the triangle is not just one gate — it is the **only validity gate that can halt evaluation**, and three independent contracts route through it.

Three concrete bridges, all explicitly in the wiki:

1. **Payload & Validity Schema bridge.** `SampleValidity` (GAS_VOCABULARY.md §5, lines 177–189) is *defined by* the triangle: `VALID = sum ∈ [14,16]`, `EXTERNAL_O2_SUSPECT = (16,18]`, `INVALID < 14 or > 18`. The schema enum literally encodes the triangle's verdict bands. Invariant 2 in §13 of the vocabulary (lines 444): *"No `chemical_state` other than `SAMPLE_INVALID` may be emitted unless `sample_validity` is `VALID`, `BORDERLINE`, or `EXTERNAL_O2_SUSPECT`."* → the triangle gates the entire emission.

2. **Gas Chemistry & Brettschneider bridge.** `GAS_WIKI.md` §6.1 (line 418) states the chemistry: "the sum [CO]+[CO₂]+[O₂] ≈ 14–16% is invariant regardless of mixture. The reaction shuffles oxygen between CO and CO₂ — the totals stay the same." That is a Brettschneider-family conservation law, not a heuristic — it is the only thing that lets λ (chemistry) be trusted, because the Brettschneider formula is the *ratio* of the same atoms the triangle conserves.

3. **Rich/Hot Fault Cluster bridge.** The collision rule (`GAS_WIKI.md` §8.5, lines 778–784) explicitly branches on the triangle:
   - `CO > tier_max AND O₂ > 2.0 % AND triangle 14–16 ⇒ RICH_MISFIRE` (Rich/Hot cluster)
   - `... AND triangle > 16 ⇒ EXHAUST_AIR_LEAK` (downstream ingress)
   
   This is what creates the cross-community edges: the triangle is the discriminator that splits a single chemistry pattern into two different fault categories.

**Reinforcing edges in the report (all EXTRACTED, not inferred):**
- `SampleValidity Enum --cites--> Exhaust Gas Triangle (Rule of 16)` — schema → physics
- `Rule Engine Priority Levels --references--> Exhaust Gas Triangle (Rule of 16)` — engine priority 95 = "Validity gate" (GAS_VOCABULARY.md §14, line 461)
- `GASLab Invariants --references--> Exhaust Gas Triangle (Rule of 16)` — invariant 2 above

**Verdict — INGEST AS-IS.** The bridge is real and load-bearing. The graph is correctly identifying the highest-leverage concept in the wiki. Anyone building rules or tests against GASLab needs this node first.

---

## Q2 — Why does `Rule Engine Priority Levels` bridge Rich/Hot, Payload-Schema, and Misfire-Wear? (betweenness 0.263)

**Answer:** because three of the rule-engine *named overrides* live at the top of the priority table, and each override resolves an ambiguity that belongs to a different community.

Priority table (`GAS_VOCABULARY.md` §14, lines 456–471):

| Priority | Rule | Community resolved | Wiki anchor |
|---|---|---|---|
| 95 | `rule_sample_invalid` (Validity gate) | Payload-Schema (validity is a contract field) | §6.1 |
| 92 | `rule_external_oxygen_warning` | Payload-Schema | §6.1 |
| 91 | `rule_sai_active_warning` | Payload-Schema (suppresses misfire verdicts) | §9.5 |
| **85** | **Masking rule (`rule_ignition_misfire`)** | **Misfire & Mechanical Wear** | **§8.4** |
| **82** | **Wrong-valve-timing rule** | **Misfire & Mechanical Wear** (mechanical, not fuel-mixture) | **§8.6** |
| **80** | **Collision rule** | **Rich/Hot Fault Cluster** (rich-misfire vs ingress split) | **§8.5** |
| 70 | Mixture rules | Rich/Hot | §7.2, §7.3 |
| 60 | Sub-class rules | spread | §7.5, §7.14, §7.15 |
| ... | (lower priorities) | — | — |

The three named overrides (§8.4, §8.5, §8.6) are mathematically *and* organisationally cross-cutting:

- **Masking rule (85)** — `HC>1000 AND O₂>3.0 AND NOₓ<50 ⇒ IGNITION_MISFIRE` overrides any LEAN verdict. Without it the graph's Misfire community would lose its rationale: lean and ignition-misfire share the O₂-up signature, NOₓ is what tells them apart.

- **Wrong-valve-timing rule (82)** — `HC>1000 AND CO>tier_max AND O₂>5.0 ⇒ WRONG_VALVE_TIMING` catches the "pure rich and pure lean cannot explain HC+CO+O₂ all elevated" case (§8.6). Sits between masking and collision because it dominates collision when HC is also high.

- **Collision rule (80)** — the rich-misfire/ingress split documented in Q1 above.

Why this is a bridge: the priority table is the only place in the system where Misfire-cluster verdicts (override 85), Mechanical-wear verdicts (override 82), and Rich/Hot verdicts (override 80) are forced to negotiate. The Payload-Schema connection comes from invariant 3 (`GAS_VOCABULARY.md` §13, line 446): *"GASLab returns exactly one `chemical_state`; ambiguity is collapsed by rule priority."* — i.e. the priority table is what makes the payload single-valued.

**Verdict — INGEST AS-IS.** Bridge is correct. The priority numbers (95/92/91/85/82/80/70/60/50/40/30/20/10) are normative and trace to `gas_lab_dataset.yaml` v2.3 per `GAS_WIKI.md` §13 line 1098.

---

## Q3 — What connects the 27 "weakly-connected" nodes? Gap or extractor miss?

**Garbage-in screen first: the "27 isolated" count is overstated.** Six of the 27 *do* participate in a hyperedge (`DNA-Gated Chemical Signatures`) but the report's `deg ≤ 1` calculation only counted pair-edges, not hyperedge membership. Real "no connection" count is 21, not 27.

Of those 21, the picture splits cleanly:

### Category A — Real diagnostic categories, missing edges the extractor should have caught (= GARBAGE-IN risk if ingested as "isolated")

These each have explicit prose cross-references in the wiki §7 atlas that the extractor did not capture as edges:

| Node | Wiki ref | Should-have edge (text evidence) |
|---|---|---|
| `LEAN_MISFIRE` | §7.5 line 484 | `LEAN_MIXTURE → LEAN_MISFIRE` ("If HC rises significantly, route to `LEAN_MISFIRE`") — §7.3 line 464 |
| `RICH_MISFIRE` | §7.6 line 492 | Already linked to collision rule — but ALSO `RICH_MISFIRE ↔ EXHAUST_AIR_LEAK` ("sum > 16% → ingress; sum ≈ 15.5 → rich misfire") |
| `EXHAUST_AIR_LEAK` | §7.7 line 500 | Disambiguator from rich-misfire; also Era-1 "Cracked exhaust manifold" (§12.1 line 1033) — both are explicit but only the collision rule edge was extracted |
| `CATALYST_NOT_LIGHTING_OFF` | §7.9 line 514 | `CATALYST_OVERWHELMED` (§7.10 same band, escalation) and `Catalyst Window` (§4.4) — both stated, only TWC edge captured |
| `CATALYST_OVERWHELMED` | §7.10 | Same as above; also `CO-to-NOₓ Failure Transition` (§9.7) explicitly names overwhelmed cat as the failure mode |
| `O2_SENSOR_BIASED_LOW/HIGH` | §7.14–7.15 | `Lambda Mismatch (Truth vs Perception)` edge IS captured (good) — but missing edge to `Brettschneider Equation` ("λ from Brettschneider chemistry reads rich while ECU perceives lean") |
| `TIMING_OVER_ADVANCED` | §7.12 line 536 | Inferred edge to HIGH_COMBUSTION_TEMP captured; missing explicit edge to `NOₓ` ("NOₓ very high") and to the era table (§12 doesn't reference but §7.8 does) |
| `WRONG_VALVE_TIMING` | §7.24 | Wrong-valve-timing-rule edge captured; missing edge to `HC` and `CO` and `O₂` ("HC and CO and O₂ are all elevated") |
| `WORN_VALVE_SEALS`, `WORN_PISTON_RINGS` | §7.21–7.22 | Inferred sibling edge captured; missing edges to `POA_SIGNATURE` (§7.23 explicitly lists them as sub-modes lines 642–646) and `Cylinder-Contribution Test` (§11.2) |

**Recommendation for Category A:** before ingesting, run a targeted re-extraction pass on §7 fault-atlas rows looking for `route to`, `see §`, `same pattern as`, `differentiator`, `sub-mode`. Each of those is an implicit edge the extractor missed. Otherwise the graph will tell downstream lookups "LEAN_MISFIRE is isolated" when in fact the wiki explicitly tells you to route there from LEAN_MIXTURE.

### Category B — Genuinely sparse in the v1.0 wiki, but documented elsewhere (= GAP that should be filled by edges to vocabulary, not by re-extraction)

| Node | Wiki anchor | Where it belongs |
|---|---|---|
| `NORMAL_OPERATION` | §7.1 | Should connect to: `Lambda (λ)` (defines normal as 0.995–1.005), `Three-Way Catalyst` (cat lit is part of normal), `Exhaust Gas Triangle` (triangle valid is part of normal). All stated in §7.1 — pure extractor miss. |
| `TIMING_RETARDED` | §7.13 | Sibling to `TIMING_OVER_ADVANCED`; both are NOₓ-shifted-without-other-gases-moving. Should be edge-paired in graph. |
| `GDI_INTAKE_VALVE_CARBON` | §7.18 | Should connect to `STRESS_IDLE` / RPM-differential — §7.18 line 586 says it "clears substantially at 2500 RPM". Also gated by `fuel_delivery_type=GDI` (in vocabulary §3.1). |
| `EGR_STUCK_OPEN` | §7.26 | EGR-equipped gate captured via hyperedge; missing the idle-vs-load directional contrast (§7.26 line 676) |
| `VVT_FAILURE` | §7.27 | Two distinct failure modes (idle-overlap vs load-NOₓ) — both stated, neither extracted |
| `EVAP_CANISTER_SATURATED` | §7.28 | Connects to fuel-trim direction (negative) and mid-load timing — stated, not extracted |
| `EngineStateBucket Enum` | VOCAB §7 | Should connect to all three RPM buckets and to `STRESS_IDLE` — vocab line 232–244 enumerates them explicitly |
| `GasBehavior Enum` | VOCAB §8 | Should connect to `Collision Rule` (which uses `behavior: COLLISION`) — vocab line 264 says so |
| `CatalystStatus Enum` | VOCAB §9 | Should connect to `Three-Way Catalyst`, `Catalyst Window`, `CATALYST_NOT_LIGHTING_OFF`, `CATALYST_OVERWHELMED` — all stated |
| `SEMANTIC_CONTRACT.md (COMLab)` | VOCAB §1 | Cross-lab anchor — currently dangling; should connect to `GasLabPayload` (which it defines) |
| `gaslab/brettschneider.py (planned)` | VOCAB §6 | Already correctly linked to `Brettschneider Equation` — this is fine, just 1-degree because nothing else points to a planned file |

### Category C — True singletons that are correctly sparse (= NOT a gap)

| Node | Why sparse is correct |
|---|---|
| `Stoichiometry (AFR 14.71)` | A constant. One edge (`Lambda (λ) → Stoichiometry`) is the right structure: a number doesn't have downstream relations. |
| `Secondary Air Injection (SAI)` | A piece of equipment that masks misfire. One edge to `Dilution Screen` is correct; the suppression list (§9.5: suppresses IGNITION_MISFIRE, LEAN_MISFIRE, LEAN_MIXTURE) is operational behaviour, not graph-worthy unless we want a "suppresses" relation type. |
| `SAMPLE_INVALID` | Correctly connected to triangle (its only definition). |
| `VACUUM_REGULATOR_DIAPHRAGM_RUPTURE` / `GDI_HPFP_INTERNAL_SEAL_LEAK` | Forms the thin community 7 — they ARE each other's only meaningful relation (identical tailpipe signature, differentiated only by crankcase evidence, §7.19/§7.20). The thin-community-warning in the report is misleading; this is the correct structure. |
| `EGR_STUCK_CLOSED` | The `→ HIGH_COMBUSTION_TEMP semantically_similar_to` inferred edge captures the key relation (§7.25 says "Same gas pattern as `HIGH_COMBUSTION_TEMP`"). |

**Verdict on Q3:** of the 27 "isolated" nodes,
- **~12 are extractor under-extraction** (Categories A+B) — re-run extraction on §7 atlas before ingest, targeting prose cross-references.
- **~6 hyperedge-credit** (the DNA-gated CS values) — the report should count hyperedge participation; not a real gap.
- **~9 are genuinely correct as singletons** (Category C) — leave them.

If we ingest as-is, "garbage in" risk is mainly that downstream lookups will think the fault atlas is more fragmented than the wiki actually documents.

---

## §4 — Thin-community audit

| Community | Verdict | Reason |
|---|---|---|
| `Fuel/Vacuum Internal Leaks` (2 nodes) | **Real** | §7.19/§7.20 explicitly define them as a pair with identical tailpipe signature; thin-cluster warning is wrong here |
| `Normal Operation` (1 node) | **Extractor miss** | Should connect to TWC, Triangle, Lambda — re-extract |
| `Timing Retarded` (1 node) | **Extractor miss** | Sibling of TIMING_OVER_ADVANCED — should be in same community, not a singleton |
| `Worn Engine` (1 node) | **Borderline** | §7.16 contrasts it with POA and MISFIRE — those are real edges, but no other concept is unique to it |
| `Flat Camshaft` (1 node) | **Correct singleton** | §7.17 is a self-contained signature, confirmed by cyl-contribution test (which IS captured) |
| `GDI Intake Carbon` (1 node) | **Extractor miss** | Should be linked to STRESS_IDLE, GDI gate, RPM-differential — all in §7.18 |
| `EGR Stuck Open` (1 node) | **Extractor miss** | Should connect to its sibling EGR_STUCK_CLOSED |
| `VVT Failure` (1 node) | **Borderline** | Real concept; its DTCs are out-of-scope per §7.27, so few edges is plausible |
| `EVAP Canister` (1 node) | **Borderline** | Same as VVT |
| `Gas Behavior Taxonomy` (1 node) | **Extractor miss** | Vocab §8 says it's used in YAML rule bodies; should connect to `Collision Rule` |
| `Catalyst Status Taxonomy` (1 node) | **Extractor miss** | Vocab §9 enumerates four states that ARE the cat fault classes |

---

## §5 — INFERRED-edge vet (8 edges, avg confidence 0.86)

| Edge | Confidence | Verdict | Source check |
|---|---|---|---|
| `Dilution Screen --semantically_similar_to--> Exhaust Gas Triangle` | 0.85 | **Correct but weak relation type.** §6.2 line 422–428 — dilution screen is the *simpler* version of the triangle. The relation should be `simplification_of` not `semantically_similar_to`. | Wiki §6.2 |
| `RICH_MISFIRE --semantically_similar_to--> RICH_MIXTURE` | 0.85 | **Misleading.** They are *contrasted*, not similar. RICH_MISFIRE is the collision; RICH_MIXTURE is the pure pattern. Better relation: `disambiguated_from`. | Wiki §7.2 vs §7.6 |
| `IGNITION_MISFIRE --semantically_similar_to--> LEAN_MIXTURE` | 0.75 | **Misleading.** They are explicit *false-positives* of each other resolved by the masking rule. Better: `mistaken_for_via_masking_rule`. | Wiki §7.4 line 472, §8.4 |
| `LEAN_MISFIRE --semantically_similar_to--> LEAN_MIXTURE` | 0.85 | **Acceptable but weak.** §7.3 says "if HC rises, route to LEAN_MISFIRE" — that's a routing edge, not a similarity edge. Better: `escalates_to`. | Wiki §7.3 line 464 |
| `EGR_STUCK_CLOSED --semantically_similar_to--> HIGH_COMBUSTION_TEMP` | 0.95 | **Correct, and §7.25 line 668 says so verbatim** ("Same gas pattern as HIGH_COMBUSTION_TEMP"). Keep. | Wiki §7.25 |
| `TIMING_OVER_ADVANCED --semantically_similar_to--> HIGH_COMBUSTION_TEMP` | 0.85 | **Partially correct.** Both elevate NOₓ, but §7.12 explicitly says "Distinct from §7.8 in that NOₓ is very high while the other four gases remain near normal." Better: `differential_diagnosis_of`. | Wiki §7.12 line 536 |
| `VACUUM_REGULATOR_DIAPHRAGM_RUPTURE --semantically_similar_to--> GDI_HPFP_INTERNAL_SEAL_LEAK` | 0.95 | **Correct.** §7.20 line 606 says "Tailpipe signature identical to §7.19". Differentiator is crankcase, not tailpipe. Keep. | Wiki §7.19/§7.20 |
| `WORN_VALVE_SEALS --semantically_similar_to--> WORN_PISTON_RINGS` | 0.85 | **Partially correct.** Same family (POA), but §7.21 line 624 vs §7.22 line 634 — the RPM-differential goes opposite directions. Better: `paired_under_POA_signature`. | Wiki §7.21/§7.22 |

**Verdict on INFERRED edges:** all 8 are pointing at real relationships, but the relation type `semantically_similar_to` is too coarse for 6 of the 8. Five of them are *disambiguation pairs* (the wiki literally exists to tell them apart), not similarity pairs. Ingesting them as "similar" is the highest-impact garbage-in risk in this report.

---

## §6 — Pre-ingestion action list

| # | Action | Severity | Why |
|---|---|---|---|
| 1 | Re-run extraction on `GAS_WIKI.md` §7 fault atlas (28 rows) with a prompt that looks for prose cross-references (`route to`, `see §`, `same pattern as`, `differentiator`, `sub-mode`). | **HIGH** | Recovers ~12 missing edges; fixes ~7 thin-community false alarms. |
| 2 | Reclassify the 6 INFERRED `semantically_similar_to` edges (rows 2–4, 6, 8 in §5) as `disambiguated_from` / `mistaken_for_via_masking_rule` / `escalates_to` / `paired_under_POA_signature`. | **HIGH** | Otherwise downstream lookups will conflate disambiguation pairs as synonyms — the exact failure mode the wiki was written to prevent. |
| 3 | Add explicit edges from `GAS_VOCABULARY.md` enum nodes (`EngineStateBucket`, `GasBehavior`, `CatalystStatus`) to the concepts they enumerate. | **MEDIUM** | Currently dangling, but vocab §7/§8/§9 enumerate the targets explicitly. |
| 4 | Fix the "27 isolated" count in `GRAPH_REPORT.md` to credit hyperedge participation (true count: 21). | **LOW** | Cosmetic; the number is overstated. |
| 5 | Keep Category C singletons (Stoichiometry, SAI, SAMPLE_INVALID, FLAT_CAMSHAFT) as-is. | **N/A** | Correct structure. |
| 6 | Add a `references_invariant` edge type so `GASLab Invariants` can correctly relate to Triangle (currently `references`, which loses the "halt-evaluation" semantics). | **LOW** | Improves query precision; not critical. |

---

## §7 — Bottom line for "should we ingest?"

**Yes, after items 1 and 2 above.** The graph's structural backbone (god nodes, community structure, the two high-betweenness bridges) is sound and the wiki backs it up. The risks are:

1. **Garbage-in via under-extraction** — fault-atlas prose cross-references missed → fixable by re-extraction.
2. **Garbage-in via too-coarse relation type** — 5 disambiguation pairs labelled as "similar" → fixable by relabel.

Both are bounded, mechanical fixes. The expensive thing (the 18 communities, the hub identification, the triangle/priority-table betweenness) is already correct.

If we ingest as-is without items 1 and 2, downstream lookups will:
- under-find paths through the §7 atlas ("LEAN_MIXTURE → LEAN_MISFIRE" disappears),
- conflate disambiguation pairs ("how is RICH_MISFIRE different from RICH_MIXTURE?" returns "they are similar" — exactly wrong).

After items 1 and 2 the graph faithfully represents the wiki.

---

## §8 — Library cross-reference (knowledge vault) — for ingestion-time challenges only

These library files are the upstream second-opinion sources if any claim above is disputed during ingestion. None were needed to answer the open questions; the wiki is internally complete.

| Disputed claim would touch… | Library file |
|---|---|
| Triangle 14–16 % envelope, dilution screen | `library/gases/master_gas_guide.md`, `library/gases/Understanding Engine Exhaust Emissions.md` |
| Rh saturation at lean / CO-to-NOₓ transition | `library/catalyst/master_catalyst_guide.md` |
| Brettschneider, AFR, λ definitions | `library/gases/AFR.md`, `library/gases/lambda.md`, `library/gases/master_gas_guide.md` |
| O₂-sensor bias signatures | `library/o2_sensor/master_o2_sensor_guide.md`, `library/extracted-diagnostics/oxygen-sensors/*` |
| Masking-rule / ignition-misfire physics | `library/ignition/master_ignition_guide.md`, `library/extracted-diagnostics/misfires/*` |
| Fuel-trim direction conventions (used in §7.19–§7.22) | `library/fuel_trim/master_fuel_trim_guide.md` |
| EGR idle-vs-load behaviour | `library/egr/master_egr_guide.md` |
| Era-specific fault list (§12) | `library/cases_petrol.html`, `library/gases/enginefaults.md` |

If any reviewer flags a wiki claim during ingestion, the matching library file is the place to confirm before changing the graph — not the place to start.

---

*End of answers. Recommend running items 1 and 2 of §6 before re-generating the graph, then re-running the betweenness/community report to confirm the bridges are still where they are now (they should be).*
