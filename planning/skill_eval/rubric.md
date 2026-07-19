# Blinded Judge Rubric — Skill-Eval

**Pack:** `planning/skill_eval/` · **Consumer:** T-SE-3..6, T-SE-FINAL · **Version:** 1.0 (frozen)

This rubric measures gate-invisible code quality (CONTRACT §3 metric 5). It is the
sole scoring instrument for the blinded LLM-as-judge. Every A/B trial's final code
artefact is scored on all six axes below, each 0–3, by K≥3 independent judge passes.

## Blinding Protocol

1. **Strip arm labels.** Before submission, rename artefact files to opaque IDs
   (e.g. `sample_01.py`, `sample_02.py`). The mapping is held by the eval runner,
   not the judge.
2. **Randomize order.** Shuffle samples so the judge cannot infer arm by position.
3. **Judge-≠-author rule.** The model acting as judge must differ from the model
   that produced the code under review. At minimum, run judge passes in a
   **separate session** from the generation session.
4. **No task-context leakage.** The judge receives only: the original task spec,
   the artefact file(s), and this rubric. No arm label, no skill name, no ledger
   notes, no conversation transcript.
5. **K ≥ 3 passes per artefact.** Each pass is independent (fresh session or
   `/clear`). Report mean ± SD per axis across passes.

## Scoring Rules

- **Every axis is scored 0–3 for every artefact.** No skipping, no N/A.
- **Anchor descriptions are minimum thresholds.** To earn score N, the code must
  meet the N anchor *and* all anchors below N on that axis.
- **Score what is present, not what is missing by design.** A single-function
  script is not penalized on "structure" for lacking modules — score it within
  its natural scale. If the task spec sets a ceiling (e.g. "no tests required"),
  note it and score the remaining axes.
- **When in doubt, score down.** The tie goes to the lower score. This makes the
  bar conservative: a skill must *clearly* improve quality to earn credit.

---

## Axis 1 — Readability

*Can a same-team colleague understand this code on first read, without asking the author?*

| Score | Anchor |
|-------|--------|
| **0** | Requires reverse-engineering to follow. Dense walls of code with no paragraph breaks. Non-idiomatic constructs used where a standard one exists. Comments are absent or lie. |
| **1** | Mostly parseable but with friction: a few over-long functions, inconsistent whitespace, or one or two "wait, what does this do?" lines. A colleague would need to re-read sections. |
| **2** | Clear on first read. Functions are short and do one thing. Whitespace groups related statements. Idiomatic Python used throughout. Comments explain *why*, not *what*. A colleague would follow it without stopping. |
| **3** | Exemplary. The code tells a story — a reader unfamiliar with the codebase can trace the flow from entry to exit without referencing external docs. Every name is self-documenting; comments only explain non-obvious domain constraints or design tradeoffs. |

---

## Axis 2 — Structure

*Are responsibilities separated? Is the organization navigable and proportional to the problem?*

| Score | Anchor |
|-------|--------|
| **0** | Monolithic: one function/class does too many unrelated things. No discernible layering. File organization is arbitrary or absent. |
| **1** | Some separation visible but inconsistent. A few god-functions or god-classes remain. Module boundaries exist but leak (import cycles, cross-cutting helpers dumped in `utils.py`). |
| **2** | Clean separation of concerns. Each module/file has a single clear responsibility. Dependencies flow one way (no cycles). The structure matches the problem's natural decomposition. |
| **3** | Architecture communicates intent. Module and package boundaries align with domain concepts, not just technical layers. A new contributor could guess where a given responsibility lives without reading the code. |

---

## Axis 3 — Naming

*Are identifiers descriptive, consistent, and conventional?*

| Score | Anchor |
|-------|--------|
| **0** | Cryptic names (`x`, `tmp`, `data`, `result` used indiscriminately). Inconsistent conventions (snake_case mixed with camelCase). Names that lie (`get_x` mutates state). |
| **1** | Mostly named but with lapses: a few single-letter or overly generic names survive in non-trivial scopes; one or two convention breaks. |
| **2** | Every name describes what the thing *is* or *does*. Consistent conventions throughout. No abbreviations that aren't domain-standard. Boolean names read as questions (`is_valid`, `has_catalyst`). |
| **3** | Names are chosen with the reader's mental model in mind. Related concepts share a consistent vocabulary (e.g. `fetch_*` vs `compute_*` vs `build_*` distinguished by cost/side-effect). Renaming a function would make the code *less* clear — the current name is the best possible choice. |

---

## Axis 4 — Cohesion / Coupling

*Do things that change together live together? Are unrelated things kept apart?*

| Score | Anchor |
|-------|--------|
| **0** | Shotgun-surgery risk: changing one rule requires edits scattered across many files. Modules import each other's internals. Global mutable state couples distant code. |
| **1** | Mostly co-located but with leaks: one or two cross-cutting imports of internal details; a shared mutable global that wasn't refactored into a parameter. |
| **2** | High cohesion, low coupling. Functions that operate on the same data live in the same module. Interfaces between modules are narrow (a few well-typed function calls). No import of private names (`_foo`) across module boundaries. |
| **3** | Modules form natural clusters with clear public APIs. Changing one domain rule touches exactly one module. The dependency graph is shallow and acyclic. Interfaces are defined by protocols or abstract bases, not concrete imports. |

---

## Axis 5 — Error Handling

*Are failures caught at the right level, with specific types, and handled or propagated correctly?*

| Score | Anchor |
|-------|--------|
| **0** | Bare `except:` or `except Exception: pass` swallows errors silently. No error propagation strategy. `assert` used for runtime validation. Exit codes or return codes used instead of exceptions. |
| **1** | Exceptions are used but imprecisely: over-broad `except Exception` where a specific type would do; error messages lack context; one or two swallowed exceptions survive. |
| **2** | Specific exception types caught. Errors are logged with context before re-raise or handled definitively. Custom exception classes carry domain context. `contextlib.suppress` used only for genuinely safe-to-ignore cases (e.g. cache file missing). No bare `except:`. |
| **3** | Error handling is designed, not accreted. The module's error strategy is visible: which errors it handles, which it propagates, and why. Recovery paths (retry, fallback, degrade) are explicit. Error messages include enough context to diagnose without a stack trace. |

---

## Axis 6 — Test Meaningfulness

*Do tests verify behavior, not implementation details? Would a test fail if the behavior broke?*

| Score | Anchor |
|-------|--------|
| **0** | No tests, or tests that assert `True`/`1 == 1`. Tests that only check mock calls without verifying outcomes. Tests that pass when the production code is commented out. |
| **1** | Tests exist but are brittle or shallow: they assert implementation details (e.g. "function X was called with exact args") rather than behavior; or they cover only the happy path with no edge cases. |
| **2** | Tests verify observable behavior. Each test has a clear arrange-act-assert structure. Edge cases covered (empty input, boundary values, error paths). A regression in the tested behavior would fail at least one test. Parametrize used for variant coverage. |
| **3** | Tests serve as executable specification. The test names describe *what* the code should do, not *how*. A reader can understand the module's contract from its tests alone. Property-based or generative tests cover input spaces systematically. Error-path tests verify both the exception type *and* the failure message pattern. |

---

## Judge Output Format

Every judge pass must return:

```json
{
  "artefact_id": "<opaque id>",
  "pass_number": 1,
  "axes": {
    "readability":       {"score": 2, "evidence": "<one-line rationale>"},
    "structure":         {"score": 2, "evidence": "<one-line rationale>"},
    "naming":            {"score": 2, "evidence": "<one-line rationale>"},
    "cohesion":          {"score": 2, "evidence": "<one-line rationale>"},
    "error_handling":    {"score": 2, "evidence": "<one-line rationale>"},
    "test_meaningfulness":{"score": 2, "evidence": "<one-line rationale>"}
  },
  "total": 12
}
```

## Aggregation

Across K passes per artefact, report per-axis mean ± SD and total mean ± SD.
The aggregated score is the **mean total across K passes**. The variance is
max(SD) across axes — conservatively, the noisiest axis governs uncertainty.
