# T-VINA-3 progress note

## Readiness
(a) Starting state matches: branch fix/T-VINA-3, HEAD d5c8c87 (spec commit, child of base aa69249), porcelain empty; preconditions printed "checked" only.
(b) New test_vref_year_window.py is written first and run on unmodified decoder: expected to fail on the two out-of-window VINs (row applied -> EURO_4/HIGH), pass on the window-null check.
(c) Expected values derived independently of the test: WBA4W9C5ZLYYYYYYY decodes 1990 (task text, B58 row later) so row is dropped -> EURO_1, rated_rpm None; VF7SA5FR8AW511081 is 2010 inside 5FR 2010-2015 -> rated_rpm 6000 (P4). Compared against make_rh.py values.
(d) No contradiction found; R1-R5 files all in Files to touch.
(e) Deliverable: decoder drops a vref row and flags vref_year_out_of_window when model_year is outside [my_start, my_end]; tests, fixture and doc follow. Decisive check: vinlab suite 229 passed 8 skipped, M1 mutant fails 4 tests, probes 8 passed.

## Time
start 2026-11-04T09:00:51Z
end 2026-11-04T09:03:08Z | about 3 min | context ABSENT (low)

| phase | start | end | minutes | context at end |
|---|---|---|---|---|
| all | 2026-11-04T09:00:33Z | 2026-11-04T09:03:08Z | 2.6 | ABSENT |

## Assumptions worked past
- Soft finding (see T-VINA-3.blocker.json): with R1, `apps/wired` `test_oil_cases_route_to_expected_faults` fails (MW-009 routes to MF-001) because the oil fixtures use WBA4W9C5ZLYYYYYYY, now EURO_1. Base (decoder.py stashed) prints 41 passed. Wired edits are outside Files to touch, so wired stays 1 failed, 40 passed. Settled by stash/pop of decoder.py only.
- Fixture rewritten in text mode on Windows, so it has CRLF like the file it replaced.

## Mutant M1
`False and ` prefixed to the elif: 4 failed, 225 passed, 8 skipped (out_of_window decoder test, roundtrip fixture, 2 year-window cases). decoder.py restored from recheck/T-VINA-3/mut, cmp clean.

## VERIFICATION GATE
Step 1 229 passed, 8 skipped | 2 3 passed | 3 dnalab 27 passed, wired 1 failed 40 passed (NOT MET), ui 30 passed | 4 probes 8 passed | 5 count 1 | 6 ruff All checks passed. Verdict: BLOCKED on criterion 2 only (caused by this change, so not CLEAN-WITH-FINDINGS).

## CODE REVIEW
Every changed line traces to R1-R5. No new field without a reader: flag `vref_year_out_of_window` is read by the new tests and documented in VIN_VOCABULARY.md. No findings beyond the wired regression.

## Round 2
Correction 01 (R6): MW-009.json vin changed to VF7SA5FR8AW511081 (one line). Start 2026-11-04T09:06:10Z, end 2026-11-04T09:06:54Z.
Verification re-run: vinlab 229 passed, 8 skipped; year-window 3 passed; dnalab 27; wired 41 passed; ui 30; probes 8 passed; doc grep 1; ruff All checks passed. Criterion 2 now MET. The round-1 blocker finding is resolved by R6; blocker.json stays uncommitted.
