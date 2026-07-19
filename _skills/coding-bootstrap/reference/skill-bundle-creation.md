# Building the `_<module>_skills/` bundle

Every module that runs the v2 atomic-task pattern has its own skill bundle
at `<project_root>/_<module>_skills/`. The bundle is what `START_HERE.md`
loads at session start, and what task files reference via their
`Load skills:` line.

This guide covers how to build one from scratch. Skip it if the module
already has a populated bundle with `_INDEX.md`.

---

## 1. The structure (mirror HFX / v2)

```
_<module>_skills/
├── _INDEX.md                              ← master index (load this first)
├── <module>-python/SKILL.md               ← universal: house style + inner loop
├── <module>-verification-loop/SKILL.md    ← universal: 6-phase outer gate
├── <module>-code-review/SKILL.md          ← universal: per-diff CODE REVIEW
└── <module>-<domain-N>/SKILL.md           ← on-demand: one per major surface (built as needed)
```

Three universal skills are mandatory. On-demand skills are authored as the
phase plan reveals which surfaces gate ≥ 3 tasks (see
`custom-skill-authoring.md`).

The naming convention is `<module>-<short-noun-phrase>`. Use the module's
short name as the prefix so the skills cleanly distinguish from other
modules' bundles (`comlab-python` vs `v2-python`, `hfx-python`).

---

## 2. Authoring the three universal skills

Each is adapted from `v2/_v2_skills/` (or `HFX/_hfx_skills/`; off-mount
pre-migration examples — on-mount, copy any lab's `labs/<lab>/_<lab>_skills/`). The
mechanical recipe:

### `<module>-python` (or whatever language)

Source: `v2/_v2_skills/python/SKILL.md`

Adaptations:
- Frontmatter `name` becomes `<module>-python`.
- The "Strategic planning" section references the module's `CLAUDE.md` /
  blueprint / wikis instead of v2-specific docs.
- The "Hard constraints" / "Forbidden patterns" section is replaced with
  the module's specific forbidden imports and tokens (v2 bans hybrid
  references; HFX bans MAF/EGR; COMLab bans v6 enum names).
- The "Inner loop" sequence stays the same shape but the package-existence
  check command may differ if the module uses a different package manager.
- The Immediate Checklist stays the same (10 items are universal).

### `<module>-verification-loop`

Source: `v2/_v2_skills/verification-loop/SKILL.md`

Adaptations:
- The 6-phase sequence stays the same shape: syntax → type → lint → pytest
  Layer-1 → corpus/benchmark/drift-guard Layer-2 → diff review.
- **Phase 5 swap:** the v2 default is "Fast accuracy benchmark." Replace
  with whatever the module's analogue is — corpus replay, wiki drift guard
  (COMLab), HFX KR3 score, etc. Phase 5 is the module-specific gate.
- The `VERIFICATION GATE` block template stays the same structure; the
  bullet list of phase results matches whatever the module's 6 phases are.
- Hard stops should reference the module's specific blocker categories.

### `<module>-code-review`

Source: `v2/_v2_skills/v2-code-review/SKILL.md`

Adaptations:
- The §1 design rule compliance section is the most module-specific —
  rewrite to enumerate **this module's** design rules and forbidden
  patterns. Use the module's BP / wiki / IMPLEMENTATION_PLAN as source.
- §2 (scope compliance), §3 (contract changes), §4 (docstrings), §6
  (Immediate Checklist), §7 (test coverage) are mostly universal.
- §5 (provenance) is module-specific — what citation format is required?
  v2 wants `source_guide:` in YAML and `# source:` in Python. COMLab wants
  `# wiki: <FILE> §<n>` in Python. Mirror the convention.
- **Add a structural-craft axis (do NOT drop it).** Append a final review row —
  an axis-8 **WARNING** (not BLOCKING, so it never overrides the module's design
  rules): smells (rigidity / fragility / needless repetition / opacity), the
  depth/deletion test (is the new module deep, or a shallow pass-through that just
  shoves complexity onto callers?), and single-responsibility + small functions
  with one or two concrete extract-and-name suggestions. This folds in the two
  highest-signal skills from the skill-eval (see §2a) — they must live somewhere
  in the bundle, and the code-review skill is their home. The COMLab bundle's
  `comlab-code-review §8` is the worked example.
- The `CODE REVIEW` block grows to 8 numbered rows (the structural-craft axis is
  row 8), each PASS / WARNING / FAIL.

---

## 2a. Which skills earn their context — the skill-eval evidence (read before trimming OR padding a bundle)

A bundle is not "load every coding skill you have." The project ran a controlled
A/B skill-eval (`ARCHIVE/skill_eval/skill_eval_final_report.md`) over 37 candidate
skills: each was measured with vs. without, scored on a rubric and a hidden oracle,
and ranked by effect size (Cohen's *d*, bar = *d* ≥ 1.0). The finding that governs
bundle-building:

- **Only ~5 skills measurably improve produced code (KEEP).** In rank order of
  measured effect: `improve-codebase-architecture` (*d*=1.79), `code-review-excellence`
  (*d*=1.59, on the oracle), `uncle-bob-craft` (*d*=1.43), `python` (*d*=1.37,
  hallucinated-API defense), `python-testing` (*d*=1.35, indicative). Everything
  else was sub-bar, out-of-scope (doc/excel/graph/PDF), or provably dead
  (empty/duplicate/stub) — pure context cost.
- **The three universal skills already carry `python` + `code-review` + the gate.**
  `verification-loop` scored sub-bar on quality (*d*=0.59) but is kept as the
  **gate** for its enforcement value, not its rubric score — that is a deliberate,
  documented exception, not a contradiction of the eval.
- **The two highest-signal skills are structural craft, and they were dropped from
  the first lab bundles (OBDLab/DTCLab).** `uncle-bob-craft` and
  `improve-codebase-architecture` (the top two by effect size) appeared in *no* lab
  bundle — neither absorbed into the `*-python` house-style skill nor the
  `*-code-review` skill. That is the single biggest avoidable miss this evidence
  surfaces. **When you author `<module>-code-review`, you fold their checks back in
  as the structural-craft axis above.** Do not ship a bundle without them.

The rule for crafting a bundle, in one line: **the three universal skills + a
structural-craft axis in code-review is the floor; on-demand domain skills are the
only thing you add, and only when the `custom-skill-authoring.md` ≥3-task trigger
fires.** Don't pad bundles with skills the eval marked out-of-scope or dead.

---

## 3. Authoring `_INDEX.md`

The master index. Worked examples to copy from:

- `v2/_v2_skills/_INDEX.md`
- `HFX/_hfx_skills/_INDEX.md`

Required sections (in order):

```markdown
# <Module> Skill Bundle — Master Index

**Version:** 1.0
**Last updated:** <date>
**Bundle root:** `<absolute path to _<module>_skills/>`

This index is the only place a coder session needs to look to know which
skills exist, which are mandatory at session start, and which to load on
demand. The bootstrap prompt (`<MODULE>_START_HERE.md`) reads this file
before anything else.

---

## Mandatory at every session start

| # | Skill | Path | Purpose |
|---|---|---|---|
| 1 | <module>-python | `_<module>_skills/<module>-python/SKILL.md` | <purpose> |
| 2 | <module>-verification-loop | `_<module>_skills/<module>-verification-loop/SKILL.md` | <purpose> |
| 3 | <module>-code-review | `_<module>_skills/<module>-code-review/SKILL.md` | <purpose> |

The workspace `CLAUDE.md` is read implicitly and carries workspace-wide rules.

---

## On-demand domain skills

Load only when the task surface matches the "Load when…" rule.

| Skill | Status | Path | Load when… |
|---|---|---|---|
| (rows added as phase plans reveal each surface gating ≥ 3 tasks) | — | — | — |

---

## On-demand verification skills

| Skill | Status | Path | Load when… |
|---|---|---|---|
| (TDD-strict, property-tests, mutation-testing, etc., authored as needed) | — | — | — |

---

## Skill-load protocol (paste into every coder session after step 1 of START_HERE)

> **Skill load protocol.** I will `Read` the mandatory skills at session
> start. I will additionally load only the on-demand skills whose
> "Load when…" rule matches the task I am about to work on. I will apply
> the Immediate Checklist to every diff, run the per-file Inner Loop
> after every Edit, and produce both a `VERIFICATION GATE` block and a
> `CODE REVIEW` block in the per-task progress note before flipping a
> task to `done`.

---

## Hard constraints (recap)

- <module-specific bullets — petrol-only, no v6, no diesel, etc.>
- The mandatory skills are non-negotiable. Session does not begin coding
  until all three are loaded.
- A task does not flip to `done` until **both** VERIFICATION GATE and
  CODE REVIEW blocks are clean.
```

Keep `_INDEX.md` under ~130 lines. It is read at the start of every
session — bloating it taxes every future session.

---

## 4. Cross-wiring `_INDEX.md` and `START_HERE.md`

In `<MODULE>_START_HERE.md` Step 6 (the on-demand skill load step), point
at `_INDEX.md`:

```markdown
**6. Load on-demand skill(s).**
`Read _<module>_skills/_INDEX.md` and find the "On-demand" tables. For each
skill whose **Load when…** rule matches this task's `Load skills:` line
(in the task file from Step 7), `Read` that skill's SKILL.md.
```

This is the contract: task files name skills, `_INDEX.md` resolves names to
paths, the bootstrap loads them.

---

## 5. Adding skills later (don't gold-plate up front)

For a new module, the three universal skills are mandatory at Step 1.
On-demand skills can be added **per task** as Step 3 (in SKILL.md) decides
they're needed — you don't have to plan them all up front.

Don't author skills speculatively. The pattern is:
1. Plan a phase.
2. For each task, ask whether a custom skill helps.
3. If yes, author it; add a row to `_INDEX.md` on-demand table; reference
   it from the task's `Load skills:` line.
4. If no, inline the rule in the task's `### Context ###`.

See `custom-skill-authoring.md` for the trigger rules.

---

## 6. Cross-references

- `custom-skill-authoring.md` — when to author an on-demand skill + shape
- `per-language-skills.md` — language-skill slot rules
- v2 worked example: `v2/_v2_skills/_INDEX.md`
- HFX worked example: `HFX/_hfx_skills/_INDEX.md`
- COMLab worked example: `4DLab/COMLab/_comlab_skills/`
