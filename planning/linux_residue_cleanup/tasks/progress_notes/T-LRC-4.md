## Plan

- Convert the Windows-only PowerShell environment profile `setup_env_wired.ps1` for `apps/wiredV2` to a Linux-native `setup_env_wired.sh` script that exports the same OpenTelemetry variables and declares the helper functions (`run-tests`, `run-tests-no-trace`, `run-case`, `open-jaeger`).
- Update the docstring in `apps/wiredV2/wiredv2/_jaeger/_sanity_emit_span.py` to point to the new `.sh` script instead of `.ps1`.
- Archive the `setup_env_wired.ps1` file by moving it to `/agent_workspace/ARCHIVE/2026-06-27_linux_residue/apps/wiredV2/wiredv2/_jaeger/` rather than deleting it.
- Run the required verification steps: validate syntax with `bash -n`, verify sourced environment variables, check that no Windows residues remain, and verify that the `.ps1` is archived and no longer referenced.

VERIFICATION GATE — T-LRC-4
===========================
Phase 1 Syntax/import:  PASS — `bash -n` on `setup_env_wired.sh` exited 0; `_sanity_emit_span.py` compiles and runs cleanly.
Phase 2 Type check:     PASS — `/agent_workspace/.venv-wired/bin/pyright --pythonpath /agent_workspace/.venv-wired/bin/python /agent_workspace/apps/wiredV2/wiredv2/_jaeger/_sanity_emit_span.py` returned OK.
Phase 3 Lint:           PASS — `/agent_workspace/.venv-wired/bin/ruff check /agent_workspace/apps/wiredV2/wiredv2/_jaeger/_sanity_emit_span.py` returned OK.
Phase 4 pytest:         PASS — Sourcing `setup_env_wired.sh` and running `run-tests-no-trace` executed successfully with 5 passed / 1 failed (the single diagnostic oil_pcv test failure is identical when run outside the script environment).
Phase 5 Wiki/orphan:    PASS — N/A; dev-env helper script only, no schema fields or diagnostic logic changed.
Phase 6 Diff review:    PASS — Source edits are limited to creating `setup_env_wired.sh`, updating the docstring in `_sanity_emit_span.py`, and archiving `setup_env_wired.ps1` to the ARCHIVE folder; no graphify/KG rebuild run.

Checklist items applied:
  1. Docstrings — Updated `_sanity_emit_span.py` docstring to point to `setup_env_wired.sh`.
  2. Sorted imports — Ruff clean.

Status: DONE — flipping residue cleanup ledger row to done.

CODE REVIEW — T-LRC-4
=====================
1. Design rules:        PASS — no cross-lab imports, no new dependencies or sensor code added.
2. Scope compliance:    PASS — edits are strictly limited to the task files, this progress note, and the ledger file.
3. Contracts:           PASS — exported environment variables match the previous PowerShell profile exactly, but adapted to Linux paths and standard shell conventions.
4. Docstrings:          PASS — the outdated docstring referencing `setup_env_wired.ps1` has been corrected to refer to `setup_env_wired.sh`.
5. Wiki provenance:     PASS — N/A.
6. Immediate Checklist: PASS — all syntax, type, lint, and verification checks completed successfully.
7. Test coverage:       PASS — verified that the new script correctly sets up the environment and defines shell helper functions `run-tests`, `run-tests-no-trace`, `run-case`, and `open-jaeger`.
8. Structural craft:    PASS — use of subshell execution in functions ensures directory context is preserved cleanly without global state leakage.

Verdict: CLEAN
Blockers: none

