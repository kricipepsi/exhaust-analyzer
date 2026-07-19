# T-DTC-CODEPREP — AST-legibility audit of the DTCLab package

**Status:** `done` · **Pack:** VAULT (DTCLab) · completed 2026-06-11 (coder)
Task spec: `Vault/tasks/T-DTC-CODEPREP_ast_legibility_audit_package.md` · Pack ledger: `Vault/tasks/DTC_VAULT_TASKS_START_HERE.md`

## Plan

Scope: production package `labs/dtclab/dtclab/` only (16 modules, ~1,582 lines). No tests, wiki, docs, or real code-graph build touched.

Applied `4dlab-code-prep` per the skill workflow:
1. Probe the local graphify extraction engine.
2. Audit machine-checkable rules I/A/T/C/S + kept R/D (E dropped).
3. Apply only behavior-neutral edits tied to a named Pass-1 consumer.

Probe answers, graphify `0.8.36`:

| Probe | Answer | Scope result |
|---|---:|---|
| Enum member `STABILIZED_IDLE` present as its own node | NO | Rule E dropped |
| `# WHY:` comment emitted as `file_type: rationale` | YES | Rule R kept |
| Formula docstring emitted as `file_type: rationale` | YES | Rule D kept |

The only graphify invocation was the permitted throwaway probe in `C:\Users\muto\claude\4DApp\4DLab\4DLabV2\scratch\gfx_probe`; it wrote only `C:\Users\muto\claude\4DApp\4DLab\4DLabV2\scratch\gfx_probe\graphify-out`.

## VERIFICATION GATE

### Audit Fix Plan (before/after)

| Rule | Count | Finding | Fix |
|---|---:|---|---|
| I | 0 | No star imports in `dtclab/` | None |
| A | 3 | `ranking.py`, `family_map.py`, `data_fusion_sanitizer.py` missing module-level `__all__` | Added `__all__` exports to make public surfaces explicit. |
| T | 0 | All public function/method signatures and class attributes are fully type-annotated. | None |
| C | 0 | No dynamic call sites found. | None |
| S | 0 | No runtime-generated query symbols found. | None |
| R | 0 | All complex logic/thresholds are accompanied by `# wiki:` / `# WHY:` comments. | None |
| D | 0 | All formula/validation methods have parameter-naming docstrings. | None |
| E | dropped | Probe returned NO for enum-member sub-nodes. | Skipped |

After counts:

| Rule | Count |
|---|---:|
| I star imports | 0 |
| A package modules missing `__all__` | 0 |
| T public signature annotation gaps | 0 |
| C forced edits | 0 |
| S runtime-generated query symbols | 0 |
| R forced edits | 0 |
| D forced edits | 0 |

### Checks run (sandbox)

```
$ ..\..\..\.venv-wired\Scripts\ruff.exe check dtclab
All checks passed!

$ ..\..\..\.venv-wired\Scripts\pyright.exe dtclab
0 errors, 0 warnings, 0 informations

$ ..\..\..\.venv-wired\Scripts\pytest.exe -x -q
576 passed in 2.94s
```

- **Ruff:** PASS, `All checks passed!`
- **Star imports:** PASS, no matches.
- **`__all__`:** PASS, `dtclab/__init__.py`, `dtclab/ranking.py`, `dtclab/family_map.py`, and `dtclab/core/data_fusion_sanitizer.py` carry explicit `__all__`.
- **pyright:** PASS, 0 errors.
- **pytest:** PASS, all 576 tests green.
- **`graph/*` collateral:** PASS, no canonical graph files touched.
- **No behaviour change:** Added `__all__` exports only. No logic changed.

### Confirmation items (success criteria)

1. [x] `4dlab-code-prep probe → audit → report` run against `labs/dtclab/dtclab/`
2. [x] In-scope fixes applied; inner loop stays green; test counts preserved (576 passed)
3. [x] No `import *`; public surface has `__all__`; public signatures typed; domain enums are real `StrEnum`s
4. [x] No behaviour change; no graphify run on canonical source; no schema field added/removed

## CODE REVIEW

PASS. The `dtclab` package is extremely well structured and type annotated.
Only the following legibility adjustments were applied:

- **Rule A:** Added explicit `__all__` lists declaring the public surfaces for:
  - `dtclab/ranking.py` (exports `MatchType`, `CandidateScore`, `rank_candidates`, `classify_top3` consumed by the Wired adapter)
  - `dtclab/family_map.py` (exports `CANONICAL_FAMILIES`, `ROUTING_TAG_TO_FAMILY`, `families_for_tags`)
  - `dtclab/core/data_fusion_sanitizer.py` (exports `DataFusionSanitizer` consumed by the main package init)

No behavior logic changed, no schema fields added/removed, no graphify run on canonical source.
