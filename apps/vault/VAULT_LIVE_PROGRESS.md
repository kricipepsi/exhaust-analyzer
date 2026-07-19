# vault-live — Progress Ledger

**Pack goal:** make the three `.base` audit views (`modules`, `consumers`,
`drift-guards`) render against the **live `labs/` tree** in Obsidian-on-root, with
every framed note carrying ≥1 **named** consumer. No mirror build; the live notes
are the graph. (Implements Phase 3 of `apps/OMP_VAULT_HARNESS_PLAN_2026-06-28.md`.)

**Tasks dir:** `apps/vault/vault_live_tasks/`
**Mode:** STRICT (dual-gate: VERIFICATION GATE + CODE REVIEW), vault-tooling lane.
**Domain skill:** `_skills/graph/4dlab-vault/` (schema + views + per-lab maps).
**Last updated:** 2026-06-28 (architect, Cowork — pack authored)

This is the only file `VAULT_LIVE_START_HERE.md` reads to find the next task. Keep
it under ~120 lines. Gate blocks go in `vault_live_tasks/progress_notes/<id>.md`.

---

## Task log

| ID | Task file | Status | Blocked by | Date | Commit | Verification | Notes |
|---|---|---|---|---|---|---|---|
| T-VLIVE-1 | `T-VLIVE-1_pilot_obdlab_live.md` | done | — | 2026-06-28 | 2cea8d2 | `_bases/` identical; `Vault/` ignored; 11 obdlab notes framed; consumers missing=0; drift rows=9; pytest 388 passed, 2 skipped; graph clean. | Map-authored corpus is 4 design docs + 7 wiki READMEs; non-map docs left plain. Test path resolver updated for live `docs/Vocabulary`. |
| T-VLIVE-2 | `T-VLIVE-2_frame_gaslab_live.md` | done | T-VLIVE-1 | 2026-06-28 | 6745503 | 15 gaslab notes framed; consumers missing=0; drift rows=13; pytest 208 passed, 2 skipped, 4 deselected; graph clean. | Wiki chunk frontmatter merged into single `§4` blocks; `code/` paths remapped to live `gaslab/`; plain-map notes left unframed. |
| T-VLIVE-3 | `T-VLIVE-3_frame_dtclab_live.md` | done | T-VLIVE-1,T-VLIVE-3b | 2026-06-29 | 5c1ef40 | 15 dtclab notes framed; consumers missing=0; drift rows=13; pytest 590 passed; graph clean. | Map-authored corpus is 4 design docs + 11 wiki notes; plain-map notes left unframed. |
| T-VLIVE-3b | `T-VLIVE-3b_reconcile_dtclab_wired_map.md` | done | — | 2026-06-29 | 3c8a136 | phantom dtw.py/T-DTW-1 edges removed; note 12 → live fault_atlas_router discriminator; LLD/DLD → pending composition.py edge; T-VLIVE-3 unblocked | Architect-lane map fix (blocks T-VLIVE-3). Drop phantom `dtw.py`/`T-DTW-1` edges; note 12 → live `fault_atlas_router` discriminator; LLD/DLD → `apps/wired/wired/composition.py (pending T-WIRE-1)`. |
| T-VLIVE-4 | `T-VLIVE-4_frame_dnalab_live.md` | done | T-VLIVE-1,T-VLIVE-4b | 2026-06-29 | d065fda | 8 dnalab notes framed; consumers missing=0; drift rows=6; pytest 27 passed; graph clean. | Map-authored corpus is 4 design docs + 4 wiki notes; chunk frontmatter merged; plain-map notes left plain. |
| T-VLIVE-4b | `T-VLIVE-4b_reconcile_dnalab_comlab_map.md` | done | — | 2026-06-29 | 53adc13 | vehicle_dna edges → horizon_context_injector/projection; schema-version → SessionMetadata.schema_version; session correlation → aggregator session_id; T-VLIVE-4 unblocked | Architect-lane map fix (blocks T-VLIVE-4). Naming fix (no deleted path): `vehicle_dna` → `horizon_context_injector.from_vehicle_dna` + `projection.py`; schema-version gate → `SessionMetadata.schema_version`; session correlation → aggregator `session_id`. No note demoted. |
| T-VLIVE-5 | `T-VLIVE-5_frame_vinlab_live.md` | done | T-VLIVE-1,T-VLIVE-5b | 2026-06-29 | 675c7f9 | 7 vinlab notes framed; consumers missing=0; drift rows=5; pytest 194 passed; graph clean. | Map-authored corpus is 4 design docs + 3 wiki notes; chunk frontmatter merged; plain-map notes left plain. |
| T-VLIVE-5b | `T-VLIVE-5b_reconcile_vinlab_map.md` | done | — | 2026-06-29 | 8527c94 | stale edges removed; assembly.py/aggregator/perception_contradiction targets repointed; T-VLIVE-5 unblocked | Architect-lane map fix (blocks T-VLIVE-5). Naming fix (no deleted path): decode_vin_payload -> build_vehicle_dna; VinDNA/rated_rpm -> projection.py; FuelSystemStatus -> fault_atlas_router. CL. No note demoted. |
| T-VLIVE-6 | `T-VLIVE-6_frame_symptomlab_live.md` | done | T-VLIVE-1 | 2026-06-28 | 128875e | 9 symptomlab notes framed; consumers missing=0; drift rows=6; pytest 63 passed; graph clean. | Wiki chunk frontmatter merged into single `§4` blocks; live package paths resolved; plain-map notes left unframed. |
| T-VLIVE-8 | `T-VLIVE-8_frame_comlab_live.md` | done | T-VLIVE-1 | 2026-06-28 | 67e730c | 12 comlab notes framed; consumers missing=0; drift rows=10; pytest 510 passed; graph clean. | Wiki chunk frontmatter merged into single `§4` blocks; wired consumers marked pending T-WIRE-1; plain-map notes left unframed. |
| T-VLIVE-9 | `T-VLIVE-9_frame_registry_schema_audit.md` | done | T-VLIVE-1 | 2026-06-28 | pending | 25 registry notes framed; consumers missing=0; drift rows=25; pytest 483 passed; graph clean. | Registry part 1 (~25 notes: SCHEMA_V2_SPEC + CHEMISTRY_COVERAGE + REGISTRY_AUDIT). Registry-specific remap: `registry/code/X`→`registry/X` (no `registry/registry/`). Promoted after T-VLIVE-1 `done`. |
| T-VLIVE-10 | `T-VLIVE-10_frame_registry_corpus_cases.md` | done | T-VLIVE-9 | 2026-06-29 | 43cda9d | 28 registry notes framed; consumers missing=0; drift rows=28; pytest 483 passed; graph clean. | Registry part 2 (28 notes: case_library + CORPUS_AUDIT). Remapped registry paths to drop mirror's code/ tier. |
| T-VLIVE-11 | `T-VLIVE-11_frame_vocabulary_live.md` | done | T-VLIVE-1 | 2026-06-29 | 76057e1 | 7 vocabulary notes framed; consumers missing=0; drift rows=7; pytest passed; graph clean. | Framed notes: OBD, GAS, DTC, SYMPTOM, VIN, DNA, SEMANTIC_CONTRACT. Remapped implements/drift_guards to live directories. |
| T-VLIVE-7 | `T-VLIVE-7_verify_bases_provenance.md` | done | T-VLIVE-2,T-VLIVE-3,T-VLIVE-4,T-VLIVE-5,T-VLIVE-6,T-VLIVE-8,T-VLIVE-9,T-VLIVE-10,T-VLIVE-11 | 2026-06-29 | pending | 137 notes framed; zero MISSING consumers; drift rows=122; pytest all passed; graph clean. | Cross-lab gate: all 137 framed notes verified; bases render from live; _bases/PROVENANCE.md written; Vault/ is ready to be archived. |

**Status values:** `pending` · `in_progress` · `done` · `blocked` · `deferred`
**Blocked by:** comma-separated task IDs that must reach `done` first, or `—`.

**Runnability convention.** `pending` = runnable now (spec authored, every
`Blocked by` is `done`). A forward-registered/unauthored placeholder stays
`deferred`, never `pending`. The guard takes the **first `pending` row
top-to-bottom**; `deferred`/`blocked` are skipped. **T-VLIVE-1 is the first
runnable task;** T-VLIVE-2…6 are authored but `deferred` until the pilot proves
the bases render on live; T-VLIVE-7 waits on all six labs.

---

## Unplanned follow-ups
Issues discovered mid-task. Logged here, not fixed in the session that found them.

| ID | Discovered in | One-liner | Status |
|---|---|---|---|
| GRAPH-TRUST | EVAL-VLIVE-1 | Framed graph carries drift (orphan/mislabel edges) — systematic map↔code audit before T-WIRE-1. Pack: `apps/vault/audit/GRAPH_TRUST_AUDIT.md`. | pending |
| T-VLIVE-3c | EVAL-VLIVE-1 | dtclab `power_loss_analytics` orphan ×8 + `perception_contradiction` mislabel — audit+fix. Spec: `apps/vault/audit/T-VLIVE-3c_reconcile_dtclab_drift.md`. | pending |

---

## Deferred (out of this pack — named for the next pack)

| ID | Item | Why deferred |
|---|---|---|
| T-VLIVE-UI-* | Frame the `apps/ui` design corpus (2 notes) | **Schema resolved** (`node_type: design` now legal; `.base` views filter on `node_type` *presence*, so no base edit needed — ui would show in `consumers.base`, and `modules.base` already matches `apps/ui` via `hasProperty("module")`... but its `inFolder("labs")` clause excludes it). **Real blocker (signal/noise):** ui's named consumers are a *pending* UI (`T-WV2-UI-*`) and point at the **deleted** `apps/wiredV2/` — they don't resolve to a live read, so framing fails the anti-orphan gate. **Prereqs:** (1) the wired UI exists; (2) repoint `vault-map.ui.yaml` consumers `wiredV2`→`wired`. Until then ui stays a plain (unframed) design corpus. |

---

## Architect-level out-of-band patches

| Date | File | Patch | Reason |
|---|---|---|---|
| 2026-06-28 | `apps/vault/**` + root `CLAUDE.md` | Authored the vault-live pack (Phase 3) and inserted the `## Session bootstrap` row for vault-live into root `CLAUDE.md`. | Move the consumer/drift-guard transparency views off the `Vault/` copy-mirror onto the live tree (Option A). |
| (pending) | `Vault/` → `ARCHIVE/2026-06-2x_vault-mirror/` | Archive the copy-mirror once T-VLIVE-7 confirms the live bases stand alone. | Mirror superseded by the live-root view; archive (never delete) per the five rules. Architect-lane (coders are blocked from editing `Vault/`). |
