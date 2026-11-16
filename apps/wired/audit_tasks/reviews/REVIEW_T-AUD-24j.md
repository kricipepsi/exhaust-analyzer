# REVIEW T-AUD-24j — LC-002 MAP gate and NORMAL HC gates (Windows Cowork, 2026-11-16)

**Verdict: ACCEPT, score 99.** Code row; Hydrogen lane (medium), so the second-model review ran through
`second_review.py` (route Codex): **APPROVE, no findings** (`C:/4DApp/recheck/codex/T-AUD-24j_review.md`; embedded
spec, diff, rule descriptions, VL-001 gate, source verdicts).

## Facts (Cowork re-ran, branch `fix/T-AUD-24j`, after promote)
- Commits after `fix/T-AUD-23d`: `53717b5` spec, lane work, `5214395` merge. Name-status: M the three rule files and
  `test_t_coma_28_sink_chemistry_gate.py`; A the note and the RESULT. No D, no R.
- The lane diff equals Cowork's rehearsal except for one wrapped line in the test (`recheck/T-AUD-24j/`).
- `labs/comlab/tests` `611 passed` (610 + 1: one test became two parametrized cases); `labs/comlab/registry/tests`
  `510 passed, 5 skipped`; step 3 `24j OK (('gt', 50.0), 50.0, 50.0)`; `git status --porcelain` empty.
- v7 corpus after promote: 10 changed, all LC-002 → LC-001; family 221 → 221; code (`expected_fault_code`)
  117 → 126 (`recheck/T-AUD-24j/score.py`).

## Register
`resync_register.py --register comlab-code --base 53717b5 --apply --drop-gone`: moved 0, changed 3, gone 0.
CK0445 `> 50.0`, CK0352 `< 50.0`, CK0524 `< 50.0`, each with `RESOLVED T-AUD-24j`. `CLAIMS OK group=comlab`.

## Findings
- **L1 (Low):** Codex notes that a MAP above 50 kPa is shared by vacuum leaks and retarded timing, so it is supporting
  evidence only. That is the SUGGESTIVE tier's meaning; no change. Score −1.
