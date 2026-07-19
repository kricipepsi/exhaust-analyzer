---
node_type: task
task_id: T-COM-WIKIPREP
status: done
pack: VAULT
lab: comlab
mode: architect/author lane
blocked_by: []
consumers:
- COMLab analytics / fault-atlas routing
- apps/4DLabWired (LabPipelineAggregator consumer)
tags:
- task
- vault
- comlab
---

# T-COM-WIKIPREP — Make wiki relations explicit (`4dlab-wiki-prep` on `labs/comlab/wiki/`)

**Status:** `done` · **Pack:** VAULT (COMLab) · **Mode:** architect/author lane (graph-tooling; no lab inner-loop)
**Origin:** pipeline guide §4 (wiki prep) · **Blocked by:** — (wiki is current as of 2026-06-21)
**Load skills:** `comlab-verification-loop`, **`4dlab-wiki-prep`**, **`comlab-vault-prep`**.
**Consumer (signal/noise):** **Adds no schema field.** Appends append-only trailer blocks making implied
wiki relations **explicit**. Even with the prose graph **waived** this pack, the explicit `CONSUMES`/
`VERIFIES` lines are the signal/noise surface the vault wiki frontmatter leans on — every such line names a
**real, existing** consumer (COMLab-internal analytics/routing, or the `apps/4DLabWired/` reader). No new fields.

### Role note ###

`4dlab-wiki-prep` runs `relations → labels → roster → verify`. It is **append-only** (trailer blocks +
canonical entity labels); it does **not** move/rename `wiki/` (graph-canonical at source) and never runs
graphify. `comlab-vault-prep` Rules 1, 2 and 4 govern the consumer framing and folder discipline here.

### Scope ###

- `labs/comlab/wiki/` — **15 chunks** `00_index.md`, `01_role_boundaries_fusion_spine.md`,
  `02_lab_input_contract.md`, `03_vehicle_dna_pruning.md`, `04_horizon_eras.md`, `05_fault_taxonomy.md`,
  `06_fault_atlas_families.md`, `07_pipeline_stages.md`, `08_scoring_to_fusion_rework.md`,
  `09_calibration_confidence.md`, `10_differential_and_symptom_prior.md`, `11_two_point_delta.md`,
  `12_corpus_eval_discipline.md`, `13_proposals_register.md`, `14_sources_appendices.md`.
- Make each implied relation explicit as `**SUBJECT** PREDICATE **OBJECT**`: `<input verdict field>
  CONSUMED-BY <COMLab path>`; `<fault taxonomy node> ROUTED-BY <fault_atlas_router family>`;
  `<pipeline stage> IMPLEMENTED-BY <core module>`; `<output> RENDERED-BY <apps/4DLabWired path>`.

### Signal/noise at the edge (critical — COMLab is the terminal spine) ###

- Every `CONSUMES`/`VERIFIES` names a real, existing path/test. The downstream consumer of a COMLab note is
  **COMLab-internal** (`analytics/`, `core/fault_atlas_router.py`, `core/lab_pipeline_aggregator.py`) or
  the **app layer** (`apps/4DLabWired/` `from comlab import LabPipelineAggregator`) — **never another lab**
  (those are inputs). Grep-confirm before framing; orphans are flagged, not shipped.
- **Proposals stay labelled proposals.** `13_proposals_register.md` and any `comlab/config/proposals/`
  token (`COMLab-DELTA`, `EP-*`) must remain `PROPOSAL`; default-off flag-gated capability
  (`enable_delta`/`enable_fatal_gates`) is noted flag-gated, never an always-live edge.
- **Scope spot-check:** at `03_vehicle_dna_pruning.md:52` confirm the `SAI stuck on` (`ERR-LC-007`) enable
  is an in-era residual (1990–2010 Euro 1–5), not a 2010–2020 perk leak (START_HERE §5). If a leak, route a
  one-line architect wiki fix — do not silently promote or delete.

### Success criteria ###

1. `4dlab-wiki-prep relations → labels → roster → verify` run over all 15 chunks; trailer blocks appended.
2. Every appended `CONSUMES`/`VERIFIES` names an existing path/test; **zero orphans** (or each routed back
   as a prep gap); no other lab appears as a COMLab consumer.
3. Proposals remain labelled; no proposal/flag-gated token appears as a live consumer edge.
4. Canonical entity labels consistent across chunks (`OrchestratorInboundRequest`, `FaultAtlasRouter`,
   `LabPipelineAggregator`, `ChemicalSignature`, `Horizon`); `verify` clean.
5. Source files unmoved/unrenamed; diffs are append-only trailer blocks.

### Out of scope ###

- Running graphify (prose Pass-3 **waived** — START_HERE §1) · editing `docs/Vocabulary/*` (vocab tier) ·
  promoting any proposal · code changes. **GRAPH GUARDRAIL:** no graphify.

### Files to touch ###

- `labs/comlab/wiki/*.md` — append-only relation/label trailer blocks (skill convention).

### Verification ###

```bash
cd <repo>/labs/comlab
grep -rln 'PROPOSAL' wiki/ | head
grep -rn 'CONSUMES\|VERIFIES' wiki/ | wc -l
grep -rn 'CONSUMED-BY .*labs/\(gaslab\|obdlab\|dtclab\|dnalab\)' wiki/ && echo "FAIL lab-as-consumer" || echo "OK terminal-spine"
```

### Progress hook ###

`Vault/tasks/progress_notes/T-COM-WIKIPREP.md` opens with the confirmed `## Plan` (chunk roster); the run
session fills `VERIFICATION GATE` (15 chunks prepped, zero orphans, proposals labelled, no lab-as-consumer,
SAI residual confirmed) + `CODE REVIEW` (relation counts, label consistency). Ledger row → `done` only when
the block is clean.
