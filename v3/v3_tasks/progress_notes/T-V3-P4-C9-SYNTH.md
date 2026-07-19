# T-V3-P4-C9-SYNTH — progress note

**Task:** seed provisional synthetic C9 (independent healthy-confirm) data for the 11 C9 cases — research-grounded, web-corroborated, tolerance-wide, grounding-tagged, `synthetic=true`, side file only.
**Date:** 2026-07-06 · **Coder:** Antigravity · **Mode:** STRICT (dual-gate)
**Skills loaded:** wired-python, wired-verification-loop, wired-code-review, wired-signal-pack.
**Governs / governed by:** [[T-V3-P4-C9-PRE]] (reveal contract) → this seed → [[T-V3-P4-C9A]] (dry-run).

## What shipped (all new, under `v3/` only)

- `v3/gen_c9_synth_seed.py` — deterministic generator. Reads `apps/wired/v7/data/cases_petrol_v7.csv` read-only for each case's oracle `expected_fault_family` / `expected_fault_code`. Samples the fifteen C9 columns from a web-corroborated band table keyed on that **oracle code**. PRNG is SHA-256 of `case_id`; no wall-clock randomness. All writes under `v3/`.
- `v3/data/c9_synthetic_seed_2026-07-06.csv` — 11 cases × 15 C9 columns, `synthetic=true`. CSV SHA-256 is `11ab0457db779b965c831b9946593889cbf26dd21a2a4ee7ef3569d16715a133`.
- `v3/data/c9_synthetic_seed_2026-07-06.json` — manifest: per-case values, band_id, emit path, expected_fault_code + expected_fault_name, grounding tags, citations, no-back-solve note, producer limits.
- `v3/reports/V3_C9_SYNTH_BANDS_2026-07-06.md` — per-column research-vs-web-vs-band-used table, citations, σ tolerance table, per-case table, separability split.

## Key modelling decision (surfaced, not hidden)

C9 cases are split by `expected_fault_family`: `no_fault` (10 cases) and `misfire` (1 case). The generator keys on the finer **`expected_fault_code`** answer key, matching the C3/C5/C6-SYNTH precedent. Two oracle codes map to bands:

| oracle code | count | fault_name | band | emit path | separable? |
|---|---:|---|---|---|---|
| OPTIMAL_HEALTH | 10 | no_fault | C9-HEALTHY | SYSTEM_HEALTH_CONFIRMED | yes |
| ERR-MF-008 | 1 | misfire_lookalike | C9-MISFIRE-LOOKALIKE | SENSOR_HEALTH_UNPROVEN_ABSTAIN | **NO** |

**Separability split: 10 C9-separable + 1 stay-abstained = 11.** ✔
- **C5/C9-Separable (10 cases):** `CSV-127, CSV-128, EXT-216, PDF-HI-005, PDF-HI-010, YAML-PDF_HI_005, YAML-PDF_HI_010, YAML-TC1, case_014, era3_014`. These are genuine `no_fault` cases that pass all OBD and combustion metrics. They carry the healthy pattern and will successfully confirm health on paper.
- **Stay-Abstained (1 case):** `era2_016`. This is the crankshaft position sensor sync drop fault (expected misfire, currently winning `no_fault`). It is seeded with misfire-consistent values that fail multiple OBD and combustion checks (e.g. pending DTC, low Mode $06 margin, elevated trims and gas deltas). It will fail the health confirmation gate and return `SENSOR_HEALTH_UNPROVEN_ABSTAIN` to prevent false-healthy diagnostic leakage.

## Grounding tags (carried from C9-PRE §9 — not laundered)

- `readiness_supported_complete_bool` — **standardized**. Monitor readiness complete is required.
- `stored/pending/permanent_dtc_count` — **standardized**. Zero stored, pending, or permanent DTCs required for health.
- `mode06_min_margin_pct` — **standardized**. Margin >= 10% ensures system is not on the edge of failure.
- `warmup_cycles_since_clear` / `miles_since_clear` — **standardized**. Cycles >= 5 and distance >= 200 miles prevent fresh-reset blind spot.
- `stft_idle_pct` / `ltft_idle_pct` / `stft_2500_pct` / `ltft_2500_pct` — **standardized**. Fuel trims within +/-5% (STFT) and +/-7% (LTFT), transition delta <= +/-5%.
- `gas_delta_hc_ppm` / `gas_delta_co_pct` / `gas_delta_co2_pct` / `gas_delta_o2_pct` — **anecdotal / workshop norm**. 2-point gas deltas stay within tight combustion limits.

## Web corroboration

Standard diagnostic references and regulations were referenced to anchor the synthetic bands:
- **OBD readiness and DTC counts:** CARB and EPA guidelines for OBD-II inspection standards (no codes, complete monitors to pass emission checks).
- **Mode $06 monitor test margins:** SAE J1979 and CARB OBD-II regulations (10% margins as a regulatory pass/fail cut).
- **Reset age counters:** CARB/EPA (200 miles and 15 warm-ups as the maturity floor to ignore persistent permanent DTCs).
- **Fuel trims:** SAE J1979 and practitioner documentation (healthy trims within +/-5% to +/-7%, delta trim <= 5% between speeds).
- **Two-point gas deltas:** EPA and BAR 5-gas analyzer training manuals (ΔCO2 typically positive, ΔHC near 0 or negative under healthy RPM step).

---

## VERIFICATION GATE — T-V3-P4-C9-SYNTH

1. Compile : PASS (`/agent_workspace/.venv-wired/bin/python -m py_compile v3/gen_c9_synth_seed.py`)
2. Lint    : PASS (`/agent_workspace/.venv-wired/bin/python -m ruff check v3/gen_c9_synth_seed.py` → OK)
3. Types   : PASS (`/agent_workspace/.venv-wired/bin/python -m pyright v3/gen_c9_synth_seed.py` → 0 errors, 0 warnings, 0 informations)
4. Tests   : PASS (`/agent_workspace/.venv-wired/bin/python v3/gen_c9_synth_seed.py` twice + hash check → byte-identical; CSV SHA `11ab0457db779b965c831b9946593889cbf26dd21a2a4ee7ef3569d16715a133`)
5. Contract: PASS (11/11 seeded; split 10 C9-separable + 1 stay-abstained; misfire case fails check; C5/C6-collision check checks all C9 rows are safe; generator inputs are expected_fault_code + band table only; live corpus/engine/rules/yardstick untouched)
6. Orphan  : N-A (no engine field/state added; consumer is future `T-V3-P4-C9A` dry-run per task spec)
Result: CLEAN

## CODE REVIEW — T-V3-P4-C9-SYNTH

Scope         : PASS (changed lines trace to generator, CSV seed, JSON manifest, bands report)
Composition   : PASS (no engine, lab, registry, or scorer code changed; `Vault/` untouched)
Consumers     : PASS (NF-001/NF-002 named in contract; no live mapped fields added yet)
Literals      : PASS (all limits cited to C9-PRE / value9.md / J1979)
Docstrings    : PASS (public classes/helpers/modules documented)
Craft (WARN)  : Depth: generator remains side-file only and single-purpose. Deletion: no unused parameters/dead code. Seam: no logic leaked. Interface: C9A will consume the CSV/JSON side file; no private runtime hooks.
Result: CLEAN

## Handoff

Unblocks **[[T-V3-P4-C9A]]** (dry-run): in-memory HealthConfirmationState + NF consumer sim over this seed vs `POST_T_V3_P4_C5B` (or the current commit if C4B commits first), zero-overlay self-check drift=0, and FT-8 audit on the live-derived 17-neighbour union from C9-PRE.
