TASK REVIEW — T-AUD-1b_deploy_manifests(3) — 2026-11-03 (Windows Cowork, round 2 after correction 01)
════════════════════════════════════════════════════════════
VERDICT: ACCEPT   (score 92) — second-model review APPROVE WITH CORRECTIONS (one LOW, not upheld)

Branch `fix/T-AUD-1b`: Cowork's spec commits `bea265a`, `5c3c0bb`, `573f76e`, then the implementer's one commit
`186aa0a fix(T-AUD-1b): unique fourdapp-* dist names, dnalab lab deps, pinned constraints.txt` (11 files).
Implementer PID 14576. Hand-back B3 (both findings upheld, owner COWORK, cost 1 round).
Score: -8 for the round spent on B3 (two Cowork defects: a verification step that could not fail in its venv, and the
AGENTS.md commit-form gap); the implementer's work needed no change.

MECHANICAL GATE
  ✓ deliverables exist           11 files in one commit; note, RESULT, blocker record
  ✓ NEW tests red on the base    implementer's red gate: 4 of 5 failed on the base; the 5th
                                 (`test_every_local_dependency_has_an_editable_line`) passes vacuously there and is
                                 exercised by M1
  ✓ mutants killed               3/3, run by the reviewer, restored with `git checkout --`:
                                 M1 dnalab name back → 2 failed; M2 `-c` line removed → 1 failed; M3 dnalab deps
                                 emptied → 1 failed
  ✓ changed files in scope       the 11 Files-to-touch paths only; no `.py` under labs/ or apps/ except the new test
  ✓ effect visible               see VERIFICATION 2-3

VERIFICATION (reviewer re-run, C:/4DApp/repo)
  1 `venv-ok` · 2 `install exit 0`, `unpinned-or-off []` (47 frozen = 47 pins; `six` is Linux-only), `imports-ok` ·
  3 in venv2 (0 fourdapp dists installed): count 2, exit 1 (`No matching distribution found for fourdapp-dnalab`);
  standalone dnalab → `fourdapp-symptomlab`, exit 1 · 4 `41 passed` · 5 `30 passed` · 6 `2 passed` · 7 ruff clean,
  one fix commit on top, status = note, RESULT, blocker record

LINUX WHEELS (reviewer, closes the second review's open point)
  All 48 pins resolve to binary wheels for Render's platform: `pip install --dry-run --only-binary=:all:
  --python-version 3.14 --implementation cp --abi cp314 --abi abi3 --abi none --platform manylinux_{2_39…1}_x86_64
  -r <constraints pins>` → exit 0. (A single `--platform manylinux_2_28_x86_64` reported no pydantic_core wheel:
  pip does not expand the tag; not a defect.)

CRITERIA
  1 MET · 2 MET · 3 MET · 4 MET · 5 MET

SECOND REVIEW
  `C:/4DApp/recheck/codex/T-AUD-1b_review.md` (gpt-6.1-sol, medium, embedded prompt 424 lines): APPROVE WITH
  CORRECTIONS. Its one LOW (the constraints header's regeneration command is generic, not R3's scratch path): NOT
  UPHELD — a tracked file should name a reproducible command, not a reviewer's scratch folder. Its notes: prefixing
  does not reserve `fourdapp-*` on PyPI (recorded residual); `-c` resolves relative to requirements.txt (agreed).

RESIDUAL (recorded, no row)
  - `fourdapp-*` names are free on PyPI today, not reserved. A squatter could publish one; the missing-`-e` case would
    then install it. Reserving names is an operator decision (PyPI account).
  - The Render build itself is unmeasured here; the operator's merge to `main` is the deploy gate.
  - `C:/4DApp/.venv` keeps the old editable dist names (imports unaffected); rebuild it from `requirements.txt` when
    convenient.
