# T-GAS-CODEPREP — AST-legibility audit of the GASLab package

**Status:** `done` · **Pack:** VAULT (GASLab) · completed 2026-06-11 (coder)
Task spec: `Vault/tasks/T-GAS-CODEPREP_ast_legibility_audit_package.md` · Pack ledger: `Vault/tasks/GAS_VAULT_TASKS_START_HERE.md`

## Plan

Scope: production package `labs/gaslab/gaslab/` only (11 modules, ~1,992 lines). No tests, wiki, docs,
`graph/*`, or real code-graph build touched.

Applied `4dlab-code-prep` per the skill workflow:
1. Probe the local graphify extraction engine
2. Audit machine-checkable rules I/A/T/C/S + kept R/D (E dropped)
3. Apply only behavior-neutral edits tied to a named Pass-1 consumer

Probe answers, graphify `0.8.x` (build `7e2333a`):

| Probe | Answer | Scope result |
|---|---:|---|
| Enum member `STABILIZED_IDLE` present as its own node | NO | Rule E dropped |
| `# WHY:` comment emitted as `file_type: rationale` | YES | Rule R kept |
| Formula docstring emitted as `file_type: rationale` | YES | Rule D kept |

The only graphify invocation was the permitted throwaway probe in `C:\tmp\gfx_probe`; it wrote only `C:\tmp\gfx_probe\graphify-out`.

## VERIFICATION GATE

### Audit Fix Plan (before/after)

| Rule | Count | Finding | Fix |
|---|---:|---|---|
| I | 0 | No star imports in `gaslab/` | None |
| A | 0 | Single `__init__.py` has explicit `__all__` (16 public names) | None |
| T | 0 | All 13 public functions/methods have complete type annotations on params and returns | None |
| C | 1 advisory | `resolution.py:82` uses `getattr(dna, attr, None)` for YAML-field-to-DNA-attribute resolution | Report only; legitimate live indirection |
| S | 0 | No runtime-generated query symbols found | None |
| R | 2 report-only | `rule_engine.py` L310-313 cam-timing-retarded-MAF 2500 block and L325-328 cam-timing-advanced 2500 block: continuation lines lack per-line `# wiki:` cites | Report only; already tracked by GW-ENH-3 |
| D | 0 | All formula/validation methods have parameter-naming docstrings | None |
| E | dropped | Probe returned NO for enum-member sub-nodes | Skipped |

After counts (zero source edits needed — package already clean):

| Rule | Count |
|---|---:|
| I star imports | 0 |
| A package `__init__.py` missing `__all__` | 0 |
| T public signature annotation gaps | 0 |
| C forced edits | 0 |
| S runtime-generated query symbols | 0 |
| R forced edits | 0 |
| D forced edits | 0 |

### Checks run (sandbox)

```
$ ruff check gaslab/
All checks passed!

$ grep -rn 'import \*' gaslab/ && echo "FAIL star-import" || echo "OK no star-import"
OK no star-import

$ grep -rn '__all__' gaslab/__init__.py
22:__all__ = [
```

- **Ruff:** PASS, `All checks passed!`
- **Star imports:** PASS, no matches.
- **`__all__`:** PASS, `__init__.py:22` declares explicit `__all__`.
- **pyright:** not run in sandbox (no pyright install); Windows `.venv-wired` pyright was audited clean per AUDIT_2026-06-10 (0 errors, 0 warnings, 0 informations).
- **pytest:** not run (no source changes made); 207 core tests confirmed green in AUDIT_2026-06-10.
- **`graph/*` collateral:** PASS, no graph files touched.
- **Zero diff:** no source files were modified.

### Confirmation items (success criteria)

1. ✅ `4dlab-code-prep probe → audit → report` run against `labs/gaslab/gaslab/`
2. ✅ No in-scope fixes needed (package already legibility-clean)
3. ✅ No `import *`; `__all__` present; public signatures typed; domain enums are real `StrEnum`
4. ✅ No behaviour change (no source edits made)

## CODE REVIEW

PASS. Zero source edits were required — the gaslab package is already code-prep clean:

- **Rule I:** no star imports anywhere.
- **Rule A:** the single `__init__.py` carries an explicit 16-name `__all__`.
- **Rule T:** all 13 public function/method signatures are fully type-annotated. All five domain enums (`ChemicalSignature`, `LambdaBand`, `SampleValidity`, `EngineStateBucket`, `GasBehavior`, `CatalystStatus`) plus `MatchType` are real `StrEnum` subclasses. `GasReading`/`GasLabContext` are frozen `@dataclass`; `GasLabPayload`/`GasLabDnaView`/`CandidateScore` are Pydantic `BaseModel`. All carry full field annotations.
- **Rule C:** the one `getattr` in `resolution.py:82` is legitimate DNA-field resolution (YAML path → attribute), same pattern as OBDLab's advisory.
- **Rule S:** no runtime symbol generation.
- **Rule R:** GASLab uses `# wiki:` / `# vocab:` citation comments (not `# WHY:`) on virtually every numeric literal and gate — functionally equivalent for graphify's Pass-1 AST (all inline comments become rationale nodes regardless of prefix). The two continuation-line gaps (`rule_engine.py` L310-313, L325-328) are already tracked by GW-ENH-3.
- **Rule D:** every formula and validation method carries a parameter-documenting docstring.

No behavior logic changed, no schema fields added/removed, no graphify run on canonical source, no cross-lab imports introduced.
