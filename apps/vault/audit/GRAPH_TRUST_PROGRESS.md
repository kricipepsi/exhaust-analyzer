# Graph-Trust Audit — Progress Ledger
**Pack:** `GRAPH_TRUST_AUDIT.md` (goal · taxonomy · seeded cases · cross-check design).
**Method spec (all `T-GTA-*` rows):** `T-GTA-METHOD.md` · **Reports:** `reports/<lab>__<agent>.md`.
**Mode:** STRICT (read-only audit; no code edits). **Last updated:** 2026-06-29 (architect, Cowork — **all 6 labs audited+unioned**; DNA/VIN unions done; **authored the 4 reconcile specs (GAS/OBD/DNA/VIN)** — now runnable. dtclab+comlab already reconciled. `T-WIRE-1` gated on the 4 reconciles). See patch log.

This is the only file `GRAPH_TRUST_START_HERE.md` reads to find the next task. Keep it
under ~120 lines. The audit is **read-only** — a `T-GTA-*` row is run by **each** owner
(its own report file), so the same target legitimately appears as three rows.

---
## Task log
| ID | Task file | Owner | Status | Blocked by | Date | Commit | Verification | Notes |
|---|---|---|---|---|---|---|---|---|
| T-VLIVE-3c | `T-VLIVE-3c_reconcile_dtclab_drift.md` | Codex | done | — | 2026-06-29 | 7e8688a | power_loss orphan ×4 map + ×4 live-mirror edges removed; perception relabeled → `rich_dtc_present`; notes 03/09 reconciled; map⇄frontmatter agree | **MUTATING** worked example. Committed: map + 6 dtclab notes. |
| T-GTA-COM·codex | `T-GTA-METHOD.md` | Codex | done | — | 2026-06-29 | 998aed6 | 108 edges classified: 99 LIVE / 2 MISLABEL / 1 ORPHAN / 6 PENDING; seeded case OK (none for comlab) | read-only → `reports/comlab__codex.md`. Audit `vault-map.comlab.yaml`. |
| T-GTA-COM·agy | `T-GTA-METHOD.md` | Agy | done | — | 2026-06-29 | 18e8394 | 108 edges: 98 LIVE / 3 MISLABEL / 1 ORPHAN / 6 PENDING; seeded OK (none for comlab) | read-only → `reports/comlab__agy.md`. |
| T-GTA-COM·claude | `T-GTA-METHOD.md` | Claude | done | — | 2026-06-29 | 3d30db3 | 108 edges: 99 LIVE / 2 MISLABEL / 0 ORPHAN / 7 PENDING; seeded OK (none for comlab) | read-only → `reports/comlab__claude.md`. MISLABELs: note02 ecu_hardware_checker `vin_dna` + aggregator `engine_state`. |
| T-GTA-UNION-COM | `reports/comlab__UNION.md` | Architect | done | T-GTA-COM·codex, T-GTA-COM·agy, T-GTA-COM·claude | 2026-06-29 | (pending) | 5 consumer-edge drifts unioned (D1-D5): agree 3/3,2/3,2/3,1/3,1/3; all ruled MISLABEL after code-verify; 0 true orphans, 0 demotions | Merged 3 comlab reports → canonical drift list. Hand-off → `T-GTA-RECONCILE-COM`. |
| T-GTA-RECONCILE-COM | `T-GTA-RECONCILE-COM_reconcile_comlab_drift.md` | Codex | done | T-GTA-UNION-COM | 2026-06-29 | c3e4453 | 5 consumer edges relabeled (D1-D5): ecu_hw vin_dna→OBD-rails; aggregator engine_state→symptom_router; RULE_HW_PRUNE→scoring-evidence; DNA-confidence→vin_confidence NONE gate; symptom_router prior→fault_atlas_router; map⇄wiki 02/03/10 agree; 0 orphaned notes | **MUTATING.** Relabel-only: 5 comlab consumer edges (map + wiki 02/03/10 frontmatter) per union D1-D5. No Python, no graphify. Gate: comlab GREEN for T-WIRE-1. |

| T-GTA-GAS·codex | `T-GTA-METHOD.md` | Codex | done | — | 2026-06-29 | b3d2162 | 156 edges classified: 155 LIVE / 0 MISLABEL / 1 ORPHAN / 0 PENDING; seeded case OK | read-only → `reports/gaslab__codex.md`. Audit `vault-map.gaslab.yaml`. |
| T-GTA-GAS·agy | `T-GTA-METHOD.md` | Agy | done | — | 2026-06-29 | dcd2707 | 156 edges classified: 155 LIVE / 0 MISLABEL / 1 ORPHAN / 0 PENDING; seeded case OK | read-only → `reports/gaslab__agy.md`. |
| T-GTA-GAS·claude | `T-GTA-METHOD.md` | Claude | done | — | 2026-06-29 | 51ed97e | 156 edges classified: 155 LIVE / 0 MISLABEL / 1 ORPHAN / 0 PENDING; seeded case OK (none for gaslab; power_loss_analytics LIVE here vs ORPHAN in dtclab) | read-only → `reports/gaslab__claude.md`. ORPHAN: note10 aggregator "chemistry confidence input" (confidence is horizon/VIN-derived only). |
| T-GTA-UNION-GAS | `reports/gaslab__UNION.md` | Architect | done | — | 2026-06-29 | (uncommitted) | 3 reports unioned; 1 drift G1 = 3/3 ORPHAN (note10 chemistry-confidence input, code-verified: aggregator confidence is horizon/VIN only) → demote 1 comlab edge; 0 MISLABEL, 0 notes demoted | Hand-off → `T-GTA-RECONCILE-GAS` (to author). Union file untracked — owner commits by path. |
| T-GTA-OBD·codex | `T-GTA-METHOD.md` | Codex | done | — | 2026-06-29 | 5c7a636 | 62 edges classified: 56 LIVE / 5 MISLABEL / 1 ORPHAN / 0 PENDING; seeded OK (none for obdlab) | read-only → `reports/obdlab__codex.md`. Audit `vault-map.obdlab.yaml`. |
| T-GTA-OBD·agy | `T-GTA-METHOD.md` | Agy | done | — | 2026-06-29 | fa399f8 | 62 edges classified: 58 LIVE / 4 MISLABEL / 0 ORPHAN / 0 PENDING; seeded case OK | read-only → `reports/obdlab__agy.md`. |
| T-GTA-OBD·claude | `T-GTA-METHOD.md` | Claude | done | — | 2026-06-29 | be872c5 | 62 edges classified: 56 LIVE / 4 MISLABEL / 2 ORPHAN / 0 PENDING; seeded OK (none for obdlab; unwired-but-tested consumers held LIVE) | read-only → `reports/obdlab__claude.md`. ORPHANs: pids-protocol+taxonomy → `fault_atlas_kg.py` (pure KG loader, 0 OBD reads). MISLABELs: delta-relations ve_engine→power_loss/perception (real reader `fault_atlas_router`); taxonomy+truth-perception → `symptom_router` (reads only engine_state). |
| T-GTA-UNION-OBD | `reports/obdlab__UNION.md` | Architect | done | — | 2026-06-29 | (uncommitted) | 3 reports unioned; 6 consumer drifts D1-D6 all ruled MISLABEL after code-verify (D2/D3/D5 ORPHAN votes collapsed; `fault_atlas_kg.py` = generic KG loader, 0 OBD reads); 0 true ORPHANs, 0 notes demoted | Hand-off → `T-GTA-RECONCILE-OBD` (to author). Union file untracked — owner commits by path. |
| T-GTA-DNA·codex | `T-GTA-METHOD.md` | Codex | done | — | 2026-06-29 | 3325fe6 | 37 edges classified: 35 LIVE / 2 MISLABEL / 0 ORPHAN / 0 PENDING; seeded case OK | read-only → `reports/dnalab__codex.md`. MISLABELs: DLD/11 schema-version consumers point at `schemas/ingestion.py` field definition; real gate/read is `core/lab_pipeline_aggregator.py` `request.metadata.schema_version`. |
| T-GTA-DNA·agy | `T-GTA-METHOD.md` | Agy | done | — | 2026-06-29 | 022ff4d | 38 edges — 36 LIVE / 2 MISLABEL / 0 ORPHAN / 0 PENDING; seeded OK | read-only → `reports/dnalab__agy.md`. Same map; reproduce the dnalab seeded case. |
| T-GTA-DNA·claude | `T-GTA-METHOD.md` | Claude | done | — | 2026-06-29 | (pending) | 38 edges — 38 LIVE / 0 MISLABEL / 0 ORPHAN / 0 PENDING; seeded OK (VehicleDNA readers from_vehicle_dna + projection.project LIVE, unwired≠orphan) | read-only → `reports/dnalab__claude.md`. Map⇄frontmatter agree (notes 10/11/12/13). |
| T-GTA-UNION-DNA | `reports/dnalab__UNION.md` | Architect | done | — | 2026-06-29 | (uncommitted) | 3 reports unioned; seeded VehicleDNA case PASS 3/3 (LIVE); 1 drift N1/N2 = 2/3 MISLABEL (schema_version edge: `ingestion.py` defines field, gate is `check_schema_version`); 0 ORPHAN | Hand-off → `T-GTA-RECONCILE-DNA`. Union file untracked — owner commits by path. |
| T-GTA-VIN·codex | `T-GTA-METHOD.md` | Codex | done | — | 2026-06-29 | 5d91037 | 72 edges classified: 70 LIVE / 2 MISLABEL / 0 ORPHAN / 0 PENDING; seeded case OK (none for vinlab); map⇄frontmatter agree | read-only → `reports/vinlab__codex.md`. Audit `vault-map.vinlab.yaml` (72 edges, 7 notes). No seed; watched `vin_confidence` semantics (comlab D4 was a 1/3 catch). |
| T-GTA-VIN·agy | `T-GTA-METHOD.md` | Agy | done | — | 2026-06-29 | 3f535b3 | 72 edges — 70 LIVE / 2 MISLABEL / 0 ORPHAN / 0 PENDING; no seeded case | read-only → `reports/vinlab__agy.md`. Same map. |
| T-GTA-VIN·claude | `T-GTA-METHOD.md` | Claude | done | — | 2026-06-29 | 245c75e | 72 edges — 70 LIVE / 2 MISLABEL / 0 ORPHAN / 0 PENDING; no seeded case. MISLABEL: LLD+DLD `fault_atlas_router (FuelSystemStatus.CL :294)` names an OBD enum read; real vinlab read is `vin_confidence` :2239 → repoint. | read-only → `reports/vinlab__claude.md`. Same map. |
| T-GTA-UNION-VIN | `reports/vinlab__UNION.md` | Architect | done | — | 2026-06-29 | (uncommitted) | 3 reports unioned; 1 drift V1/V2 = 3/3 MISLABEL (FuelSystemStatus.CL gate reads OBD, not vinlab → repoint to `vin_confidence` :2239); 0 ORPHAN | Hand-off → `T-GTA-RECONCILE-VIN`. Union file untracked — owner commits by path. |
| T-GTA-RECONCILE-GAS | `T-GTA-RECONCILE-GAS_reconcile_gaslab_drift.md` | Claude | done | — | 2026-06-29 | (pending) | 1 ORPHAN consumer edge removed (G1 chemistry-confidence input); note 10 retains LIVE consumers (2 gaslab self-consumers); map⇔wiki agree | **MUTATING**, demote-only. Reassigned Codex→Claude by manager. Files changed=3 (map + `gaslab/wiki/10` + ledger). No Python, no graphify. |
| T-GTA-RECONCILE-OBD | `T-GTA-RECONCILE-OBD_reconcile_obdlab_drift.md` | Agy | done | — | 2026-06-29 | b20a80c | 6 consumer edges relabeled (D1-D6): delta-relations x2 -> delta_engine; fault_atlas_kg x2 -> fault_atlas_router; symptom_router x2 -> router (era/injector + capped prior); map<=>4 notes agree; 0 orphaned | **MUTATING**, relabel-only. 6 edges D1-D6. Files: map + 4 `obdlab/research/chunks/*/README.md`. After `T-GTA-UNION-OBD` (done). |
| T-GTA-RECONCILE-DNA | `T-GTA-RECONCILE-DNA_reconcile_dnalab_drift.md` | Codex | done | — | 2026-06-29 | d6bb63a | 1 consumer edge relabeled on 2 notes (N1/N2 schema_version -> aggregator check_schema_version); seeded VehicleDNA untouched; map<=>notes agree | **MUTATING**, relabel-only. 1 edge ×2 notes (schema_version → `check_schema_version`). Files: map + `dnalab/docs/DLD` + `dnalab/wiki/11`. After `T-GTA-UNION-DNA` (done). |
| T-GTA-RECONCILE-VIN | `T-GTA-RECONCILE-VIN_reconcile_vinlab_drift.md` | Agy | done | — | 2026-06-29 | 14a29c2 | 1 consumer edge relabeled on 2 notes (V1/V2 FuelSystemStatus OBD gate -> vin_confidence :2239); map<=>notes agree; 0 orphaned | **MUTATING**, relabel-only. 1 edge ×2 notes (FuelSystemStatus → `vin_confidence` :2239). Files: map + `vinlab/docs/{LLD,DLD}`. After `T-GTA-UNION-VIN` (done). |
| T-WIRE-1 | `apps/wired/wired_tasks/T-WIRE-1_compose_labs_comlab.md` | Codex | done | T-GTA-RECONCILE-GAS, T-GTA-RECONCILE-OBD, T-GTA-RECONCILE-DNA, T-GTA-RECONCILE-VIN | 2026-06-29 | 52210e1 | diagnose() returns `OrchestratorFinalUIOutput`; high-idle forwarded; no deferred path; guard=73; pytest 2 passed | **GATE CLEARED.** dtclab (T-VLIVE-3c), comlab (RECONCILE-COM), and gas/obd/dna/vin reconciles are GREEN; wired T-WIRE-2/T-WIRE-3 promoted in `apps/wired/WIRED_PROGRESS.md`. |
**Status values:** `pending` · `in_progress` · `done` · `blocked` · `deferred`.
**Runnability:** `pending` = runnable now. Each owner picks the **first `pending` row whose
`Owner` = its own agent id** (codex/agy/claude); `deferred`/`blocked` skipped. One row per session.

---
## Deferred waves (promote one lab at a time, after the prior union is `done`)
comlab is the first target (above) — it is the largest, most-consumed map and the one
the wiring composes against. When `T-GTA-UNION-COM` is `done`, promote the next lab by
adding its three `T-GTA-<LAB>·{codex,agy,claude}` rows + a `T-GTA-UNION-<LAB>` row, in
this priority order (wiring-critical first):

1. **gaslab**, **obdlab** — emitter labs the composition consumes.
2. **dnalab**, **vinlab** — DNA/VIN inputs. (dtclab handled by `T-VLIVE-3c`.)
3. **symptomlab**, **registry** — lower-risk; may **partition** (one agent each) instead of 3×.

**Promoted 2026-06-29 (architect):** wave 1 (**gaslab** + **obdlab**) unioned (`done`); **wave 2 (**dnalab** + **vinlab**) promoted** — both run **3×** (full cross-check: dnalab has a seeded case, vinlab's `vin_confidence` was a 1/3 catch in comlab — partition not advised). symptomlab/registry (wave 3) are **not** in the `T-WIRE-1` gate — optional, may partition.

Final: `T-GTA-RECONCILE` — one architect-reviewed pass applying every union's
ORPHAN/MISLABEL fixes. Blocked until the promoted unions are `done`. **Gate:** do not mark
`T-WIRE-1` runnable until dtclab + gas/obd + dnalab/vinlab + comlab read GREEN here.

---
## Unplanned follow-ups
| ID | Discovered in | One-liner | Status |
|---|---|---|---|
| — | — | — | — |

---
## Architect-level out-of-band patches
| Date | File | Patch | Reason |
|---|---|---|---|
| 2026-06-29 | `apps/vault/audit/T-GTA-RECONCILE-{GAS,OBD,DNA,VIN}_*.md`, `GRAPH_TRUST_PROGRESS.md`, `.agent/assignments.md` | Unioned dnalab+vinlab (done); **authored the 4 per-lab reconcile specs** (relabel/demote-only, STRICT); added their ledger rows + a `T-WIRE-1` gate row blocked on all 4. | All 6 gate-lab audits unioned → the fixes are the last step before wiring; per-lab specs keep diffs small + parallel (independent maps). |
| 2026-06-29 | `GRAPH_TRUST_PROGRESS.md`, `.agent/assignments.md` | Unioned GAS+OBD (both `done`); promoted **wave 2 dnalab+vinlab** as runnable **3×** audits (6 coder rows + 2 union rows); cleaned stale `T-VLIVE-3c` Active pointer. | Both emitter unions done → wave-2 gate inputs (DNA/VIN feed the COMLab prior) are next; 3× kept (dnalab seeded, vinlab vin_confidence subtle). |
| 2026-06-29 | `apps/vault/audit/**`, `.agent/assignments.md`, `apps/vault/VAULT_LIVE_PROGRESS.md` | Authored the Graph-Trust audit pack (START_HERE + ledger + method + T-VLIVE-3c) after `EVAL-VLIVE-1` exposed framed-graph drift. | Make the framed graph trustworthy before `T-WIRE-1` wires the labs. |
| 2026-06-29 | `apps/vault/audit/GRAPH_TRUST_PROGRESS.md` | Promoted wave-1 emitter labs: added `T-GTA-GAS`+`T-GTA-OBD` (3 coder rows + union each), runnable. | comlab+dtclab GREEN; gas/obd are the next wiring-gate emitter maps the composition consumes. Surfaced from the doc↔code drift review. |
