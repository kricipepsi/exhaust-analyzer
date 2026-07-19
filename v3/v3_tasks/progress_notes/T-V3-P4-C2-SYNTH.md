# T-V3-P4-C2-SYNTH — progress note

**Task:** seed provisional synthetic C2 (rich_mixture vs catalyst_failure) data for the
22 C2 cases — research-grounded, web-corroborated, tolerance-wide, `synthetic=true`.
**Date:** 2026-07-01 · **Coder:** Claude Code · **Mode:** STRICT (dual-gate)

## What shipped (all new, under `v3/` only)
- `v3/gen_c2_synth_seed.py` — generator. Reads two files only (**read-only**):
  `apps/wired/v7/data/cases_petrol_v7.csv` (for each case's oracle
  `expected_fault_family`) and `V3_SIGNAL_ACQUISITION_SPEC_2026-07-01.json` (C2
  membership). Samples each case's trim/Mode-$06 columns from the web-validated band
  table keyed on its **oracle fault**. Deterministic (PRNG seeded from SHA-256 of
  `case_id`; no wall-clock/`Math.random`). All writes are under `v3/`.
- `v3/data/c2_synthetic_seed_2026-07-01.csv` — 22 cases × C2 columns, `synthetic=true`.
- `v3/data/c2_synthetic_seed_2026-07-01.json` — manifest (per-case values, band_id,
  oracle_fault, citations, no-back-solve note, research limits).
- `v3/reports/V3_C2_SYNTH_BANDS_2026-07-01.md` — per-column `cluster2.md` vs web-real
  vs band-used table, citations, σ tolerance table, per-case table, C2-separability
  disclosure.

## Findings surfaced
- **22/22 seeded.** Oracle split: **11 rich_mixture, 6 catalyst_failure, 3
  lean_condition, 2 sensor_fault** (`expected_fault_family` matches the acquisition
  spec for all 22 — verified).
- **C2-separable = 17** (rich + catalyst): rich cases seeded to total idle trim
  **≤ −12%** (research `-10%` cut cleared at every band corner), catalyst cases to
  near-zero trim + index **> 0.20** + decel CO **> 0.8%**. Audit `_assert_no_backsolve`
  asserts each C2-separable case clears its research limit across the whole spread.
- **Not C2-separable = 5, disclosed (do NOT count as wins):**
  - **3 lean_condition** (CSV-100, EXP-N017, era2_015): positive trim → fire neither
    TRUE_RICH nor a catalyst-fail; seeded honestly from lean ground truth; **stay
    abstained** under the C2 producer/consumer (need a lean/vacuum discriminator).
  - **2 sensor_fault** (case_004, era1_017): O2/ground skew → falsely-elevated index
    that *mimics* catalyst failure (both currently mis-predict `catalyst_failure`).
    Seeded ambiguous (index 0.28–0.55); the passive C2 index **cannot** separate
    sensor skew from real cat failure → likely stays mis-routed until a
    sensor-rationality signal lands. Flagged `c2_separable=false`.
- **Tolerance width stated** (uniform σ = (hi−lo)/√12): rich idle-LTFT band `[−15,−8]`
  σ≈2.02; catalyst index-fail `[0.55,0.90]` σ≈0.10; lean idle-LTFT `[9,18]` σ≈2.60.
  Worst-case corners clear the research limit with margin (report §3).
- **Web-corroboration (6 citations, report §2):** LTFT normal ±10% & rich → −20%
  (ricksfree/engineerfix); Mode $06 rear/front switch ratio healthy-low vs
  failed→1:1 (brakeandfrontend, 0.76 set P0430); healthy cat CO <0.5% vs dead cat
  several-% (aa1car/ipdusa); lean +20/+22% documented, corrects at rpm
  (vehicleservicepros/xerodrive); bad-O2 skew fakes P0420/P0430 (brakeandfrontend).
  Where web showed a wider/shifted range than `cluster2.md`, the wider band was used.
- **No back-solve:** generator inputs = oracle label + band table **only**; it never
  opens `rich_mixture.json`/`catalyst_failure.json` or reads any case's rank/prediction
  (grep-confirmed; stated in report §1 and manifest).
- **Determinism confirmed:** rerun byte-identical (diff clean).

---

VERIFICATION GATE — T-V3-P4-C2-SYNTH
1. Compile : PASS  (py_compile v3/gen_c2_synth_seed.py)
2. Lint    : PASS  (ruff check — All checks passed)
3. Types   : PASS  (pyright v3/gen_c2_synth_seed.py — 0 errors)
4. Tests   : PASS  (`python v3/gen_c2_synth_seed.py` → 22/22 seeded; rerun byte-identical; grep gate 32 matches for synthetic|band|citation|-10%|0.20|tolerance|22)
5. Contract: PASS  (22/22 seeded synthetic=true; each value inside its own oracle-fault band; C2-separable corners clear the research -10%/0.20/0.8% limits; 0 values from consumer rules; 3 lean + 2 sensor flagged not-separable/abstain)
6. Orphan  : N-A   (no engine field/consumer added — this task produces a side-file data column consumed by T-V3-P4-C2A/C2B, named in the spec)
Result: CLEAN

CODE REVIEW — T-V3-P4-C2-SYNTH
Scope         : PASS  (every line traces to the 4 deliverables; no engine/rule/scorer/corpus code)
Composition   : PASS  (no lab edit, no 2nd-lab import, no deferred path; reads corpus+spec, writes only v3/)
Consumers     : PASS  (consumer = T-V3-P4-C2A/C2B named in spec + report §5; no new live field to orphan)
Literals      : PASS  (−10% / +10% / 0.20 / 0.8% cited to cluster2.md §Quantitative Signatures + web sources in report §2)
Docstrings    : PASS  (module + no-backsolve invariant + every function documented)
Craft (WARN)  : Band table is a module-level dict keyed on oracle family; deletion test — removing a family key raises SystemExit (fail-loud), removing a citation drops it from the report only. Seam: seed is a side file (no live-corpus coupling); C2A reads it by path. Non-blocking: `mode06_catalyst_margin_pct` is derived from index vs the 0.20 research limit — documented as a derived (not sampled) column so C2A doesn't double-count it as independent evidence.
Result: CLEAN

## Guardrails honoured
- No write to `cases_petrol_v7.csv` / `corpus_curated.csv`; no engine/lab/registry/rule
  edit; no re-score; no yardstick mint; no abstain-dial change. `run_suite.py` untouched.
  `Vault/` untouched. No `graphify`/frozen-graph rebuild. No secrets. Writes only `v3/`.
- The pre-existing ` M` on `cases_petrol_v7.csv` / `rich_mixture.json` /
  `catalyst_failure.json` predate this task (present at session boot) and were **read
  only** — this task added no diff to them.
