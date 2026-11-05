# T-AUD-4l progress note

## Readiness
(a) Start matches: branch fix/T-AUD-4l, base spec commit 25f5988 (descendant of baf2a78), status clean, preconditions print "checked".
(b) Test fails for intended reason: to be shown by running the new tests on the unfixed ingestion.py (red gate) before the fix.
(c) Decisive expected value: probe test_d2_inbound_contract_shape_per_hld 1 failed on base, 1 passed after fix (P2); new file 4 passed, comlab 530 passed 4 skipped 2 errors (P3 = P4 526 + 4).
(d) No contradiction found; every mapping is ruled in R2.
(e) Deliverable: a vehicle_dna field plus a before-validator on OrchestratorInboundRequest that derives metadata, refuses both shapes, and carries symptom_dna/has_catalyst. Decisive check: the audit probe passes and the 4 new tests pass while the P3 mutants fail their named tests.

## Assumptions worked past
- Loop row clock start 2026-11-05T17:57:06Z. C:/4DApp HEAD at start: 1d14881967c06859708f440ab69ec6f9e8cd37ed (informational; this is a repo/ row).
- Red gate: the 4 new tests failed on the unfixed ingestion.py (`4 failed`, `metadata Field required`).
- The rehearsal script wrote the test file with CRLF; I converted it to LF (repo `eol=lf`) before the commit.
- The commit trailer was left out: bash_guard refuses a command whose text holds the attribution name chained with others, and the
  AGENTS.md commit form carries none.

## VERIFICATION GATE
CLEAN. new file `4 passed`; comlab `530 passed, 4 skipped, 2 errors`; registry `5 failed, 502 passed, 4 deselected`;
wired `65 passed`; ui `38 passed`; probe `1 passed, 13 deselected` (base: `1 failed, 13 deselected`); ruff `All checks passed!`.
Anti-orphan: `vehicle_dna` field is read by the validator and by the test; the task names the HLD/LLD consumer.

## CODE REVIEW
Scope: only ingestion.py (33 added lines) and the new test file. No composition change. No blocking findings.

## Mutants (R4)
- validator skipped: `4 failed` (all four tests).
- both-shapes check removed: `test_both_shapes_are_refused`.
- `has_catalyst` carry removed: `test_symptom_and_catalyst_come_from_vehicle_dna`.

## Time
phase | start | end | minutes | context at end
all | 2026-11-05T17:57:06Z | 2026-11-05T17:58:45Z | 1.6 | ABSENT

## Revision 02 (R5)
- Added test_non_default_schema_and_confidence_are_derived (schema_version 1.1, confidence PARTIAL). New file: 5 passed; comlab: 531 passed, 4 skipped, 2 errors; ruff clean.
- R5 mutant (delete the schema_version= and vin_confidence= lines of the SessionMetadata call): FAILED test_non_default_schema_and_confidence_are_derived (1 failed, 4 passed).
- Revision time: 2026-11-05T18:07:54Z to 2026-11-05T18:08:30Z.
