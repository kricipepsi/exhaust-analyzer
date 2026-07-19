# T-GTA-RECONCILE-COM — Reconcile comlab consumer drift (relabel pass)
**Pack:** GRAPH-TRUST (`GRAPH_TRUST_AUDIT.md`) · **Lane:** vault-tooling / architect-authoring · **Mode:** STRICT
**Owner:** Codex (single mutating task — edits the map; not 3x, to avoid an edit race). Architect may reassign.
**Blocked by:** `T-GTA-UNION-COM` (done — `reports/comlab__UNION.md`).
**Load skills:** `_skills/graph/4dlab-vault/SKILL.md`, `_skills/graph/4dlab-doc-prep/SKILL.md`.

### Goal ###
Relabel the **five** drifted `consumers` edges in `vault-map.comlab.yaml` (and their
mirror in the live-note frontmatter of wiki notes 02/03/10) so every comlab consumer edge
names a symbol that actually reads the named field/behaviour. The union
(`reports/comlab__UNION.md`, rows D1-D5) already classified and code-verified each one;
this task **applies** those dispositions. It is **relabel-only** — no Python, no new
readers, no graph rebuild. Done when the five edges read as in the Decision table and the
map agrees with the live-note frontmatter.

### Why ###
`EVAL-VLIVE-1` showed the framed graph carries drift that wiring would inherit. The comlab
union found five `consumers` edges that name the wrong file or a behaviour the named file
does not implement (one — `RULE_HW_PRUNE` — looked ORPHAN to 2/3 auditors but is a
**MISLABEL**: the checker is a live scoring-evidence reader, just not the prune the edge
claims). comlab is the terminal fusion-spine map `T-WIRE-1` composes against, so its edges
must be trustworthy before wiring.

### Success criteria ###
The reconcile is done when all of these pass (commands in Verification):
1. None of the five drifted edge strings survive verbatim in the map or in the wiki
   02/03/10 frontmatter (grep returns 0 for each old label).
2. Each of the five relabeled edges resolves to a real reader (grep confirms the new
   `file:symbol/field` exists in code).
3. Every comlab note still carries >=1 LIVE consumer (no note orphaned, none demoted).
4. Map `consumers:` blocks for notes 02/03/10 are byte-identical to the corresponding
   live-note frontmatter `consumers:` blocks (map <=> note agree).
5. `git --no-pager diff --stat` shows only the map + the three wiki notes + the ledger.

### Context ###
The five edges and their code-verified rulings are in `reports/comlab__UNION.md`
(rows D1-D5) with grep evidence. Map line numbers below are from
`_skills/graph/4dlab-vault/assets/vault-map.comlab.yaml` as of 2026-06-29; **re-confirm by
grep before editing** (line numbers drift). The live notes mirror the map in their YAML
frontmatter `consumers:` blocks: `labs/comlab/wiki/02_lab_input_contract.md` (~line 39),
`labs/comlab/wiki/03_vehicle_dna_pruning.md` (~line 34), `labs/comlab/wiki/10_differential_and_symptom_prior.md` (~line 37).
**Both copies must change together** — the eval read the live notes, the wiring reads the map.
**YAML wrapping caveat:** the note emitter line-wraps long edge strings (e.g. D3 in
`wiki/03` spans two lines: `... RULE_HW_PRUNE (Stage B` / `  Pass 2)`). Edit the wrapped
entry as one logical value; the "old label gone" check must normalize whitespace (see Verification).

### Consumer (signal/noise) ###
N/A — no new field/enum/fault. This task only **renames existing consumer edges** to the
readers that already exist in code (verified in the union). It adds no schema surface.

### Decision — per-edge disposition (grep-confirm each reader before writing) ###
| # | note . map line | OLD edge | -> NEW edge | reader to grep-confirm |
|---|---|---|---|---|
| D1 | 02 . 114 | `comlab: labs/comlab/comlab/core/ecu_hardware_checker.py vin_dna consumption` | `comlab: labs/comlab/comlab/core/ecu_hardware_checker.py OBD-rail evidence (intake_air_temp_c / coolant_temp_c / throttle_pos_pct / total_trim_correction_delta / per_bank_trim_delta)` | `core/ecu_hardware_checker.py:31-69` reads those rails; `grep vin_dna` there = 0 |
| D2 | 02 . 115 | `comlab: labs/comlab/comlab/core/lab_pipeline_aggregator.py engine_state ingestion` | `comlab: labs/comlab/comlab/core/symptom_router.py route_symptom engine_state suppression` | `core/symptom_router.py:60,68` reads `engine_state`; `grep engine_state core/lab_pipeline_aggregator.py` = 0 |
| D3 | 03 . 129 | `comlab: labs/comlab/comlab/core/ecu_hardware_checker.py RULE_HW_PRUNE (Stage B Pass 2)` | `comlab: labs/comlab/comlab/core/ecu_hardware_checker.py ECU-hardware digital-lie evidence (fault_atlas_router.py:1312, ecu_fault family)` | `core/fault_atlas_router.py:1312` calls `_ecu_hw_checker.check(...)`; precondition prune is a stubbed `pass` at `:902-907` (so the old prune label is drift) |
| D4 | 03 . 131 | `comlab: labs/comlab/comlab/core/lab_pipeline_aggregator.py DNA-confidence degradation` | `comlab: labs/comlab/comlab/core/lab_pipeline_aggregator.py vin_confidence==NONE fatal gate (ERR-ABORT-004)` | `core/lab_pipeline_aggregator.py:350` reads `vin_confidence == VinConfidence.NONE`; degradation mode is symptom-directive driven (`_map_degradation` :192-196), not DNA-confidence |
| D5 | 10 . 202 | `comlab: labs/comlab/comlab/core/symptom_router.py RULE_SYMPTOM_PRIOR (capped)` | `comlab: labs/comlab/comlab/core/fault_atlas_router.py RULE_SYMPTOM_PRIOR (capped 0.65)` | `core/fault_atlas_router.py:600-602,682-684` (`_max_symptom_prior_weight=0.65`), applied `:1078-1090`; `grep prior core/symptom_router.py` = 0 |

Rule for every row (from `4dlab-doc-prep` Step 4/5, signal/noise): **grep-confirm the read
exists before writing the new edge.** After the five relabels, re-check each affected note
keeps >=1 LIVE consumer (it does — see union "Net"); if any row's edit would leave a note
with zero live consumers, STOP and surface it rather than leaving an orphan to keep the note framed.

### Out of scope ###
- **Do NOT implement** the missing `RULE_HW_PRUNE` precondition prune (D3) or a PARTIAL
  DNA-confidence degradation path (D4). The union ruled both MISLABEL — the fix is to
  **relabel the edge to the live reader**, not to write the absent reader. Building either
  is a separate code task with its own spec, not this map-reconcile.
- The three **cosmetic/optional** items in the union (wiki rule-ID tokens; note 03 "VE
  polymorph" wording; note 06 "12-family" count) are NOT required. The owner MAY fold them
  in only if editing the same lines anyway; otherwise leave them and note as `T-GTA-RECONCILE-COM-b`
  follow-ups in the ledger. Do not chase them into a wider edit.
- **Leave non-`consumers` frontmatter keys untouched.** `wiki/03` defines `RULE_HW_PRUNE`
  under `entities_defined:` (line ~13) — that is a legitimate wiki anchor for the note's own
  concept, NOT a consumer edge. D3 only relabels the `consumers:` entry; do not delete or
  edit `entities_defined`, `tags`, or `related_chunks`.
- Other labs (own `T-GTA-*` audits); note **bodies** (only the frontmatter `consumers:`
  blocks change); any **Python**; the `Vault/` build output.
- GRAPH GUARDRAIL: do **NOT** run `graphify` / rebuild any knowledge graph. The framed
  notes and maps are the canonical inputs; relabeling them is a text edit, not a re-extraction.
- Surgical-change rule: every changed line must trace to a D1-D5 row (or an explicitly
  flagged cosmetic follow-up). No adjacent cleanup in this diff.

### Files to touch ###
- `_skills/graph/4dlab-vault/assets/vault-map.comlab.yaml` (MODIFY — the 5 consumer edges)
- `labs/comlab/wiki/02_lab_input_contract.md` (MODIFY — mirror D1, D2 in frontmatter)
- `labs/comlab/wiki/03_vehicle_dna_pruning.md` (MODIFY — mirror D3, D4 in frontmatter)
- `labs/comlab/wiki/10_differential_and_symptom_prior.md` (MODIFY — mirror D5 in frontmatter)
- `apps/vault/audit/GRAPH_TRUST_PROGRESS.md` (MODIFY — flip this row to done)

### Verification ###
Long edge strings wrap across lines in note YAML, so checks normalize whitespace
(`tr -s` collapses newlines+spaces) before grepping. `cw()` extracts only the
`consumers:` block of a note (stops at the next top-level key) so the `entities_defined`
`RULE_HW_PRUNE` anchor is never matched.
```bash
cd /agent_workspace
MAP=_skills/graph/4dlab-vault/assets/vault-map.comlab.yaml
W=labs/comlab/wiki
norm(){ tr -s '[:space:]' ' ' < "$1"; }                          # collapse wrap to single spaces
cw(){ awk '/^consumers:/{f=1;next} /^[a-z_]+:/{f=0} f' "$1"; }    # consumers: block only
# 1. OLD drifted labels gone from the map AND the (wrap-normalized) note consumers block -> each 0:
norm "$MAP" | grep -oE 'ecu_hardware_checker.py vin_dna' ; cw "$W"/02_lab_input_contract.md | tr -s '[:space:]' ' ' | grep -oE 'ecu_hardware_checker.py vin_dna'
norm "$MAP" | grep -oE 'lab_pipeline_aggregator.py engine_state ingestion' ; cw "$W"/02_lab_input_contract.md | tr -s '[:space:]' ' ' | grep -oE 'lab_pipeline_aggregator.py engine_state ingestion'
norm "$MAP" | grep -oE 'RULE_HW_PRUNE \(Stage B Pass 2\)' ; cw "$W"/03_vehicle_dna_pruning.md | tr -s '[:space:]' ' ' | grep -oE 'RULE_HW_PRUNE \(Stage B Pass 2\)'
norm "$MAP" | grep -oE 'DNA-confidence degradation' ; cw "$W"/03_vehicle_dna_pruning.md | tr -s '[:space:]' ' ' | grep -oE 'DNA-confidence degradation'
norm "$MAP" | grep -oE 'symptom_router.py RULE_SYMPTOM_PRIOR' ; cw "$W"/10_differential_and_symptom_prior.md | tr -s '[:space:]' ' ' | grep -oE 'symptom_router.py RULE_SYMPTOM_PRIOR'
# 2. NEW edge readers resolve in code (each >=1):
grep -cE 'intake_air_temp_c|coolant_temp_c|throttle_pos_pct' labs/comlab/comlab/core/ecu_hardware_checker.py     # D1
grep -cE 'engine_state' labs/comlab/comlab/core/symptom_router.py                                                # D2
grep -cE '_ecu_hw_checker\.check' labs/comlab/comlab/core/fault_atlas_router.py                                  # D3
grep -cE 'vin_confidence == VinConfidence.NONE' labs/comlab/comlab/core/lab_pipeline_aggregator.py               # D4
grep -cE '_max_symptom_prior_weight' labs/comlab/comlab/core/fault_atlas_router.py                               # D5
# 3. entities_defined anchor preserved (must still be 1 — D3 must NOT delete it):
grep -cE '^- RULE_HW_PRUNE$' "$W"/03_vehicle_dna_pruning.md
# 4. Every comlab note keeps >=1 non-wired comlab consumer (notes 02/03/10 — manual spot check of cw output).
# 5. Map <=> note consumers agree for 02/03/10 (compare normalized cw output of each note to the map block).
# 6. Scope:
git --no-pager diff --stat -- "$MAP" "$W"/0{2,3}_*.md "$W"/10_*.md apps/vault/audit/GRAPH_TRUST_PROGRESS.md
```
Step 1 greps must each print **nothing** (old labels gone, wrap-tolerant); step 2 each
prints **>=1**; step 3 prints **1** (anchor intact); step 6 shows only the listed files.

### Progress hook ###
`GRAPH_TRUST_PROGRESS.md` `T-GTA-RECONCILE-COM`: Status=done, Files changed=5,
Verification="5 consumer edges relabeled (D1-D5): ecu_hw vin_dna->OBD-rails; aggregator engine_state->symptom_router; RULE_HW_PRUNE->scoring-evidence; DNA-confidence->vin_confidence NONE gate; symptom_router prior->fault_atlas_router; map<=>wiki 02/03/10 agree; 0 orphaned notes".
