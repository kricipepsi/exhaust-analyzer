# T-VLIVE-3c — Reconcile dtclab COMLab consumer drift (audit + fix)
**Pack:** GRAPH-TRUST (`GRAPH_TRUST_AUDIT.md`) · **Lane:** vault-tooling / architect-authoring · **Mode:** STRICT
**Why:** `EVAL-VLIVE-1` exposed that dtclab's `power_loss_analytics` and
`perception_contradiction` consumer edges are drift. They recur **8×** across
`vault-map.dtclab.yaml` (lines 52,53,91,92,129,140,141,152,205) — the eval only
touched 2. This is dtclab's combined audit+fix and the worked example for the pack.
**Load skills:** `_skills/graph/4dlab-vault/SKILL.md`, `_skills/graph/4dlab-doc-prep/SKILL.md`.

## Verified findings (architect, 2026-06-29)
- **`power_loss_analytics.py` reads NO DTCLab output** — `grep -cE 'DTC|dtc|Mode06|routing_tag'`
  → **0**. So **every** `power_loss_analytics` dtclab edge is **ORPHAN**, regardless of
  its wording ("DTC_CONFIDENCE_WEIGHTS", "Mixture scoring", "Mode06MonitorState scoring").
- **`perception_contradiction.py` reads DTCs only via `rich_dtc_present`** (P0172/P0175,
  5 refs); it has **0** refs to `FuelSystemStatus` / `HistoricalFaultContext`. So perception
  edges are **MISLABEL** where the note is about rich-DTC perception, and **ORPHAN→repoint**
  where they name fields perception never reads.
- Real homes for the mis-claimed fields (verified): `FuelSystemStatus.CL` →
  `fault_atlas_router.py:294`; `POA_HISTORY` is **injected** by `fault_atlas_router`
  (`execute_triage_loop`), not read by perception.

## Decision — per-edge disposition (verify each before writing)
| Map line · note | Edge | Class | Action |
|---|---|---|---|
| 53,92 · LLD,DLD | `power_loss_analytics … DTC_CONFIDENCE_WEIGHTS / Mode06` | ORPHAN | remove (LLD/DLD keep `fault_atlas_router` + `lab_pipeline_aggregator` — still framed) |
| 52,91 · LLD,DLD | `perception_contradiction … HistoricalFaultContext / FuelSystemStatus` | MISLABEL | relabel → `perception_contradiction.py rich_dtc_present (P0172/P0175) gate` |
| 140 · 03_fuel_trim_grammar | `power_loss_analytics … Mixture scoring` | ORPHAN | remove |
| 141 · 03_fuel_trim_grammar | `perception_contradiction … Total Fuel Trim evaluation` | verify | if perception reads the trim/rich path → relabel to `rich_dtc_present`; else repoint to the real reader. **Note 03 must keep ≥1 live consumer or be demoted to `plain`.** |
| 152 · 04_mode06_monitors | `power_loss_analytics … Mode06MonitorState scoring` | ORPHAN | remove (note keeps `lab_pipeline_aggregator … Mode $06` — **verify that edge is LIVE**) |
| 129 · 02_freeze_frame_validity | `perception_contradiction … FuelSystemStatus / calculated_load_pct` | ORPHAN→repoint | perception reads neither → repoint to the real reader (`fault_atlas_router.py:294` `FuelSystemStatus.CL`) or demote; note keeps `lab_pipeline_aggregator … freeze_frame` if LIVE |
| 205 · 09_gas_reverse_lookup | `perception_contradiction … POA_HISTORY / perception gap` | ORPHAN→repoint | POA_HISTORY is injected by `fault_atlas_router`, not read by perception → repoint to `fault_atlas_router.py POA_HISTORY injection`. **Note 09's only consumer — must end with a live edge or be demoted.** |

Rule for every row: **grep-confirm the read exists before writing the edge.** Any note
left with no LIVE consumer after removal → name its real comlab reader, or demote to
`plain` (signal/noise) — never leave an orphan edge to keep a note framed.

## Files to touch
- edit (consumer edges only): `_skills/graph/4dlab-vault/assets/vault-map.dtclab.yaml`
- edit (mirror the same edits into the live framed frontmatter): the affected
  `labs/dtclab/docs/{LLD,DLD}_DTCLab.md` and `labs/dtclab/wiki/{02,03,04,09}_*.md`
  `consumers:` blocks (so map and live notes agree — the eval read the live notes).
- edit: `apps/vault/audit/GRAPH_TRUST_AUDIT.md` ledger (flip `T-VLIVE-3c` → done).

## Out of scope
- Other labs (own `T-GTA-*` audits); note bodies; any Python; any graph; `Vault/`.

## Verification
1. `grep -nE 'power_loss_analytics' _skills/graph/4dlab-vault/assets/vault-map.dtclab.yaml` → **0** (all removed/repointed).
2. No `perception_contradiction` edge names `FuelSystemStatus`/`HistoricalFaultContext`/
   `calculated_load_pct`/`POA_HISTORY` as a *perception* read; each remaining perception
   edge resolves to `rich_dtc_present` in code.
3. Every repointed target resolves: `grep -n 'FuelSystemStatus.CL' labs/comlab/comlab/core/fault_atlas_router.py`; `grep -n 'rich_dtc_present' labs/comlab/comlab/core/perception_contradiction.py`.
4. Every dtclab note still carries ≥1 LIVE consumer, or is in `plain:`. Map ⇄ live-note
   frontmatter agree.
5. Re-run the dtclab anti-orphan gate (dry-run framing): zero unresolved.
6. `git --no-pager diff --stat` shows only the dtclab map + the named dtclab notes + the ledger.

## Success criteria
Zero `power_loss_analytics` dtclab edges; every `perception_contradiction` edge names a
real read (`rich_dtc_present`) or is repointed/demoted; no note orphaned; map and live
frontmatter agree. This reproduces the two seeded dtclab cases in `GRAPH_TRUST_AUDIT.md`.

## Progress hook
`GRAPH_TRUST_AUDIT.md` `T-VLIVE-3c`: Status=done, Files changed={COUNT},
Verification="power_loss orphan ×N removed; perception relabeled→rich_dtc_present / repointed→fault_atlas_router; notes 03/09 reconciled; map⇄frontmatter agree".
