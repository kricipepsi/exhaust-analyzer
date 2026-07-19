# Which prompt-engineering principles drive which section

Every task file written by this skill uses
`_skills/prompt-engineering-master` principles.
This map shows which principle each section is satisfying — so when you
write a section you know what it's for and don't omit the load-bearing parts.

| Section in `task_file.md` | Principles applied | Why |
|---|---|---|
| `### Goal ###` | P9 (direct, specific task), P25 (explicit requirements) | One-paragraph contract; if you can't state it in a paragraph the task is too big |
| `### Context ###` | P21 (rich context), P3 (break down complex tasks) | Anchors the coder in why; cites prior tasks; surfaces non-obvious constraints |
| `### Deliverables ###` | P17 (specify output format), P25 (explicit requirements) | Enumerated file list + one-line per item; "done" is recognisable |
| `### Files to touch ###` | P25 (explicit requirements) | Scope boundary; coder cannot drift into unrelated files |
| `### Out of scope ###` | P25 (explicit requirements), P4 (unbiased/affirmative phrased as "what NOT to do" is the rare exception — out-of-scope must be explicit) | Pre-empts scope creep; gives coder permission to push back |
| `### Verification ###` | P17 (specify output format), P12 (step-by-step), P20 (examples — concrete copy-pasteable commands) | The success criterion is mechanical, not subjective; agent and human both see the same pass signal |
| `### Progress hook ###` | P17 (specify output format) | Exact one-liner to paste into `PROGRESS.md` — no improvisation |

For `START_HERE.md` itself:

| Section | Principles applied | Why |
|---|---|---|
| Role | P2 (specify audience), P26 (leading words) | Pins the persona and standard |
| Mandatory bootstrap | P3 (break down), P8 (delimiters — numbered list), P12 (step-by-step) | Deterministic load order; no skill misses get blamed on "I forgot" |
| Working rules | P25 (explicit requirements), P11 (affirmative directives where possible) | Constraint surface stays in view all session |
| Session-end checklist | P12 (step-by-step), P17 (output format — the confirmation line) | Mechanical close; the confirmation line is parseable by a loop runner |

## What we deliberately omit

- **Examples in every task file.** Principle 20 says provide examples — but
  for a coding task the example would be the implementation, which defeats
  the purpose. The `Verification` commands are the closest thing to an
  example (they show what "done" looks like).
- **Chain-of-thought requests.** Principle 19. The agent is already
  thinking by virtue of running code-write-test cycles; explicit "think
  step by step" instructions add noise here.
- **Comprehension testing.** Principle 14. This is for learning content,
  not for production task prompts.

## When to deviate

If a task is unusually high-stakes (e.g., touches a shared schema, or is
the first task in a phase that gates downstream work):

- Add a `### Background ###` subsection in Context with extra cited
  documentation paths.
- Add `### Examples ###` showing input → expected output for the public
  interface, when the contract is novel.
- Add `### Risks ###` listing the failure modes the agent must check for.

Don't add these by default. They tax every future task with prose that
isn't load-bearing.
