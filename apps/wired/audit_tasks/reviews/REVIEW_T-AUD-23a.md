# REVIEW T-AUD-23a — ACCEPT, score 95 (Windows Cowork, 2026-11-15)

Run: Hydrogen lane (gemini-4-hydrogen-high), 8 min agy wall time (22:35-22:43 CET); fence check PASS; promoted on
fix/T-AUD-23a (`ff9f7b8`). Docs row: no second-model review (CLAUDE.md step 6).

## Facts re-derived by Cowork (in the worktree, before promote)
- Step 1: `verdicts CONFIRMED=4 CONTRADICTED=14 PARTLY=7`, `sources 10 primary 8`, `VERDICTS OK scope=T-AUD-23a.txt
  claims 25`. Step 2: `VERDICTS OK scope=T-GASA-17.txt claims 20`. Step 3: `0` removed lines; no `search/` left.
- New sources: S012 (Wikipedia OBD-II PIDs, SECONDARY), S013 (Underhood Service misfire codes, TRADE). The era and
  no-fault verdicts cite the T-GASA-17 primary sources S001, S002, S009.

## Verdicts checked against Cowork's own knowledge
- Fuel trim ±127 (CK0181, RK0030-32, RK0082, RK0191/0192; with `same_as` also composition.py and ui_payload.py):
  CONTRADICTED. SAE J1979 PIDs 06-09 = (A-128)·100/128, -100 % .. +99.22 %. Agrees. Total trim ±254 (CK0179):
  CONTRADICTED, sum spans -200 .. +198.44 %. Agrees.
- Freeze-frame ECT/IAT 215 °C, O2 0-1.275 V: CONFIRMED (PID encodings). RPM 16383, MAF 500, IAT 140: PARTLY (inside the
  PID range). Agrees.
- Misfire P0300-P0304 (CK0482): CONTRADICTED; cylinder codes run P0301-P0312. Agrees.
- Era thresholds: CO 1.0 (Euro 1-2) and 0.5 (Euro 3-4) CONTRADICTED against 0.5 % / 0.3 % natural-idle limits (S009);
  lambda ±0.10 and ±0.05 CONTRADICTED against 1 ± 0.03 (S002 8.2.1.2); HC 150/55/15 and lambda ±0.02 PARTLY (match no
  legal value, not looser). No-fault CO 0.5 (CK0535) CONTRADICTED (0.3 %). Agrees; this settles the 2026-11-15 DISPUTE
  on the era limits.

## Findings
- -3: every J1979 verdict rests on a SECONDARY source (allowed by R5 with a note; each carries it). A CARB 13 CCR
  1968.2 draft was fetched and dropped without saying in the note why it did not state the scaling.
- -2: the RESULT omits the branch/log paste (lane prompt).

Verdict: ACCEPT. Fix rows now have evidence: fuel-trim bounds in OBDLab, COMLab, the wired app and the UI; COMLab
misfire range; era thresholds; no-fault CO ceiling.
