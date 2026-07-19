# The language-skill slot

Every project bootstrap has **exactly one** language skill loaded at
`START_HERE.md` step 1. This skill owns the per-file Inner Loop — the
syntax / lint / security / type-check sequence the agent runs after every
meaningful edit.

The language skill is the only mandatory load that doesn't depend on
strict-vs-lite. Even lite-mode projects require it, because the Inner
Loop is what stops generated code from being syntactically broken or
type-unsafe.

## Currently supported

| Language | Skill path | Status |
|---|---|---|
| Python | `v2/_v2_skills/python/SKILL.md` | BUILT |

## Slot rules

1. **One skill per project.** Mixing Python + JS in one bootstrap fragments
   the Inner Loop discipline. Split the project into two task packs if it
   spans languages.
2. **The skill must define an Inner Loop.** If a candidate skill is a
   style guide but doesn't give the agent a command sequence to run after
   every edit, it's not eligible. Wrap it in a thin Inner-Loop skill.
3. **The skill path is absolute in `START_HERE.md`.** No environment-relative
   paths. The bootstrap must work from a fresh session that knows nothing
   about prior state.

## Adding a new language

When a project needs a language not on the table above:

1. Surface this to the user — do not silently invent an Inner Loop.
2. If the user wants you to build the skill, hand off to `skill-creator`
   with a brief that the new skill must:
   - State the per-file Inner Loop as a numbered list with shell commands.
   - List the language's house-style checklist (≤ 12 items).
   - Note the package-existence-check command for the language's package
     manager.
3. Once built, add a row to the table above.

## Why this matters

Research cited in the Python skill: base LLMs hallucinate package names in
~20 % of generated code ("slopsquatting"). The package-existence check in
the Inner Loop catches this before it ships. Skip the language skill and
you skip that check.

Similarly, the per-file syntax compile step costs milliseconds and catches
the most common silent breakage (an edit that produced unbalanced braces
or a stray paste). Without the Inner Loop, you only catch these at test
time — by which point you've burned context on subsequent edits built on
the broken file.
