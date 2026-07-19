---
node_type: task
task_id: T-DTC-DOCS-V2
status: done
pack: VAULT
lab: dtclab
mode: architect/author lane
blocked_by: []
consumers:
- COMLab analytics / fault-atlas routing
tags:
- task
- vault
- dtclab
---


# T-DTC-DOCS-V2 — Reconcile the six DTCLab design docs to the shipped v2 code

**Status:** `done` (2026-06-11) · **Pack:** VAULT (DTCLab) · **Mode:** architect/author lane (design-doc authoring, no inner-loop)
**Origin:** pipeline guide §3·1D (PRD-refresh model) · **Blocked by:** —
**Consumer (signal/noise):** **Adds no schema field.** The reconciled docs are the source corpus for
`T-DTC-DOCPREP` → the (waived) docs graph and, more importantly, the **vault docs tier**: every framed
design-doc note's `implements`/`consumers` frontmatter is derived from these docs' named COMLab
consumers. Docs that describe a superseded design would inject wrong frontmatter — so the consumer here
is the vault build's docs-tier frontmatter derivation.

### What was done (this session) ###

The six design docs were reconciled to the shipped `dtclab/` package (AST ground truth, June 2026),
following the OBDLab PRD-refresh model. The drift corrected:

- Routing surface **17 → 18** `DTCRoutingTag` values: dropped the never-shipped `SAI_HISTORY`; added
  `COOLANT_SYSTEM_MALFUNCTION` and `CYLINDER_FLUID_MISFIRE`.
- `DtcEmissionsView` **4 → 3** fields (no `secondary_air_equipped`).
- DNA-gated routing entries **6 → 5**; routing map = 32 entries (27 ungated + 5 gated).
- Documented two previously-undocumented package-root modules: `ranking.py` (Phase-2 scorer —
  `MatchType`, `CandidateScore`, `rank_candidates`/`classify_top3`; consumer = COMLab Bayesian
  `combine()` (FU-1) via the Wired adapter `T-DTW-1`) and `family_map.py` (16-family canonical map).
- Documented pipeline **step 5b** (`evaluate_coolant_dtc_context`).
- Recorded `EP-DTC-NOSTART-1` as a **labelled Proposed** item (consumer COMLab `T-COMV2-NOSTART-1`).

### Deliverables ###

- `labs/dtclab/docs/HLD_DTCLab.md` — rewritten v1.0 → v2.0.
- `labs/dtclab/docs/DLD_DTCLab.md` — rewritten v1.0 → v2.0.
- `labs/dtclab/docs/LLD_DTCLab.md` — rewritten v1.0 → v2.0.
- `labs/dtclab/docs/PRD_DTCLab.md` — refreshed v1.0 → v2.0 (+ proposal §8).
- `labs/dtclab/docs/ADR_DTCLab.md` — **new** (9 Nygard records; ADR-0009 = `EP-DTC-NOSTART-1` Proposed).
- `labs/dtclab/docs/BDD_DTCLab.md` — **new** (Gherkin scenarios mapped to real test files).
- `labs/dtclab/docs/DTC_VOCABULARY.md` — surgical fixes only (18-tag labels; SAI sentence removed;
  section numbers untouched because code cites them).

### Verification (completed) ###

- No image placeholders in any `docs/*.md` (`grep -rl '!\[\]\['`).
- Counts cross-checked vs code/config: 32 YAML entries, 5 `dna_gate` lines, 18 `DTCRoutingTag` members,
  3 `DtcEmissionsView` bool fields, 33 Mode $06 MIDs, exactly 3 named HIGH gates.
- Referenced scorer test files exist (`test_rank_candidates.py`, `test_classify_top3.py`, `test_family_map.py`).
- No stale live claims (`17 routing`, `6 DNA-gated`, `26 ungated`) remain; all `SAI`/`secondary_air`
  mentions are intentional removal notes.

### Out of scope (carried to follow-ups) ###

- The two stale **code** docstrings (`vocabulary.py` "17-value", `family_map.py` "19-value") — split to
  `T-DTC-COMMENT-FIX` (coder lane; docs describe the real 18, code comments lag).
- GPF out-of-era reconciliation (`wiki/11_proposals_register.md §11.4`) — owner follow-up, START_HERE §5.

### Progress hook ###

`Vault/tasks/progress_notes/T-DTC-DOCS-V2.md` records the reconciliation deltas and the verification
results above. Row is `done`: the contracted deliverable (six current v2 design docs + fixed vocab) is met.
