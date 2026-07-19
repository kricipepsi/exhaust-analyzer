---
chunk_id: DNAWIKI-00
title: "DNALab Wiki — Index & Disposition Router"
lab: dnalab
doc: DNA_WIKI
version: v2.0
role: routing-index
status: authoritative
date: 2026-06-12
companion_docset: "docs/ (PRD, HLD, DLD, LLD, ADR, BDD, DNA_VOCABULARY)"
kg_ingestion: none
related_chunks: [DNAWIKI-10, DNAWIKI-11, DNAWIKI-12, DNAWIKI-13, DNAWIKI-90, DNAWIKI-91, DNAWIKI-92, DNAWIKI-93, DNAWIKI-94]
---

# DNALab Wiki — Index & Disposition Router

DNALab is unusual among its siblings, so its wiki is deliberately **two wikis in one
tree**, kept apart by the `role:` and `kg_ingestion:` front-matter on every page. Read this
router first; it tells you which half a page belongs to and the one rule that keeps them
from leaking into each other.

| Half | Pages | Disposition | What it is |
|---|---|---|---|
| **OWNED** | `10`–`13` | `role: reference-only`, `kg_ingestion: none` | The thin set of things DNALab genuinely owns — the envelope, versioning, assembly contract, session identity. Mirrors live code. **Carries zero measured numbers.** |
| **RESEARCH** | `90`–`94` | `role: research-evidence`, `kg_ingestion: none` | The operator-symptom + VIN-identity *channel* evidence (how far either input can be trusted). Citation-backed empirical numbers that **route out to COMLab** — never live `dnalab/` citations. |

## The one boundary rule (governs every page here)

```
OWNED pages    → mirror live code; carry NO measured/empirical number.
                 Only structural constants (SCHEMA_VERSION, the DNA_TX_ id format,
                 the ISO-8601 timestamp format) appear — none need a wiki citation.

RESEARCH pages → every empirical number carries TWO tags:
                   # source: <citation>     (where the value came from)
                   routes-to: COMLab-<X>    (the existing/proposed consumer that reads it)
                 A finding with no nameable COMLab consumer stays a QUESTION — it is
                 NOT written as a finding. The number's real home is the COMLab
                 proposals registry; this page is only its evidence trail.
```

```
dnalab/wiki/9x  research ──findings + routes-to──▶  COMLab proposals/entries.yaml
   (evidence trail)                                  (the value SHIPS here, with consumer)
dnalab/wiki/1x  owned    ──mirrors


## Graph relations (explicit)

**DNAWIKI-00** ROUTES_TO **DNAWIKI-10** (VehicleDNA envelope)
**DNAWIKI-00** ROUTES_TO **DNAWIKI-11** (schema versioning)
**DNAWIKI-00** ROUTES_TO **DNAWIKI-12** (assembly contract)
**DNAWIKI-00** ROUTES_TO **DNAWIKI-13** (session identity)
**DNAWIKI-00** ROUTES_TO **DNAWIKI-90** (research index)
**OWNED half (10–13)** MIRRORS **dnalab/ code** (live contract surface)
**RESEARCH half (90–94)** ROUTES_TO **COMLab proposals registry** (evidence trail, not live)
**OWNED notes** CONSUMED_BY **COMLab OrchestratorInboundRequest.vehicle_dna** (live)
**RESEARCH notes** CONSUMED_BY **COMLab-A/B symptom-prior** (PROPOSAL — not live)

## Core Entities

- `DNAWIKI-00-INDEX` — routing index; CONSUMER: COMLab (via owned-half live consumers)
- `OWNED half (10–13)` — live contract; CONSUMER: COMLab OrchestratorInboundRequest
- `RESEARCH half (90–94)` — evidence trail; CONSUMER: COMLab proposals registry (PROPOSAL)
