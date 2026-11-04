# T-VINA-19 progress note

## Readiness
(a) Starting state matches: branch fix/T-VINA-19, HEAD~1 = 8aeed6a, `git status --porcelain` empty. Loop-pack master HEAD 396ab962bbc583c33a371334e22b919b6ec01d14 (informational).
(b) The R2 test is applied first and run against the unchanged tool; it must give `1 failed` (U+FFFD brand wins the JTM vote 3:2).
(c) Derived by hand: JTM petrol 17-char rows = TOYOTA 2, SUBARU 1; plus 3 U+FFFD rows. Without the U+FFFD skip the U+FFFD brand has 3 and wins; expected dict is unchanged (TOYOTA). Without the 17-char filter SUBARU has 3 (1+2 16-char rows) and beats TOYOTA 2.
(d) No contradiction: anchors at build_wmi_map.py:72 and in the test match make_rh.py's old strings.
(e) Teach-back: `_registry_majority` must skip brands holding U+FFFD, and its test must carry a second 16-char SUBARU row and three 0x98 0x98 rows. Decisive check: base tool fails the new test, and mutants M1 and M2 each give `1 failed`.

## Assumptions worked past
none yet.
The commit trailer was left out: bash_guard refused the commit command while it held the attribution trailer text.
The first R1 edit wrote a literal U+FFFD character. It was corrected to the escape text `"\ufffd"` before the commit (od -c shows backslash u f f f d).

## R3 mutants (copy in recheck/T-VINA-19/mut/, restored, cmp identical)
- Red gate: R2 test on the base tool: 1 failed (JTM -> U+FFFD brand), 8 passed.
- Green after R1+R2: 9 passed.
- M1 (`if len(vin) == 17 and brand and` -> `if brand and`): 1 failed, 8 passed.
- M2 (` and "\ufffd" not in brand` removed): 1 failed, 8 passed.

## VERIFICATION GATE
CLEAN. Step 1 vinlab: 344 passed, 8 skipped. Step 2: 9 passed. Step 3: ruff All checks passed; log shows the spec commit and one commit.

## CODE REVIEW
CLEAN. The diff is one condition in the tool and two edits in the test, as R1-R2 say.

## Time
phase | start | end | minutes | context at end
all | 2026-11-04T21:13:03Z | 2026-11-04T21:15:13Z | 2.2 | ABSENT
