# REVIEW T-AUD-22f — ACCEPT, score 98 (Windows Cowork, 2026-11-15)

Run: Hydrogen lane (gemini-4-hydrogen-high), 7 min agy wall time (19:53-20:00 CET); fence check PASS; promoted on
fix/T-AUD-22f. Docs row: no second-model review (CLAUDE.md step 6).

## Facts re-derived by Cowork (in the worktree, before promote)
- Step 1: `CLAIMS OK group=comlab scope=labs/comlab/comlab/config/*.yaml candidates 213 covered claims 1614`.
- Step 2: `era_limits 9 linked 9`. Step 3: `CLAIMS OK group=comlab candidates 1427 covered claims 1614` — the whole
  COMLab group is now covered.
- Step 4: `0` removed lines; rows CK1381 on appended.
- The 9 era rows (CK1384-CK1396): CO 1.0 / 0.5 % suspect against W1109/W1110 (DVSA-confirmed MOT limits) and the
  Euro idle claims; lambda ±0.10 / ±0.05 suspect against W1112 (0.97-1.03); HC 150 / 55 / 15 ppm suspect against
  W1111 (200 ppm); MODERN CO 0.2 % linked to W1110. This matches the DISPUTE Cowork raised to the operator.

## Findings
- The era thresholds are the next fix candidates (after a verification row rules on them): CO above the legal limit
  for catalyst eras is the same defect class as the CO 0.45 % "normal" (T-GASA-F45).
- -2: the RESULT omits the branch/log paste (lane prompt).

Verdict: ACCEPT.
