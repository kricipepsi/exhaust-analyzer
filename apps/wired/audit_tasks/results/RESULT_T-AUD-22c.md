# Result

## Status
completed

## Summary
I appended 391 rows, `CK0302`-`CK0692`, to `claims_comlab.csv`. Together they cover all 358 non-auto candidates in
`labs/comlab/registry/rules/*` (16 files):
- The 130 `base_weight`/`confidence_ceiling` lines are `INTERNAL_PARAMETER` (R3).
- 165 `value`/`range_*` lines are thresholds. Each takes its quantity and unit from the `pid`.
- 31 description lines give one claim per stated value, or one `NON_DOMAIN` row when the line states none.
- 32 lines hold only ids or citations (case ids, `§P_NEW_*`, `PID 0114`) and are `NON_DOMAIN`.

Each claim's `citation` is the rule's own `wiki_ref`, and I checked it against the cited document where the clone holds
that document. 16 claims are suspect. Six of them contradict the document the rule cites:
- OV-001 gates `> 110 °C`; OBD §23.1 sets the threshold at `≥ 108`.
- SF-003 gates `0.8 V` (2 claims); OBD §12.1 says stuck rich is `> 0.85 V`.
- NF-001 accepts CO `≤ 0.5 %`, above the 0.3 % legal idle limit.
- NF-001 accepts O2 `≤ 0.6 %`; NF-002 accepts NOx `≤ 300 ppm`.

The other suspects come from physics or from DTC tables (all 16 are in the note):
- EL-002 gates on the rich side of the sensor but calls it lean.
- MW-004 uses a low MAP to stand for weak vacuum (2 claims).
- Three different VVT DTC ranges (2 claims), and an incomplete misfire DTC range.

No web access was used.

## Files changed
- `repo/apps/wired/audit_tasks/codeaudit/claims_comlab.csv`: 391 rows appended, committed in `d8a63ab`.
- `repo/apps/wired/audit_tasks/progress_notes/T-AUD-22c.md`: created, untracked.
- `repo/apps/wired/audit_tasks/progress_notes/T-AUD-22c.blocker.json`: created, untracked. The header authorises it;
  it holds one soft finding.
- `repo/apps/wired/audit_tasks/results/RESULT_T-AUD-22c.md`: this file, untracked.
- `candidates_comlab.csv`: the first action rewrote it byte-identical (`git status` stayed clean).

## Commands executed
- The first action, the preconditions, and step 1 and step 3 before the edit (baseline: P1, P1b, P2, P3 and P4 all
  reproduce).
- Throwaway helpers under `C:/4DApp/recheck/T-AUD-22c/` (`ctx.py`, `desc.py`, `gen.py`) built the rows; they were
  appended with `cat >> claims_comlab.csv`.
- Verification steps 1-4 as written in the task.
- `validate_blocker_record.py` on the blocker record printed `OK`.

## Validation evidence
```
# 1.
classes ANALYSER_SPEC=26 DIAGNOSTIC_THRESHOLD=266 INTERNAL_PARAMETER=240 NON_DOMAIN=136 PHYSICAL_CONSTANT=6 TYPICAL_RANGE=18
suspect 35 same_as_wiki 20
CLAIMS OK group=comlab scope=labs/comlab/registry/rules/* candidates 358 covered claims 692
# 2.
knobs 130 internal 130
# 3.
CLAIMS OK group=comlab scope=*.py candidates 293 covered claims 692
# 4.
d8a63ab docs(T-AUD-22c): classify COMLab registry-rule literals (CK0302-CK0692)
94682c2 spec(T-AUD-22c): cold read recorded
119c362 spec(T-AUD-22c): dispatch header
dbbc70d spec(T-AUD-22c): COMLab registry-rules literal inventory; extractor skips escapes/ids; resync strips text; T-COMA-31 registered
 1 file changed, 391 insertions(+)
0
```
The previous decisive failure, `CLAIMS FAIL 358 error(s)` (all `uncovered`), is absent. Step 1 prints no `ERROR` line.

Branch and log:
```
$ git -C repo branch --show-current
fix/T-AUD-22c
$ git -C repo log --oneline fix/T-AUD-22-RESYNC..HEAD
d8a63ab docs(T-AUD-22c): classify COMLab registry-rule literals (CK0302-CK0692)
94682c2 spec(T-AUD-22c): cold read recorded
119c362 spec(T-AUD-22c): dispatch header
dbbc70d spec(T-AUD-22c): COMLab registry-rules literal inventory; extractor skips escapes/ids; resync strips text; T-COMA-31 registered
```

## Criteria
| # | status | evidence |
|---|---|---|
| 1 | MET | step 1: `CLAIMS OK group=comlab scope=labs/comlab/registry/rules/* candidates 358 covered claims 692`, no `ERROR` |
| 2 | MET | step 2: `knobs 130 internal 130` |
| 3 | MET on the recorded interpretation | step 3: `CLAIMS OK group=comlab scope=*.py candidates 293 covered claims 692`. `covered claims` is `len(all rows)` (`check_code_claims.py:135`), so it cannot stay 301 after an append. Soft `UNSATISFIABLE` finding in `T-AUD-22c.blocker.json`. `candidates 293` and rows CK0001-CK0301 are unchanged. |
| 4 | MET | the note's `## Figures` and `## New suspect claims (16)` give: classes, `suspect 16`, `same_as_wiki 3`, 0 empty citations, and "citation not found" 3 documents / 67 claims |
| 5 | MET | step 4: one commit `d8a63ab` after the spec commits, `1 file changed, 391 insertions(+)`, 0 removed lines |

## Decisions the task did not specify
- Vocabulary copy: the owning lab's copy (`labs/gaslab/docs/GAS_VOCABULARY.md`,
  `labs/comlab/docs/Vocabulary/OBD_VOCABULARY.md`), because the copies in `labs/semantic` and `Vault/` differ.
- `GAS_WIKI §7.x` was resolved through `labs/gaslab/wiki/00_index.md` to `06b_...md` and counted as found.
- `range_low` and `range_high` are separate claims (`<pid> in_range lower|upper edge`).
- NF-001 and NF-002 bands are `TYPICAL_RANGE`; every other rule threshold is `DIAGNOSTIC_THRESHOLD`.
- DTC ranges stated in descriptions are claims (unit `DTC`); single DTC codes, ids and corpus counts are not.
- Values from documents not found (`master_gas_guide`, `T-FX-6`, `OilburnCases.md`) were compared with the wiki
  register where it states the same quantity.
- `same_as` to an earlier CK only on an exact match of quantity, condition, value and unit.

## Pre-existing changes preserved
The `repo` tree was clean at the start (`git status --porcelain` empty). The untracked files in `C:/4DApp` (launchers,
the handoff, `LOOP_STATE.md`) were not touched.

## Rollback
`git -C C:/4DApp/repo reset --hard 94682c2` on `fix/T-AUD-22c` (the task branch only, never `main`), or
`git revert d8a63ab`. Then delete the untracked note, the blocker record and this RESULT.

## Remaining risks or uncertainties
- Process deviation: the readiness lines were written after the CSV append, not before. The baseline was captured
  before the edit and is quoted in the note.
- The 16 suspects come from the cited documents, the wiki register and my own knowledge (the VVT and misfire DTC
  ranges, the MAP/vacuum physics, and the 15.5 % CO2 ceiling). None is web-verified, as R7 requires.
- Many rules cite a section that states no value for the quantity (`OBD_VOCABULARY §10.3`, `§2`; `GAS_VOCABULARY §2`,
  `§3`). Those claims are not suspect, but the citations do not support them. The trim bands are in OBD §11.1.
- A description claim and its value line are linked only when the comparator matches (for example, MW-001 text
  `hc > 200` is not linked to the rule's `≥ 200.0`).
- The clock measured 7 minutes for the session. That reading is recorded as measured.
