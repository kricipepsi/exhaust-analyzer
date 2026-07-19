# T-GV2-6a — Cam/Ignition Timing RPM-Differential Separation — progress note

**Date:** 2026-06-05
**Status:** done (both gates clean below)

## Plan

Replace the single-point 2500-RPM range checks for the `CAM_TIMING_*` family in
`apply_differentiators` (`GASLab/gaslab/resolution.py`) with the wiki's
idle→2500 RPM-differential discriminators, and add the ignition
`TIMING_OVER_ADVANCED` vs cam `CAM_TIMING_ADVANCED` separation:

- **CAM_TIMING_RETARDED_MAP** — retained only if rich idle (λ 0.75–0.88,
  O₂ ≤ 0.5) **and** partial normalisation toward 2500 (λ_high > λ_idle, CO
  falls, 2500 vector in window). Flat rich rejected (sensor/fuelling bias).
  CHI-1 `co_high_idle` override of the rich-CO lower bound preserved verbatim.
- **CAM_TIMING_RETARDED_MAF** — retained only if lean idle (λ 1.08–1.18,
  O₂ 2.0–4.5) **and** lean persists at 2500 (no normalisation). Normalising
  lean rejected (vacuum-leak behaviour).
- **CAM_TIMING_ADVANCED** — retained only if mild-lean rough idle (HC 250–600,
  λ 1.03–1.08) **and** NOₓ rises idle→2500 while HC/CO fall, 2500 vector in
  window.
- **TIMING_OVER_ADVANCED** (ignition) — appended when the idle is clean
  (05a idle vector, λ 1.01–1.04) and the only 2500 anomaly is a NOₓ spike
  (> 1200, λ 1.0–1.06, HC/CO near normal). Cam family requires the idle
  λ-offset, so a clean idle can never co-survive as cam.
- **TIMING_RETARDED** — no change needed: the wiki gives no idle→2500
  behavioural delta (HC high / NOₓ ≈ 0 at both speeds); the existing bound
  match already encodes that. No code conflict found.

The wiki gives ranges + direction-of-movement, not numeric deltas, so the
direction predicates are strict inequalities on the raw pair
(`lchem_high > lchem_idle`, `co_high < co_idle`, `nox_high > nox_idle`,
`hc_high < hc_idle`) — no invented δ thresholds (per the task's out-of-scope
rule).

**Scope amendment (architect, 2026-06-05, in-session):** the new idle-side
gates broke 3 CHI-1 fixture call-sites in `tests/test_resolution.py` (their
idle vector predated any idle gate). The architect amended the task file's
Files-to-touch to authorise an **idle-vector-only** fixture correction
(`_cam_map_idle()` = the wiki-conformant 06b rich-idle vector). The CHI-1
assertion contract — CO as the sole deciding variable for the `co_high_idle`
override — is unchanged; the idle gate was not weakened.

## Files changed

- `GASLab/gaslab/resolution.py` — timing block rewritten (idle+delta gates,
  TOA separation). +90/−25 lines.
- `GASLab/tests/test_rule_engine.py` — 6 contracted tests added (+124).
- `GASLab/tests/test_resolution.py` — CHI-1 idle fixture `_cam_map_idle()`
  (authorised amendment; idle vector only). +25/−5.

## Verification headline

- Targeted: `pytest tests/test_resolution.py tests/test_rule_engine.py` —
  60 passed.
- Full suite: `pytest tests/` — **179 passed** (173 baseline + 6 new), 0 failed.

```
VERIFICATION GATE — T-GV2-6a
Phase 1 (syntax):       PASS — python3.14 -m compileall gaslab/ (exit 0)
Phase 2 (type check):   PASS — pyright gaslab/ (0 errors, 0 warnings)
Phase 3 (lint):         PASS — ruff check gaslab/ tests/ (All checks passed)
Phase 4 (unit tests):   PASS — pytest tests/ (179 passed, 0 failed)
Phase 5 (provenance):   PASS — every numeric literal in the diff carries a
                        wiki/vocab citation (audit of added lines: only
                        comment/docstring lines uncited; tests exempt)
Phase 6 (diff review):  PASS — 3 files changed, all map to Deliverables
                        (test_resolution.py per in-session architect
                        amendment); pre-existing uncommitted changes in the
                        repo left untouched per git ritual
```

```
CODE REVIEW — T-GV2-6a
1. Design rule compliance:  PASS — wikiNEW 06b/05a/§8.9 honoured; petrol/5-gas/
                            warm-only untouched; no cross-lab, v2/v6, or
                            ARCHIVE imports
2. Scope compliance:        PASS — every changed line traces to a Deliverable
                            or the authorised CHI-1 fixture amendment; no
                            drive-by edits
3. Contract changes:        PASS — no contract changes (no enum, no field;
                            GasLabPayload/GasLabDnaView untouched)
4. Docstrings:              PASS — new test functions and fixture helpers all
                            carry docstrings naming their wiki source;
                            apply_differentiators docstring unchanged (correct)
5. Provenance:              PASS — inline `# wiki: wikiNEW/06b §FAULT_…` /
                            `# wiki: wikiNEW/05a §…` / `# vocab: GAS_VOCABULARY
                            §10.1/§10.2/§11` on every literal and direction
                            predicate
6. Immediate Checklist:     PASS — type hints, f-strings n/a, no mutable
                            defaults, no bare except, `is None` style, sorted
                            imports (resolution import added to
                            test_rule_engine in stdlib→local order)
7. Test coverage:           PASS — all six contracted tests present and green;
                            flat-rich and normalising-lean negative cases
                            covered; CHI-1 override regression suite still
                            green
```

## Consumer-existence check (anti-orphan)

Task contract: **no new field or enum value** — the five timing
`ChemicalSignature` values (in the enum since T-GV2-1) route to COMLab
`chemical_state` / fault-atlas (GASWIKI-06B). Verified no new DNA field, no
enum change, no `ranking.py` change in the diff. `reading_high` (T-GV2-4) and
`co_high_idle` (CHI-1, read at `resolution.py` `_rich_co_ceiling`) remain
consumed in live paths. No orphan introduced.

## Notes

- `TIMING_OVER_ADVANCED` is *appended* by the differential (clean idle means
  bound-matching at idle cannot propose it; the 2500 NOₓ spike is the
  evidence). It then competes normally in `_candidate_rank`.
- Pyright warning: pyright-python wrapper notes v1.1.410 available (tooling
  noise, not a code warning).
