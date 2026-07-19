# {PROJECT_NAME} — Progress Ledger

**Source prompt:** `{SOURCE_PROMPT_PATH}`
**Tasks dir:** `{TASKS_DIR}`
**Mode:** {STRICT_OR_LITE}
**Last updated:** {DATE}

This is the only file `START_HERE.md` reads to find the next task. Keep it
under ~120 lines. Bulk notes (verification blocks, code-review blocks, long
write-ups) go into `progress_notes/<task-id>.md`, not here.

---

## Task log

| ID | Task file | Status | Blocked by | Date | Commit | Verification | Notes |
|---|---|---|---|---|---|---|---|
| {TASK_ID_1} | `{TASK_FILE_1}` | pending | — | — | — | — | — |
| {TASK_ID_2} | `{TASK_FILE_2}` | pending | {TASK_ID_1} | — | — | — | — |
| {TASK_ID_3} | `{TASK_FILE_3}` | pending | {TASK_ID_1} | — | — | — | — |
| ... | ... | ... | ... | ... | ... | ... | ... |

**Status values:** `pending` · `in_progress` · `done` · `blocked` · `deferred`
**Blocked by:** comma-separated list of task IDs that must reach `done` first, or `—`.

**Runnability convention (keeps the stale-ledger guard and one-task-per-session aligned):**
`pending` means **runnable now** — spec authored, every `Blocked by` is `done`. A forward-registered
or otherwise unauthored placeholder row stays **`deferred`**, never `pending` and never a `pending (...)`
variant; promote it to `pending` only once its spec exists and blockers are `done`. The guard picks the
**first `pending` row top-to-bottom**; `deferred`/`blocked` rows are skipped.

---

## Unplanned follow-ups

Bugs and refactors discovered mid-task. Logged here, not fixed in the
session that found them.

| ID | Discovered in | One-liner | Status |
|---|---|---|---|
| — | — | — | — |

---

## Phase gates (if applicable)

{PHASE_GATES_BLOCK_OR_DELETE_THIS_SECTION}

---

## Architect-level out-of-band patches

Wiki / skill / convention edits the architect applied directly outside the
per-task diff. Capture date, file, and reason so the coder doesn't get
surprised by drift between sessions.

| Date | File | Patch | Reason |
|---|---|---|---|
| — | — | — | — |

---

## Accuracy / quality checkpoints (if applicable)

{ACCURACY_CHECKPOINTS_BLOCK_OR_DELETE_THIS_SECTION}
