---
name: registry-code-review
description: >
  Per-diff self-review for the 4DLab registry workstream. Load at every
  session start. Produces the CODE REVIEW block that must appear in
  registry/registry_tasks/progress_notes/<task-id>.md alongside the
  VERIFICATION GATE block before any task flips to done.
allowed-tools: [Read, Bash, Grep]
---

# registry-code-review — Per-Diff Self-Review

Run this after the VERIFICATION GATE is clean. The output is a `CODE REVIEW`
block written to `registry/registry_tasks/progress_notes/<task-id>.md`.

---

## Review checklist

For every changed file in the diff, check each item. Record PASS / FAIL / N/A.

### A — Architecture rule compliance

- [ ] No imports from any lab (`gaslab`, `obdlab`, `dtclab`, `dnalab`)
- [ ] No imports from `comlab`
- [ ] No imports from `4DLabWired`
- [ ] No imports from `ARCHIVE/`, `ARCHIVECOMLab/`, `v2/`, or `v6/`
- [ ] Rules-as-data discipline — rule content lives in JSON; Python in this
      workstream is restricted to schema, loader, validator, integration shim
- [ ] No diagnostic logic added inside a rule "callback" or similar Python
      escape hatch — if a rule needs evaluation logic, it's a schema-v2
      evidence-tier field, not Python code

### B — Rule contract integrity

- [ ] Every new or changed rule carries a `passes_cases:` list of curated
      case IDs (no rule may ship without naming the test cases it must PASS)
- [ ] Every case ID in `passes_cases:` resolves to a row in
      `corpus_curated.csv` (no orphan refs)
- [ ] Every numeric threshold in a rule carries a `// wiki: <FILE> §<n>`
      comment naming the wiki source (no bare magic numbers)
- [ ] No invented enum values — chemistry states, fault families, DTC routing
      tags, and evidence tiers all match the schema_v2 vocabulary
- [ ] Every fault family touched in this diff has ≥ 2 competing rules (the
      "no solo survivor" discipline); if only one rule fires for a family,
      it carries a documented confidence ceiling

### C — Surgical change

- [ ] Every changed line traces to a Deliverable in the task file
- [ ] No reformatting of adjacent unchanged code or rules
- [ ] No speculative abstractions or "while I'm here" additions
- [ ] Dead rules mentioned (as a follow-up), not deleted unless orphaned by
      this diff

### D — Test coverage

- [ ] Each new public function / method in registry tooling has ≥ 1 unit test
- [ ] Each new/changed rule file is covered by at least one curated case in
      its `passes_cases:` list (verified by `phase 5b` of the verification
      loop)
- [ ] Regression: at least one existing curated case still PASSes (verified
      by `phase 5c` once the integration shim exists)

### E — Blocking findings

Any FAIL in section A is a **blocking finding** — must fix before `done`.
FAIL in B is blocking unless the rule is explicitly stubbed (the task file
must say so). FAIL in C, D is blocking unless documented with a follow-up
row in `REGISTRY_PROGRESS.md`.

---

## CODE REVIEW block (paste into progress_notes/<task-id>.md)

```
## CODE REVIEW — <TASK_ID>

| Section | Item | Result | Note |
|---|---|---|---|
| A | No lab / COMLab / 4DLabWired imports | PASS/FAIL | |
| A | No ARCHIVE / v2 / v6 imports | PASS/FAIL | |
| A | Rules-as-data discipline | PASS/FAIL | |
| A | No diagnostic logic in Python escape hatches | PASS/FAIL/N/A | |
| B | Every rule has passes_cases list | PASS/FAIL/N/A | |
| B | Every passes_cases ID resolves in corpus_curated.csv | PASS/FAIL/N/A | |
| B | Every numeric threshold has wiki citation | PASS/FAIL/N/A | |
| B | No invented enum values | PASS/FAIL/N/A | |
| B | No solo-survivor rules (≥2 competing rules per family) | PASS/FAIL/N/A | |
| C | All lines trace to Deliverables | PASS/FAIL | |
| C | No scope creep | PASS/FAIL | |
| D | Public functions have tests | PASS/FAIL/N/A | |
| D | Every changed rule covered by ≥1 passing case | PASS/FAIL/N/A | |

**Blocking findings:** (list any A-section FAIL items, or "none")

**Follow-up rows added to REGISTRY_PROGRESS.md:** (IDs or "none")
```

Fill in every row. No row may be left blank. For audit-only tasks (no rule
files touched), B and D rows may be N/A — write the reason in the Note
column.

---

## Cross-references

- `registry-verification-loop` — the VERIFICATION GATE; both blocks must be clean
- `registry-python` — the house-style rules section A enforces
