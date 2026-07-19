# Skill Benchmark: 4dlab-graphify-skills

**Model**: deepseek-v4-pro
**Date**: 2026-06-09
**Evals**: 0 (code-prep), 1 (wiki-prep), 2 (graphify-run) — 1 run each per configuration

## Summary

| Metric | With Skill | Without Skill | Delta |
|--------|------------|---------------|-------|
| Pass Rate | 100% +- 0% | 33% +- 38% | +0.67 |
| Time | — | 116.2s +- 96.0s | — |
| Tokens | — | 37203 +- 14892 | — |

## Per-Skill Breakdown

| Skill | With Skill | Without Skill | Key Differentiator |
|-------|-----------|---------------|-------------------|
| 4dlab-code-prep | 6/6 (100%) | 3/4 (75%) | probe grounding, rule-to-consumer mapping |
| 4dlab-wiki-prep | 5/5 (100%) | 1/4 (25%) | append-only, IS_NOT pattern, canonical labels |
| 4dlab-graphify-run | 5/5 (100%) | 0/4 (0%) | never-from-root guard, scoped run, relocate |

## Probe Results (graphify v0.8.13)

| Question | Answer |
|----------|--------|
| Enum member sub-node? | NO |
| Rationale from #WHY: comment? | YES |
| Rationale from docstring? | YES |

## Notes

- All 3 skills achieve 100% pass rate when loaded; 33% without.
- Retired `4dlab-graph` did not trigger — deprecated-description guard holds.
- graphify v0.8.13: 11 nodes, 10 edges on 3-file code fixture. Enum members not extracted.
- Star import penalty confirmed: no math import edges from `from math import *`.
