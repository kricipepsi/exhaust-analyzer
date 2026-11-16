# REVIEW T-GASA-19 — Euro idle CO to DVSA bands; CAM_MAP 2500 window (Windows Cowork, 2026-11-16)

**Verdict: ACCEPT, score 97.** Code row, difficulty 3, Hydrogen lane (high). The second-model review ran through
`second_review.py` (route Codex): **APPROVE, no actionable findings**
(`C:/4DApp/recheck/codex/T-GASA-19_review.md`; embedded spec, DVSA source rows, diff, called code and override test).

## Facts (Cowork re-ran, branch `fix/T-GASA-19`, after promote)
- Commits after `fix/T-AUD-24i`: `b5da88e` spec, lane work, `d50f23c` merge. Name-status: M `resolution.py`,
  `rule_engine.py`, `test_rule_engine.py`; A the note and the RESULT. No D, no R.
- `labs/gaslab/tests` `280 passed, 2 skipped, 4 deselected` (279 before); `labs/comlab/tests` `610 passed`;
  `labs/comlab/registry/tests` `510 passed, 5 skipped`; `hc_2500_ceiling`/`hc_ceiling` count `0`/`0`; ruff clean;
  `git status --porcelain` empty.
- The lane's code edits equal Cowork's rehearsal patch line for line (`recheck/T-GASA-FEURO/rehearsal.diff` vs
  `lane.diff`); only the test formatting differs. Before the change, (a), (c) and (d) fail.
- v7 corpus: 0 of 314 changed (221 by family). The corpus does not reach these paths (the liveness probe also moved
  0), so the unit tests carry the evidence.
- Source re-derived: S009 Table 1 (`sources/S009.md:437` 0.5 % for 1/8/95-31/8/02, `:438` 0.3 % from 1/9/02).
  The review prompt's excerpt stopped at `:437`; Codex flagged the missing `:438` row, and Cowork closed it from the file.

## Behaviour change (intended, R1)
NORMAL_OPERATION's default CO maximum (`rule_engine.py:146`) moves from 0.2 to 0.3 % for Euro 4/5 and unknown, and
from 4.5 to 0.5 % for Euro 1. Euro 2/3 are unchanged. The CAM_MAP 2500 rpm gate accepts HC up to 600 ppm on every
class, and its default CO floor is 1.5 % (it was 0.2-0.5 %).

## Register
`resync_register.py --register gaslab-code --base b5da88e --apply --drop-gone`: moved 83, changed 5, gone 0.
GK0049, GK0054, GK0056 re-valued (0.5, 0.3, 0.3); GK0078/79, GK0183/84 conditions updated; all `RESOLVED T-GASA-19`.
The Euro HC-ceiling claims GK0051, GK0053, GK0055, GK0057 are retired (the field was removed). GK0091/GK0094 are
not in this row and move to T-GASA-20. `CLAIMS OK group=gaslab`.

## Findings
- **L1 (Low, Cowork):** the T-AUD-23c ruling put GK0091/GK0094 under FEURO, but the T-GASA-19 spec left them out.
  They are now recorded on T-GASA-20. Score −2.
- **L2 (Low):** the new constants `_CAM_MAP_CO_FLOOR_2500`/`_CAM_MAP_HC_MAX_2500` have no register claim (a resync
  re-keys lines and does not extract new ones). Score −1.
