# Authoring custom on-demand skills

Not every task surface deserves a custom skill. This guide gives the trigger
and anti-trigger rules so the architect doesn't gold-plate the `_INDEX.md`
on-demand tables with orphan skills, and doesn't inline rules that would be
better captured as a reusable skill.

---

## When to author a custom on-demand skill — all of these must hold

1. **The surface gates ≥ 3 atomic tasks.** A skill is amortized over the
   tasks it serves. One task is too few — the inline `### Context ###`
   section handles it. Two is borderline. Three is the threshold.

2. **There is a non-obvious invariant the coder must respect.** Concrete
   examples:
   - A naming convention (`FAULT_<DOMAIN>_<NOUN>`, UK spelling)
   - A forbidden pattern (`v6` imports, `MAF`, `MixtureClass`)
   - A design-rule layer boundary (M0–M5 boundaries, JSON-only cross-lab)
   - A threshold table with provenance requirements
   - A schema convention (three-tier symptom/fault/root-cause taxonomy)
   - A test pattern (drift-guard against a wiki, parametrised regression)

3. **The invariant is read-only authoritative.** The coder *consumes* it,
   doesn't *derive* it. If the invariant is being negotiated mid-task
   (architectural exploration), it belongs in a wiki or design doc —
   not a skill.

---

## Anti-triggers — DON'T author a custom skill when

- **The rule fits in 2 lines of inline `### Context ###` text.** Inline it.
- **The rule is trivial naming or one-line provenance.** The Immediate
  Checklist in `<module>-python` already covers it.
- **The rule is a numeric threshold table that lives in a YAML config and
  changes more often than the skills are revised.** Cite the config from
  inside the task file directly.
- **You're tempted to author a skill because "it would be more thorough."**
  The `_INDEX.md` overhead of an unused skill outweighs the value.
- **Only one task in the entire module touches this surface.** Inline it.

---

## The skill shape (when you do author one)

Use this frontmatter (mirror the v2 / HFX style):

```markdown
---
name: <module>-<surface-or-rule-cluster>
description: >
  <one-paragraph: when to load + what it covers + why ignoring it breaks
  the build. Be specific about file paths and surface areas.>
status: BUILT
---

# <module>-<surface> — <short subtitle>

## When to load this skill

- <bullet of trigger condition 1>
- <bullet of trigger condition 2>
- ...

(Mirror the `_INDEX.md` "Load when…" line. The two should match exactly.)

---

## 1. <First rule cluster>

<the rules; use code blocks for naming conventions; cite the wiki / BP
section where each rule's authority lives>

## 2. <Second rule cluster>

...

## N. <Common pitfalls>

(2–4 things coders get wrong on this surface; cite the failure mode)

## Out of scope

(Things this skill does NOT cover; cross-link to the skill that does)

---

## Cross-references

- `<wiki or BP file>` — the authoritative source for the rules above
- `<other skills in the same bundle>` — adjacent rules they enforce
```

**Sizing target:** 150–250 lines is the sweet spot. Anything longer
probably covers two surfaces — split.

---

## Worked examples — when each module added on-demand skills

### v2 — 9 domain skills, added per phase

| Skill | Tasks gated | Why authored |
|---|---|---|
| `v2-taxonomy` | ~8 (Phase 1 schema work) | Three-tier symptom/fault/root-cause schema needed pinned naming + invariants across symptoms.yaml, faults.yaml, root_causes.yaml |
| `v2-cf-inference` | ~4 (Phase 4 KG work) | CF math + edge-weight bands + no-magnet-edges rule |
| `v2-validation-layer` | ~4 (Phase 2 VL) | VL-runs-first rule + boundary rejection cases |
| `v2-era-masking` | ~3 (Phase 1 + 3 vref work) | dna_core.py / vref.db schema invariants |
| ... | ... | ... |

### HFX — 8 domain skills, all authored before phase 1

| Skill | Tasks gated | Why authored |
|---|---|---|
| `hfx-knowledge-graph` | ~5 | Node naming + threshold provenance for hfx_fault_nodes.yaml |
| `hfx-gas-chemistry` | ~3 | Brettschneider unit-test pinning + 5-gas fixtures |
| `hfx-trim-perception` | ~3 | Three-speed test logic + perception gap detection |
| `hfx-cold-start`, `hfx-non-starter`, ... | ~3 each | Each domain had its own naming + threshold invariants |

### COMLab — 1 domain skill so far (Phase 0b)

| Skill | Tasks gated | Why authored |
|---|---|---|
| `comlab-vocabulary` | 7 (T-P0b-1 through T-P0b-7) | Phase 0b enum surface + StrEnum convention + drift-guard test pattern. Above the ≥3 threshold; clearly read-only authoritative (sourced from `docs/wiki/OBD_VOCABULARY.md` + `DTC_VOCABULARY.md`). |

Future COMLab phases will get their own domain skills:
- Phase 3 (adapters): `comlab-adapters` — JSON contract handling, try/except wrapping, `LabUnavailableError`
- Phase 4 (core scripts): `comlab-fault-router` — Script 3's 5-phase routing loop, confidence scoring
- Phase 5 (e2e): `comlab-cases-corpus` — case-era inference, VIN attachment

---

## The decision flow (cheat sheet)

```
Looking at the phase plan…
│
├── Does any surface gate ≥ 3 tasks?
│   │
│   ├── No → inline rules in each task's ### Context ###. Done.
│   │
│   └── Yes → is there a non-obvious read-only authoritative invariant?
│       │
│       ├── No → inline. Done.
│       │
│       └── Yes → AUTHOR an on-demand skill.
│                 - Create _<module>_skills/<module>-<surface>/SKILL.md
│                 - Add row to _INDEX.md on-demand table
│                 - Reference from each task's `Load skills:` line
│                 - Cross-reference from wiki / BP that gives it authority
```

---

## Promoting an inlined rule to a skill later

If a phase ships with rules inlined into task `### Context ###` sections,
and a later phase reveals that those same rules now gate 3+ more tasks,
**promote**:

1. Author the skill at `_<module>_skills/<module>-<surface>/SKILL.md`.
2. Replace each inline mention in the affected tasks with the one-line
   `Load skills:` reference.
3. Add the row to `_INDEX.md` on-demand table.
4. Note the promotion in the `Architect-level out-of-band patches` table
   in `<MODULE>_PROGRESS.md` (it counts as an architect edit, since the
   skill is part of the bundle, not the per-task diff).

The reverse — demoting an unused on-demand skill back to inline — is also
fine. If a skill in `_INDEX.md` ends up referenced by only 1 task across
the whole module, demote and remove from the index.

---

## Cross-references

- `skill-bundle-creation.md` — how to build the bundle in the first place
- `breakdown-guide.md` — task-sizing rules that determine the "≥ 3 tasks"
  threshold
- v2 worked example: `v2/_v2_skills/v2-taxonomy/SKILL.md`
  (the cleanest "this surface gates many tasks" exemplar)
- COMLab worked example: `4DLab/COMLab/_comlab_skills/comlab-vocabulary/SKILL.md`
