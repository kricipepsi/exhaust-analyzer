# WTEST2_PYSCN_WIRED_2026-06-30 — `pyscn` audit of `apps/wired`

**Task:** `T-WTEST-2`  
**Mode:** read-only static audit; no source, lab, COMLab, `Vault/`, graph, hook, CI, HTML, or JSON repo edits.  
**Target:** `apps/wired` only. Labs were already audited by `T-PYSCN-1` and were not re-audited here.  
**Machine JSON:** `/tmp/pyscn_wired.json` only; the transient `.pyscn/reports/analyze_20260630_114628.json` emitted by `pyscn analyze` was removed from the repo after copying to `/tmp`.

## One-line verdict

**Clean against the pinned `T-PYSCN-1` blocking thresholds** (`--max-complexity 10`, `--max-cycles 0`, dead-code/deps selected): `pyscn check` exited `0`, no function exceeded complexity 10, no dead code was reported, and dependency cycles were `0`. **Advisory debt remains:** `pyscn analyze` reports grade `C` / health `71`, a production-heavy Type-4 clone group (`9` fragments, `6` production-only pairs), and a module-level cognitive-complexity warning for `apps/wired/wired/composition.py:1` (`56 > 25`).

## Commands and exits

| Command | Exit | Output |
|---|---:|---|
| `uvx pyscn@latest version` | 0 | `pyscn 1.24.3` / commit `4419636` / built `2026-06-21` / `go1.25.5` / `linux/amd64` |
| `uvx pyscn@latest check --select deadcode,complexity,deps --max-cycles 0 apps/wired` | 0 | `Code quality check passed` |
| `uvx pyscn@latest analyze apps/wired --json` | 0 | JSON report copied to `/tmp/pyscn_wired.json`; CLI summary reported health `71/100 (Grade: C)` |

Version drift from `T-PYSCN-1`: **none**. The observed version is still `pyscn 1.24.3` (`4419636`).

## Metrics summary

| Metric | Value |
|---|---:|
| Total files | 9 |
| Analyzed files | 9 |
| Skipped files | 0 |
| Parse failures | 0 |
| Health score | 71 / 100 |
| Grade | C |
| Total functions | 1 |
| Average complexity | 6 |
| Average cognitive complexity | 7 |
| High-complexity functions | 0 |
| Dead-code findings | 0 |
| Critical dead-code findings | 0 |
| Dependency modules | 9 |
| Dependency cycles | 0 |
| Clone groups | 1 |
| Clone pairs | 9 |
| Duplication percentage | 30.0% |
| CBO classes / high coupling | 0 / 0 |
| LCOM classes / high LCOM | 1 / 0 |
| Architecture score | 91 |
| Dependency score | 85 |

Analyzed Python files:

- `apps/wired/wired/__init__.py`
- `apps/wired/wired/composition.py`
- `apps/wired/wired/registry_guard.py`
- `apps/wired/wired/run_case.py`
- `apps/wired/wired/tracing.py`
- `apps/wired/tests/test_composition.py`
- `apps/wired/tests/test_fatal_gate.py`
- `apps/wired/tests/test_oil_cases.py`
- `apps/wired/tests/test_tracing.py`

## Production-code findings (`apps/wired/wired/*.py`)

### Blocking-threshold findings

| Check | Result | Evidence |
|---|---|---|
| Function complexity `> 10` | PASS | No function over threshold. Only reported function: `_diagnose` at `apps/wired/wired/composition.py:83`, complexity `6`, cognitive `7`, low risk. |
| Dead code | PASS | `dead_code_count = 0`, `critical_dead_code = 0`. |
| Dependency cycles | PASS | `deps_modules_in_cycles = 0`, `CyclicDependencies = 0`. |
| Parse failures | PASS | `analyzed_files = 9`, `skipped_files = 0`, no parse errors emitted. |

### Advisory production findings

| Finding | Location | Evidence | Verdict impact |
|---|---|---|---|
| Module cognitive complexity warning | `apps/wired/wired/composition.py:1` | `<module> cognitive complexity too high (56 > 25)` | Advisory only; pinned gate is function complexity `>10`, and no function crosses it. |
| Type-4 semantic clone group | `apps/wired/wired/composition.py` + `apps/wired/wired/run_case.py` | One clone group, nine fragments, six production-only pairs. | Advisory only; `T-PYSCN-1` explicitly kept clones out of the blocking gate. |

Production-only clone pairs:

| Pair | Similarity | Locations |
|---:|---:|---|
| 1 | 0.954 | `apps/wired/wired/composition.py:164-234` ↔ `apps/wired/wired/composition.py:282-345` |
| 3 | 0.821 | `apps/wired/wired/composition.py:67-80` ↔ `apps/wired/wired/composition.py:367-378` |
| 4 | 0.761 | `apps/wired/wired/composition.py:282-345` ↔ `apps/wired/wired/composition.py:367-378` |
| 6 | 0.726 | `apps/wired/wired/composition.py:83-141` ↔ `apps/wired/wired/composition.py:237-279` |
| 7 | 0.694 | `apps/wired/wired/composition.py:144-161` ↔ `apps/wired/wired/composition.py:237-279` |
| 9 | 0.653 | `apps/wired/wired/composition.py:83-141` ↔ `apps/wired/wired/composition.py:282-345` |

Interpretation: the highest production-only clone signal is the repeated mapper shape between `_run_gaslab` and `_run_obdlab`. That shape is currently a composition seam, not a correctness failure; do not refactor it in this read-only task.

## Test-file findings (`apps/wired/tests/*.py`)

| Check | Result | Evidence |
|---|---|---|
| Function complexity `> 10` | PASS | No test function complexity finding emitted. |
| Dead code | PASS | No test dead-code finding emitted. |
| Test-only clones | PASS | `0` test-only clone pairs. |
| Mixed test/production clones | ADVISORY | `3` mixed pairs involving `apps/wired/tests/test_tracing.py:85-97`. |

Mixed clone pairs:

| Pair | Similarity | Locations |
|---:|---:|---|
| 2 | 0.831 | `apps/wired/tests/test_tracing.py:85-97` ↔ `apps/wired/wired/run_case.py:49-76` |
| 8 | 0.666 | `apps/wired/tests/test_tracing.py:85-97` ↔ `apps/wired/wired/composition.py:367-378` |
| 10 | 0.652 | `apps/wired/tests/test_tracing.py:85-97` ↔ `apps/wired/wired/composition.py:144-161` |

Interpretation: these are advisory semantic-similarity matches around short orchestration/test-span shapes. They do not inflate the blocking verdict because clones are advisory and are split out from production thresholds.

## Coverage gaps and policy notes

`pyscn` does **not** cover unused package dependencies and does **not** enforce lab-isolation / cross-lab import policy. Use `deptry` for unused dependencies and `tach` or `import-linter` for package-boundary policy if a later task needs that coverage. `pyscn deps` means within-tree dependency cycles, not cross-package import policy. **Lab-isolation is N/A for `apps/wired`** because `wired` is the sanctioned composition layer that imports GASLab, OBDLab, DTCLab, DNALab, VINLab, and COMLab together.

## Follow-up candidates, not fixed here

- If the architect wants a cleanup task, start with the production clone signal in `apps/wired/wired/composition.py`, especially mapper-shape repetition across `_run_gaslab`, `_run_obdlab`, and `_run_dtclab`.
- Keep clone cleanup optional until there is a behaviour-preserving seam that does not hide the explicit lab-to-COMLab field mapping. The current explicit mapping has reviewer value.
- Do not wire `pyscn` into CI/pre-commit here; that remains the separate deferred `T-PYSCN-2` decision.
