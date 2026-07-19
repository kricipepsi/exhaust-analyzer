# T-PYSCN-1 — Evaluate `pyscn` as a pre-wiring code-audit CLI (read-only)
**Authored by:** architect (Cowork) · **Status:** `done` (completed 2026-06-29) · **Blocked by:** —
**Mode:** READ-ONLY — discovery only, no source edits (same lane as T-GTA). · **Scope owner:** tooling / code-audit.
**Surfaced by:** owner request 2026-06-29 — `fallow` is TS/JS-only, so it cannot read this Python repo;
`pyscn` is the Python analog. This is a **gate before wiring** (`apps/wired/WIRING_PREP.md`).

## Objective
Decide whether `pyscn` (a single-binary Python code-quality analyzer: dead code, clones/duplication,
cyclomatic complexity, coupling/CBO, dependency cycles) should be wired into the coder/CI loop **before**
lab→COMLab wiring starts. Deliver **one** Markdown findings report + a wire-in recommendation.
**Do not wire anything in this task** — wiring is its own follow-up (T-PYSCN-2).

## Signal/noise
Adds no domain field or fault. The deliverable's **named consumer** is the architect's wiring go/no-go
decision (and any cleanup tasks it spawns); the report at
`planning/code_audit/reports/PYSCN_EVAL_2026-06-29.md` is the artifact that consumer reads. If the verdict
is "wire in," that change ships as its **own** proposal/task, never silently here.

## Pinned facts (verified 2026-06-29, architect smoke test)
- Zero-install run: `uvx pyscn@latest <cmd>` (binary built 2026-06-21, go1.25.5, linux/amd64).
  Persistent installs: `pipx install pyscn` or `uv tool install pyscn`.
- Commands: `pyscn analyze <path>` (full run; writes HTML report — use `--json` for machine output);
  `pyscn check <path>` (CI gate to stdout, exit 1 on fail).
- `check` flags: `--select complexity,deadcode,clones,deps,mockdata,di`, `--max-complexity N` (default 10),
  `--max-cycles N`, `--skip-clones`, `--allow-dead-code`, `--allow-circular-deps`, `-q/--quiet`.
- Smoke test on `labs/gaslab` (40 `.py`): parsed clean (python3.14 OK); **150 clones** (overwhelmingly
  `tests/unit/test_rule_engine.py` parametrized blocks), **4 quality issues**, exit 1.
- **Known coverage gaps for THIS repo — report only, do not fix here:**
  pyscn does **not** detect unused *package* dependencies (that's `deptry`), and does **not** enforce
  the rule-5 *cross-lab import ban / lab isolation* (that's `tach` or `import-linter`). pyscn `deps` =
  within-tree dependency *cycles*, not cross-package import *policy*.

## Scope
**IN:**
- Run, read-only, on each lab — `gaslab obdlab dtclab comlab dnalab vinlab symptomlab semantic` — and on
  `apps/wired`:
  - `pyscn check --select deadcode,complexity,deps <path>` (capture stdout + exit code), and
  - `pyscn analyze --json` with JSON written to `/tmp/pyscn_<target>.json` (NOT into the repo).
- Capture per target: parse success/failures, dead-code count, functions over the complexity threshold,
  dependency cycles, clone count, and pyscn's health score if emitted.
- Write ONE report (paths below). **Separate production-code findings from test-file duplication** — the
  gaslab signal was almost entirely test clones; do not let that inflate the verdict.
- Recommendation: wire in or not; if yes, *where* (pre-commit hook / CI `check` gate / agent MCP server)
  and *proposed thresholds* (`--max-complexity`, `--max-cycles`, whether to `--skip-clones` on tests).

**OUT:** any source edit; any hook/CI/config commit (→ T-PYSCN-2); running `deptry`/`tach`/`import-linter`
(separate follow-ups); rebuilding any graph (`graphify` is forbidden — frozen graphs are query-only);
editing `Vault/`; committing pyscn's HTML/JSON artifacts; storing any secret.

## Steps
1. Read `AGENTS.md` (five rules) and `apps/wired/WIRING_PREP.md`. Per rule 1, query the lab graph for
   orientation rather than grepping blind. Confirm `uvx pyscn@latest version` runs.
2. For each target: run `check` (record stdout + exit), then `analyze --json /tmp/pyscn_<target>.json`.
3. Aggregate the JSON into one metrics table; tag each production-code finding with `file:line`.
4. Write `planning/code_audit/reports/PYSCN_EVAL_2026-06-29.md` (the report — see success criteria).
5. Fill the gate blocks in `planning/code_audit/tasks/progress_notes/T-PYSCN-1.md`; STOP.

## Success criteria
- pyscn completes on all 8 labs + `apps/wired`; every file it fails to parse is listed explicitly
  (expect zero, given the gaslab smoke test).
- Report exists, `.md`, containing: (a) per-target metrics table; (b) top production-code items
  — dead code + over-threshold complexity + dependency cycles — each with `file:line`; (c) clone
  test-vs-production split; (d) an explicit "pyscn does NOT cover {unused deps, lab-isolation}" line
  naming the follow-up tools (`deptry`; `tach`/`import-linter`).
- One-line verdict: wire in (where + thresholds) OR not, with the reason.
- `git status` shows only new files under `planning/code_audit/`; no source/`Vault/`/graph changes;
  no committed HTML/JSON.

## VERIFICATION GATE — T-PYSCN-1
Completed in `planning/code_audit/tasks/progress_notes/T-PYSCN-1.md`.

- `uvx pyscn@latest version`: exit 0; `pyscn 1.24.3`, commit `4419636`, built `2026-06-21`.
- `check --select deadcode,complexity,deps` exits: `gaslab=1`, `obdlab=1`, `dtclab=1`, `comlab=1`, `dnalab=0`, `vinlab=1`, `symptomlab=0`, `semantic=1` (no Python files), `apps/wired=1` (no Python files).
- `analyze --json` exits: Python-bearing targets `gaslab`, `obdlab`, `dtclab`, `comlab`, `dnalab`, `vinlab`, `symptomlab` all exit 0 with JSON copied to `/tmp/pyscn_<target>.json`; `semantic` and `apps/wired` exit 1 because no Python files exist.
- Parse failures: none for Python-bearing targets.
- Report: `planning/code_audit/reports/PYSCN_EVAL_2026-06-29.md`.

## CODE REVIEW — T-PYSCN-1
Completed in `planning/code_audit/tasks/progress_notes/T-PYSCN-1.md`.

- Read-only confirmed for source/`Vault`/graphs/hooks/CI/config; only planning audit artifacts were edited.
- `graphify` was not run.
- Report names the coverage gaps: unused package dependencies require `deptry`; lab-isolation / cross-lab import policy requires `tach` or `import-linter`.
- Report includes production-vs-test clone split and a metrics-backed verdict: wire in as non-blocking agent/code-audit tooling first; defer blocking CI/pre-commit until complexity debt is fixed or baselined.

## Commit (owner, explicit paths)
```bash
cd /agent_workspace
git add \
  planning/code_audit/tasks/T-PYSCN-1_evaluate_pyscn_audit_cli.md \
  planning/code_audit/tasks/progress_notes/T-PYSCN-1.md \
  planning/code_audit/reports/PYSCN_EVAL_2026-06-29.md
git commit -m "T-PYSCN-1: evaluate pyscn as pre-wiring code-audit CLI (read-only)"
```
