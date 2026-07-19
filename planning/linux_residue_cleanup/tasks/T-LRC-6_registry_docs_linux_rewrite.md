# T-LRC-6 — registry docs: Linux rewrite (REGISTRY_START_HERE + registry-python)

**Pack:** Linux Residue Cleanup · **Area:** labs/comlab/registry · **Blocked by:** — (OWNER + roadmap, see below) · **Status:** blocked
**Load skills:** `comlab-python`, `comlab-verification-loop`, `comlab-code-review`.

> **BLOCKED — two gates before running.** (1) **Owner:** the registry workstream root
> (`registry_tasks/`, the canonical `_registry_skills/`, `REGISTRY_PROGRESS.md`) lives **off-mount**
> (parent `4DLab/registry`); the split-registry reconciliation must be brought on-mount first, or the
> rewrite will drift from the authority. (2) **Roadmap:** COMLab-area is built **last**
> (GASLab → OBDLab → DTCLab → COMLab). Do not start until both clear; record the go-ahead in the ledger's
> "Owner decisions" section, then flip to `pending`.

### Goal ###
Rewrite the two on-mount registry bootstrap docs from their Windows-era form to this host's Linux
conventions: `labs/comlab/registry/docs/REGISTRY_START_HERE.md` and
`labs/comlab/registry/docs/_registry_skills/registry-python/SKILL.md`. Replace PowerShell git ritual,
`C:\…` paths, and obsolete sandbox-python references with the shared-venv/bash conventions, and remove the
STALE banner once the content is correct and reconciled against the on-mount authority. Done when neither
doc carries Windows residue and the registry inner loop runs on `/agent_workspace/.venv-wired`.

### Success criteria ###
- `grep -rniE 'powershell|sandbox-py|sandbox-python|C:\\' labs/comlab/registry/docs/REGISTRY_START_HERE.md labs/comlab/registry/docs/_registry_skills/registry-python/SKILL.md` returns **zero**.
- The STALE banner previously added to `REGISTRY_START_HERE.md` is removed (content now current).
- `registry-python` SKILL.md frontmatter parses (`name`/`description` present).
- Any inner-loop command the docs prescribe uses `/agent_workspace/.venv-wired/bin/...`, not `.sandbox-py` or system Python.

### Context ###
`WINDOWS_RESIDUE_FOLLOWUPS.md` §"Needs a REWRITE when the workstream is brought on-mount" specifies this:
the on-mount docs exist but are Windows-era bootstrap (PowerShell, `C:\…`, obsolete sandbox-python,
host-only git); a STALE banner was added to `REGISTRY_START_HERE.md` as an interim measure. The canonical
registry workstream is off-mount, so this rewrite is gated on it being brought on-mount and on the COMLab
build window. Mirror the Linux conventions already applied to the COMLab skills (shared venv, bash) and to
this pack's own `LINUX_RESIDUE_CLEANUP_START_HERE.md`.

### Consumer (signal/noise) ###
N/A — no new field/enum/fault. Docs/skill rewrite only.

### Deliverables ###
1. `labs/comlab/registry/docs/REGISTRY_START_HERE.md` — Windows → Linux bootstrap; STALE banner removed.
2. `labs/comlab/registry/docs/_registry_skills/registry-python/SKILL.md` — sandbox-python/PowerShell/`C:\` → shared-venv/bash.

### Files to touch ###
- `labs/comlab/registry/docs/REGISTRY_START_HERE.md` (MODIFY)
- `labs/comlab/registry/docs/_registry_skills/registry-python/SKILL.md` (MODIFY)

### Out of scope ###
The off-mount registry workstream itself (`registry_tasks/`, canonical `_registry_skills/`,
`REGISTRY_PROGRESS.md`) — not on this mount; do not recreate it here. The split-registry *reconciliation*
(a separate COMLab Stage-4 deliverable), the registry runtime code, and the other two
`_registry_skills/*` (registry-code-review, registry-verification-loop) unless they show the same residue.
Surgical: convention swaps only. GRAPH GUARDRAIL: no graphify.

### Verification ###
```bash
cd /agent_workspace
D=labs/comlab/registry/docs
! grep -rniE 'powershell|sandbox-py|sandbox-python|C:\\' "$D/REGISTRY_START_HERE.md" "$D/_registry_skills/registry-python/SKILL.md"
! grep -niF 'STALE' "$D/REGISTRY_START_HERE.md"
.venv-wired/bin/python -c "import yaml; d=yaml.safe_load(open('$D/_registry_skills/registry-python/SKILL.md').read().split('---',2)[1]); assert d['name'] and d['description']; print('frontmatter OK')"
```
All steps must pass.

### Progress hook ###
`LINUX_RESIDUE_CLEANUP_PROGRESS.md` T-LRC-6: Status=done, Verification="registry docs de-Windowsed; STALE banner removed; frontmatter OK".
