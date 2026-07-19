# OBDLab audit — Lens 1/5: `pythonskill` (python-expert-coder)

**Date:** 2026-06-08 · **Auditor role:** architect (read + report; no code edits) ·
**Skill:** `_skills/codingskills/pythonskill` (PEP 8, type hints, ruff/pyright/bandit
validation loop, modern 3.11+ patterns, no library hallucinations).
**Subject:** `4DLabV2/labs/obdlab/obdlab/` (18 modules, ~2,119 LOC) + ingested tests.

> **Why this audit exists.** No coding skill was loaded before the OBDLab coder ran
> its tasks (owner observation). This is a retroactive skills-gate: the code is run
> back through each of the five `codingskills` lenses, one report per skill.

## Method caveat — sandbox static analysis was unreliable, and not used

`ruff`/`pyright` were attempted in the Linux sandbox but the sandbox mount holds a
**partially-synced (truncated) mirror** of several source files
(`payload.py` cut to 95 lines mid-token `o2_failure_`; `vocabulary.py`, `pid_ingestion_validator.py`,
`semantic_consistency_checker.py`, `sensor_signal_translator.py`, `analytics_preconditions.py`
all shorter than the real files). The real files — confirmed via the editor/Windows
view and consistent with every test, docstring, and the KG — are intact. **The ruff run
was therefore discarded** (its "16 errors" were truncation artifacts, e.g. `F401 unused
import`, `F821 o2_failure_`). All findings below come from reading the real source.

**Action for the coder:** run the inner loop in `.venv-wired` on Windows (the canonical
files), not in the sandbox. Treat the items below as candidates to confirm there.

## Disposition

Findings carry severity (🔴 high / 🟡 important / 🟢 nit). Fixes are routed to draft
task specs at the bottom (architect deliverable) and to the shared **Unplanned
follow-ups** table in `AUDIT_03_code-review.md`. No code was changed.

---

## Findings — pythonskill lens

### 🟡 P-1 Ruff ruleset is thinner than the skill prescribes
`pyproject.toml` selects `["E","F","I","N","W","UP"]` and `pyright` is `typeCheckingMode = "basic"`.
The pythonskill protocol prescribes a **security gate (bandit / `S` rules)** and
**bugbear (`B`)**, plus stricter typing. Concretely, the current ruleset will **not**
catch the exception-chaining and mutable-pattern items below. This is the single
highest-leverage pythonskill gap: the gate the coder (would have) run is weaker than
the skill's "generate–validate–fix" loop assumes.

| Missing | Rule | What it would catch in OBDLab |
|---|---|---|
| Bugbear | `B904` | `raise PIDValidationError(...)` inside `except` without `from` (see P-2) |
| Security | bandit / `S` | none critical found, but the gate is absent (e.g. `yaml.safe_load` is correctly used — `S506` would confirm) |
| Simplify | `SIM`, `TRY` | the no-op `try/except` in `semantic_consistency_checker.py` (see `AUDIT_03` CR-3) |

### 🟡 P-2 Exception chaining lost (`raise ... from`)
`core/pid_ingestion_validator.py` raises `PIDValidationError` **inside** `except
(ValueError, TypeError)` blocks without `from`, swallowing the original cause:

- `_validate_ltft_cell_vector` — L83 (`int(cell)` failure) and L90 (`float(ltft)` failure)
- `_validate_per_cylinder_misfire_counts` — L131 (`int(cyl)`) and L139 (`int(count)`)

Per pythonskill (PEP 3134 / `B904`): `raise PIDValidationError(...) from None` (intentional
suppression) or `from exc` (preserve cause). Currently the traceback shows a confusing
chained `ValueError` "During handling of the above exception".

### 🟢 P-3 Cross-module duplicated module constants
`_ECT_WARM_THRESHOLD = 70` and `_WOT_THROTTLE_THRESHOLD = 90` are defined **identically**
in both `core/o2_normalizer.py` (L37, L40) and `core/analytics_preconditions.py` (L35, L38),
each with its own `# wiki: §9` citation. Two sources of truth for one threshold; they
will drift. (No cross-lab import rule is at stake — both are inside obdlab.)

### 🟢 P-4 Dead keyword parameter `total_trim`
`O2Normalizer.normalize(self, pids, dna_view=None, total_trim=None)` (L55-60) documents
`total_trim` as "accepted for translator compatibility", but the only caller —
`sensor_signal_translator.py` L147 — calls `self._o2_normalizer.normalize(sanitized, dna_view)`.
The parameter is never passed and never read. Speculative surface; pythonskill rule 2
("nothing speculative"). Remove it.

### 🟢 P-5 Import-time file I/O in `state_bucketing.py`
`core/state_bucketing.py` L23-24 opens and `yaml.safe_load`s `obd_translation_rules.yaml`
**at module import**. Import-time side effects (a) make the module impossible to import
if the YAML is missing/malformed — failing at collection time, not at a call the test can
target — and (b) are inconsistent with `PIDIngestionValidator`, which loads its JSON in
`__init__` (L36-39). pythonskill / modern-Python guidance: defer I/O behind a function or
a lazily-initialised loader.

### 🟢 P-6 Type-hint completeness is otherwise strong
Positive note (the skill rewards this): every public entry point is fully annotated with
modern 3.11+ unions (`float | None`, `tuple[...]`), Pydantic models carry `Field`
constraints, and enums are `StrEnum`. `from __future__ import annotations` is used where
needed (`ranking.py`, `family_map.py`). No library hallucinations — deps (`pydantic`,
`pyyaml`) are real and declared in `pyproject.toml`. The gaps above are localized, not
systemic.

---

## Draft task specs (pythonskill lens)

> Architect deliverable. IDs are provisional (`-AUDIT-` namespace) — slot into
> `tasks/PROGRESS.md` before a coder session. Signal/noise: none of these add schema
> fields, so the named-consumer rule does not bite; consumers named where a field is touched.

### T-OBDV2-AUDIT-PY-1 — Tighten the inner-loop ruleset (P-1)
- **Files:** `labs/obdlab/pyproject.toml`
- **Change:** add `"B"`, `"SIM"`, `"TRY"` to `[tool.ruff.lint].select`; raise `pyright`
  to `"standard"` (not full `strict` yet — scope creep). Add `bandit` to dev deps OR
  add ruff `"S"` rules.
- **Success:** `ruff check` and `pyright` (Windows `.venv-wired`) run clean on the real
  files after P-2/CR-3 are fixed; new rules produce zero residual errors.
- **Consumer:** the coder inner loop itself (verification-loop lens). No schema change.

### T-OBDV2-AUDIT-PY-2 — Restore exception chaining + remove dead param (P-2, P-4)
- **Files:** `core/pid_ingestion_validator.py` (4 sites), `core/o2_normalizer.py` (signature + docstring)
- **Change:** add `from exc` / `from None` to the four `raise` sites; drop `total_trim`
  from `O2Normalizer.normalize`.
- **Success:** `ruff --select B904` clean; `pytest -x -q` green (no caller passes `total_trim`).
- **Consumer:** n/a (behaviour-preserving). No schema change.

### T-OBDV2-AUDIT-PY-3 — Single-source the duplicated thresholds + defer YAML load (P-3, P-5)
- **Files:** `core/o2_normalizer.py`, `core/analytics_preconditions.py`, `core/state_bucketing.py`
- **Change:** hoist `_ECT_WARM_THRESHOLD` / `_WOT_THROTTLE_THRESHOLD` to one module
  (or a small `core/thresholds.py`) with the single wiki citation; wrap the YAML load
  in a `_load_rules()` called on first `compute_bucket`, not at import.
- **Success:** one definition per constant; importing `state_bucketing` with the YAML
  temporarily renamed raises only when `compute_bucket` is called, and a unit test asserts that.
- **Consumer:** n/a (internal). No schema change.
