# REVIEW T-AUD-22h — ACCEPT, score 92 (Windows Cowork, 2026-11-15)

Runs: Hydrogen lane (gemini-4-hydrogen-high). Run 1: 7 min (22:10-22:17 CET), promoted `5f2726f`. Correction 1:
4 min (22:23-22:27 CET), promoted `30db3c7`. Fence check PASS both times. Docs row: no second-model review
(CLAUDE.md step 6).

## Facts re-derived by Cowork (in the worktree, before each promote)
- Run 1: step 1 `CLAIMS OK group=rest scope=apps/* candidates 209 covered claims 451`; step 2 `CLAIMS OK group=rest
  candidates 411 covered claims 451`, `out_of_scope 129`; step 3 labs 202 OK; `0` removed lines; suspect 38.
- Correction 1: steps 1-3 unchanged; suspect 52 same_as_wiki 5; step 4 `0` removed lines against `79c1e1b`; step 5
  `R9 OK changed 14 missing none`; numstat 14/14 on the CSV (only the suspect field, LF kept).
- Classes after both: ANALYSER_SPEC=203 DIAGNOSTIC_THRESHOLD=36 INTERNAL_PARAMETER=46 NON_DOMAIN=140
  PHYSICAL_CONSTANT=22 TYPICAL_RANGE=4.

## Findings
- Run 1 missed R7's lab-bound comparison (a binding ruling) on five rows: MAF max 500 vs RK0188 655.35, FF RPM 16383
  vs RK0182 8000, FF ECT/IAT 215 vs RK0184/RK0204 140. Correction 1 (R9) marked them and nine more of the same kind
  (WOT lambda 0-3 vs RK0020/21 0.7-1.3, narrowband and FF O2 vs RK0015/16 0.10-0.90 V, ADV MAF/lambda). All 14 upheld
  as R7 cases; the narrowband ones compare an input range with a validity window, so the verification row judges
  whether they are defects or only different semantics.
- The fuel-trim ±127 defect is also in the wired app (`composition.py` six fields, RK0232-RK0263) and the UI
  (`ui_payload.py` OBD_TRIM_MIN/MAX, RK0374/0375): the fix row must cover OBDLab, COMLab, wired and UI together.
- Not ruled, left to the verification row as candidates: GAS CO2/O2 input max 22 % (RK0362/0365; physical ceilings
  about 15.7 % and 20.9 %), downstream O2 max 1.5 V (RK0275/0381; J1979 1.275 V), ADV_DECEL_CO_MAX 25 % (RK0416,
  flagged).
- -8: correction needed for a binding ruling (-6); the RESULT omits the branch/log paste (lane prompt, -2).

Verdict: ACCEPT. The T-AUD-22 inventory is complete: gaslab 188, comlab 1427, rest 411 candidates covered;
`apps/ui/_sample_app_reference.py` out of scope by ruling (checker `OUT_OF_SCOPE`).
