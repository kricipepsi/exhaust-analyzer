---
title: "VINLab Wiki — Index & Citation Provenance Map"
lab: vinlab
role: citation-target
status: authoritative
date: 2026-06-12
companion_docset: "docs/ (PRD, HLD, DLD, LLD, ADR, BDD, VIN_VOCABULARY)"
kg_ingestion: none
---

# VINLab Wiki — Index & Citation Provenance Map

**Disposition: citation-target (load-bearing).** Unlike its two sibling labs, VINLab
carries real numeric thresholds, and the project rule requires every numeric literal in
`vinlab/` to carry a `# source:` / `# wiki:` citation. A repo scan finds **28** such
comments. This wiki is the lab-local **provenance map** those citations resolve through:
the single place that says, for each numeric rule, *where its canonical value lives and who
owns it.*

It is realized as a **citation/provenance index, not a re-statement of the numbers.** Most
of VINLab's numbers are anchored to external standards, the contract, or shared lab-source
docs; copying them here would create a second source and invite drift. So this wiki
**references** those homes and only **owns** the decode rules that are genuinely
VINLab-specific (see "VINLab-owned" below).

There is **no knowledge-graph ingestion** for VINLab — no graphify step.

## Citation provenance map

Each `# source:` / `# wiki:` family in `vinlab/` and where it resolves:

| Code site (file) | Citation | Canonical home | Owner |
|---|---|---|---|
| `decoder.py` VIN charset / checksum | SAE J853 §4.1.2; NHTSA 49 CFR Part 565; ISO 3780 | external standards | standards body (referenced) |
| `decoder.py` valid VIN chars | `VINlookup.md §1` | source doc | VINLab docset |
| `decoder.py` petrol-only keyword guard | "H1 petrol-only" `_NON_PETROL_KEYWORDS` | **this wiki** (`10_decode_scope_rules.md`) | **VINLab-owned** |
| `decoder.py` euro_norm normalisation | `SEMANTIC_CONTRACT.md §6.4` | contract | COMLab contract |
| `decoder.py` engine-resolution heuristics | `T-FX-5` full-run analysis; `T-VL-7` | task records | **VINLab-owned** (promote to wiki) |
| `models.py` resolved_horizon (euro→horizon) | `lld §6.4` / `SEMANTIC_CONTRACT.md §6.4` | contract + `LLD_VINLab.md` | COMLab contract |
| `models.py` / `stress_rpm.py` stress-idle RPM tiers | `OBD_VOCABULARY.md §3.2`; `PATH_FORWARD.md` Risk 2; `T-VL-4` | `OBD_VOCABULARY.md` (shared) | OBDLab/shared (referenced) |
| `models.py` rated_rpm | `DBS/docs/vehicles_petrol_specimens.csv` `P14_rated_rpm` | DBS dataset | DBS (referenced) |
| `models.py` / `switches.py` O2 sensor type + year rule | `O2_MODEL_STRATEGY.md §3, §9.1`; `OBD_VOCABULARY.md §4.3`; `SEMANTIC_CONTRACT.md §6.3` | `O2_MODEL_STRATEGY.md` + contract | shared/contract (referenced) |
| `cylinder_heuristic.py` config vocabulary | `T-VL-7` success criteria | task record | **VINLab-owned** (promote to wiki) |
| `decypher.md` brand cylinder rules | `docs/decypher.md` | source doc | **VINLab-owned** |

> **Rule for the coder/architect:** when a `vinlab/` numeric cites an *external/shared*
> home (standards, contract, `OBD_VOCABULARY.md`, `O2_MODEL_STRATEGY.md`, DBS), keep citing
> that home — do **not** copy the value into this wiki. When it cites a *task record* or a
> scattered note, the value should be promoted into a VINLab-owned wiki page (below) so the
> citation has a durable canonical home instead of a transient task file.

## VINLab-owned (this wiki is the source of truth)

These rules are genuinely VINLab's and previously lived only in task records / scattered
notes. Each is now authored as a canonical citation target (2026-06-12):

- `10_decode_scope_rules.md` ✅ — petrol-only keyword guard (`_NON_PETROL_KEYWORDS`), the
  17-char length rule, charset/checksum gates + the 3 bypass paths, model-year scope
  **[1990, 2020]**, the year-passthrough set `{0, U, Z}`, and the out-of-scope exceptions.
- `11_engine_resolution.md` ✅ — WMI + low-volume rule, year/`L`-collision disambiguation,
  two-path engine resolution (VDS `vin[3:8]` → `BRAND_VDS`; legacy pos-8 `vin[7]` →
  `BRAND_POS8`), the `T-FX-5` OPSI / Mexican-Mazda finding (`3MZ/3MD/3MV`), and the
  cylinder heuristic displacement-band fallback (`T-VL-7`).
- `12_brand_cylinder_rules.md` ✅ — the per-brand engine-code → cylinder rules as shipped
  in `cylinder_heuristic.py`, promoted from the raw `decypher.md` research draft.

Each restates only **VINLab-owned** values; externally-anchored numbers (stress-idle RPM
tiers, euro→horizon, O2 type, CoC chemistry) are referenced to their homes, never copied —
a leak check across pages 10–12 confirms zero such values appear.

## Externally-anchored (reference, never duplicate)

`SEMANTIC_CONTRACT.md §4.1/§6.x` (schema, euro→horizon, air-metering, O2),
`OBD_VOCABULARY.md §3.2/§4.3` (stress-idle RPM tiers, O2 type), `O2_MODEL_STRATEGY.md`
(downstream-O2 role), the NHTSA/SAE/ISO VIN standards, and the DBS specimen CSV. VINLab
reconciles **up to** these; it does not restate their numbers.

## Canonical surface (what to read)

`VinDNA` = **16 core + 13 CoC** fields. `rated_rpm` is emitted (T-DNA-3); the `emissions`
block is formalized (T-DNA-4: `has_catalyst`/`egr_equipped` nested, `secondary_air_equipped`
dropped); `model` is **kept-empty** (T-DNA-5, no field); `fuel_type`/`altitude_band` are
**proposal-only** (COMLab-E), not live fields. Full tables: `docs/VIN_VOCABULARY.md`;
field/threshold detail: `docs/DLD_VINLab.md` / `docs/LLD_VINLab.md`.

## Graph relations (explicit)

**VINWIKI-00-INDEX** DESCRIBES **VINWIKI-10-DECODE_SCOPE_RULES**
**VINWIKI-00-INDEX** DESCRIBES **VINWIKI-11-IDENTITY_RESOLUTION**
**VINWIKI-00-INDEX** DESCRIBES **VINWIKI-12-BRAND_CYLINDER_RULES**
**vinlab.decoder.RobustVINDecoder.decode_vin_payload** CONSUMES **VINWIKI-10-DECODE_SCOPE_RULES**
**vinlab.decoder.RobustVINDecoder.decode_vin_payload** CONSUMES **VINWIKI-11-IDENTITY_RESOLUTION**
**vinlab.models.VinDNA.rated_rpm** MAPS_TO **comlab.schemas.lab_dna_views.ObdLabDnaView.rated_rpm**
**comlab.projection.project** CONSUMES **vinlab.models.VinDNA.rated_rpm**
**obdlab.core.pid_ingestion_validator.PIDIngestionValidator._check_dna_rpm** CONSUMES **comlab.schemas.lab_dna_views.ObdLabDnaView.rated_rpm**
**fuel_type / altitude_band** PROPOSED_ONLY_FOR **COMLab-E context fields**

## Core Entities

- **VINWIKI-00-INDEX** - Authoritative citation and provenance index for the VINLab wiki corpus. Consumer: `Vault/tasks/T-VIN-VAULT_build_vinlab_vault.md`.
- **VINWIKI-10-DECODE_SCOPE_RULES** - Canonical VINLab-owned decode gates and petrol-only guard. Consumer: `vinlab.decoder.RobustVINDecoder.decode_vin_payload`.
- **VINWIKI-11-IDENTITY_RESOLUTION** - Canonical WMI, year, engine, OPSI, and cylinder fallback logic. Consumer: `vinlab.decoder.RobustVINDecoder.decode_vin_payload`.
- **VINWIKI-12-BRAND_CYLINDER_RULES** - Canonical shipped per-brand cylinder heuristics. Consumer: `vinlab.overlay.cylinder_heuristic.infer_cylinder`.
- **VinDNA.rated_rpm** - Optional VIN output field sourced from DBS P14 and projected into OBDLab. Consumer: `comlab.projection.project` -> `ObdLabDnaView.rated_rpm` -> `PIDIngestionValidator._check_dna_rpm`.
- **fuel_type / altitude_band** - Proposal-only context fields. Consumer: none live; do not frame as a live `CONSUMES` edge.
