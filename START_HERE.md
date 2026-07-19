# 4DLabV2 — START HERE (bootstrap)

Read this, then `ROADMAP.md`, then the active lab's `tasks/` ledger. Do not pick work before the
bootstrap is complete.

## What this workspace is

The v2 production rebuild of the 4D petrol diagnostic engine, in a **flat** layout: five isolated labs
under `labs/`, the apps that compose over them under `apps/`, the generative test harness at
`harness/`. Each lab carries its own code, tests, tasks, wiki, and graph. Full rationale:
`../v2-restructure/V2_WORKSPACE_STRUCTURE_PROPOSAL.md`.

## Boot sequence

1. Read `AGENTS.md` (the five rules).
2. Read `ROADMAP.md` (the stage sequence: GASLab → OBDLab → DTCLab → COMLab **last**; DNALab feeds the
   COMLab prior).
3. Open the active lab's ledger: `labs/<lab>/tasks/` — implement the **task ID the manager assigned**
   you. (Running unassigned? Take the first `pending` task whose blockers are all `done`.) One task
   per session.
4. Infra (Python 3.14 sandbox restore, `.venv-wired`, git ritual) is inherited from root
   `4DLab/CLAUDE.md` — this workspace adds no infra of its own.

## Migration complete

The structural migration (Track 1) is fully complete. The v1 source directories and obsolete files have been swept to `ARCHIVE/2026-06-06_v2restructure/`. The workspace is now ready for Track 2 (analytical and diagnostic rework per lab). See `../v2-restructure/EXECUTION_LOG.md` for details.
