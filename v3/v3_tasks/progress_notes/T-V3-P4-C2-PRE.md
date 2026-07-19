# T-V3-P4-C2-PRE — progress note

**Task:** freeze the signal-pack **reveal contract** (pre-author disclosure, read-only).
**Date:** 2026-07-01 · **Coder:** Claude Code · **Mode:** STRICT (dual-gate)

## What shipped (all new, under `v3/` only)
- `v3/build_reveal_contract.py` — read-only extractor over `cluster2.md`, the C2
  acquisition contract JSON, and the two registry rule files. Derives the FT-8
  neighbour set live; writes the contract JSON. No engine/lab/registry/corpus
  import-mutation.
- `v3/reports/V3_SIGNAL_PACK_REVEAL_CONTRACT_2026-07-01.json` — machine-readable
  template + C2 worked instance.
- `v3/reports/V3_SIGNAL_PACK_REVEAL_CONTRACT_2026-07-01.md` — the frozen contract.

## Findings surfaced
- **Reveal contract (5 sections)** frozen cluster-agnostic: `BUILDABLE_NOW` /
  `SCORING_GATED` / `CODE_LANDED != SCORE_MOVED` / `REGRESSION-FT8` /
  `ABSTAIN_FALLBACK`, each with a one-line definition + how the `C*A`/`C*B` pair
  fills them.
- **C2 producer** thresholds cited to `cluster2.md`: Total Fuel Trim `<= -10%` →
  TRUE_RICH; Mode $06 index ratio `<= 0.20` → catalyst pass; `Δt_osc < 0.5 s` →
  fail; decel-sweep `CO > 0.8%` → fail; misfire/heater pre-gate → invalid.
  Producer-tuning risk flagged: `0.20` / OSC / CO cut-points are vehicle-dependent
  tuning params to confirm on real values, not universal constants (only the
  `-10%` trim cut is portable — mirrors live RM rules).
- **C2 consumers** named: `rich_mixture.json` RM-001/RM-003/RM-004 (read `longft1`/
  `shrtft1`) and `catalyst_failure.json` CF-001/CF-002/CF-006/CF-007 (read
  `CATALYST_OVERWHELMED`/`NORMAL_OPERATION` + gas PIDs).
- **C2 case split:** 22 = **0 BUILDABLE_NOW** + **22 SCORING_GATED**
  (11 OUTRANKED_HARD + 11 PRODUCER_GAP_SIGNAL_REQUIRED). Reconciles to 22. All
  need trims + Mode $06 catalyst columns → cannot move score without owner data.
- **FT-8 neighbour set** derived live = **33** cases (union of `passes_cases`
  across 4 RM + 7 CF rules, both competition groups). 5 cases
  (PDF-HI-006/CASE-023/EXT-217/RULE-CO-1/PDF-HI-001) are both C2 targets **and**
  regression-sensitive — named.
- **Owner next-task fork surfaced, NOT decided:** (i) build C2 logic now (scoring
  deferred) vs (ii) hold all pack code until C2 data — cost/benefit each.

---

## VERIFICATION GATE — T-V3-P4-C2-PRE
1. Compile : PASS  (`py_compile v3/build_reveal_contract.py`)
2. Lint    : PASS  (`ruff check v3/build_reveal_contract.py` → All checks passed!)
3. Types   : PASS  (`pyright v3/build_reveal_contract.py` → 0 errors, 0 warnings)
4. Tests   : N-A   (read-only doc-generation task; no unit test in scope — the
   task defines a run + grep gate, not a pytest. Extractor run reproduces the
   split: `22 -> 0 BUILDABLE_NOW / 22 SCORING_GATED (OUTRANKED_HARD 11 + PRODUCER_GAP 11)`,
   FT-8 union 33.)
5. Contract: PASS  (grep gate: 5 reveal sections present w/ definitions; C2
   thresholds cited to `cluster2.md`; RM/CF consumers named; 22 split & reconciled;
   owner fork stated undecided. `grep -icE 'BUILDABLE_NOW|SCORING_GATED|CODE_LANDED|FT-8|ABSTAIN|-10%|0.20|22'` = 38 lines.)
6. Orphan  : N-A   (adds no live field/consumer — this task *specifies how packs
   disclose*; the C2 consumer rules named are existing, verified present in
   `rich_mixture.json`/`catalyst_failure.json`.)
Result: CLEAN

## CODE REVIEW — T-V3-P4-C2-PRE
Scope         : PASS  (every line traces to a deliverable: template, C2 producer/
                consumer/case-split/FT-8, owner fork. No adjacent refactor.)
Composition   : PASS  (no lab/registry/engine/corpus edit; two rule JSONs read-only;
                no 2nd-lab import; no deferred path; no graphify. Writes only `v3/`.)
Consumers     : PASS  (signal/noise consumer named = owner (fork) + every later
                signal-pack task (inherits template). No new engine field added.)
Literals      : PASS  (every numeric — `-10%`, `0.20`, `0.5 s`, `0.8%`, `0.45 V` —
                carries a `cluster2.md` section/step cite in the producer table.)
Docstrings    : PASS  (module + `build_contract`/`_ft8_neighbours`/`_c2_case_split`
                docstrings present.)
Craft (WARN)  : Depth — extractor is a thin read→assemble→write seam; FT-8 union is
                computed from the live rule files (not hand-copied) so it can't
                drift from the registry. Deletion test — no dead param; the static
                threshold/section tables are the transcribed research content, not
                removable. Seam — all mapping lives in one script; the `.md` is
                hand-authored prose mirroring the JSON. Interface — extractor's
                public surface is `main()` (CLI) + `build_contract()`; run
                reproduces the disclosed numbers.
Result: CLEAN

## Guardrails honoured
No producer/consumer wired · no corpus column · no rule/weight edit · no re-score ·
no yardstick mint · no synthesized values · MARGIN unchanged (0.02) · `run_suite.py`
untouched · `Vault/` untouched · no `graphify` · no secrets · `git status` shows only
new files under `v3/`.
