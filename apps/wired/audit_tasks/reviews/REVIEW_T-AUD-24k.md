# REVIEW T-AUD-24k — SF perception-delta gates ±0.03 → ±0.05 (Windows Cowork, 2026-11-16)

**Verdict: ACCEPT, score 99.** Code row (rule data and a test). Hydrogen lane (medium), 2.0 min (lane `.exit`
11:32:04-11:34:06 CET). The second review came from a second model, `second_review.py` (ds-flash): APPROVE, no
findings (`C:/4DApp/recheck/codex/T-AUD-24k_review.md`; it cites the embedded diff lines and gates).

## Facts (Cowork re-ran, branch `fix/T-AUD-24k`, after promote)
- Commits after `fix/T-AUD-23e`: `5483dd6` spec, `897495f` lane work, `a6bb22e` merge. Name-status: M
  `sensor_fault.json` (12 lines), A `test_t_aud_24k_sf_perception_delta.py`, A note, A RESULT. No D, no R.
- The rule lines equal `recheck/T-AUD-24k/rehearsal.diff`. The test file is byte-identical to the R2 text.
- `labs/comlab/tests` 614 passed (611 before); `labs/comlab/registry/tests` 510 passed, 5 skipped; new test 3 passed
  (2 failed on base). `git status --porcelain` empty.
- Corpus on the promoted tree: changed 4, family 221 → 224, code 126 → 126, sensor_fault 37/16 → 33/16. The file is
  identical to the rehearsal variant `delta_05.json`.
- Register: `resync_register.py --register comlab-code --base fix/T-AUD-23e --apply` re-keyed the 12 changed lines;
  CK0626, 0630, 0644, 0645, 0649, 0650, 0654, 0655, 0661, 0662, 0667, 0668 are re-valued ±0.05 and marked
  `RESOLVED T-AUD-24k`; `check_code_claims.py --group comlab` CLAIMS OK (1421 candidates).

## Findings
- **L1 (Low, Cowork):** the R2 docstring names S016, S037, S038 and S040. Under the T-AUD-23e review M1 the delta
  evidence is PARTLY, so the docstring says more than the evidence does. Score −1. Not a correction: the docstring is
  a pointer to the sources.
