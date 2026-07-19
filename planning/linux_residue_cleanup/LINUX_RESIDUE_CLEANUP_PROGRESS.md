# Linux Residue Cleanup — Progress Ledger

**Source:** `/agent_workspace/WINDOWS_RESIDUE_FOLLOWUPS.md` (the outstanding buckets)
**Tasks dir:** `/agent_workspace/planning/linux_residue_cleanup/tasks/`
**Mode:** strict (dual-gate) · **Last updated:** 2026-06-27

This is the only file `LINUX_RESIDUE_CLEANUP_START_HERE.md` reads to find the next task.
Keep it under ~120 lines. Bulk notes (gate blocks, write-ups) go in `progress_notes/<task-id>.md`.

---

## Task log

| ID | Task file | Status | Blocked by | Date | Verification | Notes |
|---|---|---|---|---|---|---|
| T-LRC-1 | `tasks/T-LRC-1_bootstrap_skill_linux_pass.md` | done | — | 2026-06-27 | architect out-of-band; PowerShell/sandbox/backslash residue gone, frontmatter OK | authoring skill = architect tooling, done directly (not a coder) |
| T-LRC-2 | `tasks/T-LRC-2_bootstrap_dead_example_links.md` | done | — | 2026-06-27 | architect out-of-band; 0 `C:\` in skill (on-mount ones relinked, rest made relative) | done with T-LRC-1 in the same pass |
| T-LRC-3 | `tasks/T-LRC-3_vinlab_dataset_paths_envvar.md` | done | — | 2026-06-27 | vinlab tools env-var driven; no C:\ remains; inner loop green | Owner decision \"env-var only (no default paths)\" implemented |
| T-LRC-4 | `tasks/T-LRC-4_wiredv2_env_script_bash.md` | done | — | 2026-06-27 | setup_env_wired.sh sources clean; .ps1 archived; docstring repointed | wiredV2 setup_env_wired.ps1 → .sh conversion done |
| T-LRC-5 | `tasks/T-LRC-5_active_docs_4dlabv2_prefix.md` | done | — | 2026-06-27 | 4DLabV2/ prefix removed from Vault, planning, and labs active docs; paths resolve | Removed stale path prefix from active docs |
| T-LRC-6 | `tasks/T-LRC-6_registry_docs_linux_rewrite.md` | blocked | — | — | — | needs OWNER (registry on-mount) + roadmap (COMLab-area last) |

**Status values:** `pending` (runnable now — spec authored, blockers `done`) · `in_progress` · `done` · `blocked` (needs an owner/upstream decision) · `deferred` (forward-registered, spec not yet authored).
**Selection:** first `pending` row top-to-bottom whose every `Blocked by` is `done`; skip `deferred`/`blocked`.

---

## Unplanned follow-ups
Residue discovered mid-task. Logged here, not fixed in the session that found it.

| ID | Discovered in | One-liner | Status |
|---|---|---|---|
| — | — | — | — |

---

## Owner decisions needed (unblock the `blocked` rows)
- **T-LRC-3** — the Linux path for the external `vehicle-data` / `DBS` datasets (currently hardcoded
  `C:\Users\muto\claude\4DApp\vehicle-data` and `C:\DBS`). Provide the Linux root (or confirm
  env-var-only with no default) so the task can set a sane default. Until then T-LRC-3 stays `blocked`.
- **T-LRC-6** — bring the registry workstream on-mount (it lives off-mount at parent `4DLab/registry`)
  and confirm the COMLab-area build window (roadmap = COMLab last). Both must clear before the registry
  docs rewrite runs; until then T-LRC-6 stays `blocked`.

---

## Architect out-of-band patches
Edits the architect applied directly outside a per-task diff.

| Date | File | Patch | Reason |
|---|---|---|---|
| 2026-06-27 | `AGENTS.md`, `CLAUDE.local.md`, `HANDOFF_2026-06-27` (Desktop) | removed stale `.sandbox-py` refs | pre-pack canon scrub; live docs must not imply a second venv |
| 2026-06-27 | `_skills/coding-bootstrap/**` (SKILL.md, templates, reference) | PowerShell→bash, backslash→`/`, dropped `.sandbox-py`/sandbox-cache, neutralised all `C:\…` example paths (T-LRC-1 + T-LRC-2) | authoring skill is architect tooling and must be Linux-clean before it generates any new pack; done directly rather than via a coder |
