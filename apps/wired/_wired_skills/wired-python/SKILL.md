---
name: wired-python
description: >
  Mandatory language skill for the `wired` composition app. Load at the start of
  every wired coder session. Owns the per-file Inner Loop (syntax -> lint ->
  security -> type check after every edit), the house style, and the
  composition-only forbidden patterns. Re-scoped for `apps/wired/` on the Linux
  host shared `.venv-wired` (Python 3.14).
status: BUILT
---
# wired-python — language skill (mandatory every session)

`apps/wired/` is the **composition app**: the only package allowed to import
GASLab, OBDLab, DTCLab, DNALab, and VINLab together and hand the result to
COMLab. It holds **no diagnostic logic** — only mapping lab outputs into COMLab
payloads and a thin single-case runner.

## Environment
- **One shared venv:** `/agent_workspace/.venv-wired` (host `python3.14`, already
  built). Never create a second venv; never run bare `python`. Use the venv's
  interpreter: `/agent_workspace/.venv-wired/bin/python`.
- Install the package editable once it has a `pyproject.toml`:
  `/agent_workspace/.venv-wired/bin/pip install -e apps/wired`.
- **Run pytest/pyright with a neutral cwd** (e.g. from `/agent_workspace`, not
  from inside `labs/`) so the editable lab packages resolve and a sibling
  `obdlab/` source dir does not shadow the installed `obdlab` package.

## Per-file Inner Loop (run after EVERY meaningful edit, not just at task end)
```bash
cd /agent_workspace
PY=.venv-wired/bin/python
$PY -m py_compile apps/wired/wired/<file>.py     # 1. syntax
$PY -m ruff check apps/wired/wired/<file>.py      # 2. lint (style + simple bugs)
$PY -m pyright apps/wired/wired/<file>.py         # 3. type check (0 errors)
$PY -m pytest -x -q apps/wired/tests/<test>.py    # 4. tests (fail-fast)
```
"ruff" = the linter (flags style/lint issues); "pyright" = the static type
checker. All four must be clean before you move on. A type error or lint error
is a stop, not a warning to defer.

## House style
- Pydantic v2 models for every payload boundary; never hand-roll dict shaping
  where a typed mirror exists.
- Every field mapped lab->COMLab carries an inline `# consumer:` comment naming
  the COMLab reader (see `wired-composition-contract`). No consumer -> the field
  does not ship (signal/noise).
- Numeric literals at a boundary carry a citation comment (`# wiki: section ...`
  or `# dossier: ...`) — same rule as the labs.
- Functions stay short and single-purpose; one mapper per lab. No speculative
  abstraction, no "future use" parameters.

## Forbidden patterns (composition-only)
- **No cross-lab logic.** `wired/` maps and forwards; it never decides a fault.
  The verdict comes only from `LabPipelineAggregator.process()`.
- **No lab edits.** A wired task never modifies a file under `labs/`. If a lab
  surface is wrong, forward-register a row on that lab's ledger and hand back.
- **No legacy imports.** Never import from `ARCHIVE/`, `v2/`, `v6/`. They are
  read-only reference; the lab wikis + current code are truth.
- **No deferred fusion path.** It does not exist in the current tree — do not
  import or reference it.
- **No `graphify` / graph rebuilds** from a wired task (standing guardrail).
- **No `git add -A`** — commit by explicit path (the user runs the commit).
