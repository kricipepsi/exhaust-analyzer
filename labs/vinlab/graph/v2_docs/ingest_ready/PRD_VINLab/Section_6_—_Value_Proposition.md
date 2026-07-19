> **Context:** VINLab PRD v2.1 (2026-06-12) | Module: VINLab | Section: Section 6 — Value Proposition | Parent document: PRD_VINLab.md / SEMANTIC_CONTRACT section 4.1

## Section 6 — Value Proposition

- **Jobs addressed:** VIN structural validation (charset, length, checksum), WMI →
  brand/country resolution, model-year disambiguation, two-path engine resolution,
  emission-equipment derivation, air-metering classification, stress-idle-RPM
  targeting, cylinder-count inference (fallback), CoC emission-target overlay, and
  confidence grading.
- **Gains created:** one `decode()` call yields a fully typed `VinDNA`; downstream labs
  read enum fields, not raw strings. Air metering is classified once into both a
  developer label (`primary_load_calculation`) and the OBDLab-canonical
  `air_metering_strategy`. The CoC overlay attaches per-engine-code lambda/CO/HC
  targets so GASLab has a ground-truth reference without its own database.
- **Pains relieved:** European VINs without a check digit still decode (data-driven
  bypass via `wmi.csv` country). The `L`-year 1990/2020 collision is resolved by WMI
  `era_hint`. Pre-VIN chassis numbers are distinguished from decode failures. A missing
  reference row downgrades confidence instead of crashing.
- **Competitive advantage:** the decode is fully offline; the heuristics are
  brand-aware (per-manufacturer cylinder rules) yet gated so they never overwrite
  authoritative CSV/DB data; the output is a frozen, contract-governed dataclass that
  every other lab can rely on.

---

## Graph relations (explicit)

**Section 6 — Value Proposition** DESCRIBES **VINLab PRD v2.1 (2026-06-12)**
