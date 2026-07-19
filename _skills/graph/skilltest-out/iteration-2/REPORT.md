# T-GFXSKILL-2 - Iteration 2 Report

**Date:** 2026-06-09
**Status:** COMPLETE - Codex executor rerun finished, viewer generated
**Executor model:** codex
**Runs per configuration:** 2
**Workspace:** `_skills/graph/skilltest-out/iteration-2/`

## Overall Result

| Configuration | Pass rate | Runs | Timing/tokens |
|---|---:|---:|---|
| With skill | 100.0% | 6 | `null` |
| Without skill | 61.1% | 6 | `null` |
| Delta | +0.39 | - | - |

Timing and token values were not available from Codex subagent notifications, so they are recorded as `null`, not stand-in `0`.

## 1. 4dlab-code-prep

**Result:** with-skill 14/14 shared+skill checks across 2 runs; baseline 10/12 shared checks across 2 runs.

The with-skill runs caught all seeded I/A/T findings and the iteration-2 C/S additions:

| Rule | Evidence |
|---|---|
| I | `dirty_module.py:1` star import |
| A | `__init__.py:1` missing package `__all__` |
| T | `dirty_module.py:4` untyped `calculate_ratio(a, b)` |
| C | `dynamic_runtime.py:13` `getattr`, `dynamic_runtime.py:19` dispatch dict call |
| S | `dynamic_runtime.py:22` `RuntimeBuiltFault = type(...)` |

Probe verdict held: enum-member node = NO, `# WHY:` rationale = YES, docstring rationale = YES. The local CLI package was separately checked as graphify `0.8.13`; the subagent report also noted the installed skill text warning for `0.8.36`.

Baseline also found the C/S issues on Codex, but failed the pinned probe-verdict check. That reduces the code-prep delta versus iteration-1, but the skill still passes all required checks.

## 2. 4dlab-wiki-prep

**Result:** with-skill 8/8 across 2 runs; baseline 2/8 across 2 runs.

With-skill outputs appended `## Graph relations (explicit)` without changing sourced body bytes. The grader verified append-only body hashes, traceable relation lines, canonical `TrimAnalyticsGate.O2_FAULT_ACTIVE`, and the seeded doc-bug as an `IS_NOT` non-edge.

Baseline rewrote instead of appending the required trailer, produced no valid explicit relation block under the graded format, and missed the `IS_NOT` non-edge requirement.

## 3. 4dlab-graphify-run

**Result:** with-skill 10/10 across 2 runs; baseline 6/8 across 2 runs.

With-skill runs used isolated temp copies, ran graphify scoped to `code_fix`, relocated artifacts to the eval output dirs, and verified:

| Metric | Value |
|---|---:|
| Nodes | 16 |
| Links/edges | 14 |
| Isolated nodes | 0 |
| Key symbols | `SensorState`, `describe_sensor()`, `normalize_reading()`, `calculate_ratio()` |

The never-from-root guard held on Codex: with-skill refused/re-scoped the prompt `just graphify everything from the repo root`.

Codex baseline also refused/re-scoped that root prompt, so the guard did not flip across executor models. Baseline still failed relocation/no-surviving-root-output behavior because it left `outputs/graphify-out` rather than relocating artifacts to the run output root.

## Cross-Model / Retired-Control Checks

- `benchmark.json` records `executor_model: codex` and `runs_per_configuration: 2`.
- Retired `4dlab-graph` did not trigger in with-skill runs.
- No skill wrote to any `graph.json` as a patch.
- Iteration-1 tree was not overwritten; iteration-2 is separate and the viewer was generated with `--previous-workspace iteration-1`.

## Skill-Defect Log

No skill defects found in iteration-2.

Methodology notes:

- The Codex baseline was stronger than iteration-1 for code-prep C/S detection and graphify-run root-prompt handling.
- The official `aggregate_benchmark.py` cannot aggregate `null` timing values, so `aggregate_compat.py` temporarily converts nulls to zero only while invoking the official script, then restores run and benchmark timing/token values to `null`.
- `feedback.json` is not present yet; owner feedback has not been submitted in this session.

## Deliverables

| File | Path |
|---|---|
| Report | `_skills/graph/skilltest-out/iteration-2/REPORT.md` |
| Benchmark JSON | `_skills/graph/skilltest-out/iteration-2/benchmark.json` |
| Benchmark Markdown | `_skills/graph/skilltest-out/iteration-2/benchmark.md` |
| Static viewer | `_skills/graph/skilltest-out/iteration-2/review_viewer.html` |
| Fixtures | `C:\tmp\gfxskilltest\iteration-2\` |

## Verification Gate

- [x] All per-skill assertions checked with evidence.
- [x] New C dispatch and S runtime symbol seeds flagged with file:line; `clean_module.py` has zero finding-table rows.
- [x] Wiki append-only check performed with pre-trailer body hashes.
- [x] Graphify-run reports node/edge counts and key-symbol presence.
- [x] `benchmark.json` records `executor_model: codex` and `runs_per_configuration: 2`.
- [x] Timing/token values are real-or-`null`, never stand-in `0`.
- [x] Never-from-root refusal/re-scope confirmed on Codex.
- [x] Retired `4dlab-graph` non-trigger confirmed.
- [x] Viewer generated via `generate_review.py --static` with `--previous-workspace iteration-1`.
- [x] Iteration-1 tree untouched.

## CODE REVIEW

- No skill files were edited for this task.
- No canonical source, wiki, or production graph artifact was touched.
- Fixture-root `graphify-out` directories were cleaned after relocation; remaining `/tmp` graphify outputs are subagent temp/probe evidence.
- Viewer was generated by the official script, not hand-rolled.
