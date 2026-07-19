---
name: registry-python
description: >
  Unified Python coding skill for the 4DLab registry workstream — strict
  house-style checklist plus a deterministic generate→validate→fix inner
  loop. Load at every session start when working inside
  labs/comlab/registry/ (repo root /agent_workspace). Scoped to a rules-as-data
  module (Python 3.14, JSON rule files, Pydantic v2 for schema validation,
  pytest, ruff, pyright). The registry is self-contained: it produces rule
  data + tiny tooling, and never imports from any lab, COMLab, or 4DLabWired.
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep]
---

# registry-python — Python Coding Skill for the 4DLab Registry

Senior Python engineer, 4DLab registry workstream. Produce rule data +
minimal tooling that is correct, traceable to test cases, and verified.
The registry is **rules-as-data first** — the vast majority of artefacts
are JSON / Markdown / CSV. Python only appears where it is genuinely
needed: a schema definition (Pydantic), a loader, a validator, an
integration shim.

---

## 1. Core philosophy

- Explicit > implicit. Simple > complex. Flat > nested.
- Errors must never pass silently — specific exceptions, never bare `except:`.
- **Contract before code.** Sketch the function signature with PEP 484 type
  hints before implementation.
- **Verified > assumed.** Run the inner loop after every meaningful edit.
- **Rules-as-data first.** A rule is a JSON record, not Python. Python
  appears in the registry only for schema definitions, loaders, validators,
  and the small integration shim that hands rule data to COMLab.
- **Every rule traces to a case.** Every rule in `/registry/rules/` must
  carry a `passes_cases:` field naming the curated CSV case IDs it must
  PASS. A rule with no named case is dead code and fails review.
- **Every threshold carries a wiki citation.** Numeric literals in rule
  fields (and in any Python validator) carry an inline comment of the form
  `// wiki: <FILE> §<n>` in JSON or `# wiki: <FILE> §<n>` in Python. No
  bare magic numbers.
- **No cross-module imports.** The registry tooling never imports from
  `gaslab`, `obdlab`, `dtclab`, `dnalab`, `comlab`, or `4DLabWired`. The
  registry is the data; COMLab is the consumer. The direction is one-way:
  COMLab reads registry artefacts at integration time.

---

## 2. Strategic planning — contract-first

Before any non-trivial edit:

1. **Sketch the contract in chat.** What changes, which files, which tests.
   For a rule file: which case IDs the new/changed rule must PASS, and
   the evidence tier (definitive / suggestive / gating) it sits in.
2. **Define function signatures with PEP 484 type hints before
   implementation.**
3. **Verify library existence before importing.** Registry dependency
   surface: `pydantic>=2.0`, `pytest`, plus stdlib (`json`, `csv`,
   `pathlib`). Anything else, surface to the user — do not add silently.
4. **The import-direction rule (non-negotiable).** The registry imports
   only its own modules + stdlib + Pydantic. **No imports from any lab,
   from COMLab, or from 4DLabWired.** Before writing any `import`,
   confirm this direction.

---

## 3. Inner loop — after every meaningful edit

### For Python files

Run in this exact order. If any step fails, fix and restart from step 1.

| # | Check | Command | Pass condition |
|---|---|---|---|
| 1 | Syntax | `python3.14 -m py_compile <file>` | Exit 0 |
| 2 | Lint + autofix | `ruff check <file> --fix` | Exit 0 after fix |
| 3 | Type check | `pyright <file>` | 0 errors |
| 4 | Targeted test | `pytest <test_file>::<test_name> -x -q` | Green |

### For JSON rule files

| # | Check | Command | Pass condition |
|---|---|---|---|
| 1 | Syntax | `python3.14 -c "import json; json.load(open('<file>'))"` | Exit 0 |
| 2 | Schema validation | (once v2 schema exists) `python3.14 -m registry.validate <file>` | Exit 0 |
| 3 | Case ID resolution | `python3.14 -m registry.resolve_cases <file>` | Every `passes_cases:` entry resolves to a row in `corpus_curated.csv` |

Run from the repo root `/agent_workspace` via the shared `.venv-wired`
(Python 3.14) — invoke `python3.14` explicitly (system default is 3.12). The
registry workstream shares the wired venv; no separate environment is created.
The full 6-phase outer gate is owned by `registry-verification-loop`.

---

## 4. Immediate checklist — apply to every diff

Before marking any edit done, verify:

- [ ] Every rule file edited has a `passes_cases:` list naming curated case IDs
- [ ] Every numeric threshold in a rule carries a `// wiki: <FILE> §<n>` comment
- [ ] No imports from any lab (`gaslab`, `obdlab`, `dtclab`, `dnalab`)
- [ ] No imports from `comlab`
- [ ] No imports from `4DLabWired`
- [ ] No imports from `ARCHIVE/`, `ARCHIVECOMLab/`, `v2/`, or `v6/`
- [ ] No invented enum values — chemistry states, fault families, DTC routing
      tags, evidence tiers all match the v2 schema vocabulary
- [ ] No bare `except:` — specific exception types only
- [ ] Python 3.14 only — no `sys.version` guards
- [ ] Inner loop ran clean after this edit

---

## 5. Iterative refinement — bounded

- **Max 5 iterations** on a single fix loop. After the 5th failed attempt,
  stop, write what was tried and what failed, ask the user.
- **No speculative abstractions.** Write the minimum that makes the task's
  `### Success criteria ###` green. Off-scope discoveries go to the
  `Unplanned follow-ups` table in `REGISTRY_PROGRESS.md`, not the diff.

---

## 6. File-path conventions

```
/agent_workspace/                       ← repo root; run commands from here
├── .venv-wired/                        ← shared Python 3.14 venv
└── labs/comlab/registry/               ← this workstream
    ├── schema_v2.py                    ← Pydantic model for v2 rules
    ├── corpus_curated.csv              ← produced by AUDIT-CORPUS
    ├── corpus_meta.json                ← produced by AUDIT-CORPUS
    ├── integration_shim.py             ← hands rule data to COMLab
    ├── rules/                          ← v2 rule data, one file per fault family
    │   ├── lean_condition.json
    │   ├── rich_mixture.json
    │   └── ...
    ├── tests/                          ← Python tests for loader / validator / shim
    └── docs/                           ← workstream docs (off the package root)
        ├── _registry_skills/           ← this bundle
        ├── REGISTRY_START_HERE.md
        ├── REGISTRY_PROGRESS.md
        ├── registry_tasks/
        │   └── progress_notes/         ← VERIFICATION GATE + CODE REVIEW blocks
        ├── cvsgaps.md                  ← corpus-curation driver (input)
        ├── CORPUS_AUDIT.md             ← produced by AUDIT-CORPUS
        ├── REGISTRY_AUDIT.md           ← produced by AUDIT-REG
        ├── CHEMISTRY_COVERAGE.md       ← produced by AUDIT-CHEM
        └── SCHEMA_V2_SPEC.md           ← produced by REG-V2-SCHEMA
```

Test discovery: `python3.14 -m pytest labs/comlab/registry/tests/ -x -q` from the repo root.

---

## 7. Python environment

Registry shares **`.venv-wired`** (Python 3.14) with the wired app — no
separate environment. Invoke explicitly from the repo root (no activation
needed):

```bash
cd /agent_workspace
.venv-wired/bin/python3.14 -m pytest labs/comlab/registry/tests/ -x -q
```

The labs and COMLab are installed editable in this venv, but the registry
tooling does **not** import them.

---

## Cross-references

- `registry-verification-loop` — the 6-phase outer gate that owns task completion
- `registry-code-review` — the per-diff CODE REVIEW block
- `REGISTRY_START_HERE.md` — session bootstrap
- `_skills/coding-bootstrap/reference/code-quality-principles.md` — Karpathy 4
