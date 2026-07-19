# T-SE-2 — Progress Note

**Task:** Eval runner + matched coding-task corpus · **Date:** 2026-06-09 · **Coder:** Claude

## Plan

1. Create `corpus/` with N=5 matched coding tasks, each with `prompt.md` (coder-visible) and `oracle/test_*.py` (hidden correctness check). Mix: 2 synthetic (simple function, trap-API for hallucination metric), 2 real-adjacent (refactor, bug-fix), 1 known-API.
2. Build `runner.py` — CLI (`prepare` / `capture` / `smoke` / `validate` subcommands) that prepares trial working dirs, captures first-pass gate counts (ruff/pyright/pytest), hallucinated-API counts (imports/functions/params via AST + importlib), objective proxies (cyclomatic complexity via radon, type/docstring coverage via AST, diff churn), and writes TrialRecord JSON-lines per `metrics_schema.md` §5.
3. Write `test_runner.py` with 6 tests covering: prepare creates working dir, arm-C gate-skip, TrialRecord.to_dict(), trial ID format, write_records output.
4. Smoke run: 1 task (task_01_string_tools) × arms A/B × K=2, 4 capture runs producing valid JSON-lines.
5. Verify: arm-C gate-skip (first-pass counts all 0), oracle catches deliberately wrong solution (40% pass rate, all 3 bugs detected).

---

## VERIFICATION GATE

```
VERIFICATION GATE — T-SE-2
===========================
ruff (runner.py):           PASS (All checks passed!)
ruff (test_runner.py):       PASS (All checks passed!)
pyright (runner.py):         PASS (0 errors)
pytest (test_runner.py):     PASS (6 passed in 0.21s)

Corpus:
  task_01_string_tools:      EXISTS (prompt.md + oracle/test_string_tools.py, 10 checks)
  task_02_csv_stats:         EXISTS (prompt.md + oracle/test_csv_stats.py, 6 checks)
  task_03_trap_api:          EXISTS (prompt.md + oracle/test_data_fetcher.py, 7 checks)
  task_04_refactor:          EXISTS (prompt.md + starter_code.py + oracle/test_legacy_processor.py, 9 checks)
  task_05_bug_fix:           EXISTS (prompt.md + buggy_code.py + test_interval_merger.py + oracle/test_interval_merger.py, 5 checks)

Smoke run (4 trials × capture):
  Records emitted:           4
  Schema validation:         PASS (0 issues)
  First-pass metrics:        ruff=0, pyright=0, pytest_fail=0 (all 4 trials)
  Hallucinated-API:          hallu_imports=0, hallu_fn=0, hallu_params=0 (all 4)
  Objective proxies:         complexity_avg=2.0, type_cov=100%, doc_cov=23.1%

Arm C gate-skip:
  GATE_OFF marker:           EXISTS (trial task_01_string_tools__verification-loop__C__99)
  first_ruff_errors:         0 (gate skipped — verified)
  first_pyright_errors:      0 (gate skipped — verified)
  first_pytest_failures:     0 (gate skipped — verified)
  test_arm_c_skips_gate:     PASS (asserts all gate counts == 0)

Oracle failure detection:
  Deliberately wrong solution: 4/10 passed (40%), all 3 bugs caught
  - count_vowels bug:        FAIL (expected 1 e, 2 o; got 0, 0)
  - longest_word bug:        FAIL (expected "quick", got "the")
  - is_palindrome missing:   FAIL (AttributeError)

TrialRecord schema:
  All 31 fields present:     PASS (identity 7 + first-pass 4 + convergence 3 +
                                hallucination 3 + rubric 10 + proxies 7 + extra)
  JSON-lines roundtrip:      PASS (validate subcommand: 4 records, 0 issues)

Status: DONE
```

---

## CODE REVIEW

Self-review against task spec (T-SE-2_eval_runner_and_corpus.md):

- **Deliverable 1 (corpus/):** N=5 tasks created. Mix covers all required types: synthetic (task_01 simple function, task_03 trap-API), real-adjacent (task_04 refactor, task_05 bug-fix), known-API (task_02 csv_stats). Each has hidden oracle with `run_all()` that returns pass/fail counts. Trap-API task (task_03) explicitly mentions hallucinated libraries `fast_fetch` and `disk_cache`; oracle's `test_no_hallucinated_imports` is the primary check. PASS.
- **Deliverable 2 (runner.py):** Full CLI with prepare/capture/smoke/validate subcommands. Captures all metrics from `metrics_schema.md`: first-pass counts (ruff/pyright/pytest via subprocess with cwd set), hallucinated-API (imports via `find_spec` + local file check, functions via `importlib.import_module` + local AST check, params via AST call-site check), objective proxies (cyclomatic complexity via radon, type/docstring coverage via AST). TrialRecord dataclass matches schema exactly. Arm C: `--no-gate` flag produces GATE_OFF marker; capture_metrics skips all gate checks when no_gate=True. PASS.
- **Deliverable 3 (smoke run):** 1 task × arms A/B × K=2 = 4 trials executed. All 4 records validate against schema (0 issues). First-pass counts captured, hallucinated-API counts captured, objective proxies captured. PASS.
- **Success criteria:**
  - Runner emits full T-SE-0 metric schema: all 31 TrialRecord fields present and populated. PASS.
  - First-pass counts captured before any fix: runner captures on existing code state. PASS.
  - Arm C path provably skips inner-loop gate: `test_arm_c_skips_gate` asserts all gate counts == 0; GATE_OFF marker confirmed; manual verification shows 0 ruff/pyright/pytest. PASS.
  - Corpus tasks carry hidden oracles: all 5 tasks have oracle/test_*.py with `run_all()`. PASS.
  - Deliberately wrong solution scores as failing: oracle returned 40% pass rate, all 3 bugs detected. PASS.
  - ruff/pyright/pytest clean on runner itself: ruff PASS, pyright 0 errors, pytest 6/6 PASS. PASS.
- **Out of scope:** No full N×K×arms matrix run (that's T-SE-3..6). No skill judging. No rubric scoring (blinded judge placeholder fields are 0.0). PASS.
- **Signal/noise consumer:** `runner.py` output consumed by T-SE-3..6 and T-SE-FINAL. Every emitted field traces to a metric in `metrics_schema.md` §1-4. PASS.
- **No scope creep.** Five corpus task dirs, one runner, one test file, one progress note.
