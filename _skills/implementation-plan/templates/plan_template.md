---
goal: {ONE_SENTENCE_GOAL}
version: 1.0
date_created: {YYYY-MM-DD}
last_updated: {YYYY-MM-DD}
owner: {OWNER}
status: 'Planned'
tags: [{purpose}, {component}]
---

# Introduction

![Status: {STATUS}](https://img.shields.io/badge/status-{STATUS_URLENC}-{status_color})

{2–4 sentences: what is being built, from which authoritative source doc(s), and the single governing constraint. Note explicitly which locked facts override older statements in the source doc.}

## 1. Requirements & Constraints

- **REQ-001**: {functional requirement} (source: {doc §N / file:line})
- **SEC-001**: {safety/security requirement} (source: …)
- **CON-001**: {constraint} (source: …)
- **GUD-001**: {guideline} (source: …)
- **PAT-001**: {pattern to follow} (source: …)

## 2. Implementation Steps

### Implementation Phase 1

- GOAL-001: {phase goal, one sentence}

| Task | Description | Depends on | Completed | Date |
|------|-------------|------------|-----------|------|
| TASK-001 | {atomic, deterministic action: exact file paths, function names, literals, pinned citations} | — | | |
| TASK-002 | … | TASK-001 | | |

**Completion criteria:** {machine-checkable: named test passes / byte-identical round-trip / value equals literal}

### Implementation Phase 2

- GOAL-002: …

| Task | Description | Depends on | Completed | Date |
|------|-------------|------------|-----------|------|
| TASK-003 | … | — | | |

**Completion criteria:** …

## 3. Alternatives

- **ALT-001**: {alternative considered and why rejected}

## 4. Dependencies

- **DEP-001**: {runtime/library/data dependency, with version}

## 5. Files

- **FILE-001**: {path} — {purpose, and consumer if it defines schema}

## 6. Testing

- **TEST-001**: {test, its location, and what it proves}

## 7. Risks & Assumptions

- **RISK-001**: {risk and mitigation}
- **ASSUMPTION-001**: {assumption and how/when it gets verified}

## 8. Related Specifications / Further Reading

- {links to source HLD, boundary docs, research answers}
