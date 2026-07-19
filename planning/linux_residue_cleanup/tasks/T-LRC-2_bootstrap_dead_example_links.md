# T-LRC-2 — coding-bootstrap: neutralise dead Windows worked-example links

**Pack:** Linux Residue Cleanup · **Area:** authoring skill · **Blocked by:** T-LRC-1 · **Status:** pending
**Load skills:** `comlab-verification-loop`, `comlab-code-review` (docs/skill edit, no Python).

### Goal ###
Remove the 28 dead `C:\…` worked-example links in `_skills/coding-bootstrap` (e.g.
`C:\Users\muto\claude\4DApp\4DLab\GASLab\GASLAB_START_HERE.md`, and references to off-mount
`v2/`, `HFX/`, `COMLab/`, `TestSuite/`). These are *illustrative examples*, not live links, and the
targets are not on this mount — so convert each to either (a) the valid on-mount repo-relative path
if an equivalent exists, or (b) a clearly-marked historical illustration
(`(historical Windows-era example — not on this mount)`). Done when no `C:\` string remains in the skill.

### Success criteria ###
- `grep -rnF 'C:\' _skills/coding-bootstrap` returns **zero** lines.
- No example that previously pointed to an on-mount file is left dangling: any path-shaped example that
  remains resolves on disk (checked in Verification: every backticked repo-relative path that looks like
  a file exists, or is inside a `(historical …)` marker).
- `coding-bootstrap` SKILL.md frontmatter still parses.

### Context ###
`WINDOWS_RESIDUE_FOLLOWUPS.md` §"Skills — env residue" lists "28 dead `C:\…` worked-example links
(old Windows layout / off-mount dirs)" as the remaining bootstrap residue after T-LRC-1's convention
swap. Most targets are off-mount (parent `4DLab/…`) or Windows-only, so they **cannot be relinked** —
they must be neutralised as historical illustrations. This is split from T-LRC-1 because it is per-link
work (~28 units) and would overflow a combined task (breakdown-checklist per-unit rule). T-LRC-1 must
land first (it touches the same two files for conventions); this task then only changes the example paths.

### Consumer (signal/noise) ###
N/A — no new field/enum/fault. Doc edit only.

### Deliverables ###
1. `_skills/coding-bootstrap/SKILL.md` — `C:\…` worked-example links neutralised (relinked-if-valid or marked historical).
2. `_skills/coding-bootstrap/templates/start_here.md` — same for the `C:\…` examples in the KG/commit guidance.

### Files to touch ###
- `_skills/coding-bootstrap/SKILL.md` (MODIFY)
- `_skills/coding-bootstrap/templates/start_here.md` (MODIFY)

### Out of scope ###
PowerShell/sandbox/backslash conventions (done in T-LRC-1). The stale `4DLabV2/` prefix elsewhere
(that is T-LRC-5). Do not invent new on-mount examples or restructure the skill. Surgical: every changed
line is a `C:\…` example becoming a valid path or a marked historical note. GRAPH GUARDRAIL: no graphify.

### Verification ###
```bash
cd /agent_workspace
# (a) no Windows absolute example paths remain
! grep -rnF 'C:\' _skills/coding-bootstrap
# (b) frontmatter still valid
.venv-wired/bin/python -c "import yaml; d=yaml.safe_load(open('_skills/coding-bootstrap/SKILL.md').read().split('---',2)[1]); assert d['name']=='coding-bootstrap'; print('frontmatter OK')"
# (c) spot-check: any remaining repo-relative example paths that look like files exist on disk
#     (manual: eyeball the diff — every non-historical backticked path resolves)
```
All steps must pass.

### Progress hook ###
`LINUX_RESIDUE_CLEANUP_PROGRESS.md` T-LRC-2: Status=done, Verification="28 dead C:\\ example links neutralised; no C:\\ remains in skill".
