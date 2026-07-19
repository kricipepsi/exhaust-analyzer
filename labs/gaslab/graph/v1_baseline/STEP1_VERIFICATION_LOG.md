# GASLab Bootstrap Step 1 — Verification Log (Run 3 — direction patch)

**Run date:** 2026-05-20
**Patch type:** Option 3 deterministic — direction corrections only
**Graph state before patch:** 74 nodes · 131 links · 8 communities · 3 hyperedges

---

## §1 — Patches applied

### Issue 1: 28 reversed enumerates edges
All 28 CS-value → ChemSig Enum edges had source ↔ target swapped.
Root cause: extractor read enumeration backwards (value points to type, not type to value).
Action: swapped source/target on every enumerates link where target == gas_vocab_chemical_signature_enum.
Result: ChemicalSignature Enum (28 values) is now source of all 28 enumerates edges.
EngineStateBucket Enum enumerates (4 edges) were correct direction — not touched.

### Issue 2: 9 individual direction flips
Root cause: same direction-inversion pattern on references, tailpipe_signature_identical_to,
confirmed_by, defines, used_by, evaluates_state_of.

Edges flipped (source → target after fix):
1. NORMAL_OPERATION → Lambda (λ)                                     [GAS_WIKI §7.1]
2. NORMAL_OPERATION → Exhaust Gas Triangle (Rule of 16)              [GAS_WIKI §7.1]
3. NORMAL_OPERATION → Three-Way Catalyst (TWC)                       [GAS_WIKI §7.1]
4. EGR_STUCK_CLOSED → HIGH_COMBUSTION_TEMP                           [GAS_WIKI §7.25]
5. GDI_HPFP_INTERNAL_SEAL_LEAK → VACUUM_REGULATOR_DIAPHRAGM_RUPTURE [GAS_WIKI §7.20]
6. FLAT_CAMSHAFT → Cylinder-Contribution Test                        [GAS_WIKI §7.17]
7. SEMANTIC_CONTRACT.md (COMLab) → GasLabPayload                     [GAS_VOCAB §12]
8. GasBehavior Enum → Collision Rule                                 [GAS_VOCAB §8]
9. CatalystStatus Enum → Three-Way Catalyst (TWC)                    [GAS_VOCAB §9]

### Issue 3: 1 relation relabel
RICH_MISFIRE --escalates_to--> EXHAUST_AIR_LEAK
  → RICH_MISFIRE --disambiguated_by--> EXHAUST_AIR_LEAK
Root cause: extractor chose escalates_to (fault progression) instead of
disambiguated_by (diagnostic alternative split by Triangle test).
Wiki anchor: GAS_WIKI §7.6 line 492.

---

## §2 — Rebuild

- Community detection: same Louvain parameters; not tuned.
- GRAPH_REPORT.md: regenerated.
- Per-community wiki articles: regenerated.
- Semantic cache: untouched (direction patch does not change extraction inputs).

---

## §3 — Verification results

| Check | Result | Detail |
|---|---|---|
| C-ENUM: ChemSig Enum → 28 CS values | PASS | 28 out, 0 in — all correct direction |
| C-EB: EngineStateBucket → 4 members unchanged | PASS | 4 outgoing enumerates preserved |
| C-NORMAL: NORMAL_OPERATION → 3 references | PASS | Lambda, Triangle, TWC |
| C-TAILPIPE: EGR/GDI_HPFP are sources | PASS | Both tailpipe_signature_identical_to sources correct |
| C-CONFIRMED: FLAT_CAMSHAFT → Cyl-Contrib | PASS | confirmed_by direction correct |
| C-DEFINES: SEMANTIC_CONTRACT → GasLabPayload | PASS | defines direction correct |
| C-USEDBY: GasBehavior Enum → Collision Rule | PASS | used_by direction correct |
| C-CATALYST: CatalystStatus Enum → TWC | PASS | evaluates_state_of direction correct |
| C-DISAMBIG: RICH_MISFIRE --disambiguated_by--> | PASS | disambiguated_by present, escalates_to gone |
| C-NOGENERIC: 0 generic relations | PASS | No semantically_similar_to or conceptually_related_to |

**Final: 10/10 PASS**

---

## §4 — Final relation distribution

| Count | Relation |
|---|---|
| 32 | enumerates |
| 21 | references |
| 21 | shares_data_with |
| 16 | rationale_for |
| 6 | differential_diagnosis_of |
| 6 | gated_by |
| 5 | cites |
| 4 | confirmed_by |
| 3 | suppresses |
| 2 | disambiguated_by |
| 2 | overrides |
| 2 | tailpipe_signature_identical_to |
| 2 | sub_mode_of |
| 1 | mirrors_contract_in |
| 1 | defines |
| 1 | implements |
| 1 | simplification_of |
| 1 | used_by |
| 1 | evaluates_state_of |
| 1 | mistaken_for_via_masking_rule |
| 1 | escalates_to |
| 1 | paired_under_poa_signature |

**Total: 131 links across 22 relation types.**

---

## §5 — Step 1 status

**COMPLETE** — All 10 checks pass. Graph at graphify-out/graph.json is verified.

---

## §6 — Run 4 (KG audit cleanup)

**Run date:** 2026-05-21
**Patch type:** Option 3 deterministic — confidence promotion only
**Graph state before patch:** 74 nodes · 131 links · 9 communities · 3 hyperedges

### §6.1 — Patches applied

#### Edge 1: `LEAN_MIXTURE --escalates_to--> LEAN_MISFIRE` (ISSUE-2, INFERRED 0.85)
- **Wiki anchor:** GAS_WIKI §7.3 line 464 — "Triangle valid, HC modest. If HC rises significantly, route to `LEAN_MISFIRE` (§7.5)."
- **Verdict:** promote_to_extracted — direction and relation correct. "route to" maps to `escalates_to` per REEXTRACTION_SPEC §2.1. This is causal progression (lean → combustion instability → misfire), not a diagnostic alternative.
- **Before:** `confidence: INFERRED, confidence_score: 0.85, source_location: "§7.5 vs §7.3"`
- **After:** `confidence: EXTRACTED, source_location: "§7.3 line 464", _patched: "kg_audit_run4_2026-05-20"`

#### Edge 2: `LEAN_MIXTURE --mistaken_for_via_masking_rule--> IGNITION_MISFIRE` (ISSUE-4, INFERRED 0.75)
- **Wiki anchor:** GAS_WIKI §8.4 line 773 — "⇒ IGNITION_MISFIRE (override any LEAN verdict)"; §7.4 line 472 — "high HC + high O₂ + low NOₓ → no heat → no NOₓ → confirmed misfire (not lean)"
- **Verdict:** promote_to_extracted — direction and relation correct. LEAN_MIXTURE is the masked (superficial) fault; IGNITION_MISFIRE is the masking (true) fault. The "override any LEAN verdict" wording confirms the masking direction.
- **Before:** `confidence: INFERRED, confidence_score: 0.75, source_location: "§7.4 vs §7.3"`
- **After:** `confidence: EXTRACTED, source_location: "§8.4 line 773; §7.4 line 472", _patched: "kg_audit_run4_2026-05-20"`

### §6.2 — Rebuild

- No community detection or report re-generation (no edges added/deleted — direction unchanged, only field values on two edges).
- GRAPH_REPORT.md: not regenerated (community structure unchanged).
- Semantic cache: untouched.

### §6.3 — Verification results

| Check | Result | Detail |
|---|---|---|
| C-EDGE1: escalation promoted | PASS | `escalates_to` now EXTRACTED, anchor §7.3 line 464 |
| C-EDGE2: masking promoted | PASS | `mistaken_for_via_masking_rule` now EXTRACTED, anchor §8.4 line 773; §7.4 line 472 |
| C-NOGENERIC: 0 generic relations | PASS | No `semantically_similar_to` or `conceptually_related_to` |
| C-LINKCOUNT: 131 links | PASS | Unchanged (promotion, not addition/deletion) |
| C-NOINFERRED: 0 below 0.85 | PASS | The only sub-0.85 edge (ISSUE-4 0.75) is now EXTRACTED |
| C-ORPHANS: 0 orphans | PASS | Node set unchanged |

**Final: 6/6 PASS**

### §6.4 — Post-patch edge quality

| Confidence tier | Count | % | Δ |
|---|---|---|---|
| EXTRACTED | 124 | 95% | +2 |
| INFERRED (all ≥ 0.85) | 7 | 5% | −2 |

### §6.5 — Run 4 status

**COMPLETE** — Both ISSUE-2 and ISSUE-4 resolved. Patch script `patch_run4_kg_audit.py` is idempotent. Step 1 status unchanged (STEP 1 — PASS).

---

## §7 — Run 5 (T-DOC-5 wiki update patch)

**Run date:** 2026-05-26
**Patch type:** Option 3 deterministic — enum expansion only
**Graph state before patch:** 74 nodes · 131 links · 9 communities · 3 hyperedges

### §7.1 — Wiki change

Commit `2be513e` (T-DOC-5): added `EGR_DILUTION_MISFIRE` + `INCOMPLETE_OXIDATION` to `ChemicalSignature Enum` in GAS_VOCABULARY.md §3. Bump v1.0 → v1.1. 8 insertions, 4 deletions.

### §7.2 — Patches applied

1. Added 2 nodes: `gas_vocab_cs_egr_dilution_misfire` (EGR_DILUTION_MISFIRE), `gas_vocab_cs_incomplete_oxidation` (INCOMPLETE_OXIDATION)
2. Added 2 `enumerates` edges: `ChemicalSignature Enum → EGR_DILUTION_MISFIRE`, `ChemicalSignature Enum → INCOMPLETE_OXIDATION`
3. Updated label: `ChemicalSignature Enum (28 values)` → `ChemicalSignature Enum (30 values)`
4. Note: attempted full `--update` re-extraction first — it created 142 nodes with duplicate IDs. Reverted to old graph and applied deterministic patch. Cache preserved; no semantic re-inference.

### §7.3 — Verification results

| Check | Result | Detail |
|---|---|---|
| C-ENUM: ChemSig Enum → 30 CS values | PASS | 30 outgoing enumerates (28 original + 2 new) |
| C-NEW1: EGR_DILUTION_MISFIRE present | PASS | Node + enumerates edge, source_location §3 |
| C-NEW2: INCOMPLETE_OXIDATION present | PASS | Node + enumerates edge, source_location §3 |
| C-LINKCOUNT: 133 links | PASS | 131 original + 2 new |
| C-NODECOUNT: 76 nodes | PASS | 74 original + 2 new |
| C-NOGENERIC: 0 generic relations | PASS | No semantically_similar_to or conceptually_related_to |
| C-NOORPHANS: 0 orphans | PASS | Both new nodes reachable via enumerates |
| C-NORMAL: NORMAL_OPERATION degree ≥ 3 | PASS | Lambda, TWC, Triangle — unchanged |
| C-DIRECTION: all enumerates source→target correct | PASS | No direction regression |

**Final: 9/9 PASS**

### §7.4 — Post-patch graph state

| Confidence tier | Count | % |
|---|---|---|
| EXTRACTED | 126 | 95% |
| INFERRED (all ≥ 0.85) | 7 | 5% |

**Communities:** 7 (down from 9; community detection shift due to topology change)

### §7.5 — Run 5 status

**COMPLETE** — 2 new CS enum values integrated. Step 1 remains PASS.
