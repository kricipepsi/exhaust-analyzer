# REVIEW T-AUD-22g — ACCEPT, score 97 (Windows Cowork, 2026-11-15)

Run: Hydrogen lane (gemini-4-hydrogen-high), 11 min agy wall time (20:05-20:16 CET); fence check PASS; promoted on
fix/T-AUD-22g. Docs row: no second-model review (CLAUDE.md step 6).

## Facts re-derived by Cowork (in the worktree, before promote)
- Step 1: `CLAIMS OK group=rest scope=labs/* candidates 202 covered claims 210`; classes ANALYSER_SPEC=45
  DIAGNOSTIC_THRESHOLD=34 INTERNAL_PARAMETER=31 NON_DOMAIN=75 PHYSICAL_CONSTANT=21 TYPICAL_RANGE=4; suspect 20
  same_as_wiki 5.
- Step 2: `CLAIMS FAIL 338 error(s)` (the apps remainder, unchanged). Step 3: `0` removed lines; RK0001-RK0210.

## Findings
- 20 suspects. The largest group (14) is fuel-trim bounds of ±127 in payload.py, physical_sensor_bounds.json,
  pid_ingestion_validator.py and semantic_consistency_checker.py: SAE J1979 scales STFT/LTFT as (A-128)*100/128,
  so the range is -100 % to +99.22 %; ±127 is the raw byte, not a percent. A real cross-lab defect (COMLab CK0181-
  CK0194 hold the same), to the verification and fix rows.
- RK0088/RK0204 (IAT max 140 vs OBDLab wiki 80 C): the wiki's 80 C ceiling is itself doubtful (heat-soaked IAT can
  pass 80 C; the SAE PID range is -40 to 215 C). The verification row must judge both values, not adopt the wiki's.
- -3: the RESULT omits the branch/log paste (lane prompt); "citation not found" count only in the RESULT.

Verdict: ACCEPT.
