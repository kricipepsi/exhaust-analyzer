# T-GASA-16 progress note — WIKIAUDIT claim inventory of the vocabulary and the ontology

## Readiness

- (a) Starting state matches: branch `fix/T-GASA-16`; `git log --oneline fix/T-GASA-15..HEAD` =
  `d7244d9 spec(T-GASA-16): WIKIAUDIT vocab + ontology claim inventory`; `git status --porcelain` empty;
  `check_claims.py --scope vocab_ontology | tail -1` = `CLAIMS FAIL 488 error(s)`;
  `git -C C:/4DApp/repo rev-parse HEAD` = `d7244d95fc18a10f68e7f4da3e47111082fda6ce`. Preconditions printed `checked`.
  `tail -1 claims.csv` = `W1171,C0874,…` (P2).
- (b) Step 1 fails for the intended reason: no claims.csv row names a vocabulary or ontology candidate, so all 488 are
  `uncovered` (P3).
- (c) Independent count: `csv.DictReader(candidates.csv)` rows with an empty `auto`, by `file`:
  `docs/GAS_VOCABULARY.md` 234, `gaslab/data/gas_lab_ontology.yaml` 254, total 488 (C0878–C1565), matching P1.
- (d) No contradiction: register format fixed by `wikiaudit/README.md`, checker by `check_claims.py`; R4/R5 fix the
  `same_as` and `suspect` rules. Class choice is bounded judgement among the eight classes.
- (e) Teach-back: I append to `claims.csv`, from `W1172` in `candidates.csv` order, at least one classified row per
  in-scope vocabulary and ontology candidate, linking each value to the first wiki claim with the same quantity,
  condition and value, and flagging every value that contradicts the wiki or known fact. The decisive checks are
  `check_claims.py --scope vocab_ontology` printing `CLAIMS OK scope=vocab_ontology candidates 488 …` with the wiki
  scope still `candidates 680 covered claims 1171`, `wiki rows unchanged: True` and `seeds flagged 3 of 3`.

## Assumptions worked past

- Scratch: one read-only Bash extract wrote candidate and wiki-claim dumps to `C:/4DApp/recheck/T-GASA-16/`
  (`voc.txt`, `ont.txt`, `wiki.txt`; copies of `candidates.csv` / `claims.csv` fields, outside the clone, AGENTS.md
  § Environment). The batch tool writes only `claims.csv`.
- The impl_guard denied a write of an annotation file to `C:/4DApp/recheck/T-GASA-16/` (not in `### Files to touch ###`),
  as in T-GASA-15. The read-only dumps written before that remain there. All annotations were then passed inline.
- Bash refused commands longer than about 8 kB (`unexpected EOF while looking for matching '`), so the annotations went
  in 11 batches of 24–79 rows each. Each batch appended to `claims.csv` after asserts (candidate exists, row shape,
  candidate order, no overlap with earlier rows). The original file bytes were kept and new rows were appended after
  them.
- Values 0 and the analyser-envelope edges (HC 20000, CO 15, CO2 22, O2 22, NOx 5000, λ 0.5 / 2.5) in an ontology
  `{min, max}` are open ends. Where the closed end equals a wiki one-sided value (`> 1000` vs `1000 – 20000`), the claim
  is linked by `same_as`. `>`/`≥` and `<`/`≤` on the same number count as the same value.

## Batch tool

Each batch ran `python -I -` with a heredoc. The heredoc held `D = r'''<rows>'''` and the code below. Row format:
`CID | quantity | value | unit | condition | CLASS | same_as | suspect`, or `CID | ND` for a `NON_DOMAIN` row.
`same_as` is a `W` id, or `@Cxxxx[.k]` (the k-th new claim on that candidate). In a suspect text, `{Cxxxx[.k]}` is
resolved to the claim id of that new claim.

```python
import csv,re,io
C={r['cand_id']:r for r in csv.DictReader(open('candidates.csv',encoding='utf-8'))};O={c:i for i,c in enumerate(C)}
raw=open('claims.csv','rb').read();H=list(csv.DictReader(io.StringIO(raw.decode('utf-8'))))
K={};N={}
def k(c):
 N[c]=N.get(c,0)+1;return c if N[c]==1 else f'{c}.{N[c]}'
for r in H[1171:]:K[k(r['cand_id'])]=r['claim_id']
n=int(H[-1]['claim_id'][1:])+1;last=max([O[r['cand_id']] for r in H[1171:]],default=-1)
A=[[x.strip() for x in l.split('|')] for l in D.splitlines() if l.strip()]
for p in A:assert p[0] in C and (p[1:]==['ND'] or len(p)==8) and O[p[0]]>last and p[0] not in N,p
o=[O[p[0]] for p in A];assert o==sorted(o)
b=io.StringIO();w=csv.writer(b,lineterminator='\n')
for p in A:
 cid=f'W{n:04d}';n+=1;K[k(p[0])]=cid;c=C[p[0]]
 if p[1:]==['ND']:w.writerow([cid,p[0],c['file'],c['line'],'','','','','NON_DOMAIN','','']);continue
 s=p[6];s=K[s[1:]] if s.startswith('@') else s
 w.writerow([cid,p[0],c['file'],c['line']]+p[1:6]+[s,re.sub(r'\{(C\d{4}(?:\.\d)?)\}',lambda m:K.get(m.group(1),m.group(0)),p[7])])
open('claims.csv','wb').write(raw+b.getvalue().encode('utf-8'));print(len(A),cid)
```

The first batch (79 rows) used the same logic written out longhand. Two follow-up passes rewrote only the rows after
`W1171`, with the same `csv.writer` settings. Pass 1 resolved the one forward reference (`W1253` → `W1326`). Pass 2
added the `W1506` suspect text after a check of the ontology citations.

## Step 1 disclosure (criterion 4)

- `classes ANALYSER_SPEC=17 DIAGNOSTIC_THRESHOLD=273 INTERNAL_PARAMETER=73 LEGAL_LIMIT=4 NON_DOMAIN=91 PHYSICAL_CONSTANT=23 RULE_OF_THUMB=11 TYPICAL_RANGE=30`
- `suspect 72`
- `CLAIMS OK scope=vocab_ontology candidates 488 covered claims 522`
- New claims: 522 (`W1172`–`W1693`), of which 431 are domain claims and 91 are `NON_DOMAIN`. **New claims with a
  `same_as`: 244.** Of these, 224 point to a wiki claim (`W0001`–`W1171`) and 20 point to an earlier new claim that
  has no wiki statement (the λ bands, the triangle borderline band, the payload λ envelope, enum size 32, the collision
  tier maxima, the WVT atlas floors and the coolant rule thresholds). By file: vocabulary 260 claims (18 suspect),
  ontology 262 claims (54 suspect).
- No `auto=NON_DOMAIN` candidate got a claim (I did not use the R2 option). I checked the auto lines with number-like
  text (headings, versions, dates, section ids, `GASWIKI-0x`). None holds a domain number.

## Suspect claims (72, every new row with a suspect text)

Each row holds its own text in `claims.csv`. Grouped lines below cover several rows of one fault, and each of those
rows names its own wiki claim.

- `W1172` C0878 vocab:27 operating envelope model years `1990 – 2010`: as W0001
- `W1181` C0888 vocab:48 regulatory high idle nominal `2500`: the line cites SAE J1667 for the BAR two-speed idle; SAE J1667 is the heavy-duty diesel snap-acceleration smoke test procedure (as W0118)
- `W1240` C0952 vocab:189 catalyst light-off lambda window `0.98 – 1.02`: as W0110
- `W1247` C0961 vocab:204 catalyst light-off lambda window `0.98 – 1.02`: as W0110
- `W1253` C0968 vocab:218 triangle BORDERLINE high band `15.5 – 16`: contradicts §10.6 of the same file, where 15.0–16.0 is the normal band (W1326) and no upper borderline band exists
- `W1258` C0974 vocab:234 HC_FACTOR `0.0025`: as W0085
- `W1263` C0980 vocab:248 Hcv `1.85`: as W0090
- `W1272` C0991 vocab:275 analyser lambda accuracy `± 0.05 – 0.10`: as W0099
- `W1278` C0994 vocab:279 HC_FACTOR `0.0025`: as W0085
- `W1281` C0998 vocab:299 REGULATORY_HIGH_IDLE rpm band `2200 – 2800`: as W0118
- `W1298` C1021 vocab:367 CO tailpipe normal `0.1 – 0.45` (seed): as W0185
- `W1303` C1026 vocab:374 collision rule CO tier max `0.45`: 0.45 % is the working-cat normal CO maximum flagged at W0185: above the 0.3 % UK MOT natural-idle CO limit (W1109)
- `W1306` C1028 vocab:380 CO2 tailpipe target `14.5 – 16.0`: as W0197
- `W1326` C1050 vocab:417 triangle normal band `15.0 – 16.0`: contradicts the BORDERLINE band 15.5–16 in §5 of the same file (W1253)
- `W1332` C1057 vocab:429 catalyst light-off lambda window `0.98 – 1.02`: as W0110
- `W1341` C1070 vocab:451 HC (vocabulary band floor) `≥ 250` (WORN_PISTON_RINGS, 2500 rpm): the wiki rings row and the code test give HC > 300 ppm at 2500 rpm (W0592), not 250
- `W1396` C1143 vocab:591 lean/rich rule priority `70`: contradicts the wiki lean/rich rule priority 80 (W0303)
- `W1425` C1195 vocab:700 operating envelope model years `1990–2010`: as W0001
- `W1432` C1201 ontology:4 ontology fault entry count `32`: the ontology holds 34 fault entries and the ChemicalSignature enum is 34-value (W0006); 32 is the pre-v2.1 count
- `W1435` C1205 ontology:10 operating envelope model years `1990-2020`: contradicts the current 1990–2010 scope (W0001); the vocabulary records this string as a stale label that no code reads (T-AUD-16)
- `W1445` C1222 ontology:44 collision rule CO tier max `0.45` (seed): as W1303: 0.45 % is the working-cat normal CO maximum flagged at W0185
- `W1468` C1242 ontology:74 coolant rule CO2 dilution ceiling `≤ 12.0`: the wiki gives CO2 < 11.5 % for the same fault (W0759)
- `W1469` C1242 ontology:74 coolant rule HC floor `≥ 300`: the wiki gives HC 200–400 ppm for the same fault (W0656); a 300 ppm floor excludes the lower part
- `W1472` C1245 ontology:79 coolant rule CO2 dilution ceiling `≤ 12.0`: as W1468
- `W1473` C1246 ontology:80 coolant rule HC floor `≥ 300.0`: as W1469
- `W1477` C1255 ontology:98 CO tailpipe normal `0.1 – 0.45` (seed): as W0185
- `W1478` C1256 ontology:99 CO2 tailpipe target `14.5 – 16.0`: as W0197
- `W1483` C1263 ontology:110 RICH_MIXTURE CO `0.5 – 15.0`: floor 0.5 % differs from the wiki RICH_MIXTURE CO > 1.5 % (W0408)
- `W1485` C1265 ontology:112 RICH_MIXTURE O2 `0.0 – 1.0`: maximum 1.0 % differs from the wiki RICH_MIXTURE O2 < 0.5 % (W0410)
- `W1487` C1267 ontology:114 RICH_MIXTURE λ `0.5 – 0.97`: maximum 0.97 differs from the wiki RICH_MIXTURE λ < 0.95 (W0411)
- `W1506` C1294 ontology:157 RICH_MISFIRE HC `300 – 20000`: the cited vocabulary band real_combustion_fault starts at 250 ppm (W1293), not 300; the wiki gives no HC number for this fault
- `W1522` C1314 ontology:185 HIGH_COMBUSTION_TEMP NOx `1000 – 5000`: as W0438; the vocabulary band the comment cites, high_combustion_temp, is ≥ 1500 ppm (W1322)
- `W1542`–`W1547` C1345–C1350 ontology:239–244 TIMING_OVER_ADVANCED HC `0 – 100`, CO `0.0 – 0.5`, CO2 `13.0 – 16.0`, O2 `0.0 – 0.5`, NOx `1000 – 5000`, λ `0.97 – 1.03`: the wiki idle vector gives HC 120–250 (W0450), CO 0.10–0.30 (W0451), CO2 11.5–13 (W0452), O2 0.8–1.5 (W0453), NOx 20–60 at idle and > 1200 at 2500 rpm (W0454, W0456; the cited vocabulary band is ≥ 1500, W1322), λ 1.01–1.04 (W0455)
- `W1548`–`W1553` C1353–C1358 ontology:251–256 TIMING_RETARDED HC `0 – 100`, CO `0.0 – 0.5`, CO2 `11.0 – 16.0`, O2 `0.0 – 0.5`, NOx `0 – 50`, λ `0.97 – 1.03`: the wiki idle vector gives HC 300–800 (W0461), CO 0.05–0.15 (W0462), CO2 < 11 (W0463), O2 1.5–3.5 (W0464), NOx 0–5 (W0465), false-lean λ 1.05–1.15 (W0466)
- `W1555` C1362 ontology:263 O2_SENSOR_BIASED_LOW HC `0 – 100`: the wiki's silicone-poisoned case for this fault reads HC ~400 ppm (W0481)
- `W1556` C1363 ontology:264 O2_SENSOR_BIASED_LOW CO `0.5 – 3.0`: the wiki gives CO 4–5 % for the silicone-poisoned case (W0480) and 5–8 % for O2-sensor poisoning (W0335), above this 3.0 % maximum
- `W1569`, `W1571`, `W1572`, `W1574` C1381/C1383/C1384/C1386 ontology:292–297 WORN_ENGINE HC `35 – 300`, CO2 `13.0 – 16.0`, O2 `0.0 – 0.3`, λ `0.97 – 1.03`: the wiki gives HC 150–300 (W0487), CO2 11–13 (W0488), O2 1–2 (W0489), λ ≈ 1.0–1.03 (W0490)
- `W1575`, `W1578` C1389/C1392 ontology:304/307 FLAT_CAMSHAFT HC `0 – 100`, O2 `0.0 – 0.5`: the wiki gives HC 150–300 (W0664), O2 1.5–3.0 (W0665)
- `W1585` C1404 ontology:328 GDI_INTAKE_VALVE_CARBON O2 `2.0 – 22.0`: the wiki relation for this fault gives O2 0.8–2.0 % (W0667); this 2.0 % floor excludes it
- `W1590` C1411 ontology:341 VACUUM_REGULATOR_DIAPHRAGM_RUPTURE CO `3.0 – 15.0`: as W0565
- `W1594` C1415 ontology:345 VACUUM_REGULATOR_DIAPHRAGM_RUPTURE λ `0.5 – 0.85`: as W0566
- `W1604` C1434 ontology:381 WORN_VALVE_SEALS HC `75 – 250`: uses the superseded v1 HC range (W0586); the current wiki idle vector gives HC 300–500 ppm (W0573)
- `W1605`, `W1606`, `W1609` C1435/C1436/C1439 ontology:382/383/386 WORN_VALVE_SEALS CO `0.0 – 0.5`, CO2 `11.0 – 14.5`, λ `0.97 – 1.03`: the wiki idle vector gives CO 0.8–1.2 (W0574), CO2 12.5–13.5 (W0575), λ 0.95–0.97 (W0577)
- `W1611`, `W1613` C1444/C1446 ontology:395/397 WORN_PISTON_RINGS HC `0 – 100`, CO2 `14.5 – 16.0`: the wiki idle vector gives HC 100–150 (W0587), CO2 ~14 (W0588)
- `W1619`–`W1621` C1455–C1457 ontology:410–412 rings route at 2500 rpm HC `250 – 20000`, CO `0.8 – 15.0`, λ `0.97 – 1.03`: the wiki rings row gives HC > 300 (W0592), CO 0.5–1.0 and > 0.5 (W0593, W0645), λ < 0.99 (W0596)
- `W1650` C1496 ontology:476 EGR_STUCK_CLOSED NOx `1000 – 5000`: as W0738; the vocabulary band the comment cites, high_combustion_temp, is ≥ 1500 ppm (W1322)
- `W1664`, `W1665` C1522/C1523 ontology:522/523 EVAP_CANISTER_SATURATED HC `100 – 500`, CO `0.5 – 3.0`: the wiki says idle reads normal for this fault and its purge-valve case reads HC 40 ppm / CO 0.12 % at idle (W0756, W0757), below these floors
- `W1688`, `W1690`–`W1693` C1560/C1562–C1565 ontology:578–583 COOLANT_LEAK_INTERNAL HC `300 – 20000`, CO2 `0.0 – 12.0`, O2 `0.0 – 22.0`, NOx `0 – 100`, λ `1.0 – 2.5`: the wiki gives HC 200–400 (W0656), CO2 < 11.5 (W0759), O2 > 2 (W0657), NOx < 30 (W0658), false-lean λ > 1.05 (W0762)

## Decisions the task did not specify

- **Fault signature condition:** a linked ontology row copies the wiki claim's condition. An unlinked row reads
  `<FAULT>, idle baseline` (the ontology header: baseline Euro 4 / warm / cat at `STABILIZED_IDLE`).
- **Which wiki claim is "first":** the wiki sometimes states a fault vector twice: wiki 04 `W0317`/`W0319` give no rpm,
  and wiki 06b `W0698`/`W0702` say idle. I linked the claim whose condition names idle, because the ontology vector is
  an idle vector. NORMAL_OPERATION signature rows link to the wiki NORMAL_OPERATION gas vector (`W0402`,
  `W0405`–`W0407`). The vocabulary §10 thresholds link to the wiki 03 tailpipe values (`W0173`, `W0206`, `W0223`,
  `W0108`). CO and CO2 link to `W0185`/`W0197` in both cases, because the wiki NORMAL_OPERATION rows copy those values.
- **When a value is suspect (R4):** a value is suspect when the wiki states a number for the same fault, gas and
  condition and the ontology or vocabulary value differs, whether the band is wider or narrower. Two kinds are not
  flagged: a 0.97–1.03 band where the wiki says only "≈ 1.0", and NOx 0–100 where the wiki says "≈ 0". Rows where the
  wiki is qualitative (normal, low, variable) are not flagged.
- **Open-ended bands** (both ends at 0 / the analyser envelope) are `INTERNAL_PARAMETER` with quantity
  `<gas> band (unconstrained)`. They have no outside truth: they encode "variable".
- **Payload validator bounds** (vocab §12, C1109–C1121) link to the wiki analyser envelope (`W0060`–`W0064`), because
  the vocabulary states they match it. `lambda_chem` 0.5–2.5 has no wiki claim and is `INTERNAL_PARAMETER`.
- **Speeds:** a 2500 rpm that stands alone in a line (ontology comments `clears at 2500 RPM`, `rpm_dependent`) is
  claimed and linked to `W0121`. The bucket and test speeds link to `W0119` / `W0011`. Section numbers (`§7.x`), enum
  names with digits (`O2_…`), rule ids (`MW-00x`), versions and dates are `NON_DOMAIN`.
- **Enum size** (32 / 34) is `INTERNAL_PARAMETER`, the same as T-GASA-15's `W0006`.
- **Notation:** an ontology `{min, max}` is written `min – max` in `value`. A YAML `max:` alone is written `≤`, and a
  `min:` alone is written `≥`.

## Observations for Cowork (no claims.csv change)

- Ontology comments that cite a vocabulary band whose value differs, where the ontology value still agrees with the wiki
  (so no suspect text): LEAN_MIXTURE O2 2.5 cites `mild_lean` (1.5–4.0); LEAN_MIXTURE λ 1.05 cites §10.7 (no 1.05);
  CATALYST_OVERWHELMED HC 200 and GDI carbon HC 100 cite `real_combustion_fault` (250); CATALYST_OVERWHELMED NOx 500
  cites `elevated_idle` (100–500); POA HC 500 cites `severe_misfire` (800–2000).
- `lambda_measured` upper bound 2.0 (C1115) differs from the 2.5 of `lambda_chem` / `high_idle_lambda`. These are
  different fields, so I did not flag it.
- Possible T-GASA-15 inconsistencies (the wiki rows are out of scope, so I did not change them): `W0404` repeats
  `W0197` but has no `same_as`; `W0098` (`≈ 1.0`) repeats `W0094` (`≈ 1.000`) without a link; `W0995` links `W0001`
  without the `as W0001` text.

## VERIFICATION GATE

| step | command | expected | observed |
|---|---|---|---|
| 1 | `timeout 60 $PY -I check_claims.py --scope vocab_ontology \| tail -4` | `classes …`, `suspect N`, `CLAIMS OK scope=vocab_ontology candidates 488 …`, no `ERROR` | `classes …` (above), `suspect 72`, `CLAIMS OK scope=vocab_ontology candidates 488 covered claims 522`, exit 0; `grep -c ERROR` = 0 |
| 2 | `check_claims.py --scope wiki \| tail -1`; wiki-rows one-liner | P2 line; `wiki rows unchanged: True` | `CLAIMS OK scope=wiki candidates 680 covered claims 1171`; `wiki rows unchanged: True` |
| 3 | seed one-liner | `seeds flagged 3 of 3` | `seeds flagged 3 of 3` (W1298 C1021, W1445 C1222, W1477 C1255) |
| 4 | `git log --oneline fix/T-GASA-15..HEAD && git diff --stat HEAD~1 HEAD \| tail -1 && git status --porcelain` | spec commit + one commit; `1 file changed`; only note and RESULT untracked | `f756425 docs(T-GASA-16) …`, `d7244d9 spec(T-GASA-16) …`; `1 file changed, 522 insertions(+)`; `?? labs/gaslab/audit_tasks/progress_notes/T-GASA-16.md` (RESULT written after this run) |

Extra: `check_claims.py --scope all` → `CLAIMS OK scope=all candidates 1168 covered claims 1693`.
The previous decisive failure is gone: P3 `CLAIMS FAIL 488 error(s)` (all `uncovered`) no longer appears. Step 1 prints
no `ERROR` line and no `uncovered` line.

## CODE REVIEW

- Scope: one data file (`claims.csv`), appended; no code. The batch tool is above and writes only `claims.csv`.
- Header unchanged. `W0001`–`W1171` byte-identical (step 2). The new ids run `W1172`–`W1693` without gaps, in
  `candidates.csv` order (the batch asserts sorted order and no overlap).
- Every `same_as` resolves to an existing claim on another line (the checker enforces this). No `{C…}` token is left
  (`left 0`). No double-encoded field (the checker's mojibake check passes).
- The wiki, the vocabulary, the ontology, the code and `candidates.csv` are untouched (`git diff --name-only HEAD~1 HEAD`
  = `claims.csv` only).
- The task commit was amended once, locally on `fix/T-GASA-16` before any push, to add the `W1506` suspect text. The
  result is still one commit.
- Clean.

## Time

| phase | start | end | minutes | context at end |
|---|---|---|---|---|
| first action → inventory, commit, verification | 2026-11-14T08:30:36Z | 2026-11-14T08:53:59Z | 23.4 | ABSENT (no context meter exposed to the session) |
| note and RESULT | 2026-11-14T08:53:59Z | 2026-11-14T08:56:38Z | 2.7 | ABSENT |
| total | 2026-11-14T08:30:36Z | 2026-11-14T08:56:38Z | 26.0 | ABSENT |

Minutes are computed with a `datetime` one-liner from `date -u +%FT%TZ` reads. The stop rule (90 min) was not reached.
