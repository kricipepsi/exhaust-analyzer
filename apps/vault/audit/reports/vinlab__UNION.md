# T-GTA-UNION-VIN — vinlab graph-trust union (canonical drift list)
**Pack:** GRAPH-TRUST (`GRAPH_TRUST_AUDIT.md`) · **Step:** union of the three vinlab audits · **Author:** architect · **Date:** 2026-06-29
**Inputs (3 independent passes, all `done`):**
`reports/vinlab__codex.md`, `reports/vinlab__agy.md`, `reports/vinlab__claude.md`.
**Rule (from the pack):** an edge flagged ORPHAN/MISLABEL by **>=1** agent goes to the
reconcile list, annotated with **agreement count**; the architect reads the cited code and
issues one ruling per contested edge. Fixes -> per-lab reconcile (do not edit maps here).

## Count reconciliation across the three passes
| Pass | LIVE | MISLABEL | ORPHAN | PENDING | Total |
|---|---|---|---|---|---|
| Codex | 70 | 2 | 0 | 0 | 72 |
| Agy   | 70 | 2 | 0 | 0 | 72 |
| Claude| 70 | 2 | 0 | 0 | 72 |
Unanimous: all three enumerate 72 edges and agree on **every** classification, including the
**same one drift edge** (on two notes). vinlab carries no seeded case; this union is a 3/3
confirmation. (Note: this is the VIN map the comlab union flagged as subtle — the agreement
here is the cross-check paying off, not a rubber-stamp.)

## Canonical drift list (the reconcile superset)
Map = `_skills/graph/4dlab-vault/assets/vault-map.vinlab.yaml`. Lines are map line numbers.

| # | note . map line | edge (as framed) | Codex | Agy | Claude | agree | architect ruling | disposition |
|---|---|---|---|---|---|---|---|---|
| V1 | LLD_VINLab . 47 | `comlab: fault_atlas_router.py (FuelSystemStatus.CL comparison, :294)` | MISLABEL | MISLABEL | MISLABEL | **3/3** | **MISLABEL** — `_fuel_system_gate` (:283-295) reads **`FuelSystemStatus`**, an **OBD** live-data enum (`obd_live_data.fuel_system_status`), **not** any vinlab field. The router's real vinlab read is `vin_confidence`. Wrong-field reader -> MISLABEL, not LIVE; reader exists -> not ORPHAN. | relabel -> `comlab: fault_atlas_router.py vin_confidence consumption (request.metadata.vin_confidence, :2239)`. (If the note already carries a vin_confidence consumer edge, drop this duplicate instead. **Do not** keep it pointed at the OBD fuel-system gate.) |
| V2 | DLD_VINLab . 76 | (identical edge, second note) | MISLABEL | MISLABEL | MISLABEL | **3/3** | **MISLABEL** — same ruling as V1. | relabel -> same as V1. |

**Net:** 1 distinct consumer-edge relabel applied on 2 notes. **Zero ORPHANs, zero notes
demoted** (each note retains its LIVE `implements`/`drift_guards` + other consumer edges,
and gains a true vinlab consumer via `vin_confidence`).

## Architect code verification
Verified 2026-06-29 against `labs/comlab/comlab`:
**V1/V2 — `FuelSystemStatus.CL` gate:** `core/fault_atlas_router.py:283-295` —
`_fuel_system_gate(fuel_system_status)` classifies closed-loop authority; its docstring cites
`CONCEPT_OBD_INPUT` and `fuel_system_status` is OBD live data (sibling reads at :493-505 are all
`obd_live_data`). So the gate is an **OBD** consumer, misattributed to a VINLab note. The genuine
VINLab->comlab consumer is the **`vin_confidence`** read: `fault_atlas_router.py:2239`
(`request.metadata.vin_confidence.value`) and `lab_pipeline_aggregator.py:350`
(`vin_confidence == NONE` -> ERR-ABORT-004). -> **MISLABEL**, repoint to the `vin_confidence` read.
(`FuelSystemStatus`/`VinConfidence` are each defined twice — vinlab-native + comlab mirror —
per rule 5 "mirror types over JSON boundaries"; the duplication is expected, not drift.)

## Hand-off
Reconcile spec: **`T-GTA-RECONCILE-VIN`** — relabel the 2 FuelSystemStatus consumer edges
to the `vin_confidence` read (map + mirrored live-note frontmatter on LLD_VINLab + DLD_VINLab).
Relabel-only, STRICT, no Python, no graphify. Gate: vinlab feeds the COMLab prior — GREEN once V1/V2 reconciled.
