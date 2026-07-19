---
chunk_id: COMWIKI-04
title: Horizon Eras — LEGACY / ADAPTIVE / MODERN
doc: COM_WIKI
version: v2.0
date: 2026-06-20
status: authoritative
summary: The three vehicle eras that gate which registry rules apply, their sensitivity
  masks, and how target_horizons is assigned per fault.
entities_defined:
- CONCEPT_LEGACY
- CONCEPT_ADAPTIVE
- CONCEPT_MODERN
- RULE_HORIZON_PRUNE
- CONCEPT_ERA_MASK
related_chunks:
- COMWIKI-03
- COMWIKI-05
- COMWIKI-07
sources:
- COMLab_HLD.md §4.2
- eras_sensitivity_masks.yaml
- SEMANTIC_CONTRACT.md §6.4
node_type: wiki
lab: comlab
module: comlab
subsystem: horizon-context
implements:
- labs/comlab/comlab/core/horizon_context_injector.py
consumers:
- 'comlab: labs/comlab/comlab/core/horizon_context_injector.py RULE_HORIZON_PRUNE
  / era-mask thresholds'
- 'comlab: labs/comlab/comlab/core/fault_atlas_router.py per-era RULE_SCORING thresholds'
drift_guards:
- labs/comlab/tests/unit/test_horizon_context_injector.py
tags:
- comlab
- horizon-context
- wiki
source: labs/comlab/wiki/04_horizon_eras.md
---

# Horizon Eras — LEGACY / ADAPTIVE / MODERN

`resolved_horizon` (from `VinDNA`, pre-computed by DNALab) gates which registry rules apply.
This is Stage-B Pass 1 — the first elimination, before hardware pruning.

| Horizon | Euro | ~Years | Key tech | Dominant fuelling |
|---|---|---|---|---|
| `HORIZON_LEGACY` | Euro 1–2 | pre-1997 → ~2001 | simple/no lambda control, basic cat or none | carb → early port injection |
| `HORIZON_ADAPTIVE` | Euro 3–4 | ~2001–2011 | narrowband O₂ closed-loop, OBD-II mandatory | multi-point port injection |
| `HORIZON_MODERN` | Euro 5–6 | ~2011–present | wideband O₂, tight windows, GPF, GDI common | GDI + MPI combined |

> Scope reminder: the engine targets **petrol 1990–2010 (Euro 1–5)**. `HORIZON_MODERN` content
> tied to post-2010 Euro 6+ tech (GPF inference, LSPI, secondary-air inference) is out of scope;
> GDI / early-turbo are in scope only for vehicles sold within 1990–2010.

## HORIZON_LEGACY {#CONCEPT_LEGACY}

Pre-catalyst or early single-catalyst vehicles; lambda closed-loop absent or rudimentary; OBD-I
or early OBD-II (limited DTC sets, trims may not stream).

- Fuel trims unreliable/absent → **gas chemistry is the primary diagnostic axis**.
- EGR failures (`ERR-LC-005`) most prevalent here — `target_horizons = LEGACY` only.
- Valve-stem-seal / ring wear (`ERR-RM-001/002`) highest-incidence (high-mileage fleet).
- `degradation_mode = GAS_DOMINANT` common (no scanner / OBD-I non-streaming).

## HORIZON_ADAPTIVE {#CONCEPT_ADAPTIVE}

Euro 3–4, OBD-II mandatory, narrowband upstream O₂ as primary feedback, downstream O₂ for cat
monitoring, MAF standard, EVAP mandatory from Euro 3, COP ignition emerging.

- Closed-loop trims reliable → standard ±15 % thresholds apply.
- MAF contamination (`ERR-LC-002`, `ERR-SF-003`), EVAP purge (`ERR-RM-004`), COP arc
  (`ERR-MF-001`) become relevant. GDI still rare (`ERR-RM-005`/`ERR-MF-007` uncommon).

## HORIZON_MODERN {#CONCEPT_MODERN}

Euro 5–6, wideband (or NB-simulated-wideband) upstream O₂, tight emission windows, GDI common.

- Wideband λ makes the perception-vs-truth comparison most meaningful.
- GDI faults apply (`ERR-RM-005` HPFP, `ERR-MF-007` intake carbon).
- Tighter thresholds: +12 % trim may set P0171 in MODERN where LEGACY would not; cat-efficiency
  (P0420/P0430) most sensitive.

## Era sensitivity masks {#CONCEPT_ERA_MASK}

From `eras_sensitivity_masks.yaml` — the per-era thresholds the gates and scoring read. Each
literal is era-scoped; numeric tolerances tighten with era.

```yaml
HORIZON_LEGACY:   { gas_co_max_pct: 1.5, gas_hc_max_ppm: 300, lambda_tolerance: 0.10, routing_rigor: relaxed,  model_year_range: 1980–2001 }
HORIZON_ADAPTIVE: { gas_co_max_pct: 1.0, gas_hc_max_ppm: 200, lambda_tolerance: 0.05, routing_rigor: standard, model_year_range: 2001–2011 }
HORIZON_MODERN:   { gas_co_max_pct: 0.5, gas_hc_max_ppm: 150, lambda_tolerance: 0.02, routing_rigor: strict,   model_year_range: 2011–present }
```

> **v2 reconciliation note.** Two "engine-warmed" thresholds coexist in the codebase — **70 °C**
> gates trim analytics (`vocabulary.py` `ENGINE_COLD`) while **75 °C** defines the
> `COLD_OPEN_LOOP_INVALID` bucket. The rework reconciles these to one consistent gate
> (`OPEN_LEVERS F3`, Phase-0 — `COMWIKI-12`). Until reconciled, both must be satisfied before
> closed-loop diagnostics run. [v2: OPEN_LEVERS F3]

## Era assignment per fault {#RULE_HORIZON_PRUNE}

| Horizon scope | rationale | example faults |
|---|---|---|
| ALL | universal mechanical/sensor phenomena | ERR-RM-001/002, ERR-LC-001, ERR-MF-002 |
| LEGACY only | era-specific tech (basic EGR, carb) | ERR-LC-005 |
| ADAPTIVE + MODERN | OBD-II closed-loop dependent | ERR-LC-002, ERR-MF-001, ERR-RM-004 |
| MODERN only | GDI / tight-window Euro 5–6 | ERR-RM-005, ERR-MF-007 |

COMLab reads `resolved_horizon` directly; if absent on a v1.0 payload it falls back to
`_horizon_from_euro(euro_emission_category)`.

## Graph relations (explicit)

**resolved_horizon** GATES **registry rows** VIA **RULE_HORIZON_PRUNE (Pass 1)**
**CONCEPT_ERA_MASK** PROVIDES **per-era thresholds** TO **GATE_* and RULE_SCORING**
**RULE_HORIZON_PRUNE** RUNS_BEFORE **RULE_HW_PRUNE (COMWIKI-03)**
**70 °C vs 75 °C warmed thresholds** RECONCILED_BY **OPEN_LEVERS F3 (COMWIKI-12)**

## Core Entities

- **CONCEPT_LEGACY** — Pre-catalyst/early single-catalyst vehicle profile (Euro 1–2). Consumer: `comlab/core/horizon_context_injector.py`.
- **CONCEPT_ADAPTIVE** — Euro 3–4 vehicle profile with narrowband feedback. Consumer: `comlab/core/horizon_context_injector.py`.
- **CONCEPT_MODERN** — Euro 5–6 vehicle profile with wideband feedback and GDI. Consumer: `comlab/core/horizon_context_injector.py`.
- **RULE_HORIZON_PRUNE** — Pruning candidate faults whose target horizons exclude the resolved era. Consumer: `comlab/core/horizon_context_injector.py`.
- **CONCEPT_ERA_MASK** — Per-era thresholds specifying sensitivity and limits for gates. Consumer: `comlab/core/horizon_context_injector.py`.
