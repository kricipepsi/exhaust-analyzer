Handoff — graphify skill work, 2026-06-09
Done this session

Verified graphify pipeline from source (README + how-it-works.md @ v8): Pass 1 = tree-sitter AST (code, offline, free); Pass 3 = LLM (prose, tokens); code-only corpus skips Pass 3. Premise resolved: code prep §3 (docstrings/# WHY: → rationale nodes) IS valid — captured in Pass 1, not the skipped LLM pass.
Wrote labs/obdlab/GRAPHIFY_CODE_INGESTION_FORMATTING.md (rule→mechanism guide; reconciles/corrects CodeIngestionPrep.md — §4 test-naming is out of scope, belongs to T-KG-OBD-3).
Assessed 4dlab-graph: proven IngestGraph wiki process is graphify-aligned; the skill was over-built (18KB-chunk assumption, in-file vocab/ENTITY/TABLE markers, Option-3 fake-EXTRACTED patch all dropped).

Built (under 4DLabV2/_skills/graph/) — 3 skills, not 4 (ingestion merges, prep doesn't):

4dlab-code-prep/SKILL.md — source/Pass-1 prep: probe/audit/report, no auto-edit.
4dlab-wiki-prep/SKILL.md — prose/Pass-3 prep: relations/labels/roster/verify, honesty guard.
4dlab-graphify-run/SKILL.md — unified ingestion, code+wiki branches, never-from-root guard, relocate, verify.
4dlab-graph/SKILL.md — RETIRED (deprecation banner added; won't trigger).
SKILLS_TEST_TASK.md — coder acceptance test (with/without, /tmp fixtures only).

Done 2026-06-09 (architect authoring) — both next-session specs are now written:

- T-GFXSKILL-2 (`_skills/graph/T-GFXSKILL-2_skillcreator_eval_loop.md`) — skill-creator eval loop on
  the 3 skills (with/without subagents → `--static` viewer). Reuses T-GFXSKILL-1's fixtures + criteria
  as graded assertions; SUPERSEDES the manual T-GFXSKILL-1 (banner added). Tooling task, not an OBDLab
  ledger row.
- T-KG-OBD-2-PREP (`labs/obdlab/tasks/T-KG-OBD-2-PREP_code_prep_obdlab_source.md`) — the Step-3
  code-prep coder task: apply `4dlab-code-prep` (probe→audit→fix) to `obdlab/obdlab`. Registered in
  `tasks/PROGRESS.md`; now **blocks** T-KG-OBD-2 (re-sequenced from "ready" → "blocked").

Next coder sessions (one task each, recommended order):
1. T-GFXSKILL-2 — validate the 3 skills (hardens code-prep before it touches real source).
2. T-KG-OBD-2-PREP — code-prep `obdlab/obdlab` (probe runs graphify on a /tmp sample ONLY).
3. T-KG-OBD-2 — ingest the prepped, frozen source → `graph/v2_code/`.

Constraints: one task per coder session; skills are repo files in _skills/; commit by explicit path in PowerShell.