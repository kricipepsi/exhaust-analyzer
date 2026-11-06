# T-AUD-4o progress note

## Readiness
(a) Start matches: branch fix/T-AUD-4o, HEAD 54eace8 (spec commit, child of 680a90b), `git status --porcelain` empty; preconditions print `checked`.
(b) Rehearsed test file run from the recheck dir on the base: 3 failed, 1 passed (P3 base). The AppTest failure there is a path error from the recheck location; it is re-run in place after the copy.
(c) Expected value derived from the task: base `3 failed, 1 passed`, fix `4 passed`; ui 45 -> 49; wired 85.
(d) No contradiction or missing decision found.
(e) Deliverable: R1 (HIGH-only checkbox) and R2 (NARROWBAND override in basic mode) plus the 4-test file. Decisive check: the new file prints `4 passed` and f9_wideband.py shows a FULL_FUSION verdict both ways.

## Assumptions worked past
none

## VERIFICATION GATE
- step 1: new file `4 passed`; ui `49 passed`.
- step 2: wired `85 passed`.
- step 3: `upstream widget: [('Upstream O₂ (V)', 0.0, 1.0)]`, decode banner, two `use_decoded_dna` lines -> EF-004 mode=FULL_FUSION (no OBD_INPUT_INCOMPLETE).
- step 4: ruff `All checks passed!`; commits 54eace8 (spec), 3f7589e (fix); `git status --porcelain` lists only this note (RESULT added after).
- Mutants: M1 (app.py reverted) `1 failed, 3 passed`: test_partial_decode_is_basic_mode. M2 (ui_payload.py reverted) `2 failed, 2 passed`: test_basic_mode_pins_narrowband, test_partial_wideband_vin_runs_in_basic_mode. Both files restored; the new file is `4 passed` again.
- pyright, bandit: NOT RUN (the task does not require them).

## CODE REVIEW
Scope: only R1, R2 and the R3 file changed; the patch applied unchanged (9 insertions, 1 deletion). Contracts: no new payload field; `upstream_o2_type` is an existing override read by the composition. Tests use no network. No findings.

## Time
phase | start | end | minutes | context at end
implement and verify | 2026-11-06T09:25:27Z | 2026-11-06T09:26:39Z | 1 | ABSENT
