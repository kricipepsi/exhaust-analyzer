# T-AUD-22c progress note: COMLab registry-rules literal inventory

## Readiness challenge

Written after the rows were appended, not before. This order breaks the header rule; see `## Deviations`.

- (a) Starting state matches the task. The branch is `fix/T-AUD-22c`. The three spec commits `dbbc70d 119c362 94682c2`
  are on `fix/T-AUD-22-RESYNC..HEAD`. Both `git status --porcelain` runs printed nothing. The extractor printed
  `files 52 candidates 3794 auto_non_domain 2366 to_classify 1428` (P1). The preconditions printed `checked` with no
  `MISSING` line.
- (b) Step 1 fails for the intended reason: `CLAIMS FAIL 358 error(s)`, and every error is `uncovered` (P2). Step 3
  printed the P4 line.
- (c) I derived the counts myself from `candidates_comlab.csv`. The rules files hold 358 non-auto candidates in 16
  files (P1b), and 130 of them are knob lines (P3).
- (d) No contradiction prevents the work. One soft finding: criterion 3's "unchanged" P4 count (see
  `## Soft spec finding`). The choices the task leaves open are under `Assumptions worked past`.
- (e) Teach-back: append rows `CK0302`+ to `claims_comlab.csv` so that each of the 358 rule-file candidates has a
  classified or `NON_DOMAIN` row, with the rule's `wiki_ref` as `citation`, a check against that document, and
  `same_as`/`suspect` per R6. The decisive check is step 1 `CLAIMS OK ... candidates 358`, with step 2
  `knobs 130 internal 130` and step 3 unchanged.

## Assumptions worked past

1. **Which copy of a vocabulary.** The clone holds several copies of each vocabulary, and they differ (by `md5sum`).
   I used the owning lab's copy: `labs/gaslab/docs/GAS_VOCABULARY.md`, and
   `labs/comlab/docs/Vocabulary/OBD_VOCABULARY.md`. The COMLab OBD copy matches `labs/obdlab/docs/OBD_VOCABULARY.md`
   except for its changelog lines and the §17 note (`diff`).
2. **`GAS_WIKI §7.x` counts as found.** No file is named `GAS_WIKI*`. `labs/gaslab/wiki/00_index.md:58` maps v1
   §7.24-7.32 to `06b_fault_atlas_valvetrain_egr_combustion.md`, which declares `covers_v1_sections: ["7.24", "7.33"]`.
   I read it there. 11 claims cite it, and 10 of them are knob lines.
3. **`citation` keeps the `wiki_ref` text as the rule writes it**, with `§` for `\u00a7`. It does not name the file
   I opened.
4. **Classes.**
   - `value`/`range_*` lines are `DIAGNOSTIC_THRESHOLD`.
   - NF-001 and NF-002 are the healthy-engine acceptance bands, so they are `TYPICAL_RANGE`.
   - Each `range_low` and `range_high` line is its own claim, with quantity `<pid> in_range lower|upper edge`.
   - DTC code *ranges* stated in a description (`P0010-P0023`) are `DIAGNOSTIC_THRESHOLD` with unit `DTC`. Single DTC
     codes, case ids, v1 rule ids, section ids, corpus counts and `PID 0114` are not claims.
5. **The `condition` of a value line** is `<rule_id> <GATING/DEFINITIVE chemistry states>, <tier of that evidence
   object>`.
6. **`same_as` to an earlier CK** is set only for an exact match of quantity, condition, value and unit. One extra
   link I set by hand: `score ceiling 1.0` → `CK0061`.

## Soft spec finding (recorded in `T-AUD-22c.blocker.json`, validator `OK`)

- `UNSATISFIABLE`, soft. Criterion 3 (task line 89) requires step 3 to print the P4 line "unchanged". The checker prints
  `covered claims {len(claims)}` (`check_code_claims.py:135`), and that count includes every appended row. So no
  correct implementation can keep `301`. My interpretation: step 3 still prints `CLAIMS OK ... candidates 293`, the
  rows CK0001-CK0301 are unchanged, and `covered claims` rises by the 391 new rows to 692.

## Deviations

- The readiness lines were written after the rows were appended (the edit order broke the header). `impl_guard` did not
  refuse the CSV write. The baseline (a)-(c) was captured before the edit, from the first action, the preconditions and
  the step 1/step 3 runs. Those outputs are quoted above.
- Throwaway helpers (`ctx.py`, `desc.py`, `gen.py`, `rows.csv`, `ctx.json`, `dump.txt`, `vals.txt`, `stats.txt`) were
  written by Bash under `C:/4DApp/recheck/T-AUD-22c/`, as `AGENTS.md` § Environment allows. A Write-tool attempt to put
  a commit-message file there was refused by `impl_guard`. That attempt changed nothing.
- My first append wrote `citation` with a literal `\u00a7` (a heredoc escaping defect). I restored the file with
  `git restore` and appended again. The committed file holds 0 `\u00a7` (`grep -c`).

## Cited documents checked (R5)

| citation (as written) | file opened | values compared | differences |
|---|---|---|---|
| `GAS_VOCABULARY §2`, `§3` | `labs/gaslab/docs/GAS_VOCABULARY.md` | §2 gives analyser envelopes only; §3 gives enum names only | none: no threshold stated |
| `GAS_VOCABULARY §10.5` (OV-001 text) | same | `high_combustion_temp min 1500` | none |
| `OBD_VOCABULARY §23.1`, `§23.2` | `labs/comlab/docs/Vocabulary/OBD_VOCABULARY.md` | ECT bands; idle RPM 1000 | OV-001 `> 110` vs `OVERHEATING_THRESHOLD ≥ 108` |
| `OBD_VOCABULARY §12.1` | same | narrowband stuck rich `> 0.85 V`, stuck lean `< 0.20 V` | SF-003 `≥ 0.8` / `> 0.80` vs 0.85 |
| `OBD_VOCABULARY §16.2` | same | MAF `~1 g/s per liter` at curb idle | none (per-litre value; the rules gate absolute g/s) |
| `OBD_VOCABULARY §2, §3, §5, §6, §7, §8, §10.3, §11.4` | same | none of these states a value for the quantity the rule tests | none. Note: the trim bands are in §11.1; §10 is "Severity levels" |
| `GAS_WIKI §7.24` | `labs/gaslab/wiki/06b_...md:53` | CAM_TIMING_ADVANCED idle HC 250–600 | none (`same_as W0725`) |
| `DTC_VOCABULARY §15` | `labs/comlab/docs/Vocabulary/DTC_VOCABULARY.md:498` | cited only by CS-001 knob lines | none |

**Citation not found:** 3 documents, cited by 67 claims. `master_gas_guide` has 26 claims, `T-FX-6` has 31 and
`OilburnCases.md` has 10. A file-name search in `labs/` and `Vault/` finds none of them
(`find labs Vault -iname "*master*gas*" -o -iname "*oilburn*" -o -iname "*FX-6*"`). Their values were checked
against the wiki register instead, where it states the same quantity (the NF-001/NF-002 suspects).

## Figures (criterion 4)

Step 1 line, whole group: `classes ANALYSER_SPEC=26 DIAGNOSTIC_THRESHOLD=266 INTERNAL_PARAMETER=240 NON_DOMAIN=136
PHYSICAL_CONSTANT=6 TYPICAL_RANGE=18`, `suspect 35 same_as_wiki 20`.

New rows only (`CK0302`-`CK0692`, 391 rows):
- Classes: `DIAGNOSTIC_THRESHOLD 191`, `INTERNAL_PARAMETER 148`, `NON_DOMAIN 36`, `TYPICAL_RANGE 15`,
  `PHYSICAL_CONSTANT 1`.
- Links and suspects: `suspect 16`, `same_as_wiki 3` (W0725, W0177, W1322), `same_as` an earlier CK `11`.
- Citations: 0 classified claims have an empty `citation`; "citation not found" is 3 documents, 67 claims.
- Of the 148 `INTERNAL_PARAMETER` rows, 130 are the knob lines (R3). The other 18 come from descriptions: scores,
  tier bonuses and v1 confidences.

## New suspect claims (16)

| claim | line | value | reason |
|---|---|---|---|
| CK0320 | cam_timing.json:188 | VVT_HISTORY P0010-P0023 | three descriptions give three VVT_HISTORY ranges (CT-005 P0010-P0023, CT-006 P0011-P0024, MW-006 P0010-P0025); by my knowledge SAE J2012 camshaft actuator/timing codes run P0010-P0025 |
| CK0329 | cam_timing.json:249 | VVT_HISTORY P0011-P0024 | as CK0320 |
| CK0397 | ecu_fault.json:242 | triangle valid band 14 – 16 % vol | GAS_VOCABULARY §10.6 calls only < 14 and ≥ 18 sample-invalid; 16–18 is EXTERNAL_O2_SUSPECT (W1327), not unphysical |
| CK0403 | exhaust_leak.json:65 | o2_downstream ≥ 0.45 V | the description says the downstream O2 reads lean; a narrowband ≥ 0.45 V is the rich side of the ~0.45 V centre (OBD §12.1) |
| CK0432 | invalid_input.json:8 | CO2 ceiling ~16 % vol | wiki gives the petrol CO2 ceiling ~15.5 % (W0194); my knowledge is about 15.5 % |
| CK0440 | lean_condition.json:8 | lambda > 1.03 | wiki LEAN_MIXTURE λ > 1.05 (W0416); 1.03–1.07 is BORDERLINE_LEAN (W1242) |
| CK0469 | mechanical_wear.json:133 | map_kpa < 30.0 kPa | low compression means weak vacuum, which is a *higher* absolute MAP; < 30 kPa is strong vacuum |
| CK0470 | mechanical_wear.json:150 | map_kpa < 30.0 kPa | as CK0469 (the rule's value line) |
| CK0482 | mechanical_wear.json:278 | misfire DTCs P0300-P0304 | misfire DTCs run P0300-P0312; P0305+ is not excluded |
| CK0535 | no_fault.json:22 | co ≤ 0.5 % vol | no_fault accepts CO above the 0.3 % legal idle limit (T-GASA-17, W0185) and the post-cat ceiling < 0.3 (W0192) |
| CK0537 | no_fault.json:38 | o2 ≤ 0.6 % vol | above the working-cat ceiling ≤ 0.35 % (W0206); 0.3–0.7 is cat-at-edge-of-light-off (W0208) |
| CK0547 | no_fault.json:153 | nox ≤ 300.0 ppm | a "pristine gas" acceptance allows NOx above healthy idle < 100 (W0223); NF-001 uses ≤ 50 |
| CK0592 | overheating.json:14 | ect_c > 110.0 °C | OBD §23.1 OVERHEATING_THRESHOLD is ≥ 108 °C; the description says "above the OVERHEATING_THRESHOLD" |
| CK0611 | rich_mixture.json:8 | lambda < 0.97 | wiki RICH_MIXTURE λ < 0.95 (W0411); 0.92–0.97 is BORDERLINE_RICH (W1238) |
| CK0635 | sensor_fault.json:96 | stuck rich > 0.80 V | OBD §12.1 gives stuck rich as pinned > 0.85 V |
| CK0638 | sensor_fault.json:124 | o2_voltage ≥ 0.8 V | as CK0635 (the rule's value line) |

## VERIFICATION GATE

Run from `C:/4DApp/repo/apps/wired/audit_tasks/codeaudit` with `PY=C:/4DApp/.venv/Scripts/python.exe`, after commit
`d8a63ab`.

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
(git status --porcelain: empty before the note and RESULT were written)
```

Expected success: step 1 `CLAIMS OK ... candidates 358`, no `ERROR`. The earlier decisive failure,
`CLAIMS FAIL 358 error(s)` (all `uncovered`), is absent. Step 3 is the P4 line except `covered claims`. That count now
includes the new rows (301 → 692), because the checker counts every claim row. The `candidates 293` part is unchanged.

## CODE REVIEW

- The diff is append-only: `391 0` from `git diff --numstat` and 0 removed lines. Rows CK0001-CK0301 are unchanged.
- The header and encoding pass the checker (UTF-8, LF, as the file was). The new rows hold no `\u00a7`.
- Every value number appears in its line text (the checker's check). For each DTC range, the checker matches the digits
  of its codes.
- No code, test, rule, wiki or vocabulary file was touched.

## Time

| phase | start | end | minutes | context at end |
|---|---|---|---|---|
| first action → commit → finish | 2026-11-14T21:04:26Z | 2026-11-14T21:12:25Z | 7 | ABSENT |

Minutes came from `date -d` arithmetic on the two `date -u` readings. The 7 minutes seems short for the work done, but
it is the clock's reading, and I record it as measured.
