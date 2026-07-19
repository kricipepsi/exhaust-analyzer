# T-V3-P4-C6-SYNTH — progress note

**Task:** seed provisional synthetic C6 (sensor fault under-detection) data for the 14 C6 cases — research-grounded, web-corroborated, tolerance-wide, grounding-tagged, `synthetic=true`, side file only.
**Date:** 2026-07-05 · **Coder:** Codex · **Mode:** STRICT (dual-gate)
**Skills loaded:** wired-python, wired-verification-loop, wired-code-review, wired-signal-pack, firecrawl.
**Governs / governed by:** [[T-V3-P4-C6-PRE]] (reveal contract) → this seed → [[T-V3-P4-C6A]] (dry-run) → C6B (commit).

## What shipped (all new, under `v3/` only)

- `v3/gen_c6_synth_seed.py` — deterministic generator. Reads one live file read-only (`apps/wired/v7/data/cases_petrol_v7.csv`) for each case's oracle `expected_fault_family` / `expected_fault_code`. Samples the nine C6 sensor-dynamics columns from a web-corroborated band table keyed on that **oracle code**. PRNG is SHA-256 of `case_id`; no wall-clock randomness. All writes under `v3/`.
- `v3/data/c6_synthetic_seed_2026-07-05.csv` — 14 cases × 9 C6 columns, `synthetic=true`.
- `v3/data/c6_synthetic_seed_2026-07-05.json` — manifest: per-case values, band_id, emit path, oracle_fault_code + fault_name, grounding tags, citations, no-back-solve note, producer limits.
- `v3/reports/V3_C6_SYNTH_BANDS_2026-07-05.md` — per-column research-vs-web-vs-band-used table, citations, σ tolerance table, per-case table, separability split.

## Key modelling decision (surfaced, not hidden)

13/14 C6 cases share `expected_fault_family = sensor_fault`, so the family is not a usable band discriminator. The generator keys on the finer **`expected_fault_code`** answer key, matching the C3-SYNTH precedent. Four oracle codes map to bands:

| oracle code | count | fault_name | band | emit path | separable? |
|---|---:|---|---|---|---|
| ERR-SF-001 | 9 | upstream_o2_sensor_lazy_response | C6-O2-LAZY | O2_LAZY_OR_BIASED | yes |
| ERR-SF-005 | 3 | sensor_fault_normal_operation | C6-O2-IMPLAUSIBLE-NORMAL-CHEM | O2_LAZY_OR_BIASED | yes |
| ERR-SF-004 | 1 | sensor_fault_vvt_context | C6-MAF-UNDERREAD | MAF_UNDERREAD | yes |
| ERR-MF-005 | 1 | misfire_lookalike_pdf_4g_05 | C6-HEALTHY-LOOKALIKE-MISFIRE | SENSOR_HEALTH_UNPROVEN_ABSTAIN | **NO** |

**Separability split: 13 C6-separable + 1 stay-abstained = 14.** ✔ `PDF-4G-05` is the named lookalike from the task: oracle `misfire`, current engine says `sensor_fault`. It is seeded healthy on every C6 signal — Mode $06 margin high, O2 timing fast, MAF deltas normal — so C6 stops supporting the wrong sensor verdict and leaves it for a misfire discriminator.

## Grounding tags (carried from C6-PRE §8 — not laundered)

- `mode06_o2_response_margin_pct` — **standardized-transport / manufacturer-specific numeric limit**. Seeded as a relative margin to the vehicle's own limit; no universal numeric Mode $06 limit is claimed.
- `o2_rich_to_lean_ms` / `o2_lean_to_rich_ms` — **manufacturer-typical**. Direction is strong; the synthetic slow bands are provisional and deliberately not presented as fleet-wide fail lines.
- `maf_actual_calc_delta_pct_idle` / `maf_actual_calc_delta_pct_2500` — **empirical-inferred**. Fault band is >15% under-read at both points, widened past the 10–15% research screen and Bosch component-level accuracy.
- `maf_gps_*` / `calc_airflow_gps_*` — derived support values. MAF-less/speed-density support exists in the generator (`maf_applicable=false` → all MAF columns `None`); this case split has **0** MAF-less rows.

## Web corroboration

Firecrawl was the mandated path for live web research. `firecrawl --status` initially failed (`command not found`), `npm install -g firecrawl-cli` succeeded, then `firecrawl --status` reported **not authenticated**. No `.firecrawl/` scratch artifact was produced. The report and manifest therefore cite the already-landed, web-corroborated `cluster6.md` source set plus its primary URLs:

- CARB OBD II final regulation for O2 monitor/response-rate framework and Mode $06/J1979-style result/limit reporting.
- Bosch HFM2 datasheet mirror for MAF component accuracy / response anchor.
- DENSO MAF technical page for contamination / load-input corruption mechanism.
- Gears Magazine professional trade article for practical MAF rationality comparison.

This preserves the task's web-corroboration requirement without fabricating a fresh scrape.

---

## VERIFICATION GATE — T-V3-P4-C6-SYNTH

1. Compile : PASS (`/agent_workspace/.venv-wired/bin/python -m py_compile v3/gen_c6_synth_seed.py`)
2. Lint    : PASS (`/agent_workspace/.venv-wired/bin/python -m ruff check v3/gen_c6_synth_seed.py` → OK)
3. Types   : PASS (`/agent_workspace/.venv-wired/bin/python -m pyright v3/gen_c6_synth_seed.py` → 0 errors, 0 warnings, 0 informations)
4. Tests   : PASS (`/agent_workspace/.venv-wired/bin/python v3/gen_c6_synth_seed.py` twice + hash check → byte-identical; CSV `2adec94f…`, JSON `9a6b1259…`, MD `9861e411…`; keyword check count 51)
5. Contract: PASS (14/14 seeded; split 13 C6-separable + 1 stay-abstained; PDF-4G-05 below every C6 gate; generator inputs are oracle label + band table only; live corpus/engine/rules/yardstick untouched by this task)
6. Orphan  : N-A (no engine field/state added; consumers are future `T-V3-P4-C6A` dry-run and C6B commit per task spec)
Result: CLEAN

## CODE REVIEW — T-V3-P4-C6-SYNTH

Scope         : PASS (changed lines trace to the four deliverables: generator, CSV seed, JSON manifest, bands report)
Composition   : PASS (no lab edits, no live corpus edit, no registry/rule edit, no deferred path, no `Vault/`, no `graphify`)
Consumers     : PASS (no live mapped field added; task names `T-V3-P4-C6A`/C6B as consumers; manifest carries emit-path mapping for O2_LAZY_OR_BIASED / MAF_UNDERREAD / SENSOR_HEALTH_UNPROVEN_ABSTAIN)
Literals      : PASS (producer limits and synthetic bands are cited to C6-PRE / cluster6.md / web-corroborated source set; report states manufacturer-specific and empirical-inferred limits explicitly)
Docstrings    : PASS (new generator module + public helper functions documented where useful)
Craft (WARN)  : Depth: generator stays side-file only and single-purpose. Deletion: no unused parameters or dead branches; `maf_applicable=false` support is retained because the task explicitly requires MAF-less rows to become `None`. Seam: no mapping logic leaked into wired/ or labs/. Interface: C6A will consume the CSV/JSON side file; no private runtime hook added.
Result: CLEAN

## Handoff

Unblocks **[[T-V3-P4-C6A]]** (dry-run): in-memory SensorDynamicsState + SF/NF consumer sim over this seed vs `POST_T_V3_P4_C3B`, zero-overlay self-check drift=0, scenario ladder (Mode $06 only / O2 timing fallback / MAF plausibility / all columns), and FT-8 audit on the live-derived 33-neighbour union from C6-PRE. C6A must treat `PDF-4G-05` staying abstained as correct, not as a shortfall.
