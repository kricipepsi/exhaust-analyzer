# T-WTEST-2 — `pyscn` static audit of `apps/wired` (read-only)

**Authored by:** architect (Cowork), 2026-06-30 · **Status:** `deferred` (→ `pending` when T-WTEST-1 is `done`) · **Blocked by:** T-WTEST-1
**Mode:** READ-ONLY — discovery only, no source edits (same lane as T-PYSCN-1). · **Scope owner:** wired-test / code-audit.

## Objective
Run `pyscn` (the Python code-quality analyzer — the analog to the TS/JS-only
`fallow`) over **`apps/wired` only**, now that it contains live Python
(`wired/*.py` + `tests/`). At T-PYSCN-1 time `apps/wired` had **no `.py`** and
pyscn exited 1 with nothing to analyze; the seven labs were audited there and are
**not** re-audited here. Deliver one Markdown findings report + a one-line verdict
for the wiring code against the thresholds T-PYSCN-1 already pinned.

## Signal/noise
Adds no domain field or fault. The **named consumer** is the architect's cleanup
go/no-go for the wiring code (and any cleanup task it spawns); the report at
`apps/wired/test_tasks/reports/WTEST2_PYSCN_WIRED_<date>.md` is the artifact that
consumer reads. Any "wire pyscn into CI/pre-commit" decision is **out** — that is
the deferred T-PYSCN-2, not this task.

## Pinned facts (from T-PYSCN-1, verified 2026-06-29 — re-confirm version in-session)
- `pyscn 1.24.3` (commit `4419636`, go1.25.5, linux/amd64); zero-install run:
  `uvx pyscn@latest <cmd>`. Source: `planning/code_audit/reports/PYSCN_EVAL_2026-06-29.md`.
- CI gate form: `pyscn check --select deadcode,complexity,deps --max-cycles 0 <path>`
  (stdout, exit 1 on fail). Full run: `pyscn analyze <path> --json` (machine output).
- Pinned thresholds: `--max-complexity` default **10**; `--max-cycles 0` (no
  within-tree dependency cycles tolerated). Clones are **advisory**, split
  test-vs-production, never a default gate.
- **Coverage gaps (report only, do not fix here):** pyscn does **not** detect
  unused *package* deps (that is `deptry` — already swept clean 2026-06-29, see
  `planning/code_audit/STAGE4_COMPLEXITY_INPUTS.md`), and `pyscn deps` means
  *within-tree cycles*, **not** cross-package import policy. **Lab-isolation
  (rule 5) does not apply to `apps/wired`** — wired is the *sanctioned* multi-lab
  importer, so do not flag its lab imports as violations.

## Scope
**IN:**
- `pyscn check --select deadcode,complexity,deps --max-cycles 0 apps/wired`
  (capture stdout + exit code).
- `pyscn analyze apps/wired --json` with JSON written to `/tmp/pyscn_wired.json`
  (**NOT** into the repo).
- Capture: parse success/failures per file, dead-code count, functions over the
  complexity threshold (each with `file:line`), within-tree dependency cycles,
  clone count split test-vs-production, and the health score if emitted.
- Write ONE report at `apps/wired/test_tasks/reports/WTEST2_PYSCN_WIRED_<date>.md`:
  (a) metrics summary for `apps/wired`; (b) production-code items (`wired/*.py`)
  separated from test-file items (`tests/*.py`) — do not let test clones inflate
  the verdict; (c) the explicit "pyscn does NOT cover {unused deps, lab-isolation};
  lab-isolation N/A for wired" line; (d) one-line verdict: clean / has-debt (with
  the worst items named) against the pinned thresholds.

**OUT:** any source edit; auditing the labs again (done in T-PYSCN-1); any
hook/CI/config commit (→ T-PYSCN-2); running `deptry`/`tach`/`import-linter`;
`graphify`; editing `Vault/`; committing pyscn HTML/JSON; storing any secret.

## Steps
1. Confirm `uvx pyscn@latest version` runs; record the version (flag any drift from
   1.24.3).
2. Run `check` (record stdout + exit), then `analyze --json /tmp/pyscn_wired.json`.
3. Tag each production finding with `file:line`; split clones test-vs-production.
4. Write the report (paths above).
5. Fill the gate blocks in `test_tasks/progress_notes/T-WTEST-2.md`; STOP.

## Success criteria
- pyscn parses every `apps/wired/**/*.py`; any file it fails to parse is listed
  explicitly (expect zero — Python 3.14 parsed clean on gaslab in T-PYSCN-1).
- Report exists, `.md`, with: metrics summary; production-vs-test split; the
  coverage-gap line (incl. lab-isolation N/A for wired); one-line verdict against
  the pinned thresholds (`--max-complexity 10`, `--max-cycles 0`).
- `git status` shows only new files under `apps/wired/test_tasks/`; no source/
  `Vault/`/graph changes; no committed HTML/JSON.

## VERIFICATION GATE — T-WTEST-2
Complete in `test_tasks/progress_notes/T-WTEST-2.md`: `pyscn version`; `check`
stdout + exit; `analyze --json` exit + JSON path; parse failures (expect none);
report path.

## CODE REVIEW — T-WTEST-2
Complete in `test_tasks/progress_notes/T-WTEST-2.md`: read-only confirmed for
source/`Vault`/graphs/hooks/CI; `graphify` not run; report names the coverage gaps
and the lab-isolation N/A; verdict is metrics-backed.

## Commit (owner, explicit paths)
```bash
cd /agent_workspace
git add \
  apps/wired/test_tasks/reports/WTEST2_PYSCN_WIRED_<date>.md \
  apps/wired/test_tasks/progress_notes/T-WTEST-2.md \
  apps/wired/test_tasks/TEST_PROGRESS.md
git commit -m "T-WTEST-2: pyscn static audit of apps/wired (read-only)"
```
