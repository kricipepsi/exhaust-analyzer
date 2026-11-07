# REVIEW T-VINA-6 — ACCEPT, score 96 (Windows Cowork, 2026-11-07)

Facts first: `fix/T-VINA-6` from `origin/main` `8b4d343`: spec `302a954`, build `ee538f8` (84 map rows
`PORT_INJECTION` → `DIESEL`, new test), revision 02 spec `3ee93cd`, test commit `9e51f6d`. Both builds equal Cowork's
rehearsal (map hunks identical; test file `cmp` equal to `recheck/T-VINA-6/test_h1_diesel_map_rows_r02.py`).
`decoder.py` untouched. Porcelain: note and RESULT only. Both headless runs exit 0.

## Gates re-run by Cowork
- vinlab `381 passed, 8 skipped` (base 376); `test_h1_diesel_map_rows.py` `5 passed`; base map `3 failed, 2 passed`.
- wired `85 passed`, ui `49 passed` (equal on the base); ruff clean.

## Second review
ds-flash APPROVE WITH CORRECTIONS (`C:/4DApp/recheck/codex/T-VINA-6_review.md`, cites the embedded diff and decoder
lines). Upheld: test gaps (real VIN, petrol controls, per-key counts) → revision 02. Not upheld (re-derived): BMW FE435
share 0.333 and the cylinder fields (that column is unreliable map-wide; the engine code is the evidence). The
revision is a test-only change rehearsed byte for byte: no second review of it.

## Criteria
1-2 MET.

## Score
100 − 4 (a revision owed to Cowork's own spec: the first test had no real VIN and no petrol control) = 96.

## Follow-up
T-VINA-6b (registered): diesel codes TecDoc does not key (K9K A7, F9Q G7, D4EA-V, D4HE; Mazda WL variants) and the
electric brands LIVEWIRE/ZEEHO; needs a source first.
