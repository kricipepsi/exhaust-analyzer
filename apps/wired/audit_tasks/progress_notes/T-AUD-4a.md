# T-AUD-4a progress note

## Readiness challenge
(a) Start matches: branch `fix/T-AUD-4a`, HEAD `12f853a` (descendant of `49060ac`, recorded as base), `git -C repo status --porcelain` empty; preconditions print `checked`.
(b) The two NEW tests fail on the base (`2 failed, 28 passed`: reads_measured_downstream, absent_without_live_reading); the PIN passes. Failure cause: base dispatch reads FF B1S1 (0.85 / 0.85 instead of 0.10 / None).
(c) Derived expected values: two-source payload `downstream_o2_v` 0.10 -> `o2_downstream` 0.10; FF-only -> None; `o2_voltage` 0.85. Match P2.
(d) No contradiction. Spec says tests "built on `_build_observation` or `_resolve_pid_from_payload`"; I use the latter.
(e) Deliverable: change `_PID_DISPATCH["o2_downstream"]` to `(("obd","downstream_o2_v"),)` with three tests. Decisive check: step 1 `30 passed`, both mutants fail named tests, step 4 shows non-None 11 and 0 verdict changes.

## Assumptions worked past
- The test files are edited in place, CRLF/LF preserved by detection.

## VERIFICATION GATE
CLEAN. Steps 1-5 run as written; results in the RESULT. ruff: All checks passed. Mutants: base entry fails both NEW tests; base+ff fallback fails the absent test.

## CODE REVIEW
Scope: only the one dispatch entry (+comment) and three tests. Contracts/provenance: comment cites OBDLiveDataPayload.downstream_o2_v. Anti-orphan: no new name beyond tests; the entry's consumers are SF-006/EL-002. No findings.

## Time
phase | start | end | minutes | context at end
build | 2026-11-05T12:09:57Z | 2026-11-05T12:12:12Z | see clock | ABSENT
