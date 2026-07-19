# T-PYSCN-1 — progress note
_(coder fills)_

## Plan (as executed)

1. Read `AGENTS.md` and `apps/wired/WIRING_PREP.md`; queried existing lab graph JSONs for orientation without running `graphify`.
2. Confirmed `uvx pyscn@latest version` works: `pyscn 1.24.3`, commit `4419636`, built `2026-06-21`, Go `1.25.5`, `linux/amd64`.
3. Ran `uvx pyscn@latest check --select deadcode,complexity,deps <target>` for:
   `labs/gaslab`, `labs/obdlab`, `labs/dtclab`, `labs/comlab`, `labs/dnalab`, `labs/vinlab`, `labs/symptomlab`, `labs/semantic`, and `apps/wired`.
4. Ran `uvx pyscn@latest analyze --json <target>` from `/tmp`; copied emitted JSON to `/tmp/pyscn_<target>.json` when present.
5. Aggregated metrics and production/test splits into `/tmp/pyscn_aggregate.json`.
6. Wrote the findings report at `planning/code_audit/reports/PYSCN_EVAL_2026-06-29.md`.

## VERIFICATION GATE — T-PYSCN-1

- **Version proof:** `uvx pyscn@latest version` exited 0 and printed `pyscn 1.24.3` / commit `4419636`.
- **Per-target `check` exits:**
  - `labs/gaslab`: exit 1; 4 complexity issues.
  - `labs/obdlab`: exit 1; 2 complexity issues.
  - `labs/dtclab`: exit 1; 1 complexity issue.
  - `labs/comlab`: exit 1; 8 complexity issues.
  - `labs/dnalab`: exit 0; passed.
  - `labs/vinlab`: exit 1; 21 complexity issues.
  - `labs/symptomlab`: exit 0; passed.
  - `labs/semantic`: exit 1; invalid input, no Python files found.
  - `apps/wired`: exit 1; invalid input, no Python files found.
- **Per-target `analyze --json` exits:**
  - `labs/gaslab`: exit 0; JSON copied to `/tmp/pyscn_gaslab.json`.
  - `labs/obdlab`: exit 0; JSON copied to `/tmp/pyscn_obdlab.json`.
  - `labs/dtclab`: exit 0; JSON copied to `/tmp/pyscn_dtclab.json`.
  - `labs/comlab`: exit 0; JSON copied to `/tmp/pyscn_comlab.json`.
  - `labs/dnalab`: exit 0; JSON copied to `/tmp/pyscn_dnalab.json`.
  - `labs/vinlab`: exit 0; JSON copied to `/tmp/pyscn_vinlab.json`.
  - `labs/symptomlab`: exit 0; JSON copied to `/tmp/pyscn_symptomlab.json`.
  - `labs/semantic`: exit 1; no Python files found, no JSON emitted.
  - `apps/wired`: exit 1; no Python files found, no JSON emitted.
- **Parse-failure list:** none observed for Python-bearing targets; JSON analysis error arrays were empty. `labs/semantic` and `apps/wired` are invalid-input/no-Python targets, not parse failures.
- **Report path:** `planning/code_audit/reports/PYSCN_EVAL_2026-06-29.md`.
- **Verdict:** wire in only as non-blocking agent/code-audit tooling first; do not add a blocking pre-commit/CI gate until current complexity debt is fixed or explicitly baselined.

## CODE REVIEW — T-PYSCN-1

- Read-only scope respected: no source, `Vault/`, graph, hook, CI, or config edits were made.
- `graphify` was not run; existing graph JSONs were queried only.
- Report includes per-target metrics, production-code complexity items with `file:line`, dead-code and cycle results, clone test-vs-production split, and the explicit coverage gap: `pyscn` does not cover unused dependencies (`deptry`) or lab-isolation / cross-lab import policy (`tach` / `import-linter`).
- Generated JSON/log artifacts were kept under `/tmp` and not committed into the repo.
