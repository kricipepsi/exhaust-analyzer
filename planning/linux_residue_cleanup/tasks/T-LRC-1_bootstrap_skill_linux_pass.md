# T-LRC-1 — coding-bootstrap: Linux conventions pass

**Pack:** Linux Residue Cleanup · **Area:** authoring skill · **Blocked by:** — · **Status:** pending
**Load skills:** `comlab-verification-loop`, `comlab-code-review` (no language skill — this is a docs/skill edit, no Python).

### Goal ###
Convert the `_skills/coding-bootstrap` authoring skill from its Windows-era conventions to this
host's Linux conventions, so every START_HERE/task pack it generates is Linux-clean. Concretely:
replace the PowerShell git-ritual guidance and the PowerShell commit block in
`templates/start_here.md` (the fenced ` ```powershell ` block ~line 238) with the bash equivalent,
convert the backslash path placeholders (`{LOCAL_ROOT}\PROGRESS.md`, `\progress_notes`, etc.) to
forward-slash, and remove the obsolete `.sandbox-py` / "sandbox-py cache" / "sandbox-Python cache"
mentions (`templates/start_here.md:232`, `SKILL.md:478`). Done when the verification greps below
return no PowerShell/sandbox hits and the skill frontmatter still parses.

### Success criteria ###
- `grep -rInE 'powershell|sandbox-py|sandbox-python' _skills/coding-bootstrap` returns **zero** lines.
- `grep -rnF '}\' _skills/coding-bootstrap/templates` and `grep -rnF '\progress_notes' _skills/coding-bootstrap/templates` return **zero** lines (placeholders use `/`).
- The commit block in `templates/start_here.md` is a ` ```bash ` block (user-run in a terminal), not PowerShell backtick continuation.
- `coding-bootstrap` SKILL.md still loads: frontmatter `name`/`description` parse (check in Verification).

### Context ###
The tree migrated Windows→Linux (native host, one shared venv, no sandbox — see `AGENTS.md` and
`CLAUDE.local.md`). `WINDOWS_RESIDUE_FOLLOWUPS.md` §"Skills — env residue" flags this skill as the
one piece of **authoring infra** still carrying Windows conventions, and warns it must be fixed
**before** it is next used to author a pack or it re-propagates residue into generated docs. The
residue is confined to two files: `_skills/coding-bootstrap/SKILL.md` (§"Git in generated
bootstraps…", and line ~478) and `_skills/coding-bootstrap/templates/start_here.md` (the commit
block ~line 238, the backslash placeholders, the sandbox-py cache note ~line 232). The bash git
ritual to mirror is the one in this pack's own `LINUX_RESIDUE_CLEANUP_START_HERE.md` §session-end.

### Consumer (signal/noise) ###
N/A — no new field/enum/fault. Convention/doc edit only.

### Deliverables ###
1. `_skills/coding-bootstrap/templates/start_here.md` — PowerShell commit block → bash; backslash placeholders → forward-slash; drop "no sandbox-py cache" (keep "no `__pycache__/`").
2. `_skills/coding-bootstrap/SKILL.md` — §"Git in generated bootstraps…" PowerShell guidance → bash; line ~478 "sandbox-Python cache / user-run PowerShell" → Linux wording.

### Files to touch ###
- `_skills/coding-bootstrap/templates/start_here.md` (MODIFY)
- `_skills/coding-bootstrap/SKILL.md` (MODIFY)

### Out of scope ###
The 28 dead `C:\…` worked-example *links* — those are **T-LRC-2** (do not touch them here; this task
is conventions only). No restructuring, no rewording beyond the Windows→Linux swap, no template
content changes. Surgical: every changed line is a PowerShell→bash, backslash→slash, or sandbox-removal
edit. GRAPH GUARDRAIL: do not run `graphify` or touch any `graph/` artefact.

### Verification ###
```bash
cd /agent_workspace
# (a) no PowerShell / sandbox residue remains in the skill
! grep -rInE 'powershell|sandbox-py|sandbox-python' _skills/coding-bootstrap
# (b) no backslash path placeholders remain in templates
! grep -rnF '}\' _skills/coding-bootstrap/templates
! grep -rnF '\progress_notes' _skills/coding-bootstrap/templates
# (c) commit block is now bash
grep -nF '```bash' _skills/coding-bootstrap/templates/start_here.md
# (d) skill frontmatter still valid
.venv-wired/bin/python -c "import yaml; d=yaml.safe_load(open('_skills/coding-bootstrap/SKILL.md').read().split('---',2)[1]); assert d['name']=='coding-bootstrap' and d['description']; print('frontmatter OK')"
```
All steps must pass (the `! grep` lines pass when they find nothing).

### Progress hook ###
`LINUX_RESIDUE_CLEANUP_PROGRESS.md` T-LRC-1: Status=done, Verification="bootstrap skill PowerShell/sandbox/backslash residue gone; frontmatter OK".
