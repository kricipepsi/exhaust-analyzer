# Registry Skill Bundle — Master Index

**Version:** 1.1
**Last updated:** 2026-06-28 (de-Windowsed to in-mount Linux paths; added vault-pack on-demand skill rows)
**Bundle root:** `labs/comlab/registry/docs/_registry_skills/` (repo root `/agent_workspace`)

This index is the only place a coder session needs to look to know which
skills exist, which are mandatory at session start, and which to load on
demand. `REGISTRY_START_HERE.md` reads this file during bootstrap.

**Authoritative source documents:**
- `registry/cvsgaps.md` — corpus-curation driver (keep/drop/add input)
- `4DLabWired/_jaeger/runs/20260527-044325/DIAGNOSTIC_CAPABILITY_ANALYSIS.md`
  — per-phase failure analysis that frames the rebuild
- `4DLabWired/docs/JAEGER_FIX_IMPLEMENTATION_PLAN_2026-05-27.md` §10 —
  the workstream plan
- `TestSuite/cases_petrol_master_v6.csv` — 281-case input corpus
- (Once produced) `registry/CORPUS_AUDIT.md` + `corpus_curated.csv` +
  `corpus_meta.json` — the curated ground truth all v2 rules author against

The registry is **self-contained**: it produces rule data plus minimal
tooling, and never imports from any lab, COMLab, or 4DLabWired. The
direction is one-way — COMLab reads registry artefacts at integration
time (REG-V2-INTEGRATE), the registry never reads COMLab.

---

## Mandatory at every session start

| # | Skill | Path | Purpose |
|---|---|---|---|
| 1 | registry-python | `labs/comlab/registry/docs/_registry_skills/registry-python/SKILL.md` | House style + Immediate Checklist + per-file Inner Loop (py_compile → ruff → pyright → pytest; or JSON parse → schema-validate → case-ID resolve for rule files). |
| 2 | registry-verification-loop | `labs/comlab/registry/docs/_registry_skills/registry-verification-loop/SKILL.md` | 6-phase outer gate; produces the `VERIFICATION GATE` block. Phase 5 = rule-set integrity (schema validity + case-ID resolution + harness side-by-side). |
| 3 | registry-code-review | `labs/comlab/registry/docs/_registry_skills/registry-code-review/SKILL.md` | Per-diff self-review; produces the `CODE REVIEW` block. Both blocks must be clean before any task flips to `done`. |

The workspace `CLAUDE.md` files are read implicitly and carry workspace-wide rules.

---

## On-demand domain skills

Load only when the task surface matches the **Load when…** rule.

| Skill | Status | Path | Load when… |
|---|---|---|---|
| 4dlab-code-prep | shared | `_skills/graph/4dlab-code-prep` | Running `T-RVAULT-2` — AST-legibility audit of the registry package + `tests/` before Pass-1 graphify. |
| 4dlab-doc-prep | shared | `_skills/graph/4dlab-doc-prep` | Running `T-RVAULT-3` — explode/anchor/relations the explicit docs list into `graph/v2_docs/ingest_ready/`. |
| 4dlab-graphify-run | shared | `_skills/graph/4dlab-graphify-run` | Running `T-RVAULT-4` (Pass-1 code+tests) or `T-RVAULT-5` (Pass-3 docs). KG-lane only. |
| 4dlab-vault | shared | `_skills/graph/4dlab-vault` | Running `T-RVAULT-6` — author `vault-map.registry.yaml`, register the corpus, build into `Vault/labs/comlab/registry/`. |
| html-extractor | shared | `anthropic-skills:html-extractor` | `T-RVAULT-3` only, IF `case_library.html` must be converted to markdown for doc-prep. |

These are **shared** pipeline skills (not copies in this bundle); the vault-pack task
files name them on their `Load skills:` line. Read the cited phase of
`planning/LAB_TO_VAULT_PIPELINE_GUIDE.md`, not the whole guide.

**Skills that may be added after AUDIT-REG** (do not author speculatively;
add only when the trigger condition fires):

- `registry-rule-authoring` — would gate every REG-V2-AUTHOR-{family} task.
  Author after REG-V2-SCHEMA lands; it would encode the rule-template
  invariants (evidence tiers, competition groups, passes_cases discipline)
  for ≥ 13 author tasks. **Defer until v2 schema exists.**
- `registry-chemistry-coverage` — would gate AUDIT-CHEM and several
  authoring tasks that key on chemistry. Author only if the chemistry
  matrix needs a non-obvious vocabulary invariant the audit produces.

Per `_skills/coding-bootstrap/reference/custom-skill-authoring.md`: a
domain skill is justified only when (1) it gates ≥ 3 atomic tasks AND
(2) encodes a non-obvious read-only invariant AND (3) the invariant is
authoritative, not derivable. The two candidates above satisfy (1) and
(2); confirm (3) at the moment of authoring.

---

## On-demand verification skills

| Skill | Status | Path | Load when… |
|---|---|---|---|
| (none authored yet) | — | — | — |

---

## Skill-load protocol (paste into every coder session after Step 1 of START_HERE)

> **Skill load protocol.** I will `Read` the three mandatory skills at
> session start. I will additionally load only the on-demand skills whose
> "Load when…" rule matches the task I am about to work on (the task
> file's `Load skills:` line names them). I will apply the Immediate
> Checklist to every diff, run the per-file Inner Loop after every Edit,
> and produce both a `VERIFICATION GATE` block and a `CODE REVIEW` block
> in the per-task progress note before flipping a task to `done`.

---

## Hard constraints (recap)

- **Self-contained.** The registry imports only its own modules + stdlib
  + Pydantic. No imports from any lab, COMLab, or 4DLabWired.
- **Rules-as-data first.** Rules live in JSON; Python in this workstream
  is restricted to schema, loader, validator, integration shim.
- **Every rule traces to a case.** `passes_cases:` is non-negotiable.
- **Every threshold carries a wiki citation.** No bare magic numbers.
- **Petrol-only, v1.** No diesel, LPG, or CNG paths.
- **Python 3.14.** Shared `/agent_workspace/.venv-wired`; invoke `python3.14`
  explicitly (system default 3.12 breaks on `StrEnum`).
- **No legacy imports.** Never import from `ARCHIVE/`, `ARCHIVECOMLab/`,
  `v2/`, or `v6/`.
- The three mandatory skills are non-negotiable. A session does not begin
  coding until all three are loaded.
- A task does not flip to `done` until **both** the `VERIFICATION GATE`
  and `CODE REVIEW` blocks are clean in
  `labs/comlab/registry/docs/registry_tasks/progress_notes/<task-id>.md`.

---

## Maintenance

When a future phase reveals a new surface gating ≥ 3 tasks with a
non-obvious read-only invariant, author a new on-demand skill, add a row
above, and reference it from each affected task's `Load skills:` line.
Do not author orphan skills (one skill, one task) — inline single-task
rules into that task's `### Context ###` instead. See
`_skills/coding-bootstrap/reference/custom-skill-authoring.md`.
