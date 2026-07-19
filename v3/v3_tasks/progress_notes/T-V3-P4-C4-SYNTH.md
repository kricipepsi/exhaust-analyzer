# T-V3-P4-C4-SYNTH — progress note

**Task:** seed provisional synthetic C4 (exhaust_leak vs true_lean vs biased_o2) data for the 11 C4 cases — research-grounded, web-corroborated, tolerance-wide, `synthetic=true`.
**Date:** 2026-07-05 · **Coder:** Antigravity · **Mode:** STRICT (dual-gate)

## What shipped (all new, under `v3/` only)
- `v3/gen_c4_synth_seed.py` — generator. Reads two files only (**read-only**): `apps/wired/v7/data/cases_petrol_v7.csv` (for each case's oracle `expected_fault_family`) and `v3/reports/V3_SIGNAL_ACQUISITION_SPEC_2026-07-01.json` (C4 membership). Samples each case's trim and C4-distinct columns from the web-validated band table keyed on its **oracle fault**. Deterministic (PRNG seeded from SHA-256 of `case_id`; no wall-clock/`random`). All writes are under `v3/`.
- `v3/data/c4_synthetic_seed_2026-07-01.csv` — 11 cases × C4 columns, `synthetic=true`.
- `v3/data/c4_synthetic_seed_2026-07-01.json` — manifest (per-case values, band_id, oracle_fault, citations, no-back-solve note, research limits).
- `v3/reports/V3_C4_SYNTH_BANDS_2026-07-01.md` — per-column `value4.1.md` vs web-real vs band-used table, citations, σ tolerance table, per-case table, C4-separability disclosure.

## Findings surfaced
- **11/11 seeded.** Oracle split: **7 exhaust_leak, 3 lean_condition, 1 sensor_fault** (`expected_fault_family` matches the acquisition spec for all 11 — verified).
- **C4-separable = 11** (when all columns are used): leak cases seeded to delta STFT **[−15.0%, −5.0%]** (collapses at 2500 RPM) + diluted CO2 **[8.0%, 13.0%]** + elevated tailpipe O2 **[1.0%, 5.0%]**, lean cases to persistent positive trim + healthy CO2 **[14.0%, 15.5%]** + normal tailpipe O2 **[0.1%, 0.8%]**, sensor bias to persistent positive trim + healthy CO2/O2 + high downstream O2 voltage **[0.60 V, 0.95 V]** + sluggish propane trim shift **[−14.0%, −2.0%]**.
- **The 3 lean_condition vs 1 sensor_fault** split needs downstream-O2 and propane shift, which are not currently in the corpus. Adding them is a `C4B` decision gated on `C4A` showing whether ΔSTFT-alone is insufficient.
- **Tolerance width stated** (uniform σ = (hi−lo)/√12): leak delta-STFT band `[−15, −5]` σ≈2.89; leak CO2 `[8, 13]` σ≈1.44; biased downstream O2 `[0.60, 0.95]` σ≈0.10. Worst-case corners clear the research limits with safety margin.
- **Web-corroboration (5 citations, report §2):** ΔSTFT leak heuristic (AVI OnDemand / StackExchange), CO2 dilution (Bridge Analyzers), O2 elevation (Bridge Analyzers), downstream O2 bias (Chrysler manuals), propane trim shift (ALLDATA).
- **No back-solve:** generator inputs = oracle label + band table **only**; it never opens rule JSONs or reads case rank/prediction (stated in report §1 and manifest).
- **Determinism confirmed:** rerun byte-identical (diff clean).

---

VERIFICATION GATE — T-V3-P4-C4-SYNTH
1. Compile : PASS  (py_compile v3/gen_c4_synth_seed.py)
2. Lint    : PASS  (ruff check — All checks passed)
3. Types   : PASS  (pyright v3/gen_c4_synth_seed.py — 0 errors)
4. Tests   : PASS  (`python v3/gen_c4_synth_seed.py` → 11/11 seeded; rerun byte-identical; grep gate 26 matches for synthetic|anecdotal|band|value4.1|delta.?stft|tolerance|11)
5. Contract: PASS  (11/11 seeded synthetic=true; each value inside its own oracle-fault band; C4-separable corners clear the research limits; 0 values from consumer rules)
6. Orphan  : N-A   (no engine field/consumer added — this task produces a side-file data column consumed by T-V3-P4-C4A/C4B, named in the spec)
Result: CLEAN

CODE REVIEW — T-V3-P4-C4-SYNTH
Scope         : PASS  (every line traces to the 4 deliverables; no engine/rule/scorer/corpus code)
Composition   : PASS  (no lab edit, no 2nd-lab import, no deferred path; reads corpus+spec, writes only v3/)
Consumers     : PASS  (consumer = T-V3-P4-C4A/C4B named in spec + report §5; no new live field to orphan)
Literals      : PASS  (limits cited to value4.1.md §Quantitative Signatures + web sources in report §2)
Docstrings    : PASS  (module + no-backsolve invariant + every function documented)
Craft (WARN)  : Band table is a module-level dict using the FamilyBandInfo dataclass for complete pyright strict-mode compliance; deletion test — removing a family key raises SystemExit (fail-loud). Seam: seed is a side file (no live-corpus coupling); C4A reads it by path. Non-blocking: stft_2500_pct is derived from stft_idle_pct + delta_stft to guarantee in-band delta STFT values without knife-edge alignment.
Result: CLEAN

## Guardrails honoured
- No write to `cases_petrol_v7.csv` / `corpus_curated.csv`; no engine/lab/registry/rule edit; no re-score; no yardstick mint; no abstain-dial change. `run_suite.py` untouched. `Vault/` untouched. No `graphify`/frozen-graph rebuild. No secrets. Writes only `v3/`.
