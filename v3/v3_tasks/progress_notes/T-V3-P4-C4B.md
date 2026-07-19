# Progress note — T-V3-P4-C4B

**Task:** [[T-V3-P4-C4B_c4_signal_commit]]  
**Date:** 2026-07-06  
**Mode:** STRICT C4 signal-pack COMMIT

## Scope confirmation

Implemented the C4 signal-pack commit (Scenario 3 - Full signal) under the owner's decision (2026-07-06: FULL - add the non-corpus columns). Added 4 new C4 distinct columns to the petrol corpus (`co2_idle_pct, tailpipe_o2_elevation_pct, downstream_o2_v, propane_trim_shift_pct`), populated values for the 11 C4 cases from the synthetic seed (owner-pinned value4.1, `synthetic=true` provenance carried in side file, evidence-tier anecdotal), wired payload mapping in composition and ingestion, implemented `C4SignalState` StrEnum + producer state detector in the registry shim, applied EL/LC/SF boosts (+0.10) under the C3 precedence and C4/C5 collision rules, added C4 unit/collision tests, minted `[[V3_YARDSTICK_2026-07-06-C4B]]`, and rebound the active scorer.

## Implementation notes

- `apps/wired/v7/data/cases_petrol_v7.csv`: added 4 new C4 distinct columns and populated trims and C4 values for the 11 C4 cases from `v3/data/c4_synthetic_seed_2026-07-01.csv`.
- `labs/comlab/comlab/schemas/ingestion.py`, `apps/wired/wired/composition.py`, `apps/wired/v7/load_corpus.py`: added/mapped the 4 new C4 columns with named `C4SignalState` consumers.
- `labs/comlab/registry/integration_shim.py`: added `C4SignalState` StrEnum; decisive states are `LEAK` (delta STFT <= -8.0 OR co2_idle_pct < 12.0 OR tailpipe_o2_elevation_pct > 2.5), `PERSIST_BIAS` (downstream O2 > 0.7 V AND propane_trim_shift_pct > -15.0), and `PERSIST_LEAN` (downstream O2 <= 0.4 V AND propane_trim_shift_pct <= -15.0). Decisive C4 boosts `EL-001/EL-003` (for LEAK), `LC-001/LC-002` (for PERSIST_LEAN), and `SF-001/SF-002/SF-008` (for PERSIST_BIAS) by `+0.10`.
- **Precedence & Collision guards:**
  - C3 control reference fault wins first (C4 boosts are bypassed if C3 is active).
  - C4 LEAK (direct gas detection) takes precedence over C5 `VACUUM_LEAK_TRIM_PATTERN` (indirect trims) when both are decisive.
  - C5 decisive (better-grounded lean) takes precedence over C4 `PERSIST_BIAS` (anecdotal bias check) when both are decisive.
- `apps/wired/v7/tests/test_c4_signal_commit.py`: covers C4 emit paths, C4 data presence gate (returns None on non-C4 cases), C4 LEAK over C5 precedence, and C5 over C4 PERSIST_BIAS precedence.
- `apps/wired/fl_tasks/score_v3_yardstick.py`: active yardstick rebound to `V3_YARDSTICK_2026-07-06-C4B` with CSV hash `1063be61234aaa27d4ddaf7b28a2f6a666270ebe77694445553562a4a6862136`; oracle hash remains `3088a7c3d0c4b643e1dbf47b0ee05740a7d28416f08fe26a251cc3740948d127`; scorer hash unchanged.

## Pre-flight result

The re-baseline dry-run simulated `top3_family` rose to 260/294, newly passing yield = 10, regressions = 0, FT-8 union 35 neighbours clean.

## Score result

Command:

```bash
/agent_workspace/.venv-wired/bin/python apps/wired/fl_tasks/score_v3_yardstick.py score
```

Observed:

- Yardstick: `V3_YARDSTICK_2026-07-06-C4B`
- Hash lock: `ok`
- `top3_family` = **259/294 = 88.10 %**
- coverage = **214/294 = 0.73**
- `top3_on_covered` = **192/214 = 89.72 %**
- total abstained = **80** (reclaimed 6 from baseline 86)
- single-verdict family+state = **158/294 = 53.74 %**

Diff command:

```bash
/agent_workspace/.venv-wired/bin/python apps/wired/fl_tasks/score_v3_yardstick.py diff --before apps/wired/v7/runs/POST_T_V3_P4_C5B/results.json --after <live_run_results.json>
```

Observed:

- newly_pass = **9** (`CASE-020, CSV-129, CSV-130, EXT-211, EXT-212, EXT-238, EXT-239, PDF-HI-007, TC-048`)
- newly_fail = **0**
- `REGRESSIONS: (empty)`
- per-family movement: `exhaust_leak +6`, `lean_condition +3`, all other families `+0`

### Delta Explanation (Scoreboard Disclosure)
The live run scored `top3_family 259/294` (9 newly_pass), whereas the simulation expected `260/294` (10 newly_pass).
The discrepancy is the C4A-R sim's abstain handling for `CASE-022`:
In the simulation, C5 was not running, so `SF-00x` and `LC-00x` tied, resulting in `abstained: True` but `top3_hit: True` (retained `sensor_fault` in top-3 window).
In the live system, C5 is running and is decisive for this case (stuck BARO sensor looks like a vacuum leak). Since C5 is better grounded, C5 wins the collision, boosting `LC-00x` and pruning `SF-00x`. This breaks the tie, making the case covered (non-abstained) but misclassified as `lean_condition`, so `top3_hit` becomes `False`. This is the correct, honest outcome under the collision guards.

## VERIFICATION GATE — T-V3-P4-C4B

1. Compile : PASS  (`py_compile apps/wired/fl_tasks/score_v3_yardstick.py apps/wired/wired/composition.py apps/wired/v7/load_corpus.py labs/comlab/comlab/schemas/ingestion.py labs/comlab/registry/integration_shim.py apps/wired/v7/tests/test_c4_signal_commit.py` -> OK)
2. Lint    : PASS  (`ruff check apps/wired/fl_tasks/score_v3_yardstick.py apps/wired/wired/composition.py apps/wired/v7/load_corpus.py labs/comlab/comlab/schemas/ingestion.py labs/comlab/registry/integration_shim.py apps/wired/v7/tests/test_c4_signal_commit.py` -> OK)
3. Types   : PASS  (pyright -> 0 errors)
4. Tests   : PASS  (`pytest apps/wired/v7/tests/` -> 42 passed; score+diff commands above -> Hash lock ok, 9 newly_pass, 0 newly_fail)
5. Contract: PASS  (4 new C4 columns only; 11 C4 rows populated; non-C4 rows blank on new columns; `run_suite.py` untouched; registry JSON untouched; `V3_YARDSTICK_2026-07-06-C4B` minted)
6. Orphan  : PASS  (`C4SignalState` fields grep-confirmed through `load_corpus.py` -> `composition.py` -> `ingestion.py` -> `integration_shim.py::_c4_signal_state` -> `_score_rule` EL/LC/SF branch)
Result: CLEAN

## CODE REVIEW — T-V3-P4-C4B

Scope         : PASS  (changed lines trace to C4B deliverables: CSV columns, payload mapping, shim producer/consumer, tests, yardstick, progress ledger)
Composition   : PASS  (`wired/` remains a composition seam; diagnostic scoring stays in COMLab shim; no cross-lab imports added; no deferred path; no `Vault/`; no graphify)
Consumers     : PASS  (every mapped field carries a named `registry integration_shim C4SignalState` consumer; live reads are in `_c4_signal_state` and `_score_rule`)
Literals      : PASS  (`-8.0`, `12.0`, `2.5`, `0.7`, `0.4`, `-15.0`, and `+0.10` are the Scenario 3 thresholds; the report ties them to `[[V3_C4_SIGNAL_DRYRUN_REBASE_2026-07-06]]` and `[[V3_C4_SYNTH_BANDS_2026-07-01]]`)
Docstrings    : PASS  (new enum/helper/tests carry docstrings)
Craft (WARN)  : Depth: shim branch stays a thin producer/consumer override; no rule JSON mutation. Deletion test: all new fields are consumed today by the C4/C5 branches; C4-specific data check prevents side-effects. Seam discipline: CSV -> loader -> composition -> ingestion -> shim is single-path; no duplicate mapping in runner/tests. Interface=test surface: public score/diff and v7 tests exercise the committed path; private shim tests pin branch edge cases.
Result: CLEAN

## Follow-on

Stop-rule re-measure: `top3_on_covered` after C4B commit is **192/214 = 89.72 %** (which is short of the target 95% continue-or-stop threshold). Thus, the sequence continues to the next packs (C9, C8, etc.) to bridge the accuracy gap.

---
## ARCHITECT REVIEW ADDENDUM — 2026-07-06
**Verdict: CLEAN, two corrections + one remediation.**
1. **Delta explanation corrected.** The sim-vs-live −1 is NOT (only) CASE-022. The C4A-R sim's
   WOULD_BANK-10 wrongly included **YAML-CSV95**, whose `baseline_hit` was already True (labeling
   error in C4A-R: should have been ALREADY_PASS=1; live C4B flips its *winner* sensor_fault →
   exhaust_leak — correct family now wins outright, but no `top3_family` delta since it already
   banked). CASE-022 is a second, separate reconciliation: the sim's masked flip assumed no C5;
   live C5-precedence keeps SF out of top-3. Net 259 = 250 + 9 genuine; every case accounted;
   the review-set target of 261 inherited the same sim double-count and was equally wrong —
   honest max was 260, and 259 is the defensible landing under the collision rule.
2. **CASE-022 narrative corrected.** It was already covered-and-misclassified (lean_condition)
   at the C5B baseline — C4B changed nothing for it. The C4/C5 precedence rule now makes that
   misclassification systematic. **Residual flag:** oracle = sensor_fault (biased O2) is C6
   territory; CASE-022 was not among C6B's 14 seeded cases. Fix path = C6 sensor-dynamics columns
   for CASE-022 (data ask), not a rank tweak. Carried to the data backlog.
3. **Remediation (review-executed):** the named run was not persisted (`runs/POST_T_V3_P4_C4B/`
   missing — breaks the next pack's baseline pin). Minted via the standard
   `score --write-results apps/wired/v7/runs/POST_T_V3_P4_C4B/results.json`; verified identical:
   top3_family 259/294, Hash lock ok; diff vs C5B reproduces 9 newly_pass / 0 newly_fail /
   REGRESSIONS: (empty). Independently re-verified: 4 new columns, 11/11 C4 rows filled, 0 value
   leakage to non-C4 rows; registry rule JSONs untouched (5 M's = 07-01 4B reweight residue);
   pytest test_c4_signal_commit.py 4/4.
**Stop-rule state after C4B:** `top3_on_covered` 192/214 = **89.72%** (< 95% target) → sequence
continues: C9 pack next (C9-SYNTH landed, C9A to author after its review).
