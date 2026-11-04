TASK REVIEW — T-VINA-5_wmi_brand_table(4) — 2026-11-04 (Windows Cowork, round 2 after correction 01; B7 → correction 02)
════════════════════════════════════════════════════════════
VERDICT: ACCEPT   (score 91) — second review (second_review.py, off-peak → ds-flash) APPROVE WITH CORRECTIONS: 6
findings, 0 upheld as defects, 3 nits

Branch fix/T-VINA-5: spec d13b885 … 54ed256 (correction 02), fix cb31bd8 (wmi.csv), fix ed53d94 (vds_engine_map.csv),
test bbc1b6e. Implementer impl-T-VINA-5, PID 8180, t=25 min (10 plan + 10 round-2 parity + 5 build). Score: −3 ×3
nits (N1-N3). Hand-back B7 (soft, COWORK) cost 0 rounds.

MECHANICAL GATE
  ✓ deliverables exist           wmi.csv 5 brand cells; vds_engine_map.csv 12,900 → 12,928; test_wmi_brands.py (19);
                                 note with ## Plan round 2; RESULT
  ✓ changed files in scope       git diff 54ed256..HEAD: the 3 Files-to-touch paths; porcelain: note, RESULT,
                                 blocker JSON (header-authorised sibling)
  ✓ commits on the task branch   cb31bd8, ed53d94, bbc1b6e: `git branch --contains` → fix/T-VINA-5 only
  ✓ tests                        reviewer re-run: vinlab `248 passed, 8 skipped`; test_wmi_brands `19 passed`; dnalab
                                 27, wired 41, ui 30; comlab 526/4/2 (known collection errors), dtclab 590, gaslab
                                 208/2/4 deselected, obdlab 388/2, symptomlab 72 (all = base); ruff clean
  ✓ red on base                  test on 54ed256 data: `10 failed, 9 passed` (make ×5, wrong-side conflict ×5)
  ✓ mutant M8 (reviewer run)     every pick inverted → all 9 test_conflict_key_winner fail; 133/133 served codes flip
  ✓ effect visible               census `real decodes by (WMI, make): []`; engine resolved WDB 26/26, KMH 40/40,
                                 JSA 19/19, JN1 9/10, SAX 9/9 (P3 floors 25/40/19/8/9); C6 f2_ 6 failed → 6 passed

INDEPENDENT DATA CHECK (C:/4DApp/recheck/scratch/vina5_review.py, against vina5_vote_picks.json)
  133 differing keys: served code = vote winner 133/133; share = winner votes / all votes (files 1+2) 133/133.
  347 non-differing wrong-brand keys resolve under the true brand: 0 misses. MAYBACH/DATSUN/STERLING rows 0;
  GENESIS 130, KAWASAKI 152 kept. Exact duplicates 0; folded 123 → 97, after ⊆ before. 11,254 other-brand rows
  identical.

SECOND REVIEW (ds-flash, embedded 44 KB; out C:/4DApp/recheck/codex/T-VINA-5_review.md)
  F1 (HIGH) 7 right-wins MERCEDES-BENZ keys keep a `MERCEDES BENZ` row: NOT UPHELD as a defect. wmi.csv gives every
     Mercedes WMI `MERCEDES-BENZ`/`Mercedes-Benz` (24) or `Mercedes-AMG` (1); the exact key `MERCEDES-BENZ_<vds>` is
     served first, so the spelling rows are unreachable. Pre-existing duplicates → T-VINA-11. The literal wording of
     correction 02 (3) covers them: N1, my wording.
  F2 (MED) the conflict test uses the exact brand only: NOT UPHELD (no WMI yields the space spelling).
  F3 (MED) pos-8 fallback could mask Path A: NOT UPHELD (0 pos-8 rows for the ten brands).
  F4 (MED) kept GENESIS/KAWASAKI rows untested: R4 did not require it; N3, follow-up with T-VINA-12 (5NM/KMT/JSK/JSL).
  F5 (MED) share check inconsistent: NOT UPHELD. My prompt wrote "(w+r)"; the check uses all votes on the key
     (20102: 28/57 = .491), which is R2's rule.
  F6 (LOW) criterion 4 lists only note and RESULT: the blocker JSON is header-authorised; N2, my wording.

DISCLOSED EFFECTS (accepted)
  83 of 133 winners carry share < 0.70 → vds_engine_ambiguous on 42 → 45 of 104 decoded real VINs; cylinder_count
  0 → a count on 27 VINs; agreement with cylinder_count_resolved.md: numeric-share rows 44/38, blank 21/0 (circular).

LEDGER NOTE (R3, written by Cowork)
  # source: wmi.csv rows WDB/KMH/JSA/JN1/SAX hand-fixed (T-VINA-5); vds_engine_map.csv wrong-brand rows re-keyed,
  133 conflicts settled by the Nio 1+2 vote; build_wmi_map.py keeps the last of several vPIC makes per WMI (unfixed
  → T-VINA-12).
