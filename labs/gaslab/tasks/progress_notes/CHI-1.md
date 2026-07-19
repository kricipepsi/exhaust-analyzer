# CHI-1 — Wire `co_high_idle` to its consumer — progress note

## Plan (as executed)

**Goal:** Give the orphan DNA field `co_high_idle` (defined `gaslab/dna_view.py:39`,
read in 0 code paths) a live consumer in `gaslab/resolution.py`, closing the
T-GV2-4 orphan so T-GV2-4 can reach a legitimate `done`.

**Decision locked (owner, 2026-06-04): Option 1 — wire, single branch.**
The v2 wiki (`GAS_VOCABULARY §11`, table L431) maps `co_high_idle` to exactly one
value: `mild_rich.max` (default **1.5 %CO** at 2500 RPM, `GAS_VOCABULARY §10.2`
L336). In `resolution.py` that literal `1.5` appears as the rich-CO **lower bound**
of the CAM_TIMING_RETARDED_MAP window only (`1.5 <= reading_high.co <= 4.5`). The
catalyst-dead branch's `co > 0.5` is `mild_rich.min` (a floor) — **not** the
ceiling the wiki names, so it is left untouched (overriding it would be a
provenance mismatch). Citation target corrected to `§11`/`§10.2` (the prompt's
"L425/L431" pointed at the same §11 override table; the precise anchors are §11
for the gate and §10.2 for the default value).

**Mapping:**
`co_high_idle` → `resolution._rich_co_ceiling(dna)` → the rich-CO lower bound in
the CAM_TIMING_RETARDED_MAP branch. Override applies only when
`dna.confidence == "HIGH"` and `dna.co_high_idle is not None` (`GAS_VOCABULARY §11`);
literal `1.5` is the fallback (`GAS_VOCABULARY §10.2`).

**Files touched:**
- `gaslab/resolution.py` — added `_rich_co_ceiling(dna)` helper; replaced the
  literal `1.5` lower bound in the CAM_TIMING_RETARDED_MAP branch with the helper.
- `tests/test_resolution.py` — added the two contracted tests + a `_cam_map_high`
  builder.

**Out of scope (untouched, as contracted):** no new schema field; `dna_view.py`,
`reading_high` plumbing, lean/CAM lambda checks, catalyst-dead `0.5` floor, and
the wired mapper all unchanged. Literal *values* unchanged — only made overridable.

**TDD:** wrote both tests first.
- `test_co_high_idle_overrides_literal_when_high_conf` — RED first
  (`co=1.8` survived under the literal 1.5), GREEN after wiring (per-vehicle
  ceiling 2.0 → `co=1.8` dropped, `co=2.2` kept). Proves the per-vehicle value,
  not the literal, is the active bound.
- `test_co_high_idle_falls_back_to_literal` — GREEN throughout (regression guard:
  `co_high_idle=None` and `confidence != HIGH` both keep the literal-1.5 path,
  `co=1.8` survives — byte-identical to pre-CHI-1).

Lambda hand-verified in-window for both CO variants (HC_FACTOR=0.0025): co=1.8 →
λ≈0.886, co=2.2 → λ≈0.876, both ∈ [0.85, 0.95]; o2/hc/nox bounds also satisfied,
so CO is the sole deciding variable.

---

VERIFICATION GATE — CHI-1
Phase 1 (syntax):       PASS — python -m compileall gaslab/ (exit 0)
Phase 2 (type check):   PASS — pyright gaslab/ (0 errors, 0 warnings, 0 informations)
Phase 3 (lint):         PASS — ruff check gaslab/ tests/ (All checks passed)
Phase 4 (unit tests):   PASS — pytest tests/ (173 passed, 0 failed; was 171 → +2 new)
Phase 5 (provenance):   PASS — every changed literal cited: 1.5 → vocab §10.2 (mild_rich.max),
                        4.5 → vocab §10.2, override gate → vocab §11. No uncited literal.
Phase 6 (diff review):  PASS — 2 files (resolution.py helper+CAM branch; test_resolution.py
                        +2 tests). Every line traces to the CHI-1 deliverable.

Notes: pyright emits a version-update WARNING (1.1.409→1.1.410) on stdout; not a
type finding — error/warning/information counts are all 0. Inner loop and gate run
via Windows PowerShell + `.venv-wired` (Python 3.14.5): the bash sandbox mount this
session exposed only `4DLab/{.sandbox-py,diag,DTCLabSimple}` — `GASLab/` was not
mounted, so per workspace CLAUDE.md the Windows path was used.

---

CODE REVIEW — CHI-1
1. Design rule compliance:  PASS — petrol/5-gas/warm unaffected; no cross-lab/v2/v6/ARCHIVE
   imports; consumer reads the locally-declared `GasLabDnaView`. Override matches
   GAS_VOCABULARY §11 (HIGH-confidence gate) + §10.2 (default).
2. Scope compliance:        PASS — only the CAM_MAP rich-CO lower bound + helper changed;
   catalyst-dead 0.5 floor, dna_view.py, reading_high plumbing, wired mapper untouched.
3. Contract changes:        PASS — no contract changes. No enum/payload/DNA-view field added
   or altered; `co_high_idle` already existed (T-GV2-3), this only adds its reader.
4. Docstrings:              PASS — `_rich_co_ceiling` has a docstring naming §11/§10.2.
5. Provenance:              PASS — see Phase 5; gate + default + 4.5 ceiling all cited.
6. Immediate Checklist:     PASS — type hints, `is not None` (not `== None`), f-strings in
   asserts, no mutable defaults, no bare except, sorted imports unchanged.
7. Test coverage:           PASS — override path and both fallback sub-cases (None /
   non-HIGH) covered; CAM/catalyst T-GV2-4/5 tests stay green.

Both gates PASS — CHI-1 done; T-GV2-4 consumer obligation now met → flip to done.
