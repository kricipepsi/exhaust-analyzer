# Result

## Status
completed

## Summary
I appended 522 claims (`W1172`–`W1693`) to `labs/gaslab/audit_tasks/wikiaudit/claims.csv`. They cover all 488
non-auto candidates of `docs/GAS_VOCABULARY.md` (234) and `gaslab/data/gas_lab_ontology.yaml` (254). 244 claims carry a
`same_as`: 224 point to the wiki claim with the same value and 20 to an earlier new claim. 72 carry a `suspect` text,
including the three CO 0.45 % seeds.

The main finding: the ontology, which is what the code loads, differs from the wiki atlas on many fault signatures.
- TIMING_OVER_ADVANCED and TIMING_RETARDED differ on all six gases.
- WORN_ENGINE, FLAT_CAMSHAFT, WORN_VALVE_SEALS (which uses the superseded v1 HC range), WORN_PISTON_RINGS and the
  rings route at 2500 rpm differ on several gases.
- COOLANT_LEAK_INTERNAL: the CO2 ceiling is 12.0 against the wiki's 11.5, and the HC floor is 300 against 200–400.
- RICH_MIXTURE: CO, O2 and λ edges differ.
- HIGH_COMBUSTION_TEMP, EGR_STUCK_CLOSED and TIMING_OVER_ADVANCED: the NOx floor is 1000, while the vocabulary band
  the comments cite is ≥ 1500.
- EVAP: the idle floors contradict the wiki's "idle normal".

The vocabulary contradicts itself on the triangle borderline band (§5 vs §10.6), and gives a mixture-rule priority of 70
against the wiki's 80. I verified nothing on the web (R6).

## Files changed
- `repo/labs/gaslab/audit_tasks/wikiaudit/claims.csv`: 522 rows appended (commit `f756425`).
- `repo/labs/gaslab/audit_tasks/progress_notes/T-GASA-16.md`: created (untracked).
- `repo/labs/gaslab/audit_tasks/results/RESULT_T-GASA-16.md`: this file (untracked).

## Commands executed
- First action and preconditions (task text), read-only. Output: `fix/T-GASA-16`, `d7244d9 spec(T-GASA-16) …`, clean
  status, `CLAIMS FAIL 488 error(s)`, `checked`.
- Read-only extracts of `candidates.csv` / `claims.csv` with `C:/4DApp/.venv/Scripts/python.exe -I -c …`.
- 11 append batches with `python -I -` and a heredoc (tool in the note § Batch tool), plus two row-fix passes on the
  rows after `W1171`.
- `git add labs/gaslab/audit_tasks/wikiaudit/claims.csv`, then
  `git -c user.name=Claude -c user.email=noreply@anthropic.com commit` (amended once to add the `W1506` text).
- `### Verification ###` steps 1–4, plus `check_claims.py --scope all`.

## Validation evidence
```
classes ANALYSER_SPEC=17 DIAGNOSTIC_THRESHOLD=273 INTERNAL_PARAMETER=73 LEGAL_LIMIT=4 NON_DOMAIN=91 PHYSICAL_CONSTANT=23 RULE_OF_THUMB=11 TYPICAL_RANGE=30
suspect 72
CLAIMS OK scope=vocab_ontology candidates 488 covered claims 522      (exit 0; grep -c ERROR = 0)
CLAIMS OK scope=wiki candidates 680 covered claims 1171
wiki rows unchanged: True
seeds flagged 3 of 3
f756425 docs(T-GASA-16): WIKIAUDIT claim inventory of GAS_VOCABULARY and the ontology (W1172-W1693)
d7244d9 spec(T-GASA-16): WIKIAUDIT vocab + ontology claim inventory
 1 file changed, 522 insertions(+)
?? labs/gaslab/audit_tasks/progress_notes/T-GASA-16.md
CLAIMS OK scope=all candidates 1168 covered claims 1693
```
The previous decisive failure is gone: P3 `CLAIMS FAIL 488 error(s)` no longer appears.

Branch and log:
```
$ git -C repo branch --show-current
fix/T-GASA-16
$ git -C repo log --oneline e4967bd..HEAD
f756425 docs(T-GASA-16): WIKIAUDIT claim inventory of GAS_VOCABULARY and the ontology (W1172-W1693)
d7244d9 spec(T-GASA-16): WIKIAUDIT vocab + ontology claim inventory
```

## Criteria
| # | status | evidence |
|---|---|---|
| 1 | MET | step 1: `CLAIMS OK scope=vocab_ontology candidates 488 covered claims 522`, no `ERROR` |
| 2 | MET | step 2: `CLAIMS OK scope=wiki candidates 680 covered claims 1171`; `wiki rows unchanged: True` |
| 3 | MET | step 3: `seeds flagged 3 of 3` |
| 4 | MET | note § Step 1 disclosure (`classes`, `suspect 72`, 244 with `same_as`) and § Suspect claims (all 72 with reasons) |
| 5 | MET | step 4: one commit `f756425` after `d7244d9`; `git diff --name-only HEAD~1 HEAD` = `claims.csv` only |

## Decisions the task did not specify
The full list is in the note, § Decisions the task did not specify. In short:
- An ontology `{min, max}` with an end at 0 or at the analyser envelope edge is an open end. It links to a wiki
  one-sided value with the same closed end. `>`/`≥` count as the same value.
- A value is suspect when the wiki states a number for the same fault, gas and condition and the ontology or vocabulary
  value differs, wider or narrower. A 0.97–1.03 band against a wiki "≈ 1.0" is not flagged.
- For a fault vector stated twice in the wiki, `same_as` takes the idle-condition claim.
- Payload validator bounds link to the analyser envelope claims.
- Bands with both ends open are `INTERNAL_PARAMETER`.
- A standalone 2500 rpm links to `W0121`.
- Repeated vocabulary/ontology values with no wiki statement link to the first new claim (20 rows).

## Pre-existing changes preserved
None existed in `repo/`: the starting status was clean. The `C:/4DApp` master working tree (LOOP_STATE.md, handoffs,
launchers) was not touched.

## Rollback
`git -C C:/4DApp/repo reset --hard d7244d9` on `fix/T-GASA-16` (task branch only). Delete the untracked note and RESULT.

## Remaining risks or uncertainties
- Class and `same_as` choices are judgement. A missed link leaves `same_as` empty and costs one extra verification. A
  wrong link would skip a check. I linked only on matching fault/gas/condition, and the observations in the note list
  the borderline cases.
- Three suspect texts rest on my own knowledge, not on a wiki claim: SAE J1667 is a diesel smoke test (`W1181`); the
  32-entry comment (`W1432`) was checked against a count of 34 ontology fault keys; the stale scope label is `W1435`.
- An impl_guard denial and an ~8 kB Bash command limit forced inline batches. The appended bytes were checked by the
  checker (mojibake, values present in each line).
- Scratch dumps (copies of CSV fields) remain under `C:/4DApp/recheck/T-GASA-16/`, outside the clone.
- Time: 26.0 min total (2026-11-14T08:30:36Z → 08:56:38Z), inside the 30 min expected and the 90 min stop rule. Context use is ABSENT (no meter exposed).
