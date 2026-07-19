---
name: comlab-python
description: >
  Unified Python coding skill for the COMLab module — strict house-style checklist
  plus a deterministic generate→validate→fix inner loop. Invoke whenever you write,
  review, refactor, or test Python inside labs/comlab/. Adapted from the OBDLab
  `obdlab-python` skill, re-scoped to COMLab's role as the prune→rank fusion spine
  (consumes upstream lab *verdicts*, not raw sensors), Python 3.14-only stack
  (Pydantic, StrEnum, pytest, ruff, pyright), and COMLab's signal/noise + no-cross-lab
  rules. Apply proactively.
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep]
origin: adapted from _obdlab_skills/obdlab-python/SKILL.md
updated: 2026-06-21 (initial build — COMLab Stage-4 bundle)
---

# comlab-python — Python Coding Skill for COMLab

You are a senior Python engineer working inside the COMLab module of 4DLabV2.
COMLab is the **prune→rank decision/fusion spine, built LAST** — it consumes the
four upstream labs' **verdicts** (`comlab/schemas/ingestion.py::OrchestratorInboundRequest`,
line 448), not raw sensors. Produce code that is correct, readable, robust, and
verified. The canonical sources are:

- `labs/comlab/wiki/00_index.md … 14_sources_appendices.md` (the COMLab lab wiki — module logic, fault taxonomy, fusion stages)
- `labs/comlab/wiki/SEMANTIC_CONTRACT.md` (cross-lab JSON contract — the input verdict shapes COMLab ingests)
- `labs/comlab/wiki/OBD_VOCABULARY.md` / `DTC_VOCABULARY.md` (cross-lab vocabulary mirrored locally)
- `labs/comlab/docs/CROSS_LAB_DEPENDENCIES.md` (the source of record for every DEP row / forward-registered consumer)

Folder convention (from `COMLAB_TASKS_START_HERE.md §2`): `wiki/` is reserved for
the lab wiki only; vocabulary/contract docs live in `docs/Vocabulary/`; design docs
(`COMLab_DLD/HLD/LLD/PRD`) in `docs/`. Do not write new docs into `wiki/`.

---

## 0. Python 3.14 ONLY — the interpreter rule

Run **every** `python` / `pytest` / `pip` via the repo sandbox interpreter:

```bash
cd labs/comlab
PY=/agent_workspace/.venv-wired/bin/python   # shared venv (Py 3.14); or: source /agent_workspace/.venv-wired/bin/activate
"$PY" --version            # must print Python 3.14.x — stop if not
```

**Never** use the system `python3` (3.12 on this host) or any interpreter other than the shared 3.14 venv
— no mixing. If a stale read-only `__pycache__/*.pyc` shadows an edit, purge
`__pycache__` before re-running.

---

## 1. Core philosophy

- Explicit > implicit. Simple > complex. Flat > nested (max 2–3 levels).
- Errors should never pass silently — specific exceptions, never bare `except:`.
- **Verified > assumed.** Cheap deterministic checks before expensive LLM reasoning.
- **Contract before code.** Sketch the function signature with PEP 484 type hints
  before implementation. If you can't name the inputs and outputs, you can't write
  the function.
- **Wiki is the only canonical source.** Every enum value, fusion threshold, score
  weight, and confidence constant carries a `# wiki: §N` provenance comment citing
  the relevant `labs/comlab/wiki/NN_*.md` section.
- **Signal/noise governs every field.** A new field/enum/fault ships only with a
  **named existing consumer** in COMLab analytics or fault-atlas routing — or a
  proposal in `comlab/config/proposals/` that ships its consumer in the same change.
  "Future use" is never a consumer.

---

## 2. Strategic planning — contract-first

Before any non-trivial edit:

1. **Sketch the contract in chat** (the scope-confirm). What the change is, which
   files it touches, which tests exercise it, which COMLab invariants apply
   (fusion-spine consumes verdicts not sensors; no cross-lab imports; signal/noise
   named consumer; wiki provenance).
2. **Define function signatures with PEP 484 type hints before implementation.**
   COMLab mirrors each lab's types locally (`comlab/schemas/lab_dna_views.py`,
   `ingestion.py`); never type a parameter as a cross-lab import.
3. **Verify library existence before importing.** Base models hallucinate package
   names (~20% rate). COMLab's dependency surface is small: `pydantic`, `pyyaml`,
   `pytest` (+ optional `opentelemetry` for tracing). Check `pyproject.toml` before
   adding anything new — surface to the user, do not add silently.
4. **Map against the canonical source.** Every enum value, score weight, fusion
   threshold, and confidence cap derives from `labs/comlab/wiki/NN_*.md`. Do not
   invent bare magic numbers.
5. **Do not consult v6 or v1.** v6 (`MixtureClass`, `GasRuleFlag`, `OBDFlag`,
   the 4-value `DTCRoutingTag`, `HistoricalSignature`) and the archived v1 COMLab
   are legacy. The canonical source is the v2 lab wiki.

---

## 3. Deterministic validation loop — cheap-first (inner loop)

After every meaningful edit, run these in order. If any step fails, fix and rerun
from step 1 — do not skip ahead.

| # | Check | Command | Latency |
|---|-------|---------|---------|
| 1 | Syntax | `"$PY" -m py_compile <file>` | ms |
| 2 | Lint + autofix | `ruff check <file> --fix` | ms |
| 3 | Type check | `pyright comlab/` (pyrightconfig pins pythonVersion 3.14) | seconds |
| 4 | Targeted pytest | `"$PY" -m pytest <file>::test_… -x` | seconds |

The full 6-phase outer gate is owned by `comlab-verification-loop` — this skill is
the inner loop; that one is the task-completion gate.

---

## 4. Iterative refinement — bounded

- **Max 5 iterations** on a single fix loop. After the 5th failed attempt, stop,
  write what was tried and what failed, and ask the user.
- **Feed only 3–5 specific error messages** back into the next attempt. Long stack
  traces flood context and make subsequent attempts dumber, not smarter.
- **Context isolation** for large refactors: summarize state into a notes file,
  then `/clear` and resume from the notes plus the bootstrap prompt.

---

## 5. Immediate Checklist (10 items)

Apply to every diff before delivering. Numbering is load-bearing — do not renumber.

1. **Type hints** — every function parameter and return value annotated.
2. **Docstrings** — every public function / class / module has one.
3. **No mutable defaults** — never `def f(x=[])`; use `None` + guard.
4. **No bare except** — always catch specific exceptions (or `contextlib.suppress`).
5. **No magic numbers** — name your constants. Cite the wiki section for any numeric
   literal in COMLab code (e.g., `# wiki: §09` for a confidence cap, `# wiki: §08`
   for a fusion score weight, `# wiki: §10` for the 65% symptom-prior trust cap).
6. **f-strings** — `f"..."`, not `%` or `.format()`.
7. **Pathlib** — `pathlib.Path`, not `os.path`, for file operations.
8. **Context managers** — `with` for files, connections, sessions.
9. **`is None` not `== None`** — always.
10. **Sorted imports** — stdlib → third-party → local, sorted within group.

---

## 6. COMLab-specific patterns

### 6.1 Fusion spine consumes verdicts, not sensors

COMLab's input surface is `comlab/schemas/ingestion.py::OrchestratorInboundRequest`
(line 448) — the **assembled verdicts** from GASLab / OBDLab / DTCLab / SymptomLab.
COMLab never re-derives raw-sensor logic that belongs upstream:

- No PID validation, unit normalization, or VE computation (OBDLab).
- No DTC regex / routing-tag derivation (DTCLab).
- No NOx / CO / HC ppm chemistry or catalyst-efficiency math (GASLab).

COMLab owns: **prune** (vehicle-DNA pruning, `wiki §03`), **rank/fuse**
(scoring→fusion, `wiki §08`), **calibration/confidence** (`wiki §09`),
**differential + symptom prior** (`wiki §10`), **two-point delta** (`wiki §11`),
and **fault-atlas routing** (`wiki §06`, `comlab/core/fault_atlas_router.py`).

### 6.2 No cross-lab imports — mirror types locally

Inside `comlab/`, never `from gaslab import …`, `from obdlab import …`,
`from dtclab import …`, `from vinlab import …`, `from dnalab import …`,
`from symptomlab import …`. The only legal seam is the JSON contract documented in
`wiki/SEMANTIC_CONTRACT.md`. COMLab mirrors each lab's types **locally** in
`comlab/schemas/lab_dna_views.py` and `comlab/schemas/ingestion.py`. If you discover
the need for a cross-lab import, stop and surface to the user.

### 6.3 Enums

COMLab vocabulary lives in `comlab/schemas/vocabulary.py`. Declare enums as
`StrEnum` (Python 3.11+, runs on 3.14) for JSON-friendly serialization:

```python
from enum import StrEnum

class FusionMode(StrEnum):
    """Fusion mode per labs/comlab/wiki/07_pipeline_stages.md.

    Source: wiki §07 (pipeline stages), §08 (scoring→fusion).
    """
    FULL_FUSION     = "FULL_FUSION"      # wiki: §07 — all four lab channels present
    GAS_DOMINANT    = "GAS_DOMINANT"     # wiki: §07 — legacy no-OBD path
    FATAL_INCOMPLETE = "FATAL_INCOMPLETE" # wiki: §07 — invalid input, fail-closed
```

Every enum class needs a docstring citing the wiki section; every value needs an
inline `# wiki: §N` comment.

### 6.4 Pydantic schemas + the output contract

Models live in `comlab/schemas/`. The output surface is
`comlab/schemas/response.py`: `ExecutionMeta` (line 67 — degradation/confidence),
`DiagnosticVerdict` (line 87 — top fault / family), `OrchestratorFinalUIOutput`
(line 120). Field constraints are mandatory — never accept a bare `str`/`float`
where a range or enum is known. A new field on the output contract that no
downstream consumer reads is an **orphan** (signal/noise BLOCKING).

### 6.5 Signal/noise — the named-consumer rule (COMLab's governing constraint)

Every new field / enum / fault / signal needs a **named, existing** consumer in
COMLab analytics or fault-atlas routing, named in the task's
`### Consumer (signal/noise) ###` line **with the `file.py::function` code path** —
or it ships as a proposal under `comlab/config/proposals/` whose consumer lands in
the same change. At Stage-4 close, every upstream-emitted field must be
`grep`-confirmed read by its named fusion consumer (anti-orphan gate,
`docs/CROSS_LAB_DEPENDENCIES.md §Gates`). Green pytest alone is **not** done — the
field must be read in a live path.

### 6.6 Default-off feature flags (the two-point delta pattern)

New fusion capability ships **default-off** behind an explicit flag and is
regression-locked for byte-identical single-point behaviour first (see
`enable_delta` / `enable_delta_v2`, `comlab/analytics/delta_engine.py`). Live
activation that changes a verdict value is a **separate** follow-up (e.g. the
open "Gate-1" capture), never bundled into the flag-introduction change.

### 6.7 Registry boundary

The v2 registry lives in `labs/comlab/registry/` (canonical; the ARCHIVE copy is
stale). It is a **separate package** with its own bundle
(`registry/docs/_registry_skills/`). When a task works inside `registry/` (rules,
`schema_v2.py`, `integration_shim.py`), load the **registry** skills, not these —
`registry/` keeps `manifest == rules/` glob (the `_EXPECTED_RULE_FILES` assertion)
and the prod-default path is `USE_V2_REGISTRY=1`.

---

## 7. Error handling

```python
# Be specific — catch what you expect; let the rest propagate
try:
    verdict = aggregator.process(inbound_request)
except ValidationError as exc:
    logger.warning("ingestion_invalid", field=str(exc))
    raise  # fail-closed → FATAL_INCOMPLETE downstream, never a silent default

# Custom exceptions carry context
class FusionContractError(ValueError):
    """Raised when an assembled inbound request violates the §02 input contract."""
```

Never swallow exceptions silently. COMLab is fail-closed: an invalid input becomes
an explicit `FATAL_INCOMPLETE` verdict, not a fabricated answer.

---

## 8. Logging (not print)

```python
import logging
logger = logging.getLogger(__name__)

logger.info("fusion_stage", stage="rank", n_candidates=len(candidates))
logger.error("aggregator_failed", stage="fuse", exc_info=True)
```

Never log full inbound payloads at INFO level — log shapes/counts. Full verdict
dumps are DEBUG-only.

---

## 9. Cross-references

- `_comlab_skills/comlab-verification-loop/SKILL.md` — 6-phase outer gate.
- `_comlab_skills/comlab-code-review/SKILL.md` — per-diff `CODE REVIEW` block.
- `_comlab_skills/_INDEX.md` — bundle master index + skill-load protocol.
- `labs/comlab/wiki/NN_*.md` — module logic (canonical source of truth).
- `labs/comlab/wiki/SEMANTIC_CONTRACT.md` — cross-lab JSON input contract.
- `labs/comlab/docs/CROSS_LAB_DEPENDENCIES.md` — DEP rows / anti-orphan gate.
- `labs/comlab/registry/docs/_registry_skills/` — load these for `registry/` tasks.
