### Goal ###

{ONE_PARAGRAPH — what this task produces, in concrete language. Name the
function, file, or artefact that proves it's done. If the goal can't be
stated in one paragraph, the task is too big — split it.}

### Success criteria ###

{TESTS-FIRST PHRASING — the test(s) that go green when this task is done.
Examples:
- `tests/test_<x>.py::test_<case>` passes (write it failing first, make it
  pass).
- Existing tests `tests/<y>.py` continue to pass before and after.
- Smoke check: `python -m <module> --selftest` exits 0.

If the success criterion can't be stated as a runnable check, surface this
to the user — fuzzy criteria are the failure mode this section exists to
prevent. See `reference/code-quality-principles.md` §A4.}

### Context ###

{ONE_PARAGRAPH — why this task exists. Which source-prompt step it covers,
which rule or invariant it closes, which prior task it builds on. Cite
file paths and line numbers where useful. Surface any non-obvious design
constraint that future-you will want to know.}

{PIN EXACT CITATIONS — this is a context-budget feature, not just provenance.
The coder's bootstrap reads ONLY what this file names (READ-NARROW). So name the
exact anchors, not "see the wiki": the wiki/spec `§N.M` (plus the line number if
known), the exact numeric literal/threshold, and the exact `file.py::function`
target to edit. A vague reference forces a whole-file read and blows the
bootstrap budget; a pinned `§8.9 (line 941)` lets the coder read ~60 lines.}

{STRICT-ONLY: Load skills: {COMMA_SEPARATED_ON_DEMAND_SKILLS}.}
{IF THIS TASK NEEDS WEB DATA — an API ref, current docs, a value to corroborate — name it here and
add `firecrawl` to the Load skills line. Web work uses the firecrawl skill
(`_skills/firecrawl-web-scraping-search/SKILL.md`), never WebFetch/WebSearch; results go to `.firecrawl/` and are read narrowly.}

### Consumer (signal/noise) ###

{REQUIRED WHEN THIS TASK ADDS OR WIDENS A SCHEMA — any new field, enum value,
fault, or signal. Name the consumer and the exact code path that reads it, so
the coder never has to stop to ask for it (that mid-session stop is the spec
gap this field exists to close). Fill both lines:

- **Consumer:** {the named reader in COMLab analytics OR fault-atlas routing —
  not a layer, a specific decision/branch}.
- **Code path:** {the exact `file.py::function` that consumes it, and what it
  does with the value}.

Rules:
- "Future use", "may be needed later", or a consumer you cannot name = the field
  does not ship. Cut it from Deliverables.
- The consumer may be one this task ADDS in the same diff (v2-rework default:
  ship the field and its reader together as a **proposal**). If so, mark it
  `PROPOSAL`, name the same-diff code path, and register it in the proposals
  registry (e.g. `comlab/config/proposals/`) — never silently inside the live
  registry/KG.
- If this task adds no schema surface, write `N/A — no new field/enum/fault.`}

### Disclosure ###
{OPTIONAL — include when this task *reveals* a fact a later decision depends
on (a measured number, a residual, a feasibility), or when it is a
measurement/checkpoint. Name what the task must **surface, not hide**: the
exact figure/artefact it discloses, and the guard that a shortfall or surprise
is reported rather than rounded away. Tier the output essential-first (headline
→ per-bucket/summary → per-case detail in JSON). If a downstream commitment
(threshold, re-tune, re-pin) is calibrated on this disclosure, it belongs in a
SEPARATE task `Blocked by` this one — do not fold it in here. Omit this section
if the task neither discloses nor measures.}

### Deliverables ###

1. {FILE_PATH_1} — {one-line description of what changes}
2. {FILE_PATH_2} — {one-line description}
{ADD_MORE_AS_NEEDED — but if the list exceeds ~6 items, the task is probably too big}

### Files to touch ###

- `{FILE_PATH_1}` (CREATE | MODIFY)
- `{FILE_PATH_2}` (CREATE | MODIFY)

### Out of scope ###

{ONE_PARAGRAPH — explicitly call out what this task does NOT do. Future
features, adjacent bugs, refactors that could be tempting. Scope creep
is a blocking finding in code review — being explicit here gives the
coder permission to push back.

Surgical-change rule: every changed line must trace to a Deliverable. If
the coder spots unrelated dead code or adjacent improvements, they MENTION
them (as `T##b` rows in PROGRESS.md "Unplanned follow-ups") — they do not
edit them in this task's diff.

GRAPH GUARDRAIL (standing, every task): do NOT run `graphify` / `graphify
update` or rebuild any knowledge graph. The verified `graph/.../graph.json`
(and repo-root `graphify-out/graph.json`) is the canonical artefact —
re-running extraction clobbers verified state and is forbidden unless the
task explicitly instructs it. "Keep the graph current" is not a licence; a
code-only task touches code + tests, never the graph.}

### Verification ###

Concrete commands the coder runs at task end. Every command must be
copy-pasteable and produce a pass/fail signal. Mix language-specific
inner-loop checks (compile, lint, type-check), structural checks
(file exists, function present, contract held), and functional checks
(unit test green, integration test green).

```bash
cd {REPO_ROOT}

# Inner loop on each edited file
{LANGUAGE_INNER_LOOP_COMMANDS}

# Structural checks
{STRUCTURAL_CHECK_COMMANDS}

# Functional / test checks
{TEST_COMMANDS}
```

All steps must pass.

### Progress hook ###

PROGRESS.md `{TASK_ID}`: Status=done, Files changed={COUNT}, Verification="{ONE_LINE_HEADLINE}"
