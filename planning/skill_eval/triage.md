# Skill Triage — Static Inspection Results

**Task:** T-SE-1 · **Date:** 2026-06-09 · **Total files:** 37

## In-Scope Shortlist (A/B track)

These 8 skills claim to shape produced-code quality and will proceed to empirical trials:

| # | Path (under `_skills/`) | `name:` | Cohort |
|---|---|---|---|
| 1 | `codingskills/pythonskill/python/SKILL.md` | `python` | SE-3 |
| 2 | `codingskills/uncle-bob-code-craftsmanship/SKILL.md` | `uncle-bob-craft` | SE-3 |
| 3 | `codingskills/Improve Codebase Architecture/SKILL.md` | `improve-codebase-architecture` | SE-3 |
| 4 | `codingskills/ecc-subset/python-testing/SKILL.md` | `python-testing` | SE-4 |
| 5 | `codingskills/ecc-subset/ai-regression-testing/SKILL.md` | `ai-regression-testing` | SE-4 |
| 6 | `codingskills/ecc-subset/verification-loop/SKILL.md` | `verification-loop` | SE-5 |
| 7 | `codingskills/code-reviev/SKILL.md` | `code-review-excellence` | SE-5 |
| 8 | `prompt-engineering-master/SKILL.md` | `grey-haven-prompt-engineering` | SE-6 (borderline) |

### Ledger reconciliation

- `eval-harness` is listed in CONTRACT §7 as borderline in-scope but the ledger already dispositions it OUT-OF-SCOPE ("tool used *by* the pack; OUT-OF-SCOPE as a code skill"). This triage agrees with the ledger: it is the measurement instrument, not a subject. **Delta explained.**
- `code-simplifier` (no `name:`, no frontmatter) was not in the ledger at all. Discovered during triage; disposition DEAD. **Delta: new find.**
- Otherwise the shortlist matches the ledger's per-skill table exactly.

---

## Full Inventory

| # | Path (under `_skills/`) | `name:` | Disposition | Evidence |
|---|---|---|---|---|
| 1 | `coding-bootstrap/SKILL.md` | `coding-bootstrap` | OUT-OF-SCOPE | Builds infra/tooling, does not shape produced code |
| 2 | `codingskills/code-reviev/SKILL.md` | `code-review-excellence` | IN-SCOPE | Coding skill — review standard; SE-5 cohort |
| 3 | `codingskills/code-simplifier/SKILL.md` | _(none)_ | DEAD | No YAML frontmatter, no `name:` field — unloadable |
| 4 | `codingskills/ecc-subset/ai-regression-testing/SKILL.md` | `ai-regression-testing` | IN-SCOPE | Coding skill — escaped-defect catch; SE-4 cohort |
| 5 | `codingskills/ecc-subset/eval-harness/SKILL.md` | `eval-harness` | OUT-OF-SCOPE | Measurement tool used *by* the eval pack, not a code-quality skill |
| 6 | `codingskills/ecc-subset/python-testing/SKILL.md` | `python-testing` | IN-SCOPE | Coding skill — coverage/mutation/asserts; SE-4 cohort |
| 7 | `codingskills/ecc-subset/verification-loop/SKILL.md` | `verification-loop` | IN-SCOPE | Coding skill — gate-overlap; SE-5 cohort (needs arm C) |
| 8 | `codingskills/Improve Codebase Architecture/SKILL.md` | `improve-codebase-architecture` | IN-SCOPE | Coding skill — cohesion/coupling; SE-3 cohort. **Canonical copy.** |
| 9 | `codingskills/pythonskill/python/SKILL.md` | `python` | IN-SCOPE | Coding skill — house-style + validate loop; SE-3 cohort. **Canonical copy.** |
| 10 | `codingskills/uncle-bob-code-craftsmanship/SKILL.md` | `uncle-bob-craft` | IN-SCOPE | Coding skill — structure/naming; SE-3 cohort |
| 11 | `doc/hld-reviewer-technical-design-expert/SKILL.md` | `hld-reviewer` | OUT-OF-SCOPE | Doc authoring — produces HLD documents, not code |
| 12 | `doc/md-prep/SKILL.md` | `md-prep` | OUT-OF-SCOPE | Doc authoring — markdown preparation |
| 13 | `doc/prd-scaffolding-expert/SKILL.md` | `create-prd` | OUT-OF-SCOPE | Doc authoring — PRD scaffolding |
| 14 | `doc/product-feature-specifications/SKILL.md` | `feature-spec` | OUT-OF-SCOPE | Doc authoring — feature specifications |
| 15 | `doc/project-architecture-guidelines-template-1772334166937/SKILL.md` | _(none)_ | DEAD | No `name:` field; untranslated template for unrelated project (Zenith) |
| 16 | `excel/excel-analysis/SKILL.md` | `Excel Analysis` | OUT-OF-SCOPE | Domain: Excel. **Canonical copy.** |
| 17 | `excel/excel-data-analysis/SKILL.md` | `Excel Analysis` | DEAD | Byte-identical to `excel/excel-analysis/SKILL.md` (SHA256: `FB681B86...`) |
| 18 | `excel/excel-spreadsheet-automation-10/SKILL.md` | `xlsx` | OUT-OF-SCOPE | Domain: Excel/spreadsheet automation |
| 19 | `firecrawl-web-scraping-search/SKILL.md` | `firecrawl` | OUT-OF-SCOPE | Domain: web scraping |
| 20 | `FolderStruct/skill.md` | _(none)_ | DEAD | No YAML frontmatter, no `name:` field — unloadable. Python project-structure content but not wired as a skill. |
| 21 | `graph/SKILL.md` | `stats` | OUT-OF-SCOPE | KG tooling — graph statistics |
| 22 | `graph/4dlab-code-prep/SKILL.md` | `4dlab-code-prep` | OUT-OF-SCOPE | KG tooling — code preparation for graphify |
| 23 | `graph/4dlab-graph/SKILL.md` | `4dlab-graph` | DEAD | Retired 2026-06-09. File explicitly says "DEPRECATED — Do NOT load." Split into 4dlab-code-prep, 4dlab-wiki-prep, 4dlab-graphify-run. |
| 24 | `graph/4dlab-graphify-run/SKILL.md` | `4dlab-graphify-run` | OUT-OF-SCOPE | KG tooling — graphify execution + verify |
| 25 | `graph/4dlab-wiki-prep/SKILL.md` | `4dlab-wiki-prep` | OUT-OF-SCOPE | KG tooling — wiki preparation for graphify |
| 26 | `graph/mcpmarket-plugin-my-toolkit-claude/mcpmarket-my-toolkit/skills/sync/SKILL.md` | _(none)_ | DEAD | No `name:`; byte-identical to 3 other sync stubs (SHA256: `F06B766B...`, 1938 bytes) |
| 27 | `graph/mcpmarket-plugin-my-toolkit-claude(1)/mcpmarket-my-toolkit/skills/sync/SKILL.md` | _(none)_ | DEAD | No `name:`; byte-identical duplicate of #26 |
| 28 | `graph/mcpmarket-plugin-my-toolkit-claude(3)/mcpmarket-my-toolkit/skills/graph/SKILL.md` | `graph` | OUT-OF-SCOPE | KG tooling — graph operations |
| 29 | `graph/mcpmarket-plugin-my-toolkit-claude(3)/mcpmarket-my-toolkit/skills/knowledge-graph-construction/SKILL.md` | `knowledge-graph-construction` | OUT-OF-SCOPE | KG tooling — graph construction |
| 30 | `graph/mcpmarket-plugin-my-toolkit-claude(3)/mcpmarket-my-toolkit/skills/remember/SKILL.md` | `remember` | OUT-OF-SCOPE | Meta — memory/persistence, does not shape code |
| 31 | `graph/mcpmarket-plugin-my-toolkit-claude(3)/mcpmarket-my-toolkit/skills/sync/SKILL.md` | _(none)_ | DEAD | No `name:`; byte-identical duplicate of #26 |
| 32 | `graph/mcpmarket-plugin-my-toolkit-claude(3)/mcpmarket-my-toolkit/skills/understand-chat/SKILL.md` | `understand-chat` | OUT-OF-SCOPE | Meta — chat understanding, does not shape code |
| 33 | `graph/mcpmarket-plugin-my-toolkit-claude2/mcpmarket-my-toolkit/skills/sync/SKILL.md` | _(none)_ | DEAD | No `name:`; byte-identical duplicate of #26 |
| 34 | `Improve Codebase Architecture/SKILL.md` | `improve-codebase-architecture` | DEAD | Byte-identical to `codingskills/Improve Codebase Architecture/SKILL.md` (SHA256: `9E9B617B...`). **Top-level orphan — keep the codingskills copy.** |
| 35 | `pdf-to-markdown-converter-5/SKILL.md` | `pdf-to-markdown` | OUT-OF-SCOPE | Domain: document format conversion |
| 36 | `prompt-engineering-master/SKILL.md` | `grey-haven-prompt-engineering` | IN-SCOPE | Borderline — shapes prompting which shapes code. Flagged for SE-6 review. |
| 37 | `pythonskill/python/SKILL.md` | `python-redirect` | DEAD | Redirect stub. Content: "Stub. The canonical Python skill has moved." Points to `codingskills/pythonskill/python/SKILL.md`. |

### Summary counts

| Disposition | Count |
|---|---|
| IN-SCOPE | 8 |
| OUT-OF-SCOPE | 18 |
| DEAD | 11 |
| **Total** | **37** |

### DEAD breakdown

| Reason | Count | Paths |
|---|---|---|
| No `name:` field (unloadable) | 7 | `code-simplifier`, `FolderStruct/skill.md`, `doc/project-architecture-...`, 4× `sync` stubs |
| Byte-identical duplicate | 2 | `Improve Codebase Architecture/` (top-level), `excel/excel-data-analysis/` |
| Redirect stub | 1 | `pythonskill/python/SKILL.md` |
| Retired/deprecated | 1 | `graph/4dlab-graph/SKILL.md` |

---

## Verification

```powershell
# Expected: 37
(Get-ChildItem -Path "C:\Users\muto\claude\4DApp\4DLab\4DLabV2\_skills" -Recurse -Filter "*kill.md" -File).Count
```

Duplicate hashes reproduced:
- `9E9B617B1C70D390E37DBFD1C031C11B3DE850E2E3D01C4A2C2888BDB386A247` — `Improve Codebase Architecture/` (top-level) ≡ `codingskills/Improve Codebase Architecture/`
- `FB681B860B4D3BC20938CFBE490EBDC39D679D1634F1A6C12727BD4AB7AC91D0` — `excel/excel-analysis/` ≡ `excel/excel-data-analysis/`
- `F06B766B50CB4656CA63245D8506CD4CE3D02D6224024BB4D82D22CFB37E47B9` — all 4 `sync/SKILL.md` stubs (1938 bytes each)
