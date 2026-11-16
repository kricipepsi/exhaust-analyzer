# T-GASA-19 progress note — Euro idle CO to DVSA bands and CAM_MAP 2500 rpm window

## Readiness

- (a) Starting state matches task: branch `agy/T-GASA-19` (expected per lane rules; `git log fix/T-AUD-24i..HEAD` shows `b5da88e spec(T-GASA-19): Euro idle CO to DVSA bands; CAM_MAP 2500 window`), `git status --porcelain` empty, preconditions `checked` with no `MISSING`, `resolution.py:39-43` matches P1, `hc_2500_ceiling` counts are `resolution.py:2` and `rule_engine.py:1`, and baseline `labs/gaslab/tests` prints `279 passed, 2 skipped, 4 deselected` (P2).
- (b) Test fails for intended reason: on base code, R5(a) expects Euro-4 CO ceiling `0.3` (base has `0.2`), R5(c) expects `CAM_TIMING_RETARDED_MAP` 2500 rpm HC window `<= 600` independent of Euro class (base uses `hc_2500_ceiling`: `1200` for Euro 2, `200` for Euro 4), and R5(d) expects DVSA bands `{1: 0.5, 2: 0.5, 3: 0.3, 4: 0.3, 5: 0.3}` and unknown `0.3` (base has `{1: 4.5, 2: 0.5, 3: 0.3, 4: 0.2, 5: 0.2}`). Verified in red-gate run before R1–R4.
- (c) Independently derived decisive expected value compared with test: per DVSA S009 Table 1 (natural idle CO: `0.5 %` for 1/8/95–31/8/02 mapped to Euro 1–2, `0.3 %` from 1/9/02 mapped to Euro 3–5 and unknown fallback) and `GASWIKI-06B §FAULT_CAM_TIMING_RETARDED_MAP` (2500 rpm: `CO 1.5–4.5 %`, `HC 200–600 ppm`), R5(a)/(d) assert `0.3` / `{1: 0.5, 2: 0.5, 3: 0.3, 4: 0.3, 5: 0.3}` and R5(c) asserts `hc=500` survives and `hc=800` drops for both Euro 2 and Euro 4 at `co=2.2`. This agrees with criteria 1–3.
- (d) No contradiction or missing decision prevents implementation: R1–R5 give exact text and line targets matching P1 and P4.
- (e) Teach-back: Update `_EURO_THRESHOLDS` to hold only the DVSA natural-idle CO bands (`0.5` for Euro 1–2, `0.3` for Euro 3–5) and decouple the `CAM_TIMING_RETARDED_MAP` 2500 rpm check (`resolution.py` and `rule_engine.py`) to use `_CAM_MAP_CO_FLOOR_2500 = 1.5` and `_CAM_MAP_HC_MAX_2500 = 600` instead of Euro legal limits. The decisive checks are `labs/gaslab/tests` printing `280 passed, 2 skipped, 4 deselected` with R1–R5, `labs/comlab/tests` and `labs/comlab/registry/tests` unchanged at P3, `hc_2500_ceiling`/`hc_ceiling` counts `0`/`0`, and ruff clean.

## Assumptions worked past

- Lane rules override the task header's branch name (`agy/T-GASA-19` instead of `fix/T-GASA-19`), forbid `git commit`/`git push`/`git switch`/`git checkout`, and skip the RESULT's git branch/log paste.
- `rule_engine.py:16` import line with `_CAM_MAP_HC_MAX_2500` added alphabetically exceeds 100 chars if single-line; formatted cleanly per ruff check while keeping alphabetical order (`_CAM_MAP_HC_MAX_2500` first).
- `_CAM_MAP_CO_FLOOR_2500` and `_CAM_MAP_HC_MAX_2500` are placed directly above `def _rich_co_ceiling` with two blank lines after the preceding function and two blank lines before `def _rich_co_ceiling` per PEP 8 / ruff.
- `test_cam_map_hc_window_2500_ignores_euro_class` loops over `("Euro 2", "Euro 4")` inside one test function rather than `@pytest.mark.parametrize` so the pytest total matches P2 (`280 passed, 2 skipped, 4 deselected`).
- `labs/comlab/registry/tests` modifies `labs/comlab/registry/docs/case_library.html` (CRLF); restored with `git restore labs/comlab/registry/docs/case_library.html` instead of `git checkout` per lane rules.

## VERIFICATION GATE

| step | command | expected | observed |
|---|---|---|---|
| 1 | `labs/gaslab/tests` (`$PY -m pytest -p no:cacheprovider -q`) | `280 passed, 2 skipped, 4 deselected` (P2 with R1–R5), `0 failed` | `280 passed, 2 skipped, 4 deselected in 11.16s` |
| 2 | `labs/comlab/tests` (`$PY -m pytest -p no:cacheprovider -q`) | `610 passed` (P3), `0 failed` | `610 passed in 11.41s` |
| 3 | `labs/comlab/registry/tests` + restore `case_library.html` | `510 passed, 5 skipped` (P3), `0 failed` | `510 passed, 5 skipped in 2.15s`; `case_library.html` restored |
| 4 | `hc_2500_ceiling` and `hc_ceiling` counts in `resolution.py`, `rule_engine.py` | `0` and `0` | `0` and `0` |
| 5 | `ruff check` on the three touched files + `git status --porcelain` | `All checks passed!`; only write scope | `All checks passed!`; `git status --porcelain` shows only the 3 modified files + progress note (and RESULT after creation) |

Additional inner-loop checks run before final verification: `py_compile` passed, `ruff check --select S` passed on `resolution.py` and `rule_engine.py`, `py -m pyright --pythonpath C:/4DApp/.venv/Scripts/python.exe` returned `0 errors, 0 warnings, 0 informations`, deployed-layout import (`from wired import diagnose`) printed `import ok`, and `audit/tools/isolation.py` printed `violations: 4` (baseline R0-2 only).

## CODE REVIEW

- **Scope:** Only the 3 files in `### Files to touch ###` were modified (`labs/gaslab/gaslab/resolution.py`, `labs/gaslab/gaslab/rule_engine.py`, `labs/gaslab/tests/unit/test_rule_engine.py`), plus this note and `RESULT_T-GASA-19.md`. Out-of-scope items (`_coc_adjust_normal_bounds` at `rule_engine.py:146`, `co_high_idle` override, `gas_lab_ontology.yaml`, `Vault/`, code-audit registers) were left untouched.
- **Contracts & Anti-orphan:** `_EURO_THRESHOLDS` holds only `co_idle_ceiling: float`; `_euro_thresholds` is read in `rule_engine.py:146` and `test_rule_engine.py`. `_CAM_MAP_CO_FLOOR_2500` is read by `_rich_co_ceiling` (`resolution.py:112`); `_CAM_MAP_HC_MAX_2500` is read in both `resolution.py:416` and `rule_engine.py:401`.
- **Provenance:** All numeric thresholds carry inline `# wiki:` / `# vocab:` citations (`DVSA S009 Table 1`, `GASWIKI-06B §FAULT_CAM_TIMING_RETARDED_MAP`, `GAS_VOCABULARY §10.2`/`§11`).
- **Boundaries & Craft:** No cross-lab imports added; `isolation.py` stays at the 4 baseline violations; ruff and pyright report 0 errors.

## Time

| phase | start (UTC) | end (UTC) | minutes | context at end |
|---|---|---|---|---|
| implement | 2026-11-16T09:05:54Z | 2026-11-16T09:09:48Z | 3.9 | ABSENT |

Computed via `datetime.fromisoformat` in Python from clock reads at First action and Verification completion. Stop rule 75 min: not reached.
