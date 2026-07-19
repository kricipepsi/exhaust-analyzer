# T-GTA-UNION-DNA — dnalab graph-trust union (canonical drift list)
**Pack:** GRAPH-TRUST (`GRAPH_TRUST_AUDIT.md`) · **Step:** union of the three dnalab audits · **Author:** architect · **Date:** 2026-06-29
**Inputs (3 independent passes, all `done`):**
`reports/dnalab__codex.md`, `reports/dnalab__agy.md`, `reports/dnalab__claude.md`.
**Rule (from the pack):** an edge flagged ORPHAN/MISLABEL by **>=1** agent goes to the
reconcile list, annotated with **agreement count**; the architect reads the cited code and
issues one ruling per contested edge. Fixes -> per-lab reconcile (do not edit maps here).

## Count reconciliation across the three passes
| Pass | LIVE | MISLABEL | ORPHAN | PENDING | Total |
|---|---|---|---|---|---|
| Codex | 35 | 2 | 0 | 0 | 37 |
| Agy   | 36 | 2 | 0 | 0 | 38 |
| Claude| 38 | 0 | 0 | 0 | 38 |
The 37-vs-38 total is a counting artifact (one doc edge). All three agree on every
`implements`/`drift_guards` edge (LIVE) and **reproduce the seeded case 3/3** (below).
The only disagreement is **one `consumers` edge** that appears on two notes.

## Seeded-case self-check (REQUIRED — dnalab is a seeded lab)
**PASS 3/3.** `VehicleDNA` readers classified **LIVE** by all three:
`horizon_context_injector.from_vehicle_dna` reads `vehicle_dna.vin_dna`
(`core/horizon_context_injector.py:70-79`) and `projection.project()` reads
`vehicle_dna_json["vin_dna"]` (`projection.py:46-56`); both are unit-tested but not yet
called by the (unbuilt) pipeline — **LIVE, not ORPHAN**, exactly as the seed requires.

## Canonical drift list (the reconcile superset)
Map = `_skills/graph/4dlab-vault/assets/vault-map.dnalab.yaml`. Lines are map line numbers.

| # | note . map line | edge (as framed) | Codex | Agy | Claude | agree | architect ruling | disposition |
|---|---|---|---|---|---|---|---|---|
| N1 | DLD_DNALab . 53 | `comlab: ingestion.py SessionMetadata.schema_version (MIN_SUPPORTED_SCHEMA_VERSION gate)` | MISLABEL | MISLABEL | LIVE | **2/3** | **MISLABEL** (code upholds the 2) — `ingestion.py:160` only **defines** the field (a Pydantic field, not a reader). The MIN_SUPPORTED gate is the consumer: `lab_pipeline_aggregator.check_schema_version` reads `request.metadata.schema_version`. A field definition is not a consumer (signal/noise). | relabel -> `comlab: lab_pipeline_aggregator.py check_schema_version (request.metadata.schema_version vs MIN_SUPPORTED_SCHEMA_VERSION, :231/:233-245/:358; ERR-ABORT-005)`. |
| N2 | 11_schema_versioning . 79 | (identical edge, second note) | MISLABEL | MISLABEL | LIVE | **2/3** | **MISLABEL** — same ruling as N1. | relabel -> same as N1. |

**Net:** 1 distinct consumer-edge relabel applied on 2 notes. **Zero ORPHANs, zero notes
demoted** (each note keeps its LIVE `implements`/`drift_guards` + other consumer edges).

## Architect code verification
Verified 2026-06-29 against `labs/comlab/comlab`:
**N1/N2 — `schema_version`:** `schemas/ingestion.py:160` — `schema_version: str = Field(default="1.0", ...)`
is a **field definition** (its `# lld §6.3` comment names the gate but does not perform it).
The gate/consumer is `core/lab_pipeline_aggregator.py`: `MIN_SUPPORTED_SCHEMA_VERSION="1.0"`
(:231); `check_schema_version()` compares and raises `AggregatorAbort(ERR-ABORT-005)` (:233-245);
called at :358 on `request.metadata.schema_version`. Reader exists in a **different file**
than the edge names -> **MISLABEL** (Claude's LIVE treated the field def as the consumer).

## Hand-off
Reconcile spec: **`T-GTA-RECONCILE-DNA`** — relabel the 2 schema_version consumer edges
(map + mirrored live-note frontmatter on DLD_DNALab + 11_schema_versioning). Relabel-only,
STRICT, no Python, no graphify. Gate: dnalab feeds the COMLab prior — GREEN once N1/N2 reconciled.
