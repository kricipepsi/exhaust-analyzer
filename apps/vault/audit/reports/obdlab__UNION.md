# T-GTA-UNION-OBD — obdlab graph-trust union (canonical drift list)
**Pack:** GRAPH-TRUST (`GRAPH_TRUST_AUDIT.md`) · **Step:** union of the three obdlab audits · **Author:** architect · **Date:** 2026-06-29
**Inputs (3 independent passes, all `done`):**
`reports/obdlab__codex.md` (commit 5c7a636), `reports/obdlab__agy.md` (fa399f8), `reports/obdlab__claude.md` (be872c5).
**Rule (from the pack):** an edge flagged ORPHAN/MISLABEL by **>=1** agent goes to the
reconcile list, annotated with **agreement count**. The architect then reads the cited
code and issues a single code-grounded ruling per contested edge. Fixes are handed to a
per-lab reconcile spec (do not edit maps here).

## Count reconciliation across the three passes
| Pass | LIVE | MISLABEL | ORPHAN | PENDING | Total |
|---|---|---|---|---|---|
| Codex | 56 | 5 | 1 | 0 | 62 |
| Agy   | 58 | 4 | 0 | 0 | 62 |
| Claude| 56 | 4 | 2 | 0 | 62 |
All three enumerate the same 62 edges and agree on every `implements`/`drift_guards` edge
(LIVE) and on the doc-tree consumer edges. **Every disagreement is confined to six
`consumers` edges** on the four wiki README notes — listed below. The class split is
MISLABEL-vs-ORPHAN only (no LIVE-vs-drift dispute except D3/D5, resolved by code).

## Canonical drift list (the reconcile superset)
Map = `_skills/graph/4dlab-vault/assets/vault-map.obdlab.yaml`. Lines are map line numbers.

| # | note . map line | edge (as framed) | Codex | Agy | Claude | agree | architect ruling | disposition |
|---|---|---|---|---|---|---|---|---|
| D1 | delta-relations . 106 | `power_loss_analytics.py — lambda-delta-vector scoring` | MISLABEL | MISLABEL | MISLABEL | **3/3** | **MISLABEL** — `power_loss_analytics.py` only passes `lambda_perception_delta` through; the cross-operating-point delta calculator is `delta_engine.py`. | relabel -> `comlab/analytics/delta_engine.py` (the two-operating-point delta reader; its docstring names `delta-relations/*` as its source). |
| D2 | delta-relations . 107 | `perception_contradiction.py` | ORPHAN | MISLABEL | MISLABEL | **3/3** (2 MISLABEL / 1 ORPHAN) | **MISLABEL** (resolves the split) — `perception_contradiction.py` has 0 cross-state/two-speed delta refs, so not LIVE-as-labeled; but a reader exists (`delta_engine.py`), so not ORPHAN. | relabel -> `comlab/analytics/delta_engine.py`. |
| D3 | pids-protocol . 127 | `fault_atlas_kg.py — PID/Mode06/readiness fault-atlas keys` | MISLABEL | LIVE | ORPHAN | **2/3** flag (MISLABEL/ORPHAN; agy LIVE) | **MISLABEL** (code resolves the 3-way split) — `fault_atlas_kg.py` is a generic boot-time KG loader (indexes `kg/*.json` by `fault_id`; its docstring: "no hardware precondition filtering"); it reads no PID/Mode06/readiness field. A real reader exists -> not ORPHAN; it is the wrong file -> not LIVE. | relabel -> `comlab/core/fault_atlas_router.py` (reads `mode_06_monitors` / `Mode06MonitorState`, :455/:471-475). |
| D4 | taxonomy . 138 | `symptom_router.py — era/emission symptom-prior routing` | MISLABEL | MISLABEL | MISLABEL | **3/3** | **MISLABEL** — `symptom_router.py` routes only on `engine_state`/`occurs_during` (:60-61); no era/emission routing. | relabel -> `comlab/core/horizon_context_injector.py` + `comlab/core/fault_atlas_router.py` (era/horizon-mask checks; `# wiki: 04_horizon_eras.md`, target-horizon filtering). |
| D5 | taxonomy . 139 | `fault_atlas_kg.py` | MISLABEL | LIVE | ORPHAN | **2/3** flag (MISLABEL/ORPHAN; agy LIVE) | **MISLABEL** (code resolves) — same generic loader as D3; it does **no** era/emission taxonomy checks (grep = 0). The era/horizon checks live in the router/injector. | relabel -> `comlab/core/fault_atlas_router.py` (+ `horizon_context_injector.py`). |
| D6 | truth-perception . 150 | `symptom_router.py — symptom prior` | MISLABEL | MISLABEL | MISLABEL | **3/3** | **MISLABEL** — `symptom_router.py` has 0 prior/truth-perception reads; the capped symptom prior lives entirely in `fault_atlas_router.py` (corroborated by `comlab__UNION.md` D5). | relabel -> `comlab/core/fault_atlas_router.py` (`_max_symptom_prior_weight = 0.65`, :600-602; apply :1078-1090). |

**Net:** 6 consumer-edge relabels. **Zero true ORPHANs** (D2/D3/D5 ORPHAN votes collapse
to MISLABEL once the real reader is found). **Zero LIVE-as-labeled** (D3/D5 LIVE votes fall
once the named file is shown to be a generic loader). **Note-demotion check (reconcile must
confirm):** each affected note (delta-relations, pids-protocol, taxonomy, truth-perception)
retains >=1 LIVE consumer after relabel — e.g. truth-perception keeps line 149
`perception_contradiction.py — truth-vs-perception override core` (LIVE, 3/3). Verify no
note drops to zero LIVE consumers before demoting any edge.

## Architect code verification (evidence for each ruling)
Verified 2026-06-29 against `labs/comlab/comlab`:
**D1/D2 — delta-relations -> `power_loss_analytics.py` / `perception_contradiction.py`:**
`delta_engine.py:1-22` is documented as "COMLab's stateless two-operating-point delta
calculator... the long-open FU-2 consumer for the OBDLab `delta-relations/*` research";
it differences a `second_operating_point` frame against the low-idle primary and emits a
`DeltaSignature`. `power_loss_analytics.py:189-239` only forwards `lambda_perception_delta`
(static kinetics/catalyst indexes). `perception_contradiction.py` has **0** hits for
`second_operating_point|two-speed|cross-state|delta_engine|operating_point|volumetric`.
-> both edges name the wrong file; real reader is `delta_engine.py` -> **MISLABEL**.
**D3/D5 — `fault_atlas_kg.py`:** `core/fault_atlas_kg.py:1-25` — "Fault-Atlas Knowledge Graph
loader. Loads all `comlab/config/kg/*.json` once... O(1) `resolve()` by `fault_id`... **No
hardware precondition filtering** (that is Stage B's responsibility)." `grep -niE
'pid|mode_?06|readiness|era|emission|horizon|stft|ltft|trim'` -> **0**. So it reads neither
PID/Mode06/readiness (D3) nor era/emission taxonomy (D5). The Mode06 reader is
`fault_atlas_router.py:455` (`mode_06_monitors`), :471-475 (`Mode06MonitorState`); era/horizon
is `fault_atlas_router.py:95` (`wiki: 04_horizon_eras.md`) + `horizon_context_injector.py`.
Reader exists but in a different file -> **MISLABEL** (not agy's LIVE, not claude's ORPHAN).
**D4/D6 — `symptom_router.py`:** `core/symptom_router.py:6-7,60-61` reads only
`environmental_conditions.engine_state` and `occurs_during`; it does no era/emission routing
(D4) and no symptom-prior/truth-perception read (D6). The era path is the injector/router;
the capped symptom prior is `fault_atlas_router.py` (`_max_symptom_prior_weight=0.65`,
:600-602 / apply :1078-1090) — the same reader the comlab union (D5) located. -> **MISLABEL**.

## Seeded-case self-check
obdlab has **no** seeded case in `GRAPH_TRUST_AUDIT.md`. The crux distinction held: no agent
flagged a LIVE-but-unwired reader as ORPHAN; the only ORPHAN votes (D2/D3/D5) were
wrong-file calls that code resolves to MISLABEL, not true orphans.

## Hand-off
Reconcile spec (to author): **`T-GTA-RECONCILE-OBD`** — relabel the 6 comlab consumer edges
(map + mirrored live-note frontmatter on the four wiki README notes) per D1-D6; relabel-only,
STRICT, no Python, no graphify. Gate: obdlab is one of the emitter maps `T-WIRE-1` composes
against — it reads GREEN here once D1-D6 are reconciled.
