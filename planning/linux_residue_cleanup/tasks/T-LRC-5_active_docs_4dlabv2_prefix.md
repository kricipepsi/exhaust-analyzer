# T-LRC-5 — strip stale `4DLabV2/` path prefix from one area's ACTIVE docs

**Pack:** Linux Residue Cleanup · **Area:** `{AREA}` (one per instance) · **Blocked by:** — · **Status:** deferred (template — promote per area as it is picked up)
**Load skills:** `comlab-verification-loop`, `comlab-code-review` (docs edit, no Python).

> **TEMPLATE TASK — instantiate one `{AREA}` at a time.** Copy this file to
> `T-LRC-5-<area>_<slug>.md`, replace `{AREA}` with the concrete path (a lab dir, `Vault`, or a
> `planning/<workstream>` dir), add a row to the ledger, and run it when that area is the active work.
> Do **not** run a single blunt repo-wide `4DLabV2/` strip — it would rewrite historical records (see Out of scope).

### Goal ###
In the ACTIVE entry-point/task docs of `{AREA}` only, remove the stale `4DLabV2/` path prefix so in-repo
paths resolve. The child `4DLabV2/` is now the mount root `/agent_workspace`, so `labs/x` should
read `labs/x`. Done when `grep -rnF '4DLabV2/' {AREA}` over the active docs (excluding `progress_notes/`,
`graph/`, and other historical/frozen files) returns zero, and the de-prefixed paths point at real files.

### Success criteria ###
- `grep -rnF '4DLabV2/' {AREA} --include='*.md'` filtered to active docs (exclude `progress_notes/`, `graph/`, `*HANDOFF_2026-06-0*`, `AUDIT_*`) returns **zero**.
- Spot-check: every path that was de-prefixed resolves on disk (checked in Verification by re-rooting at `/agent_workspace`).
- No edits under `{AREA}/progress_notes/` or `{AREA}/graph/`.

### Context ###
`WINDOWS_RESIDUE_FOLLOWUPS.md` §"Stale `4DLabV2/` path prefix" documents this systemic residue
(distribution at authoring time, active docs only: Vault 46, obdlab 37, gaslab 11, dnalab 10, semantic 6,
root 11, plus `planning/skill_eval` 16, `planning/test_rollout` 14, `planning/oil_consumption` 5). The agreed
approach is per-area, as that area is picked up — never a repo-wide `sed`. `Vault/tasks/COM_VAULT_TASKS_START_HERE.md`
was already done as the worked example. The transform is literal: `4DLabV2/` → `` (empty) inside in-repo
path references; leave prose mentions of the layout migration intact where they are *describing* the rename.

### Consumer (signal/noise) ###
N/A — no new field/enum/fault. Path-prefix doc fix only.

### Deliverables ###
1. The active entry/task docs under `{AREA}` (START_HERE, current task specs, READMEs) — `4DLabV2/` path prefix removed.

### Files to touch ###
- `{AREA}/**` active `*.md` entry/task docs (MODIFY) — enumerate the concrete files in the instantiated copy.

### Out of scope ###
`{AREA}/progress_notes/*` and any `HANDOFF_2026-06-0*`, `AUDIT_*`, `handoff*.md` historical records — the
`4DLabV2/` prefix there is an **accurate record of the old layout**; rewriting it falsifies history
("archive, don't delete"). Frozen `graph/**` artefacts (provenance). Other areas (one area per instance).
Prose that *describes* the migration (e.g. "the former `4DLabV2/` child"). Surgical: every changed line is a
path de-prefix. GRAPH GUARDRAIL: no graphify.

### Verification ###
```bash
cd /agent_workspace
AREA={AREA}   # e.g. Vault  or  labs/gaslab  or  planning/test_rollout
# (a) no 4DLabV2/ left in the area's ACTIVE docs
! grep -rnF '4DLabV2/' "$AREA" --include='*.md' \
    | grep -vE '/progress_notes/|/graph/|HANDOFF_2026-06-0|/AUDIT_|handoff[0-9]*\.md'
# (b) de-prefixed in-repo paths resolve (sample the ones you touched; each `labs/...`/`apps/...` exists)
#     manual: eyeball the diff — every de-prefixed path exists under /agent_workspace
```
Step (a) must pass; (b) is a manual diff check.

### Progress hook ###
`LINUX_RESIDUE_CLEANUP_PROGRESS.md` T-LRC-5-<area>: Status=done, Verification="4DLabV2/ prefix removed from {AREA} active docs; paths resolve".
