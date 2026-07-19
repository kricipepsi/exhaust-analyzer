# T-TH-2 Progress Notes

## VERIFICATION GATE — T-TH-2

```
VERIFICATION GATE — T-TH-2
Phase 1 (syntax):       PASS — python -m py_compile (overlap.py + test_overlap.py)
Phase 2 (type check):   PASS — pyright (0 errors, 0 warnings, 0 informations)
Phase 3 (lint):         PASS — ruff check (All checks passed)
Phase 4 (unit tests):   PASS — pytest tests/test_overlap.py (16 passed, 0 failed, 0 skipped)
Phase 5 (provenance):   N/A — harness code under TestSuite/, not gaslab/. No wiki-derived numeric
                        literals in overlap.py; Monte Carlo parameters are standard algorithm
                        constants, not GASLab thresholds.
Phase 6 (diff review):  PASS — 2 files created (harness/generators/overlap.py,
                        tests/test_overlap.py), 1 edited (HARNESS_PROGRESS.md ledger row).
                        All map to Deliverables.
```

Notes:
- Phase 5 does not apply: `overlap.py` lives under `TestSuite/harness/`, not `gaslab/`. Its only numeric literals are `_MONTE_CARLO_N = 50_000` and `_SEED = 42`, which are algorithm parameters, not wiki-derived thresholds. The `_ENVELOPE` dict values are duplicated from `descriptor.py` (which already carries citations) for the analyzer's standalone use.
- The GASLab integration test generated `T-TH-2_overlap_report.md` (434 lines) directly from the live 34-box descriptor. Key findings: 331/561 overlapping pairs, 21 identical-gas-signature pairs, 100% discrimination ceiling (driven by SAMPLE_INVALID + 5 envelope-only boxes), 13 zero-coverage boxes (volume too small for 50k-sample Monte Carlo).

## CODE REVIEW — T-TH-2

```
CODE REVIEW — T-TH-2
1. Design rule compliance:  PASS — harness code imports no lab; static geometry only;
                            no cross-lab imports; petrol-only box table from descriptor.
2. Scope compliance:        PASS — 2 files created exactly match Deliverables. No
                            "while I was in there" edits. Overlap detection + coverage
                            gap + .md report only. No entry_point calls.
3. Contract changes:        PASS — no changes to ModuleDescriptor, FaultBox, or any
                            existing interface. OverlapAnalyzer consumes the existing
                            descriptor.boxes dict.
4. Docstrings:              PASS — every public class (OverlapAnalyzer, OverlapResult,
                            CoverageGapEstimate, OverlapReport) and public function
                            (write_overlap_report, analyze_overlaps, estimate_coverage,
                            run) has a docstring.
5. Provenance:              N/A — harness code; no wiki citations required (enforced
                            only for gaslab/ per gaslab-wiki-provenance §2).
6. Immediate Checklist:     PASS — type hints on all functions; no mutable defaults;
                            no bare except; f-strings; pathlib (Path); with (write_text);
                            is None checks; sorted imports.
7. Test coverage:           PASS — 16 tests: 6 overlap detection (intersection, disjoint,
                            touching, identical, multiple pairs, one-dim gap), 4 coverage
                            gap (sums to 100%, reproducibility, full-envelope, identical
                            boxes), 1 run(), 4 report writing (basic, identical section,
                            disjoint count, zero-hit section), 1 GASLab integration.
```

Both gates clean. Ready to flip ledger row to `done`.
