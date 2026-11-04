TASK REVIEW — T-VINA-12_wmi_make_by_registry(4) — 2026-11-04 (Windows Cowork)
════════════════════════════════════════════════════════════
VERDICT: ACCEPT   (score 90) — code and data row; plan gate plus two second reviews (Codex)

Branch `fix/T-VINA-12`: spec `2e544a3`, plan approval `6d23acd` + `d08fdf6` (C1-C6), then `7ea84b8` (R1+R2 data) and
`e34003b` (R3 tool + R4 tests). Implementer PID 7824 (default model, effort high). One return (the plan gate).

MECHANICAL GATE
  ✓ deliverables exist           2 commits; note (plan, round 2, mutants, join totals) and RESULT
  ✓ changed files in scope       the 5 code and data files of `### Files to touch ###` only
  ✓ data equals the plan         `wmi.csv` and `vds_engine_map.csv` byte-equal to `plan/rekey.py`'s output (`cmp`);
                                 the `wmi.csv` diff is exactly R1 (10 brand cells, `LSJ,MG,CHINA,modern`); both LF
  ✓ tests fail without the fix   red run `20 failed, 23 passed` before the edits; M1-M7 each fail a named test
  ✓ effect visible               rerun by the reviewer: vinlab `344 passed, 8 skipped` (base 320); brand + tool files
                                 `43 passed`; dnalab 27, wired 41, ui 30; probes `14 passed`; ruff clean; join on
                                 held-out file 3: W `eng 1126 match 1004` (base 1125/1001), C `5071/4388` and N
                                 `44941/40056` equal to the base; other labs 0 failed

CRITERIA
  1 MET · 2 MET · 3 MET · 4 MET

PLAN GATE (corrections/T-VINA-12_plan_correction_20261104.md)
  Accepted A2: the `1C4` loss of 2 matches (Chrysler Voyagers under a Jeep WMI); totals bind. Cowork added control N.

SECOND REVIEW OF THE CODE (recheck/codex/T-VINA-12_review.md, APPROVE WITH CORRECTIONS), re-derived
  MEDIUM 17-char filter mutant survives     UPHELD: without the length check JTM ties TOYOTA 2 / SUBARU 2 and
                                            `most_common` returns the first seen → T-VINA-19
  LOW replacement-char brand counted        UPHELD (cp1250 `errors="replace"`, no `�` skip) → T-VINA-19
  LOW JTE case not discriminating           NOT UPHELD as a gap: M6 is killed by the JTM, build and pick cases
  LOW CLI parsing edge                      NOT UPHELD: the same pattern as the existing `--petrol-csv`
  LOW per-WMI floors                        accepted residual (A2)
  LOW Cowork rerun pending                  resolved: rerun above

FINDINGS
  concern  The two upheld items are test and filter hardening in `_registry_majority`; they change no shipped data.
           Registered as T-VINA-19 (difficulty 1), not a second return.
  nit      The implementer amended one local unpushed commit after a `bash_guard` refusal; recorded in the note.
