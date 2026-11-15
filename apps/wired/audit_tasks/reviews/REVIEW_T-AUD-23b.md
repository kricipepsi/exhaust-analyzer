# REVIEW T-AUD-23b — ACCEPT, score 96 (Windows Cowork, 2026-11-15)

Run: Hydrogen lane (gemini-4-hydrogen-high), 20 min agy wall time (22:48-23:07 CET; note: 18.5 min); fence check
PASS; promoted on fix/T-AUD-23b (`20f9274`). Docs row: no second-model review (CLAUDE.md step 6).

## Facts re-derived by Cowork (in the worktree, before promote)
- Step 1: `verdicts CONFIRMED=5 CONTRADICTED=9 PARTLY=15`, `sources 25 primary 10`, `VERDICTS OK scope=T-AUD-23b.txt
  claims 29`. Step 2: T-GASA-17 20 and T-AUD-23a 25 `VERDICTS OK`. Step 3: `0` removed lines; no `search/` left.
- 15 new sources S014-S028: OIML R 99 (PRIMARY_STANDARD), CARB 13 CCR 1968.2 (LII copy, PRIMARY_LAW), Bosch
  Motorsport NTC and LSU 4.9 pages, Toyota repair manual (OEM), trade texts (Walker, Fluke, ALLDATA, Gears, Underhood
  Service, Bridge, Crypton, Apex), Wikipedia VE (SECONDARY).

## Verdicts checked against Cowork's own knowledge
- CONTRADICTED and agreed: ECT NTC >10 kohm at 20 °C and 2-3 kohm at 90 °C (CK1378/CK1376; Bosch 2.5 kohm and 0.24
  kohm); MAF idle 2-8 g/s per litre (CK1359; ~1 g/s/L); no-fault O2 <= 0.6 % and NOx <= 300 ppm (CK0537/CK0547; a
  working catalyst gives O2 below about 0.35 % and near-zero idle NOx); post-repair HC < 120 ppm (CK1326); the
  catalyst-overwhelmed rear O2 window 0.4-0.5 V (CK0714/0715; a failed catalyst makes the rear sensor switch); VE skew
  fault above 90 % (RK0062; healthy NA engines reach 85-95 %).
- PARTLY and agreed: the wide UI input bounds (CO2/O2 22 %, decel CO 25 %, downstream O2 1.5 V, WOT lambda 0-3)
  exceed the physical or analyser range but block no real reading; stuck-rich 0.7/0.8 V and lazy-sensor < 0.25 Hz are
  defensible thresholds that differ from the vocabulary; ECT > 80 °C vs OEM 75 °C enable.
- CONFIRMED: CO2 ceiling ~16 % (theoretical dry maximum ~15.5 %, disclosed under Disputes), pinned-rich > 0.80 V,
  switching > 0.5 Hz and 1-2 Hz, wideband AFR 14.7.

## Findings
- -2: the RESULT omits the branch/log paste (lane prompt). -2: 13 of 29 verdicts rest on TRADE or SECONDARY sources
  (allowed by R5 with a note; each carries it).

Verdict: ACCEPT. The fix rows have evidence for: the ECT NTC table, MAF idle baseline, no-fault gas window, catalyst
rear-O2 gate, VE skew cutoff (with T-AUD-23a: fuel trims, misfire range, era thresholds, no-fault CO).
