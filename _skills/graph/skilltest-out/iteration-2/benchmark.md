# Skill Benchmark: 4dlab-graphify-skills

**Executor model:** codex
**Analyzer model:** codex
**Date:** 2026-06-09
**Runs per configuration:** 2
**Evals:** 0 `4dlab-code-prep`, 1 `4dlab-wiki-prep`, 2 `4dlab-graphify-run`

## Summary

| Metric | With Skill | Without Skill | Delta |
|--------|------------|---------------|-------|
| Pass Rate | 100.0% +/- 0.0% | 61.1% +/- 28.2% | +0.39 |
| Time | null | null | null |
| Tokens | null | null | null |

Timing and token values were not available from the Codex subagent notifications, so they are recorded as `null`, not stand-in `0`.

## Denominators

Shared assertion denominators are aligned per eval/config. Skill-only checks are included only in the with-skill configuration and are called out in the assertion text.

| Eval | Config | Runs | Assertions per run |
|------|--------|------|--------------------|
| 0 code-prep | with_skill | 2 | 7 (6 shared + 1 skill-only retired-control check) |
| 0 code-prep | without_skill | 2 | 6 shared |
| 1 wiki-prep | with_skill | 2 | 4 shared |
| 1 wiki-prep | without_skill | 2 | 4 shared |
| 2 graphify-run | with_skill | 2 | 5 (4 shared + 1 skill-only retired-control check) |
| 2 graphify-run | without_skill | 2 | 4 shared |

## Notes

- Code-prep with-skill caught I/A/T plus the new C dispatch and S runtime-symbol seeds with file:line evidence.
- Wiki-prep with-skill preserved append-only body hashes and wrote the seeded doc-bug as an `IS_NOT` non-edge.
- Graphify-run with-skill scoped, relocated, verified counts/symbols, and refused/re-scoped the repo-root prompt.
- Codex baseline also refused/re-scoped the graphify-run repo-root prompt, so the guard did not flip on Codex; the remaining baseline failure there is relocation/no surviving `graphify-out`.
