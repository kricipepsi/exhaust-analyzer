# T-AUD-7h progress note

## Readiness
- (a) Starting state matches: branch `fix/T-AUD-7h`, `HEAD~1` = `0fdf971`, `git status --porcelain` empty. HEAD is `907536b`.
- (b) Test fails for the intended reason: base `rules_base.out` last line is `sides not found: 21` (target 22).
- (c) Expected values derived from `rehearsal.diff`: AGENTS.md +3/-2, 4DLab_CLAUDE.md +3/-3, total 6 insertions, 5 deletions. `sides not found: 22`; 1 `wiredV2`/`Vault/tasks` line left (`:178`); `ADR-0002` once.
- (d) No contradiction or missing decision. All preconditions exist.
- (e) Teach-back: Make four exact text edits (R1 in `AGENTS.md`, R2-R4 in `4DLab_CLAUDE.md`) as `make_rh.py` defines them, and commit them once. The decisive check is `rules.py` ending `sides not found: 22` and `paths.py` leaving only `4DLab_CLAUDE.md:178`.

## VERIFICATION GATE
CLEAN. All in-scope gates passed (docs row, no code, no `.py` touched).
- step 1: `sides not found: 22`, then `1` (X10 `NOT FOUND` line).
- step 2: `4DLab_CLAUDE.md:178`, then `1` (`ADR-0002` once).
- step 3: spec commit `907536b` then `2ba729f docs(T-AUD-7h)`; `2 files changed, 6 insertions(+), 5 deletions(-)`; `git status --porcelain` lists only this note (the RESULT follows).
- Diff changes match `rehearsal.diff` line for line (CR-stripped compare); 0 CR bytes in the diff (LF kept).

## CODE REVIEW
CLEAN. Every changed line traces to R1-R4. `Vault/`, ledgers, `DECISIONS.md`, ADRs and `4DLab_CLAUDE.md:178` are untouched.

## Assumptions worked past
- `bash_guard` refused the first commit because the message held the attribution trailer. I committed without the trailer. The commit is otherwise as specified.

## Time
| phase | start | end | minutes | context at end |
|---|---|---|---|---|
| first action to finish | 2026-11-04T23:51:21Z | 2026-11-04T23:52:34Z | 1 | ABSENT |
