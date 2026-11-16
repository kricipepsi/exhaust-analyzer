# REVIEW T-AUD-24h — upstream-O2 tooltips per widget (Windows Cowork, 2026-11-16)

**Verdict: ACCEPT, score 98.** Code row; Hydrogen lane (medium), so the second-model review ran through
`second_review.py` (route Codex): **APPROVE, no findings** (`C:/4DApp/recheck/codex/T-AUD-24h_review.md`, embedded
prompt with the spec, the diff and the called code).

## Facts (Cowork re-ran, branch `fix/T-AUD-24h`, after promote)
- Commits after `fix/T-AUD-23c`: `484ac1c` spec, `b722a03` lane work, `006c493` merge. Name-status: M `app.py`,
  M `ui_payload.py`, A the new test, A the note and the RESULT. No D, no R.
- `apps/ui/tests`: `79 passed` (76 before + 3). New test: `3 passed`. Before the change, the new test failed 3 of 3
  (Cowork rehearsal and the note's (b)). `git status --porcelain` empty.
- Tooltips, read from `FIELD_HELP`: `Range: 0.0–1.0 V`, `Range: 0.7–1.3 λ`, `Range: 10.0–20.0 AFR`. These are the
  widgets' own `min_value`/`max_value` constants.
- `app.py`: only the `help=` key on lines 538 and 540 changed. `obd_upstream_o2_val` kept (coverage test).
- Note: readiness (a)-(e), VERIFICATION GATE CLEAN (ruff, pyright 0 errors), CODE REVIEW, `## Time` 1.8 min.

## Register
`resync_register.py --register rest-code --base 484ac1c --apply --drop-gone`: moved 12, changed 4, gone 0. RK0445,
RK0446 re-valued to the constant names, `same_as` RK0404/RK0405, suspect `RESOLVED T-AUD-24h`. `CLAIMS OK group=rest`.

## Findings
- **L1 (Low):** the note says `bash` on PATH resolved to WSL, so the agent ran in PowerShell. This is a lane
  environment fact, not a defect of the row. Score −2.
