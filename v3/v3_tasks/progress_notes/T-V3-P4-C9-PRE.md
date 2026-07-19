# T-V3-P4-C9-PRE — progress note

**Task:** C9 reveal-contract DISCLOSURE (read-only) — instance the frozen signal-pack reveal-contract template for C9.
**Date:** 2026-07-06 · **Coder:** Agy · **Mode:** STRICT (dual-gate)
**Skills loaded:** wired-python, wired-verification-loop, wired-code-review, wired-signal-pack.
**Governed by:** [[T-V3-P4-C5B]] (done) / [[T-V3-P4-C4A-R]] (done) → this task → unblocks C9-SYNTH / C9A.

## Disclosures established

1. **C9 Source Docs Located:** Verified the existence of `cluster9.1.md` and `cluster9.2.md` in `v3/research/research_answers/` and `value9.md` in `v3/research/value_answers/` as the valid C9 cluster studies. No improvisation was needed.
2. **Quantitative Thresholds & Grounding:** Transcribed 13 C9 producer thresholds covering readiness monitor completeness, DTC counts (stored/pending/permanent), Mode $06 margins, warm-up/mileage reset age, STFT/LTFT trims, trim delta, and two-point 5-gas deltas. Grounding tags are assigned (standardized, manufacturer-typical, anecdotal) and citations are pinned to `cluster9.1.md` and `value9.md`.
3. **Already-Live Column Audit:** Checked C9 columns against the active petrol cases CSV header. Found that 4 columns (`stft_idle_pct, ltft_idle_pct, stft_2500_pct, ltft_2500_pct`) are already live (landed in C2B/C5B), while 11 columns are genuinely new (readiness completeness, stored/pending/permanent DTC counts, Mode $06 minimum margin, warm-up cycles since clear, miles since clear, and 4 gas deltas).
4. **C6 & C3 Interactions Disclosed:**
   - C6 interaction: C6B prunes NF-001/NF-002 when `c6_decisive` is True (sensor dynamics show degradation). C6 prune takes precedence over C9 boost to prevent overriding degraded/lazy sensors.
   - C3 interaction: C3 active control reference faults inherently invalidate C9 no_fault calls because they represent active ECU faults.
5. **Case Split Reconciled:** Reconciled all 11 C9 cases: 10 SCORING_GATED (DATA_GAP_ACQUISITION_GAP) + 1 TUNABLE_HELD (`era2_016`, misfire lookalike, currently winning no_fault in baseline but expected misfire).
6. **FT-8 Neighbour Union:** Live derived 17 neighbour cases from `no_fault.json` rules NF-001/002 + runtime baseline winners. Pinned the 5 dual target+neighbour cases: `PDF-HI-005, PDF-HI-010, YAML-PDF_HI_005, YAML-TC1, era2_016`.
7. **Extractor Script Built:** Authored `v3/build_c9_contract.py` which dynamically generates the JSON contract and the Markdown report. Passed all linting and type-checking checks.

---

## VERIFICATION GATE — T-V3-P4-C9-PRE

1. Compile : PASS (`/agent_workspace/.venv-wired/bin/python -m py_compile v3/build_c9_contract.py`)
2. Lint    : PASS (`/agent_workspace/.venv-wired/bin/python -m ruff check v3/build_c9_contract.py` → OK)
3. Types   : PASS (`/agent_workspace/.venv-wired/bin/python -m pyright v3/build_c9_contract.py` → 0 errors, 0 warnings)
4. Reports : PASS (Generated JSON twin `v3/reports/V3_C9_REVEAL_CONTRACT_2026-07-06.json` and Markdown `v3/reports/V3_C9_REVEAL_CONTRACT_2026-07-06.md` matches C5 template format)
5. Contract: PASS (11 case split reconciled; 17 FT-8 union neighbours audited regression-free; C6/C3 interactions documented; 11 new vs 4 live columns audited)
6. Orphan  : N/A (read-only disclosure, no live code modifications)
Result: CLEAN

## CODE REVIEW — T-V3-P4-C9-PRE

Scope         : PASS (only created build_c9_contract.py, generated reports, and modified PROGRESS.md / progress notes)
Composition   : PASS (no lab edits, no live registry/rule edit, no deferred path, no `Vault/`, no graph-building-tool calls)
Consumers     : PASS (NF-001/NF-002 consumer mapping documented and interaction with C6/C3 shim logic disclosed)
Literals      : PASS (retained all quantitative threshold citations to cluster9.1.md and value9.md)
Docstrings    : PASS (provided clear docstrings on all functions in build_c9_contract.py)
Craft (WARN)  : Depth: stays side-file only under v3/. Deletion: no code deleted. Seam: no changes leak into live code. Interface: output JSON and Markdown reports conform to spec.
Result: CLEAN
