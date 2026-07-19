### Goal ###
C9 provisional-synthetic seed (side file only) for the 11 C9 cases, per the C9 reveal contract
(`V3_C9_REVEAL_CONTRACT_2026-07-06`) — the values C9A will dry-run on. No live corpus/rules/
yardstick edit. Policy: grounded + tolerance-wide + `synthetic=true` labeled.
### Seeding rule — oracle-keyed, no back-solve ###
Generator keys on the **oracle label + the contract band table only** (never on current ranks,
never on consumer thresholds tuned to flip a case):
- **10 no_fault-oracle cases** (CSV-127, CSV-128, EXT-216, PDF-HI-005, PDF-HI-010,
  YAML-PDF_HI_005, YAML-PDF_HI_010, YAML-TC1, case_014, era3_014) → genuinely-healthy bands from
  contract §2: readiness complete, stored/pending/permanent DTCs = 0, `mode06_min_margin_pct` ≥ 10
  (tolerance-wide above the cut), `warmup_cycles_since_clear` ≥ 5 and `miles_since_clear` ≥ 200
  (comfortably above — do NOT seed near the freshly-cleared blind spot), trims inside ±5/±7
  (P10–P90 spread, not point values), gas deltas inside the §2 bands (Tier-B anecdotal — tag it).
- **era2_016 (oracle = misfire, currently WINNING no_fault)** — the contract's named back-solve
  trap. Seed it per its ORACLE fault: misfire-consistent values that FAIL at least one healthy gate
  honestly (e.g. pending misfire DTC and/or Mode $06 misfire-monitor margin < 10 and/or unstable
  trims). The C9 producer must emit `SENSOR_HEALTH_UNPROVEN_ABSTAIN` on it — this case exists to
  prove C9 does NOT resurrect a false healthy verdict. Never seed it into a passing band.
### Columns ###
All 15 contract columns in the side file (including the 4 already-live trim columns — side file
only; live corpus rows stay empty/null). New-ask columns per contract §5 (11).
### Success criteria ###
1. Generator `v3/gen_c9_synth_seed.py` (adapt `gen_c5_synth_seed.py`): deterministic,
   byte-identical rerun (record csv sha); py_compile+ruff+pyright clean.
2. Side files `v3/data/c9_synthetic_seed_<date>.{csv,json}` + bands report
   `v3/reports/V3_C9_SYNTH_BANDS_<date>.md` with per-column grounding tags carried from the
   contract (§2/§9) and cites (cluster9.1.md / value9.md). Web corroboration where bands are
   anecdotal (C3-SYNTH precedent).
3. Split reconciles: 10 healthy-separable-on-paper + 1 stay-abstained = 11. Paper-separability
   caveat stated (paper > actual flips is the norm — C9A measures).
4. Grep gate; no live corpus/rules/scorer/yardstick/`run_suite.py` touched; score unchanged
   (`top3_family` 250/294 — or the post-C4B number if C4B lands first: re-pin and say so);
   `Hash lock: ok`; `Vault/` untouched.
### Progress hook ###
Ledger T-V3-P4-C9-SYNTH → done; dual-gate note `progress_notes/T-V3-P4-C9-SYNTH.md`. Unblocks
**T-V3-P4-C9A** (dry-run, forward-registered — author after this lands).
### Depends on ###
T-V3-P4-C9-PRE done ✓. Independent of C4B (but if C4B commits first, re-pin baseline in reports).
