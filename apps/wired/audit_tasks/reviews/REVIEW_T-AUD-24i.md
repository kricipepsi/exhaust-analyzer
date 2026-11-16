# REVIEW T-AUD-24i — COMLab data to own vocabulary (Windows Cowork, 2026-11-16)

**Verdict: ACCEPT, score 99.** Code row; Hydrogen lane (medium), so the second-model review ran through
`second_review.py` (route Codex): **APPROVE, no findings** (`C:/4DApp/recheck/codex/T-AUD-24i_review.md`, embedded
prompt with the spec, the diff, the schema and shim operator code, and the three cited sources).

## Facts (Cowork re-ran, branch `fix/T-AUD-24i`, after promote)
- Commits after `fix/T-AUD-24h`: `9b79bcb` spec, lane work, `a25bcc3` merge. Name-status: M on the four files of
  Files to touch, A the note and the RESULT. No D, no R.
- `labs/comlab/tests` `610 passed`; `labs/comlab/registry/tests` `510 passed, 5 skipped` (equal to base; base +
  R1-R3 without R4 fails 1). Step 3: `24i OK (('ge', 108.0), '2.5', True)`. `git status --porcelain` empty.
- v7 corpus after promote: 0 of 314 changed, 221 correct by family (`recheck/T-AUD-24i/promoted.json`).
- Diff: OV-001 `gt 110.0` → `ge 108.0`; `_FLATCAM_ELEV_O2_MIN` `2.0` → `2.5` (comment kept); LC-001 text
  `> 1.03` → `>= 1.05`; `test_ov001_ect_definitive_108` asserts `ge`/`108.0`. OV-002/003/004 unchanged.
- Note: readiness (a)-(e), VERIFICATION GATE, CODE REVIEW, `## Time`.

## Register
`resync_register.py --register comlab-code --base 9b79bcb --apply --drop-gone`: moved 0, changed 3, gone 0.
CK0012 `≥ 2.5`, CK0440 `≥ 1.05`, CK0592 `≥ 108.0`, each with suspect `RESOLVED T-AUD-24i`. `CLAIMS OK group=comlab`.

## Findings
- **L1 (Low):** note (b) predicts the old test's failure instead of running it; Cowork's rehearsal ran it (1 failed).
  Score −1.
