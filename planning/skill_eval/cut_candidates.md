# Cut Candidates — Safe to Delete/Dedupe

**Task:** T-SE-1 · **Date:** 2026-06-09

> **Do not delete here.** This pack measures, it doesn't prune. These paths are for the owner to action separately.

## Delete (redirect stub + empty parent)

| # | Path to delete | Reason |
|---|---|---|
| 1 | `_skills\pythonskill\python\SKILL.md` | Redirect stub — canonical skill is at `codingskills/pythonskill/python/SKILL.md`. Delete the empty `_skills\pythonskill\` tree afterward. |

## Delete (no `name:` — unloadable)

| # | Path to delete | Reason |
|---|---|---|
| 2 | `_skills\codingskills\code-simplifier\SKILL.md` | No YAML frontmatter, no `name:` field — cannot be loaded as a skill |
| 3 | `_skills\FolderStruct\skill.md` | No YAML frontmatter, no `name:` field — untemplated Python project-structure doc |
| 4 | `_skills\doc\project-architecture-guidelines-template-1772334166937\SKILL.md` | No `name:` field; untranslated Chinese template for unrelated project (Zenith) |

## Delete (retired)

| # | Path to delete | Reason |
|---|---|---|
| 5 | `_skills\graph\4dlab-graph\SKILL.md` | Retired 2026-06-09; split into `4dlab-code-prep`, `4dlab-wiki-prep`, `4dlab-graphify-run` |

## Delete (byte-identical duplicates — keep canonical)

| # | Path to delete | Reason |
|---|---|---|
| 6 | `_skills\Improve Codebase Architecture\SKILL.md` | Byte-identical to `codingskills/Improve Codebase Architecture/SKILL.md` (SHA256: `9E9B617B...`). Keep the codingskills copy. |
| 7 | `_skills\excel\excel-data-analysis\SKILL.md` | Byte-identical to `excel/excel-analysis/SKILL.md` (SHA256: `FB681B86...`). Keep `excel-analysis`. |

## Delete (4× byte-identical sync stubs — keep none)

All four are byte-identical (SHA256: `F06B766B...`, 1938 bytes), no `name:` field, no unique content:

| # | Path to delete |
|---|---|
| 8 | `_skills\graph\mcpmarket-plugin-my-toolkit-claude\mcpmarket-my-toolkit\skills\sync\SKILL.md` |
| 9 | `_skills\graph\mcpmarket-plugin-my-toolkit-claude(1)\mcpmarket-my-toolkit\skills\sync\SKILL.md` |
| 10 | `_skills\graph\mcpmarket-plugin-my-toolkit-claude(3)\mcpmarket-my-toolkit\skills\sync\SKILL.md` |
| 11 | `_skills\graph\mcpmarket-plugin-my-toolkit-claude2\mcpmarket-my-toolkit\skills\sync\SKILL.md` |

Also safe: the now-empty parent directories `mcpmarket-plugin-my-toolkit-claude/`, `mcpmarket-plugin-my-toolkit-claude(1)/`, `mcpmarket-plugin-my-toolkit-claude2/` (the `(3)` copy still has other skills: `graph`, `knowledge-graph-construction`, `remember`, `understand-chat`).

## Summary

| Action | File count | Bytes saved (approx) |
|---|---|---|
| Delete (redirect stub) | 1 | ~650 B |
| Delete (no `name:`) | 3 | ~8 KB |
| Delete (retired) | 1 | ~33 KB |
| Delete (byte-dup) | 2 | ~9 KB |
| Delete (sync stubs ×4) | 4 | ~7.8 KB |
| **Total** | **11 files** | **~58 KB** |

After deletion, `_skills/` retains 26 skill files: 8 IN-SCOPE + 18 OUT-OF-SCOPE.
