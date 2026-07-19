# T-WTEST-2 — progress note

## Plan

Scope confirmation: I am taking `T-WTEST-2` only. This is a read-only `pyscn` audit of `apps/wired`; I will touch only `apps/wired/test_tasks/progress_notes/T-WTEST-2.md`, `apps/wired/test_tasks/reports/WTEST2_PYSCN_WIRED_2026-06-30.md`, and `apps/wired/test_tasks/TEST_PROGRESS.md`; I will run `uvx pyscn@latest version`, `uvx pyscn@latest check --select deadcode,complexity,deps --max-cycles 0 apps/wired`, and `uvx pyscn@latest analyze apps/wired --json` with machine JSON kept at `/tmp/pyscn_wired.json` only. No source, lab, COMLab, `Vault/`, graph, hook, CI, HTML, or JSON repo edits are in scope; AGENTS.md risk is avoiding graphify and preserving wired's sanctioned multi-lab-import role, so lab-isolation is reported as N/A for wired.

## `pyscn` version

Command: `cd /agent_workspace && uvx pyscn@latest version`  
Exit code: `0`

```text
pyscn 1.24.3
Commit: 4419636
Built: 2026-06-21
Go: go1.25.5
OS/Arch: linux/amd64
```

Version drift from `T-PYSCN-1`: **none**.

## `pyscn check`

Command: `cd /agent_workspace && uvx pyscn@latest check --select deadcode,complexity,deps --max-cycles 0 apps/wired`  
Exit code: `0`

```text
stdout: <empty>
stderr:
🔍 Running quality check (complexity, deadcode, deps)...
✅ Code quality check passed
```

## `pyscn analyze --json`

Command: `cd /agent_workspace && uvx pyscn@latest analyze apps/wired --json`  
Exit code: `0`  
Machine JSON path: `/tmp/pyscn_wired.json` (`82,261` bytes)  
Repo JSON/HTML artifacts: none retained; the transient `.pyscn/reports/analyze_20260630_114628.json` emitted by `pyscn` was copied to `/tmp/pyscn_wired.json` and removed. `glob` found no `.pyscn/**/*`, `apps/wired/test_tasks/**/*.json`, or `apps/wired/test_tasks/**/*.html`.

```text
📊 Unified JSON report generated: /agent_workspace/.pyscn/reports/analyze_20260630_114628.json

📊 Analysis Summary:
Health Score: 71/100 (Grade: C)
Total time: 7202ms

📈 Detailed Scores:
  Complexity:      70/100 ⚠️  (avg: 6.0, high-risk: 0 functions)
  Dead Code:      100/100 ✅  (0 issues, 0 critical)
  Duplication:      0/100 ❌  (30.0% fragments cloned, 1 groups)
  Coupling (CBO): 100/100 ✅  (avg: 0.0, 0/0 high-coupling)
  Cohesion (LCOM):100/100 ✅  (avg: 1.0, 0/1 high-lcom)
```

## Parsed findings

| Metric | Value |
|---|---:|
| Total files | 9 |
| Analyzed files | 9 |
| Skipped files | 0 |
| Parse failures | 0 |
| Health score | 71 / 100 |
| Grade | C |
| Total functions | 1 |
| High-complexity functions | 0 |
| Dead-code findings | 0 |
| Dependency cycles | 0 |
| Clone groups | 1 |
| Clone pairs | 9 |
| Production-only clone pairs | 6 |
| Mixed test/production clone pairs | 3 |
| Test-only clone pairs | 0 |

Production threshold findings: none. Only function-level complexity finding was `_diagnose` at `apps/wired/wired/composition.py:83` with complexity `6`, cognitive complexity `7`, and low risk.  
Advisory findings: module cognitive-complexity warning at `apps/wired/wired/composition.py:1` (`56 > 25`) and one Type-4 semantic clone group (`9` fragments, `6` production-only pairs, `3` mixed pairs).  
Report path: `apps/wired/test_tasks/reports/WTEST2_PYSCN_WIRED_2026-06-30.md`.

## Coverage-gap line

`pyscn` does **not** cover unused package dependencies and does **not** enforce lab-isolation / cross-lab import policy. Use `deptry` for unused dependencies and `tach` or `import-linter` for package-boundary policy if a later task needs that coverage. `pyscn deps` means within-tree dependency cycles, not cross-package import policy. **Lab-isolation is N/A for `apps/wired`** because `wired` is the sanctioned composition layer that imports GASLab, OBDLab, DTCLab, DNALab, VINLab, and COMLab together.

## VERIFICATION GATE — T-WTEST-2

```text
VERIFICATION GATE — T-WTEST-2
1. Compile : PASS  (N/A: read-only audit; no Python source touched)
2. Lint    : PASS  (N/A: read-only audit; no Python source touched; pyscn check exited 0)
3. Types   : PASS  (N/A: read-only audit; no Python source touched)
4. Tests   : PASS  (uvx pyscn@latest version -> 0; check --select deadcode,complexity,deps --max-cycles 0 apps/wired -> 0; analyze apps/wired --json -> 0)
5. Contract: PASS  (version pinned at 1.24.3; /tmp/pyscn_wired.json captured; parse failures 0; report written at apps/wired/test_tasks/reports/WTEST2_PYSCN_WIRED_2026-06-30.md; report separates production/test findings and names coverage gaps)
6. Orphan  : N-A   (no field/fault/consumer mapping added; report consumer is architect cleanup go/no-go)
Result: CLEAN
```

## CODE REVIEW — T-WTEST-2

```text
CODE REVIEW — T-WTEST-2
Scope         : PASS  (changed only this progress note, the WTEST2 Markdown report, and TEST_PROGRESS.md for the T-WTEST-2 ledger row)
Composition   : PASS  (no lab edits, no COMLab edits, no source edits, no second-lab import changes, no deferred path, no graphify)
Consumers     : PASS  (N/A: no mapped fields; named consumer is architect cleanup go/no-go via the report artifact)
Literals      : PASS  (N/A: no boundary literals added)
Docstrings    : PASS  (N/A: no public functions added)
Craft (WARN)  : depth=N/A read-only audit; deletion=no scaffolding/source code added; seam=no mapping logic touched; interface=pyscn run against public apps/wired target, not private helper-only inspection
Result: CLEAN
```

## Workspace note

No generated JSON/HTML artifact was retained in the repo. `glob` found no `.pyscn/**/*`, `apps/wired/test_tasks/**/*.json`, or `apps/wired/test_tasks/**/*.html` after cleanup. The `/tmp/pyscn_wired.json` machine artifact remains outside the repo as required.
