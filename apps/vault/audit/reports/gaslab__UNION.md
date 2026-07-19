# T-GTA-UNION-GAS — gaslab graph-trust union (canonical drift list)
**Pack:** GRAPH-TRUST (`GRAPH_TRUST_AUDIT.md`) · **Step:** union of the three gaslab audits · **Author:** architect · **Date:** 2026-06-29
**Inputs (3 independent passes, all `done`):**
`reports/gaslab__codex.md` (commit b3d2162), `reports/gaslab__agy.md` (dcd2707), `reports/gaslab__claude.md` (51ed97e).
**Rule (from the pack):** an edge flagged ORPHAN/MISLABEL by **>=1** agent goes to the
reconcile list, annotated with **agreement count**. The architect then reads the cited
code and issues a single code-grounded ruling per contested edge. Fixes are handed to a
per-lab reconcile spec (do not edit maps here).

## Count reconciliation across the three passes
| Pass | LIVE | MISLABEL | ORPHAN | PENDING | Total |
|---|---|---|---|---|---|
| Codex | 155 | 0 | 1 | 0 | 156 |
| Agy | 155 | 0 | 1 | 0 | 156 |
| Claude | 155 | 0 | 1 | 0 | 156 |
All three enumerate the same 156 edges and agree on **every** `implements` edge (59, file
exists), **every** `drift_guards` edge (50, test file exists), and 46 of 47 `consumers`
edges (LIVE). **The sole disagreement-free drift point is one `consumers` edge**, below —
unanimous, so this union is a 3/3 confirmation rather than a contest.

## Canonical drift list (the reconcile superset)
Map = `_skills/graph/4dlab-vault/assets/vault-map.gaslab.yaml`. Line is the map line number.

| # | note . map line | edge (as framed) | Codex | Agy | Claude | agree | architect ruling | disposition |
|---|---|---|---|---|---|---|---|---|
| G1 | 10_limited_scope_confidence . 264 | `comlab: lab_pipeline_aggregator.py chemistry confidence input` | ORPHAN | ORPHAN | ORPHAN | **3/3** | **ORPHAN** — no COMLab reader of any gas/chemistry confidence exists; the aggregator derives confidence only from horizon/VIN/override, and `GasLabPayload` carries no confidence field. | **Demote/remove this one comlab consumer edge.** Note 10 stays framed via its LIVE gaslab self-consumers (`gaslab/ranking.py _clamped_confidence`) and its other LIVE comlab `sample_validity`/`lambda` edges — no note demotion. If a gaslab-confidence consumer is wanted in COMLab later, it ships as a proposal with a named reader (AGENTS.md rule 4). |

**Net:** 1 consumer-edge demotion. **Zero MISLABELs. Zero notes demoted** (note 10 retains
>=1 LIVE consumer after the edge is dropped).

## Architect code verification (evidence for the ruling)
Verified 2026-06-29 against `labs/comlab/comlab`:
**G1 — `lab_pipeline_aggregator.py chemistry confidence input`:**
`grep -niE 'confidence' core/lab_pipeline_aggregator.py | grep -iE 'gas|chem|lambda'` -> the
only hit is a **docstring** (`:324`), not a read. Aggregator confidence is horizon/VIN/override
only (`_confidence_from_horizon` :203/:479/:550; `vin_confidence` :270/:350/:480; override :286/:537).
`GasLabPayload` (`schemas/ingestion.py:165-205`) defines **no** confidence field. The aggregator
does read gaslab `sample_validity`/`lambda_chem`/`lambda_measured` (those edges are LIVE and
elsewhere on the note) but **not** a chemistry confidence -> **ORPHAN** (3/3 confirmed).

## Seeded-case self-check
gaslab has **no** seeded case in `GRAPH_TRUST_AUDIT.md` (the three seeds are dtclab x2 + dnalab x1).
All three passes correctly preserved the crux distinction by cross-applying the
`power_loss_analytics` lesson: in **dtclab** it is ORPHAN (0 DTC refs), in **gaslab** it is **LIVE**
(`comlab/analytics/power_loss_analytics.py` genuinely reads `gas_co/gas_hc/gas_o2/lambda_chem`).
The contrast confirms the method — a LIVE-but-unwired reader was **not** misflagged as ORPHAN.

## Hand-off
Reconcile spec (to author): **`T-GTA-RECONCILE-GAS`** — demote the single comlab
chemistry-confidence consumer edge on note 10 (map + mirrored live-note frontmatter);
relabel/demote-only, STRICT, no Python, no graphify. Gate: gaslab is one of the emitter
maps `T-WIRE-1` composes against — it reads GREEN here once G1 is reconciled.
