TASK REVIEW — T-VINA-17_type_code_wmis_measured(2) — 2026-11-04 (Windows Cowork)
════════════════════════════════════════════════════════════
VERDICT: ACCEPT   (score 91) — code row; second review run on round 1 (Codex, APPROVE WITH CORRECTIONS)

Branch `fix/T-VINA-17`: spec `c9a2c0d`, round 1 `193dc69`, correction 01 `bfa6af8`, round 2 `44670bc`.
Implementer PID 3920 (sonnet, medium). One return (correction 01).

MECHANICAL GATE
  ✓ deliverables exist           2 code commits; note and RESULT with `## Round 2`
  ✓ changed files in scope       `decoder.py`, `test_type_code_year.py`, `wiki/10_decode_scope_rules.md` only
  ✓ text equals the rehearsal    round 1 byte-equal to `make_rh.py`'s copy, round 2 to `make_rh2.py`'s copy (`cmp`)
  ✓ tests fail without the fix   M1 (set back to 6 WMIs) 6 failed in round 1, 7 in round 2 (the new WDF test also
                                 fails); M2 (digits condition removed) 4 failed; M3 (`vin[9] == "1"` added) 1 failed
  ✓ effect visible               rerun by the reviewer on `44670bc`: vinlab `320 passed, 8 skipped` (base 313);
                                 type-code file `16 passed`; probes `8 passed`; dnalab 27, wired 41, ui 30; doc grep 2;
                                 ruff clean. `VSA63823413020157` → None; `4JGBF71EX7A107518` → 2007

CRITERIA
  1 MET · 2 MET · 3 MET · 4 MET · 5 MET

SECOND REVIEW (recheck/codex/T-VINA-17_review.md, re-derived with recheck/T-VINA-17/non1.py)
  HIGH WDF non-`1` VINs        NOT UPHELD as HIGH: 0 of 5 within one year of registration; the 2 `J` (2018) match only
                               on the 30-year cycle, out of scope. Residue: `WDF63981583465221` (`8`, 2010) ambiguous;
                               the rule returns None, not a wrong year. Stated in the wiki.
  MEDIUM wording               UPHELD → R5.1, fixed in round 2
  MEDIUM surviving mutant      UPHELD → R5.3 + M3, fixed in round 2
  LOW unsourced labels         UPHELD → R5.1, R5.2, fixed in round 2

FINDINGS
  concern  The same digit-form rule suppresses 4 WDB VINs whose non-`1` position 10 matches the registration year
           (non1.out). Pre-existing since T-VINA-2; failure mode None. Not a new row: too small (4 of 23,467).
  nit      Score: one return, caused by the spec's wording (Cowork's), not the implementer.
