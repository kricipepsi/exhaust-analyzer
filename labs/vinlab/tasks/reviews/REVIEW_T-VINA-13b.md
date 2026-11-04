TASK REVIEW — T-VINA-13b_vref_tecdoc_merge(5) — 2026-11-04 (Windows Cowork; plan correction 01 + B8, review correction 02)
════════════════════════════════════════════════════════════
VERDICT: ACCEPT   (score 92) — second review (second_review.py: ds route exit 1 → codex) APPROVE WITH CORRECTIONS:
2 test gaps, both upheld and fixed in revision 02; no data or code defect found

Branch fix/T-VINA-13b on fix/T-VINA-13a: spec 6da3b90, correction 01 11dfa95, build 5bf69e5, correction 02 fe64c8c,
tests 2dfbbba. Implementer impl-T-VINA-13b (opus xhigh), PID 2080. Score: −5 revision round (two rules without an
isolating test), −3 B8 (three spec defects of mine, soft, 0 rounds).

MECHANICAL GATE
  ✓ deliverables exist           merge tool; vref.db 72 → 1,234 rows; builder DDL + migration guard (C1); test file
                                 (20); note with ## Plan, round 2, Revision 02; RESULT with reach.py before/after
  ✓ changed files in scope       git diff 6da3b90..HEAD: the 4 Files-to-touch paths + spec commits; no dnalab/wired/ui
                                 fixture; porcelain: note, RESULT, blocker JSON (header-authorised)
  ✓ commits on the task branch   5bf69e5, 2dfbbba: `git branch --contains` → fix/T-VINA-13b only
  ✓ tests                        reviewer re-run: vinlab `281 passed, 8 skipped`; new file `20 passed`; dnalab 27,
                                 wired 41, ui 30; comlab 526/4/2 (known), dtclab 590, gaslab 208/2/4, obdlab 388/2,
                                 symptomlab 72 (all = base); ruff clean
  ✓ red                          tool moved aside: `18 errors` (before revision 02)
  ✓ mutants (reviewer run)       M5 (0 for has_maf/has_map) 2 failed; M12 (G2 dropped) 1 failed; M19 (G2 iii
                                 qualifier restored) 1 failed; a corrupted original row (5FR rated_rpm + 1) fails the
                                 pinned-digest test
  ✓ effect visible               reach.py row_applied 15 → 506 (predicted 506); second merge run inserts 0 rows,
                                 vref.db unchanged

INDEPENDENT DATA CHECK (Cowork, against `git show 11dfa95:…/vref.db` and the extract)
  72 base rows equal column by column; notnull has_maf/has_map/my_start/my_end 0; 1,162 added rows: has_maf NULL
  1,162, has_map NULL 1,162, o2_type '' 1,162, NULL years 0, start > end 0; 0 collision codes inserted; window
  (min start, max end or 2019, + 1), displacement, induction, euro equal the extract: 0 mismatches.

SECOND REVIEW (codex gpt-6.1-sol, embedded 64 KB; out C:/4DApp/recheck/codex/T-VINA-13b_review.md)
  F1 (MED) G2 (iii) without the "map configuration is blank" qualifier had no isolating test: UPHELD → revision 02
     `test_cylinder_heuristic_two_bank_hint_alone_is_skipped` (kills M19).
  F2 (MED) the 72-row test compared against a baseline rebuilt from the shipped file: UPHELD → revision 02
     `test_shipped_original_rows_match_the_pinned_base_digest` (sha256 89403096…5275 of the 11dfa95 rows).
  No merged value without TecDoc provenance; transaction, rebuild and idempotence found sound.

DISCLOSED EFFECTS (accepted; C2 lists in the RESULT)
  Real VINs: displacement 485, induction 28, fuel GDI 14, air metering MAF_ONLY → HYBRID_MAF_MAP 32 (from stated
  turbo/supercharged/GDI through the unchanged heuristic), euro EURO_1 → EURO_4 11, banks 18, cylinders 12; O₂ and
  confidence 0. Skipped: 24 in vref, 44 collision codes (72 VINs), 35 without my_start, G1 2, G2 39.
  C6 probe f1 population falls 1,113 → 566 (it counts any vref row as euro known); stays red.
FOLLOW-UPS: T-VINA-14 (decoder banks/induction, then rerun the merge for the 41 guarded codes), T-VINA-15 (13 old rows
with has_maf/has_map 0).
