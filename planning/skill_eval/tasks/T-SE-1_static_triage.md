# T-SE-1 — Static skill triage (cheap wins, no trials)

**Status:** authored · runnable · **Blocked by:** — · **Pack:** `planning/skill_eval/`
**Mode:** STRICT
**Load skills (session start):** read `SKILL_EVAL_START_HERE.md`; sandbox Python 3.14;
mandatory pair. (No skill is loaded *as a subject*; this is inspection only.)

## Goal

Enumerate every `SKILL.md`/`skill.md` under `_skills/` and assign each a
disposition **by inspection** — `DEAD` (empty/no `name:`, redirect stub, byte-
duplicate) or `OUT-OF-SCOPE` (output-format/domain/meta skill that never shapes
produced code) — leaving the **in-scope coding shortlist** for the A/B track. A
duplicate or empty skill is provable waste; it must not consume an A/B trial.

## Deliverables

1. `triage.md` — a table: skill path · `name:` · disposition (`DEAD`/`OUT-OF-SCOPE`/
   `IN-SCOPE`) · evidence (e.g. `byte-identical to <path>` via `cmp`/`sha256`;
   `no name: field`; `redirect stub`; `domain=excel`).
2. The **in-scope shortlist** (the AB-track skills) echoed at the top of `triage.md`
   and reconciled against the ledger's per-skill table (flag any mismatch).
3. A `cut_candidates.md` list: exact paths safe to delete/dedupe (stubs, duplicates,
   empties) with the one-line reason — for the owner to action separately (do **not**
   delete here; this pack measures, it doesn't prune the tree).

## Success criteria

- Every `*kill.md` on disk appears in `triage.md` exactly once (count matches `find`).
- Each `DEAD`/duplicate carries machine evidence (hash/`cmp` output, not opinion).
- The in-scope shortlist equals CONTRACT §7 in-scope set, or the delta is explained.

## Out of scope

Deleting files; running any A/B trial; judging an in-scope skill's quality.

## Signal/noise consumer

The shortlist is consumed by T-SE-2 (corpus arms) and T-SE-3..6 (which skills to test).

## Verification

`find _skills -iname '*kill.md' | wc -l` equals the `triage.md` row count;
duplicate claims reproduced with `sha256sum`.

## VERIFICATION GATE / CODE REVIEW
(coder fills in `progress_notes/T-SE-1.md`, opening with `## Plan`.)
