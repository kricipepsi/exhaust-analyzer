# REVIEW T-AUD-11d — ACCEPT, score 96 (Windows Cowork, 2026-11-05 22:08 CET)

Facts first: commit `b103252` on `fix/T-AUD-11d` (after spec `a4db998`) changes only
`audit/drift/2026-11-05_DRIFT_REPORT_dtclab.md`. Cowork re-run of `check_report.py`: `sections 8/8, findings 44,
refs ok 77/77`, `REPORT OK` (exit 0). Porcelain: note and RESULT only. Headless run 20:55:15-21:01:42 UTC, exit 0.
Docs row: no second-model review.

## Findings re-derived (44 bullets = 12 distinct drifts, all UPHELD)
Code facts measured by Cowork (venv import and grep):
1. Count notes (PRD:21,56,81,177; HLD:23,25; LLD:54; DLD:51-53,332,429; ADR:104,205,206): `len(DTCRoutingTag)` = 17;
   `routing_tag_map.yaml` 30 `- patterns` entries, 3 `dna_gate:`; `DtcEmissionsView` has 2 fields
   (`dna_view.py:80-81`); the mapper names 2 gates.
2. Derived symptom flags 6 vs 7 (PRD:118, HLD:90, LLD:129, DLD:191, BDD:73): `freeze_frame.py:77-95` has 7 `ff_*` bools.
3. No-start / `MONITOR_ABORTED` called proposed or absent (PRD:159, HLD:217,272, LLD:98, DLD:97,284, BDD:122,
   ADR:243): `Mode06MonitorState` has 4 members, `MONITOR_ABORTED` included.
4. Phase-2 scorer "shipped via the Wired adapter" (PRD:127, HLD:124, DLD:84, ADR:186): `grep -rn classify_top3\|rank_candidates`
   outside the lab finds only `audit/scratch/C3/edge_sweep.py`. **No production caller.**
5. `COMLab.project(..., target='dtc')` builds the view (HLD:48, VOCAB:506, ADR:37): `comlab/projection.py:42` has
   `project`, but `composition.py` never calls it; it uses `_build_dtc_dna_view` (`:596`, T-AUD-4d).
6. "wired (pending T-WIRE-1)" (LLD:27, DLD:26): `composition.py:631` already calls the sanitizer.
7. `rpm <= 180` without a `# wiki:` comment (LLD:51): `freeze_frame_extractor.py:166`.
8. B/C/U "filtered at the ingestion gate" (VOCAB:24): `DTC_REGEX` = `^[BCPU][0-3][0-9A-F]{3}$` (`vocabulary.py:109`),
   and `validate_dtc_list` returns every valid code (`dtc_ingestion_gate.py:53`). **Behaviour, not wording.**
9. Missing mandatory PID "marks the payload FREEZE_FRAME_INCOMPLETE and degrades confidence" (VOCAB:344): the
   extractor raises `FreezeFrameIncompleteError` (`:60`). **Behaviour, not wording.**
10. P0601-P0606 routed (`yaml:151`) but not in the vocabulary fan-out (VOCAB:167).
11. `gpf_combined` gate scenario (BDD:180): no GPF/P244A text in the lab code.
12. `evaluate_monitor` signature: two extra arguments not in the HLD (HLD:217, `mode06_evaluator.py:82`).
- REJECTED: none.

## Score
100 − 2 (`## Time` one phase) − 2 (count findings quote a docstring "17-value canonical form" instead of the enum
itself; re-derived by import) = 96.

## Follow-up
T-AUD-15 (DTCLab docs drift fixes): drifts 1-3, 5-7, 10-12 are wording. Drifts 4, 8 and 9 need a ruling first:
wire the Phase-2 scorer into the composition or document it as unused; filter B/C/U at the gate or correct the
vocabulary; mark-and-degrade or raise on an incomplete freeze frame.

Measured: DTCLab (111 KB docs, 1,664 code lines) → 44 bullets / 12 drifts in 6 min on Sonnet medium.
