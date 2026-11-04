TASK REVIEW — T-AUD-7b_git_rule_stale_docs(1) — 2026-11-04 (Windows Cowork)
════════════════════════════════════════════════════════════
VERDICT: ACCEPT   (score 98) — docs row; no second review (CLAUDE.md step 6)

Branch `fix/T-AUD-7b`: spec `e93ee08`, then `da34ae7 docs(T-AUD-7b): point five stale git-rule docs at the 4DLab git
rule`. Implementer PID 11704 (sonnet, medium).

MECHANICAL GATE
  ✓ deliverables exist           5 docs edited in one commit; note, RESULT (untracked, as the spec says)
  ✓ changed files in scope       the 5 files of `### Files to touch ###` only (`git diff --stat HEAD~1..HEAD`:
                                 5 files changed, 9 insertions(+), 10 deletions(-))
  ✓ text equals R1-R5            each committed file is byte-equal to the base with Cowork's rehearsal script
                                 applied (`recheck/scratch/rehearse_7b.py` on a `git archive e93ee08` copy, `cmp`)
  ✓ effect visible               rerun by the reviewer: step 1 `0`; step 2 only `planning/graph_rollout/LMM-gphfy.md`;
                                 eol `5 i/lf w/lf`

CRITERIA
  1 MET · 2 MET · 3 MET · 4 MET

FINDINGS
  nit  The commit has no co-author trailer. The implementer reports that `bash_guard` refuses command text that
       contains the trailer's file word; recorded in the RESULT. No effect on the deliverable.
  nit  `## Time` records 1 min from clock reads, less than the session's wall-clock. Accepted as the edit phase only.

Out of scope and still open: the other T-AUD-7 items (F-D3-2…9, 13; R0-3, R0-5) in `audit/FIX_PLAN.md`.
