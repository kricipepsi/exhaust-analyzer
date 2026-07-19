# Skill-Eval Final Report — Per-Skill Verdicts + Recommended Load-Set

**Pack:** `planning/skill_eval/` · **Task:** T-SE-FINAL · **Date:** 2026-06-10
**Status:** COMPLETE
**Model:** opus-4.7@t=0.0 across all cohorts

This is the terminal deliverable of the skill-eval pack. It answers: *for each of the 37
inventoried skills, does loading it measurably improve produced code — or does it only
consume context?*

---

## 1. Verdict Table — All 37 Skills

### 1.1 Empirically Evaluated (AB / AB+C track)

| # | Skill | Path (under `_skills/`) | Track | Primary metric | Mean(A) ± SD | Mean(B) ± SD | Cohen's d | Bar cleared | Token delta | Verdict |
|---|-------|------------------------|-------|---------------|-------------|-------------|-----------|------------|-------------|---------|
| 1 | python | `codingskills/pythonskill/python` | AB | rubric_structure | 0.95 ± 0.43 | 1.67 ± 0.59 | 1.37 | YES | N/A (unmeasured) | **KEEP** |
| 2 | uncle-bob-craft | `codingskills/uncle-bob-code-craftsmanship` | AB | rubric_total | 8.00 ± 1.12 | 9.31 ± 0.65 | 1.43 | YES | N/A (unmeasured) | **KEEP** |
| 3 | improve-codebase-architecture | `codingskills/Improve Codebase Architecture` | AB | rubric_structure | 0.95 ± 0.43 | 1.67 ± 0.36 | 1.79 | YES | N/A (unmeasured) | **KEEP** |
| 4 | python-testing | `codingskills/ecc-subset/python-testing` | AB | rubric_test_meaningfulness | 1.11 ± 0.37 | 1.74 ± 0.55 | 1.35 | YES | N/A (unmeasured) | **KEEP** * |
| 5 | ai-regression-testing | `codingskills/ecc-subset/ai-regression-testing` | AB | mutation_score | 0.500 ± 0.433 | 0.583 ± 0.331 | 0.22 | no | N/A (unmeasured) | **TRIM** * |
| 6 | verification-loop | `codingskills/ecc-subset/verification-loop` | AB+C | oracle_failures (arm C) | 4.40 ± 1.40 (C_no_skill) | 3.40 ± 1.92 (C_skill) | 0.59 | no | N/A (unmeasured) | **TRIM** |
| 7 | code-review-excellence | `codingskills/code-reviev` | AB+C | oracle_failures (arm C) | 4.40 ± 1.40 (C_no_skill) | 1.20 ± 2.48 (C_skill) | 1.59 | YES | N/A (unmeasured) | **KEEP** |
| 8 | grey-haven-prompt-engineering | `prompt-engineering-master` | T + 1×AB | rubric_total | 12.0 ± 0.0 | 12.0 ± 0.0 | undefined | no (null) | N/A (unmeasured) | **OUT-OF-SCOPE** |

`*` Indicative — N=3 corpus tasks (below frozen §5.1 N≥5). See FU-SE-3.

**Notes on rows:**
- Rows 1–3: Arm A vs Arm B (both gated). The primary metric shown is the skill's **strongest**
  claim metric (CONTRACT §5.3). Python's strongest is `rubric_structure` (d=1.37), not
  `rubric_total` (d=0.49). Improve-codebase-architecture's strongest is `rubric_structure`
  (d=1.79), not `rubric_total` (d=0.98).
- Row 6–7: Arm C (no-gate ablation). The primary metric is `oracle_failures` (escaped defects
  vs hidden oracle). C_no_skill is arm A with gate removed. Lower is better — a negative
  effect on `oracle_failures` indicates recovery of gate-caught quality.
- Row 8: Confirmatory A/B null (SD=0 both arms → null per CONTRACT §5.3). Inspection
  verdict OUT-OF-SCOPE confirmed.

### 1.2 OUT-OF-SCOPE (by inspection — 18 skills)

These skills do not shape produced code in the coder loop. Disposition is by inspection
(T-SE-1 triage), not by trial.

| # | Skill | Path (under `_skills/`) | Rationale |
|---|-------|------------------------|-----------|
| 9 | coding-bootstrap | `coding-bootstrap` | Builds infra/tooling, not code |
| 10 | eval-harness | `codingskills/ecc-subset/eval-harness` | Measurement instrument — circular |
| 11 | hld-reviewer | `doc/hld-reviewer-technical-design-expert` | Doc authoring |
| 12 | md-prep | `doc/md-prep` | Doc authoring |
| 13 | create-prd | `doc/prd-scaffolding-expert` | Doc authoring |
| 14 | feature-spec | `doc/product-feature-specifications` | Doc authoring |
| 15 | Excel Analysis | `excel/excel-analysis` | Domain: Excel |
| 16 | xlsx | `excel/excel-spreadsheet-automation-10` | Domain: Excel |
| 17 | firecrawl | `firecrawl-web-scraping-search` | Domain: web scraping |
| 18 | stats | `graph/SKILL.md` | KG tooling |
| 19 | 4dlab-code-prep | `graph/4dlab-code-prep` | KG tooling |
| 20 | 4dlab-graphify-run | `graph/4dlab-graphify-run` | KG tooling |
| 21 | 4dlab-wiki-prep | `graph/4dlab-wiki-prep` | KG tooling |
| 22 | graph | `graph/mcpmarket-.../skills/graph` | KG tooling |
| 23 | knowledge-graph-construction | `graph/mcpmarket-.../skills/knowledge-graph-construction` | KG tooling |
| 24 | remember | `graph/mcpmarket-.../skills/remember` | Meta — memory, not code |
| 25 | understand-chat | `graph/mcpmarket-.../skills/understand-chat` | Meta — chat understanding |
| 26 | pdf-to-markdown | `pdf-to-markdown-converter-5` | Domain: document conversion |

### 1.3 DEAD (by inspection — 11 skills)

These skills are empty, redirect stubs, byte-duplicates, or lack a `name:` field. They are
provable waste — no trial needed.

| # | Skill | Path (under `_skills/`) | Reason |
|---|-------|------------------------|--------|
| 27 | _(none)_ | `codingskills/code-simplifier` | No YAML frontmatter, no `name:` |
| 28 | _(none)_ | `doc/project-architecture-guidelines-template-1772334166937` | No `name:`; untranslated Zenith template |
| 29 | Excel Analysis (dup) | `excel/excel-data-analysis` | Byte-identical to `excel/excel-analysis` |
| 30 | _(none)_ | `FolderStruct/skill.md` | No YAML frontmatter, no `name:` |
| 31 | 4dlab-graph (retired) | `graph/4dlab-graph` | DEPRECATED — "Do NOT load" |
| 32 | _(none)_ | `graph/mcpmarket-.../sync` (×4 stubs) | No `name:`; byte-identical across 4 copies |
| 33 | improve-codebase-architecture (dup) | `Improve Codebase Architecture` (top-level) | Byte-identical to `codingskills/...` copy |
| 34 | python-redirect | `pythonskill/python` | Redirect stub — "do not load" |

> The 4 `sync` stubs are counted as a single DEAD disposition (4 byte-identical copies of
> the same unloadable file). Together with the other 9 DEAD skills this makes 10 rows
> covering 11 files — the 37-file inventory is complete.

### Summary counts

| Verdict | Count |
|---------|-------|
| KEEP | 5 |
| TRIM | 2 |
| CUT | 0 |
| OUT-OF-SCOPE | 18 |
| DEAD | 10 rows (11 files, 4 sync stubs collapsed) |
| **Total** | **35 rows / 37 files** |

---

## 2. Recommended Default Coder Load-Set

### 2.1 KEEP — load every coding session

These skills cleared the ≥1-SD bar on their strongest claim metric. They earn their context.

| Load order | Skill | One-line reason |
|------------|-------|----------------|
| 1 | **python** | Hallucinated-API defense (0.0 vs 0.4 baseline) + rubric_structure d=1.37. The mandatory language skill. |
| 2 | **uncle-bob-craft** | rubric_total d=1.43, rubric_structure d=3.03, rubric_cohesion d=1.36. Strongest signal in the entire eval. |
| 3 | **improve-codebase-architecture** | rubric_structure d=1.79. Top structure score of any skill. |
| 4 | **code-review-excellence** | Arm-C oracle recovery +3.2 (d=1.59). Arrests edge-case/error-handling/structure defects at authoring time. |
| 5 | **python-testing** | rubric_test_meaningfulness d=1.35. Produces meaningfully better test suites. (Indicative — N=3.) |

### 2.2 TRIM — load situationally

These skills show positive effect but sub-bar on their primary metric. Keep a slimmer version
or load only when the task matches their mechanism.

| Skill | One-line reason | When to load |
|-------|----------------|-------------|
| **verification-loop** | Oracle recovery +1.0 (d=0.59 sub-bar). Positive but below KEEP threshold. Its gate-replication mechanism is partially redundant with the base gate. | Load as the gate skill (mandated by pack bootstrap). Its pytest-enforcement alone justifies context cost even if the oracle recovery is sub-bar. |
| **ai-regression-testing** | Escaped-defect signal positive (+0.083 mutation, +0.250 on task_02) but sub-bar at N=3. Catches boundary defects the general-purpose suite misses. | Load when writing test suites for modules with subtle boundary conditions (stdev, empty-collection, division-by-zero). |

### 2.3 Do NOT load

All 18 OUT-OF-SCOPE skills and all 11 DEAD files. They either do not shape code quality
(doc/excel/graph/PDF skills), are measurement instruments (eval-harness), or are provably
empty/duplicate (no `name:`, byte-identical copies, redirect stubs).

The explicit exclusion list:
- **DEAD (unloadable):** `code-simplifier`, `FolderStruct`, `project-architecture-guidelines-template-*`,
  all 4 `sync` stubs, `4dlab-graph` (retired), `Improve Codebase Architecture` (top-level dup),
  `excel/excel-data-analysis` (dup), `pythonskill/python` (redirect stub)
- **OUT-OF-SCOPE:** `coding-bootstrap`, `eval-harness`, `hld-reviewer`, `md-prep`, `create-prd`,
  `feature-spec`, `Excel Analysis`, `xlsx`, `firecrawl`, `stats`, `4dlab-code-prep`,
  `4dlab-graphify-run`, `4dlab-wiki-prep`, `graph`, `knowledge-graph-construction`,
  `remember`, `understand-chat`, `pdf-to-markdown`, `grey-haven-prompt-engineering`

---

## 3. Caveats Register

### 3.1 Indicative verdicts (FU-SE-3)

The test-craft cohort (T-SE-4) ran on only N=3 corpus tasks that elicit a fresh test suite
(task_01, task_02, task_03) — below the frozen §5.1 N≥5 requirement. The `python-testing`
KEEP and `ai-regression-testing` TRIM verdicts are **indicative** until 2+ test-craft corpus
tasks are added. The bar is the same (d ≥ 1.0) but the smaller N inflates the influence of
any single task.

### 3.2 Judge-bias for code-review-excellence (T-SE-5)

The rubric judge uses heuristics that mirror the code-review-excellence standard itself
(edge cases, error handling, structure). A rubric-based verdict for this skill would be
circular. The KEEP verdict rests on the **objective** `oracle_failures` metric (arm C),
which is independent of the judge. The rubric axes are reported for completeness but are
not the basis of the verdict.

### 3.3 Token cost unmeasured

The eval runner (`runner.py`) does not capture per-trial token counts (`total_tokens` = 0
in all JSONL records). The "token delta" columns are therefore N/A. The verdicts are based
solely on quality metrics — the "is it worth the context?" question is answered by
**effect size** rather than cost accounting. A future runner upgrade adding token capture
would sharpen the TRIM/CUT boundary.

### 3.4 Equivalent mutants flatten mutation_score (FU-SE-6)

On task_02, 6 of 8 injected mutants are `round(x,4)` → `round(x,5)` — equivalent on the
test inputs, so no suite can kill them. This depresses absolute `mutation_score` and
narrows the arm A/B differential. A killable-mutant filter would sharpen discrimination
but is a metric change outside the frozen contract.

### 3.5 Temperature=0, single-session trials

All trials used opus-4.7 at temperature=0.0 in a single session per cohort. Within-arm
variance comes from task-level differences (N=5), not seed-level (K=3 seeds with t=0.0
produce near-identical code). Multi-session trials would provide stronger arm separation,
but the current design already produces d ≥ 1.0 separations for the strongest skills.

### 3.6 Sub-variance nulls

- `grey-haven-prompt-engineering`: confirmatory A/B shows SD=0 on both arms for
  `rubric_total`. Per CONTRACT §5.3, SD=0 both arms → **null** (no measurable effect).
  OUT-OF-SCOPE confirmed.

---

## 4. Independent Verification

One skill's full §5.5 line was independently recomputed from the raw `.jsonl`:

**Skill:** `uncle-bob-craft` / `rubric_total` (cohort_housestyle_scored.jsonl)

| Statistic | Cohort report | Independent recompute | Match |
|-----------|--------------|----------------------|-------|
| mean(A) | 8.00 | 8.00 | ✓ |
| SD(A) | 1.12 | 1.12 | ✓ |
| mean(B) | 9.31 | 9.31 | ✓ |
| SD(B) | 0.65 | 0.65 | ✓ |
| Effect (B−A) | +1.31 | +1.31 | ✓ |
| Pooled SD | — | 0.915 | — |
| Cohen's d | 1.43 | 1.43 | ✓ |
| Bar cleared (d ≥ 1.0) | YES | YES | ✓ |

All values match within rounding. The cohort report's statistics are reproducible from the
raw trial data.

---

## 5. Verdict Cross-Check

| Check | Result |
|-------|--------|
| 37 files inventoried (triage.md) | ✓ — 8 IN-SCOPE + 18 OUT-OF-SCOPE + 11 DEAD = 37 |
| Every KEEP traces to d ≥ 1.0 on its strongest claim metric | ✓ — see §1.1 |
| Every CUT cites null/negative effect | N/A — no CUT verdicts (the two sub-bar skills are TRIM, not CUT) |
| Every OUT-OF-SCOPE / DEAD traced to triage.md disposition | ✓ — see §1.2, §1.3 |
| Recommended load-set contains only KEEP + TRIM skills | ✓ — see §2 |
| Do-NOT-load list covers all 29 OUT-OF-SCOPE + DEAD files | ✓ — see §2.3 |

---

## 6. Consumer

This report is the terminal consumer of the skill-eval pack. Its recommended load-set (§2)
is the artefact the whole pack exists to produce — it tells every future coder session which
skills earn their context and why.

The 4DLabV2 bootstrap files (`START_HERE.md`, per-lab `*_START_HERE.md`, per-pack
`*_START_HERE.md`) should reference the KEEP + TRIM skills listed here as their mandatory
skill load, replacing any prior ad-hoc selection.

---

*Generated by T-SE-FINAL aggregator. Verdict methodology per SKILL_EVAL_CONTRACT.md §5.*
