> **Context:** VINLab PRD v2.1 (2026-06-12) | Module: VINLab | Section: Section 3 — Background | Parent document: PRD_VINLab.md / SEMANTIC_CONTRACT section 4.1

## Section 3 — Background

**Context.** The 17-character VIN (ISO 3779 / SAE J853 / NHTSA 49 CFR Part 565) encodes
the World Manufacturer Identifier (positions 1–3), the Vehicle Descriptor Section
(positions 4–9), and the Vehicle Identifier Section (positions 10–17, with the model
year at position 10). Decoding a VIN to a usable engine profile is not a pure
character lookup: European-market VINs frequently omit the NHTSA check digit, the
year code `L` collides between 1990 and 2020, low-volume manufacturers (SAE J853,
`vin[2] == '9'`) place their identifier at positions 12–13, and many engine attributes
must be resolved from a reference database keyed by engine code rather than from the
VIN string itself.

**Why now.** The 4D engine needs a vehicle profile to *filter* the diagnosis — to hide
bank-2 inputs on an inline engine, suppress turbo-boost fields on a naturally-aspirated
car, and pin the per-engine-code emission targets that GASLab compares chemistry
against. The decode must run on the technician's device with no connectivity, so all
reference data (`wmi.csv`, `years.csv`, `vds_engine_map.csv`, `vref.db`) is baked into
`vinlab/data/` at build time and the runtime is network-free and MySQL-free.

**What recently became possible (v2 sibling split, T-RM-2-DNA, 2026-06-06).** VINLab
was forked from v1 `DNALab/VINLab/` into an **independent module** with its own
`pyproject.toml`, own folder, and the no-cross-lab-import boundary. Enum-typed fields
replaced bare `str` annotations (ADR-0004 / T-FX-5). The single-deep-module
air-metering classifier (T-FX-2) replaced two parallel switches. A last-resort
cylinder-count heuristic (T-VL-7) was added behind a `cylinder_count == 0` gate so it
can never overwrite real data. The CoC emission targets were overlaid from petrol CSV
medians keyed by engine code.

---

## Graph relations (explicit)

**Section 3 — Background** DESCRIBES **VINLab PRD v2.1 (2026-06-12)**
