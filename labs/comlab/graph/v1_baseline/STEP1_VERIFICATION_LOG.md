# COMLab Bootstrap Step 1 — Verification Log

**Run date:** 2026-05-22
**Spec:** `graphify-out/REEXTRACTION_SPEC.md` (v1.0, 2026-05-21)
**Graph state:** 48 nodes · 229 links · 0 hyperedges · 10 communities
**Backend:** Claude (general-purpose subagents)
**Extraction strategy:** augmented prompt per REEXTRACTION_SPEC §5, 2-chunk
family-coherent split (chunk_a: RM + MF + foundation; chunk_b: LC + SF + EF +
no_fault + foundation)

---

## §1 — Option 3 deterministic edge additions

No patches required. All 25 proof-set edges were emitted by the augmented
chunked extraction. No edges were inserted post-hoc.

| # | Edge | Action | Reason |
|---|---|---|---|
| — | — | — | All proof-set edges present after extraction (25/25) |

**Net edges added by §1:** 0

---

## §2 — Rebuild

- Build: `graphify.build.build_from_json(extraction, directed=True)` — directed
  graph (proof-set edges are directional).
- Community detection: `graphify.cluster.cluster(G)` — default Louvain
  parameters, not tuned. 10 communities detected.
- GRAPH_REPORT.md: regenerated.
- No per-community wiki articles generated (out of scope for T-PREP-1).

---

## §3 — Criteria verification

| # | Criterion | Result | Detail |
|---|---|---|---|
| C1 | Fault node coverage | **PASS** | 30/30 fault IDs present (28/30 required) |
| C2 | Family cluster nodes | **PASS** | 6/6 family slugs present as nodes |
| C3 | Differential sibling edges | **PASS** | 60 sibling edges (≥ 20 required) |
| C4 | No generic fault-to-fault relations | **PASS** | 0 `semantically_similar_to` / `conceptually_related_to` between fault nodes |
| C5 | Legacy alias links | **PASS** | 3/3 alias `maps_to` edges present (ERR-LC-005→ERR-E1-M032, ERR-MF-001→ERR-E2-I104, ERR-RM-005→ERR-E3-F501) |
| C6 | Cross-file coherence | **PASS** | 219 cross-file edges (≥ 10 required) |
| Proof-set | 25-edge recovery | **PASS** | 25/25 (≥ 18/25 required) |

**Final: 6/6 PASS, proof-set 25/25.**

### Relation distribution

```
   78  targets_horizon
   60  has_differential_sibling
   44  enumerates
   30  belongs_to_family
   14  describes
    3  maps_to
```

No `semantically_similar_to`, `conceptually_related_to`, `shares_data_with`,
or `references` relations anywhere in the graph — the augmented prompt's
explicit ban held.

---

## §4 — Spot-check (random.seed=42, 5 edges)

| # | Edge | Citation | Verdict |
|---|---|---|---|
| 1 | `err_lc_007 --has_differential_sibling--> err_lc_006` | `wiki/ERR-LC-007_SAI_Stuck_On.md` YAML.differential_siblings list contains `"ERR-LC-006"` | **PASS** |
| 2 | `err_rm_006 --belongs_to_family--> rich_mixture` | `wiki/ERR-RM-006_ECT_Sensor_Bias_Cold.md` YAML.fault_family = `rich_mixture` | **PASS** |
| 3 | `err_rm_002 --belongs_to_family--> rich_mixture` | `wiki/ERR-RM-002_Worn_Piston_Rings.md` YAML.fault_family = `rich_mixture` | **PASS** |
| 4 | `err_sf_004 --targets_horizon--> horizon_modern` | `wiki/ERR-SF-004_MAP_Sensor_Drift.md` YAML.target_horizons list contains `"HORIZON_MODERN"` | **PASS** |
| 5 | `err_mf_006 --has_differential_sibling--> err_rm_002` | `wiki/ERR-MF-006_Low_Compression_Misfire.md` YAML.differential_siblings list contains `"ERR-RM-002"` | **PASS** |

**Spot-check result: 5/5 PASS**

---

## §5 — Step 1 status

| Gate | Result |
|---|---|
| Criteria | **6 / 6 PASS** |
| Proof-set | **25 / 25** (threshold ≥ 18/25) |
| Spot-check | **5 / 5 PASS** |
| Truncation canary (ERR-SF-006) | **PASS** — node `err_sf_006` present, sourced from `wiki/ERR-SF-006_Downstream_O2_Contaminated.md` |
| Out-of-scope generic relations between fault nodes | **PASS** — zero |

**Step 1 complete.**

---

## §6 — Notes for downstream tasks

- 4 foundation-doc nodes are isolated by design (no incoming/outgoing edges):
  `comlab_diagnostic_logic`, `comlab_dna_architecture`, `comlab_horizon_eras`,
  `comlab_lab_input_reference`. These docs are reference material, not
  participants in the fault routing graph. Not a blocker for T-PREP-1.
- The graph captures `targets_horizon` edges to three horizon nodes
  (`horizon_legacy`, `horizon_adaptive`, `horizon_modern`) — 78 edges total,
  consistent with most fault profiles spanning multiple horizons.
- Per REEXTRACTION_SPEC §1, the primary KG data source for T-P2-1 remains the
  YAML frontmatter in each wiki `.md` file (direct parse). graph.json is
  retained for entity-inventory and cross-file coherence checks only.
