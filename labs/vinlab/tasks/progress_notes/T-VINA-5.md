# T-VINA-5 progress note: WMI brand table and engine-map keys (F-C6-2)

Task: `repo/labs/vinlab/tasks/T-VINA-5_wmi_brand_table(4).md` (plan: REQUIRED). Session 1 = precheck + plan, stop at
the plan gate. No production edit made.

## Baseline (read-only)

- `cd C:/4DApp/repo && git branch --show-current && git rev-parse --short HEAD && git status --porcelain` →
  `fix/T-VINA-5`, `d13b885` (`spec(T-VINA-5): …`, parent `448c3ac`), porcelain empty. **Base = `d13b885`.**
- Preconditions loop → `checked`, no `MISSING`, no `EXISTS`.
- P1: `grep -n "^WDB,\|^KMH,\|^JSA,\|^JN1,\|^SAX," labs/vinlab/vinlab/data/wmi.csv` → the 5 rows exactly as pinned
  (lines 12288 JN1 Datsun SWITZERLAND, 12312 JSA Kawasaki, 12365 KMH Genesis, 12895 SAX Sterling Motor Car, 13156 WDB Maybach).
- P2/P3: `(cd audit/scratch/C6 && $PY C:/4DApp/recheck/T-VINA-5/measure.py)` → identical to P2 and P3
  (`real decodes by (WMI, make): [(('JN1','Datsun'),10), (('JSA','Kawasaki'),19), (('KMH','Genesis'),40),
  (('SAX','Sterling Motor Car'),9), (('WDB','Maybach'),26)]`; engine `JN1 8/10, JSA 19/19, KMH 40/40, SAX 9/9, WDB 25/26`).
- P4: `grep` of `wmi.csv` → Kawasaki `JK1 JK8 JKA JKB JSA JSK JSL LM4 MH4 ML5 RK6 RK7`; Genesis `5NM KMH KMT`; Maybach,
  Datsun, Sterling Motor Car one row each. Matches P4.
- P5: `(cd labs/vinlab && $PY -m pytest -q -p no:cacheprovider --basetemp=C:/4DApp/recheck/T-VINA-5/pt/vbase)` →
  **`229 passed, 8 skipped`** (a first run without `mkdir -p …/pt` gave `224 passed, 8 skipped, 5 errors`, all
  `FileNotFoundError` on the missing basetemp parent; Verification's own `mkdir -p` prevents it).
- C6 probe base: `$PY -m pytest -q -p no:cacheprovider audit/scratch/C6/test_c6_probes.py -k f2_ --basetemp=…/pt/c6base`
  → **`6 failed, 45 deselected`** (every case fails `assert expected_make in d.make.upper()` on the wrong make).
  Whole C6 file: `22 failed, 29 passed`.
- `git status --porcelain` after all base runs: empty.

## Readiness challenge

- (a) Starting state matches: branch `fix/T-VINA-5`, HEAD `d13b885` child of `448c3ac`, tree clean; P1-P5 reproduce.
- (b) Fails for the intended reason: C6 `-k f2_` = 6 failed, each on the wrong make (`Maybach`, `Genesis`, `Kawasaki`,
  `Datsun`, `Sterling Motor Car`), not on a decode error.
- (c) Independent expected value: an in-memory simulation (decoder indexes rebuilt from the edited rows, no file
  written) predicts, after R1+R2 as planned, census `[]` and engine resolved `JN1 9/10, JSA 19/19, KMH 40/40, SAX 9/9,
  WDB 26/26`; each ≥ P3 (`8, 19, 40, 9, 25`). Dropping the wrong-brand rows instead predicts `JSA 11, KMH 37, SAX 6`
  (below P3), so R2 cannot be "drop".
- (d) No contradiction blocks implementation. One open decision (5NM) is put to the plan review below; it does not
  block the five pinned rows.
- (e) Teach-back: the five `wmi.csv` rows take their true makes and the wrong-brand engine-map rows are re-keyed so
  the true brand reaches them wherever it had no row of its own. The decisive check is the census: no real VIN decodes
  to a wrong-brand make, and per-WMI engine resolution is not below P3, pinned by `test_wmi_brands.py` and its mutants.

## Assumptions worked past

1. **Spelling = upper case** (`MERCEDES-BENZ`, `HYUNDAI`, `SUZUKI`, `NISSAN`, `ROVER`). R1 binds to the map/§12.1
   spelling; `wmi.csv` already holds upper-case precedent (`MERCEDES-BENZ` ×2, `HYUNDAI` ×4, `SUZUKI` ×7, `NISSAN` ×4,
   `ROVER` ×1). §12.1 quotes: `MERCEDES`, `MERCEDES-BENZ`, `MERCEDES BENZ` | `HYUNDAI`, `KIA` | `NISSAN`; SUZUKI and
   ROVER are not dispatched (displacement fallback), so the map spelling `SUZUKI`, `ROVER` applies. No downstream code
   compares the make case-sensitively (`grep -rni` over `apps`, `labs/dnalab`, `labs/comlab/comlab`: no hit;
   `overlay/cylinder_heuristic.py:381` upper-cases).
2. **Country and era cells stay.** `JN1` carries `SWITZERLAND` (wrong: Japan). R1 scopes the manufacturer; the decoder
   reads country only in `_is_non_nhtsa_wmi` (`decoder.py:245-254`), and both `SWITZERLAND` (`_EUROPEAN_COUNTRIES`)
   and `JAPAN` (`_NON_NHTSA_COUNTRIES`) skip the check digit, so the change is behaviour-neutral. Left as a follow-up.
3. The ledger "`# source:` note" of R3 is Cowork's write (I may not edit `PROGRESS.md`); I propose its text in the RESULT.

## Plan

### Source of the wrong names (R3)

`tools/build_wmi_map.py::_load_vpic_wmis` joins `Wmi → Wmi_Make → Make`. vPIC maps one WMI to several makes
(WDB: Mercedes-Benz and Maybach; KMH: Hyundai and Genesis; JSA: Suzuki and Kawasaki; JN1: Nissan and Datsun; SAX:
Rover and Sterling), the query has no `ORDER BY`, and `result[wmi_key] = …` keeps the **last** row SQLite returns.
The CSV-only branch has the same flaw (`LIMIT 1` without `ORDER BY`). The engine map then inherited the wrong keys:
`tools/build_vds_map.py` Pass B (`_pass_b_nio_majority_vote`, lines 143-157, 209-227) keys each Nio VIN by the
`wmi.csv` brand, so the `MAYBACH` rows are a majority vote over real `WDB` (Mercedes) VINs; Pass A adds vPIC
patterns under every make of the WMI.

**Tool fix: not taken.** Any rule that picks the right make among several needs the vPIC tables, and neither builder
can run here: `~/.vinlab-cache` is absent, `ensure_vpic_db` downloads from `corgi.cardog.io`, `VEHICLE_DATA_ROOT` is
unset (the module raises at import), and the Nio CSVs are not on this host (`find /c/4DApp -maxdepth 5 -iname "*nio*"`:
none). So the data files are fixed directly, `build_wmi_map.py` is untouched, and the RESULT carries the proposed
ledger note: `# source: wmi.csv rows WDB/KMH/JSA/JN1/SAX hand-fixed (T-VINA-5); build_wmi_map.py keeps the last of
several vPIC makes per WMI, so a rerun reintroduces F-C6-2 (test_wmi_brands.py catches it)`.

### R1: `wmi.csv` (5 rows, brand cell only)

`WDB,MERCEDES-BENZ,GERMANY,modern` · `KMH,HYUNDAI,SOUTH KOREA,modern` · `JSA,SUZUKI,JAPAN,modern` ·
`JN1,NISSAN,SWITZERLAND,modern` · `SAX,ROVER,UNITED KINGDOM,modern`.

**Open case 5NM — proposed change to `HYUNDAI` (Cowork rules; drop it with a one-line correction).** The evidence is
one in-repo fact plus one external fact. In-repo: the decoder emits a make only for model years 1990-2010 (it raises
`Year out of supported scope 1990-2010`). External, not checkable on this host: Genesis became a separate make in
November 2015, and 5NM is Hyundai Motor Manufacturing Alabama (Santa Fe, from 2006). So every 5NM VIN that decodes is
a Hyundai, which is the KMH defect by the same mechanism. Population on host: **0** real 5NM VINs (`real_vins()`), so
false pass and false fail on real VINs are `ABSENT`. Rejected alternative: leave it. That is the right call if Cowork
does not accept an external fact as evidence under R1.
**KMT stays `Genesis`.** It is Genesis Motor's own WMI (2016+, outside the year scope). **All Kawasaki WMIs other than
JSA stay.** P4's `JK1 JK8 JKA JKB LM4 MH4 ML5 RK6 RK7` are Kawasaki motorcycle plants. I have no evidence either way
on `JSK`/`JSL` (inside Suzuki's `JS` block), so R1's default holds: unchanged, listed as a follow-up.

### R2: the engine-map rows keyed by the wrong brands

Rule (**right brand wins; a wrong-brand row only fills a key the right brand misses**): for each wrong→right pair
(MAYBACH→MERCEDES-BENZ, GENESIS→HYUNDAI, KAWASAKI→SUZUKI, DATSUN→NISSAN, STERLING MOTOR CAR→ROVER) and each
wrong-brand row with `vds_full` (none of the 10 brands has a `pos_8_only` row: measured 0):
- if the decoder's own lookup for the right brand already hits that `vds_full` (exact `R_vds` **or** folded
  `fold(R)_vds`; the folded check matters for Mercedes, whose map also holds 206 `MERCEDES BENZ` rows), the existing
  right-brand row wins and the wrong row is not copied;
- otherwise a copy of the row with `brand = R` is added, every other cell verbatim (engine code, displacement,
  `majority_share`).
- The originals: `MAYBACH`, `DATSUN`, `STERLING MOTOR CAR` are carried by no WMI after R1 (P4: one WMI each), so their
  rows are **re-keyed (moved)**: the originals are deleted and git keeps them. `GENESIS` and `KAWASAKI` are still read
  by `KMT` (and by `5NM` if the 5NM change is rejected) and by the Kawasaki WMIs, so their originals **stay** and only
  the copies are added.

Counts (measured in memory, `vds_full` collisions via exact or folded key):

| wrong brand | rows | collide (same / differ) | copied to right brand |
|---|---|---|---|
| MAYBACH | 131 | 103 (23 / 80): 54 via `MERCEDES-BENZ`, 49 via `MERCEDES BENZ` | 28 |
| GENESIS | 130 | 66 (30 / 36) | 64 |
| KAWASAKI | 152 | 25 (18 / 7) | 127 |
| DATSUN | 39 | 18 (7 / 11) | 21 |
| STERLING MOTOR CAR | 28 | 16 (9 / 7) | 12 |

Reconciliation with P2's `44 + 36 + 7 + 11 + 7`: identical except Mercedes, where P2 counts exact `MERCEDES-BENZ` only
(54 overlap, 10 same, 44 differ). With the folded `MERCEDES BENZ` keys the decoder also reaches, 103 collide and 80
differ. Map after the edit: 12,900 − 198 deleted + 252 added = **12,954 rows**. No duplicate exact or folded key is
created, so file order does not change behaviour (exact index is last-write, folded is `setdefault`). I insert each
copy directly after its source row, and edit the moved rows in place, to keep the diff reviewable. The edit is made at
line level (brand prefix replaced on the original text), so quoting and LF endings are preserved.

**Why the right brand wins on the differing keys**, with the rule's false pass and false fail measured on the real
VINs (`real_vins()` population, the 5 WMIs: 104 decoded VINs). "Observed" is the engine code and displacement that
`cylinder_count_resolved.md` lists for that VIN:

| rule | resolved WDB/KMH/JSA/JN1/SAX | code matches observed | displacement matches |
|---|---|---|---|
| base | 25/40/19/8/9 | 13/25/12/6/6 = 62 | 10/19/11/6/7 = 53 |
| **right wins (taken)** | **26/40/19/9/9** | **18/39/17/8/7 = 89** | **20/38/15/9/7 = 89** |
| `majority_share` wins (T-SHIP-3 precedent, rejected) | 26/40/19/9/9 | 14/25/12/6/6 = 63 | 13/20/13/7/7 = 60 |
| wrong row wins (rejected) | 26/40/19/9/9 | 14/25/12/7/6 = 64 | 11/19/11/7/7 = 55 |
| drop wrong rows (rejected) | 26/**37**/**11**/9/**6** | — | — |

- **False pass (a known bias):** many right-brand rows with blank `majority_share` appear to come from the same
  OPSI specimens that `cylinder_count_resolved.md` lists, so this population favours "right wins". The rule's real
  margin is smaller than 89 vs 63. Counter-evidence it wins on: `WDB1400511A086331` (observed `119.970`: wrong row
  `119970` matches, right row `119980`), `WDB12602212002803` (observed `110987`: wrong row matches, right row
  `MB617912` is a diesel code), `JN1BAAN15U0606594` (observed `GA14`: wrong row matches, right row `QG15`), and
  `WDB2010241A317401` (observed `M102102962`: wrong row `102962` matches, right row `102985`).
  Of the 60 real VINs where both rows exist and the codes differ, these **4** are the rule's false fails.
  On **29**, only the right row matches the observed code.
- **False fail on other populations:** none measured. On the 76 real VINs of the right or wrong brands under other
  WMIs (WDD, WDC, JS2, SAR, …), "right wins" changes **0** engine results. "Wrong wins" would change 2
  (`SJNFAAN16U0174039`, `WDD1680311K013197`).
- **Rejected T-SHIP-3 precedent:** that rule settled spelling duplicates of one population. Here the two rows come
  from different populations (Nio WDB vs other WMIs/OPSI), and it scores 63 against 89.

**`majority_share` and `vds_engine_ambiguous`:** both apply unchanged. The share is copied verbatim with its row. The
decoder computes the flag at lookup from the winning row (`decoder.py:776-784`). The votes are not merged into a new
share, because per-code counts are not in the CSV and the populations differ.

**Cylinder effect (§12.1 now reachable):** on the 104 decoded real VINs, 40 change `cylinder_count` (WDB 13, KMH 21,
JSA 4, JN1 2), and every one goes from `0` (unresolved) to a count. None changes from one count to another. No test
holds a VIN of these WMIs except `tests/unit/test_type_code_year.py` (3 WDB VINs, year only, unaffected by the brand;
`grep -rnoE` over `labs/dnalab apps/wired apps/ui labs/vinlab/tests`). So **no existing test's cylinder value changes**.

### R4: `tests/unit/test_wmi_brands.py` (NEW, 12 tests; shared `decoder` fixture, shipped data, no network)

1. `test_real_vin_decodes_true_make[WMI]` ×5: these are the C6 probe's real OPSI VINs, checked by exact equality
   (`WDB1290601F037844`→`MERCEDES-BENZ`, `KMHBF31SPMU250917`→`HYUNDAI`, `JSAEAB35S00110744`→`SUZUKI`,
   `JN1BCAN1480756536`→`NISSAN`, `SAXXNNAZRWD148244`→`ROVER`). Red on base, by design.
2. `test_open_case_wmi_brand[5NM-HYUNDAI]`, `[KMT-Genesis]` ×2: read `decoder.wmi_index`. If Cowork rejects the 5NM
   change, the first case becomes `5NM-Genesis` (or is removed) and the count drops to 11.
3. `test_engine_resolved_not_below_base[WMI]` ×5: floors are P3 (`WDB 25, KMH 40, JSA 19, JN1 8, SAX 9`).
   - **Real VINs:** the test reads them from inside `labs/vinlab/` by the same regex as `c6_lib.real_vins`
     (`labs/vinlab/*.md|*.csv`, `Path(__file__).parents[2]`), with no import from `audit/`.
   - **Count:** a VIN counts when it decodes and `decoder._resolve_engine(d.vin, d.make, [])` returns an `engine_code`.
   - **Floors and denominator:** all floors are > 0, so an empty population fails. On base this test is green
     (25/40/19/8/9 ≥ floors), because it is a non-regression guard; its red is shown by mutant M6.
   - **False fail:** a later row that tightens decode scope (the year rules) could lower a count. The test message
     prints the counts so that is visible.

**Mutants** (copies kept in `C:/4DApp/recheck/T-VINA-5/mut/`, copied over the tracked file after the fix commit, test
run, then `git -C repo restore <path>`):

| mutant | change | must fail |
|---|---|---|
| M1-M5 | revert one R1 row each | `test_real_vin_decodes_true_make[<WMI>]` (and, for WDB/JN1/SAX, the count test, since the moved rows are gone) |
| M6 | delete the 252 copied rows | `test_engine_resolved_not_below_base[KMH]`, `[JSA]`, `[SAX]` (predicted 37, 11, 6) |
| M7 | revert 5NM | `test_open_case_wmi_brand[5NM-HYUNDAI]` |

### Commands and the paths they write

1. Edit `labs/vinlab/vinlab/data/wmi.csv` (5 rows, or 6 with 5NM) by exact line replacement. Edit
   `labs/vinlab/vinlab/data/vds_engine_map.csv` with a one-off `$PY -` stdin script: no file is created, the script
   writes only that CSV, and it prints the per-pair counts above as its check.
2. Create `labs/vinlab/tests/unit/test_wmi_brands.py`. Red gate: run it on the data before the edit, so step 1 is
   made after the test is written. Expect the 5 make cases (and 5NM) to fail and the count cases to pass.
3. Inner loop: `py_compile`, then `py -m ruff check` and `--select S`, then `py -m pyright --pythonpath …` on the new
   test.
4. Verification steps 1-5, exactly as written. Predicted: step 1 **`241 passed, 8 skipped`** (229 + 12); step 2
   **`12 passed`**; step 3 `27 / 41 / 30 passed`; step 4 `real decodes by (WMI, make): []` and
   `{'JN1': '9/10', 'JSA': '19/19', 'KMH': '40/40', 'SAX': '9/9', 'WDB': '26/26'}`. C6 `-k f2_`: `6 passed, 45
   deselected`. I also rerun the whole C6 file and name every probe that changes colour (base `22 failed, 29 passed`).
   Writes: `C:/4DApp/recheck/T-VINA-5/pt/*` only.
5. Mutants M1-M7 (writes `…/mut/*`, plus a transient tracked-file overwrite that `git restore` undoes). Then
   `git status --porcelain` must be empty before the next step.
6. Commits on `fix/T-VINA-5`, by explicit path: `fix(T-VINA-5): wmi.csv true makes …`,
   `fix(T-VINA-5): re-key wrong-brand engine-map rows …`, `test(T-VINA-5): …`.
   - **Order:** the test is committed last but written first (the red gate).
   - **Effect on later steps:** the map step changes what the step-4 census and the count test run against. The R1
     step alone gives `KMH 37/40, JSA 11/19, SAX 6/9` until the map step lands, so Verification runs only after both.
7. Write the note's `VERIFICATION GATE`, `CODE REVIEW` and `## Time` blocks, and `tasks/results/RESULT_T-VINA-5.md`.

### Out of scope, held

No edit to `decoder.py`: the join code stays and only data changes. No edit to `build_wmi_map.py` (R3 above). No
year, vref, era, O₂ or petrol-guard change. No push.

### Follow-ups for Cowork (not done here)

- `JN1` country `SWITZERLAND` → `JAPAN` (behaviour-neutral today).
- `JSK`/`JSL` makes: unverified.
- `build_wmi_map.py` keeps the last make: a deterministic rule needs vPIC on the host.
- Several WMI → make mappings may carry the same flaw elsewhere in `wmi.csv`, but this host cannot enumerate them
  without vPIC.

## Plan round 2

Redispatch (correction 01, `tasks/corrections/T-VINA-5_plan_correction_20261104.md`; plan APPROVED with R2-R5).
**Base = `2fd3f8e`** (`spec(T-VINA-5): first-action base line; register T-VINA-12`, descended from `d13b885`):
`git branch --show-current` → `fix/T-VINA-5`; `git status --porcelain` → only `?? labs/vinlab/tasks/progress_notes/T-VINA-5.md`.

### Changes from round 1

- **R1:** exactly the five P1 rows, brand cell only, upper case. **Dropped:** the 5NM change, the open-case tests, M7.
  5NM/KMT stay `Genesis`, JSK/JSL stay `Kawasaki`, JN1 keeps `SWITZERLAND` (RESULT follow-ups).
- **R2:** on the 133 differing keys, the Nio files 1+2 vote picks the winner (tie → right). This replaces "right wins".
  - **Wrong wins:** every right-brand row on the key's folded key is deleted, and a copy of the wrong row is added with
    `brand = R`.
  - **Right wins:** the wrong row is not copied.
  - **Share:** on every differing key, the winner's `majority_share` = winner votes / all votes (files 1+2, 3 dp).
  - **Unchanged from round 1:** same-code collisions (right wins, nothing copied) and keys with no right-brand row
    (copy, share verbatim).
  - **Originals:** MAYBACH, DATSUN and STERLING MOTOR CAR are deleted. GENESIS and KAWASAKI stay.
- **R3:** the tool is not fixed; the ledger note text goes in the RESULT. **R4:** see the tests below. **R5:** the
  order is test → red run → both CSVs → Verification 1-4 → commit → mutants (`git restore` after each) → step 5.

### Parity (before the first edit)

- **Key set.** The decoder's lookup for R hits and the `_normalise_code` codes differ on 133 keys (141 raw),
  by brand MERCEDES-BENZ 74, HYUNDAI 34, NISSAN 11, SUZUKI 7, ROVER 7. This set equals Cowork's JSON keys (0 symmetric
  difference).
- **Vote.** I scanned Nio files 1, 2 and 3 with my own script, on stdin:
  - filters: Pass B's (`P13 == "P"`, 17-char `E-VIN`, non-empty `P15`, `_is_quarantined`);
  - population: the post-R1 `wmi.csv` brand, folded;
  - file 1: 650,000 rows, 3,722 key hits. File 2: 650,000 rows, 3,486. File 3: 506,029 rows, 2,813.
- **Result:** picks wrong **109**, right **24** (15 ties at files 1+2, 0 keys without votes).
  - Held-out file 3: winner **1,872** of 2,813 (right-wins 459, wrong-wins 1,754). File 3 decides 104 keys and the
    vote agrees on **84**.
  - `MERCEDES-BENZ_20102` → wrong `102962` (28 votes against 7, of 57). `NISSAN_BAAN1` → right `QG15` (61 against 56,
    of 120).
  - **Per-key comparison with `C:/4DApp/recheck/scratch/vina5_vote_picks.json`: 0 differences on 133 keys** (all of
    `pick r12 w12 tot12 r3 w3 tot3`). No stop.
- **Test VIN set.** The `labs/vinlab/*.md|*.csv` regex, filtered to the five WMIs, gives 121 VINs. It is set-equal to
  `c6_lib.real_vins()` filtered the same way (121; the whole of `real_vins()` is 1,364). Decoded denominators:
  WDB 26, KMH 40, JSA 19, JN1 10, SAX 9 (= P3).
- **Duplicate-key assertion: SOFT finding**, recorded in `progress_notes/T-VINA-5.blocker.json` (validator `OK`).
  - The base map already holds 123 folded duplicate keys, 119 of them `MERCEDES BENZ` against `MERCEDES-BENZ`.
    "No folded key is duplicated" is therefore unreachable without a Mercedes dedupe outside R2.
  - Chosen interpretation: the script asserts 0 exact duplicates map-wide and no new folded duplicate (after ⊆
    before), and asserts that every key the edit writes has exactly one row.
  - Dry run: 0 exact; folded 123 → 97, 0 new; 361 written keys, all unique.

### Predicted counts (in-memory dry run of the edit)

- **Map:** **12,928 rows** (12,900 → 12,928).

  | wrong brand | copy | same-code | right-wins | wrong-wins |
  |---|---|---|---|---|
  | MAYBACH | 28 | 29 | 17 | 57 |
  | GENESIS | 64 | 32 | 2 | 32 |
  | KAWASAKI | 127 | 18 | 1 | 6 |
  | DATSUN | 21 | 7 | 4 | 7 |
  | STERLING MOTOR CAR | 12 | 9 | 0 | 7 |

  Left after the edit: MAYBACH 0, DATSUN 0, STERLING MOTOR CAR 0, GENESIS 130, KAWASAKI 152.
- **Winners whose new share is below 0.70:** 83 of 133. These keys raise `vds_engine_ambiguous` at lookup. On the 104
  decoded real VINs the flag rises from 42 to 45.
- **Census (step 4):** `[]`; engine resolved `JN1 9/10, JSA 19/19, KMH 40/40, SAX 9/9, WDB 26/26`.
- **Real-VIN outcome table** (`cylinder_count_resolved.md`, worded as agreement; the 104 decoded VINs of the five
  WMIs, split by the serving row's `majority_share`):

  | serving row's share | agrees with the reference | disagrees |
  |---|---|---|
  | numeric | 44 | 38 |
  | blank | 21 | 0 |
  | unresolved (no row) | 1 | |

  The blank rows copy the reference verbatim, so their 21 agreements validate nothing.
- **Cylinder count:** 27 of the 104 decoded VINs change, all from `0` to a count; none changes count to count.
  **Tests whose value changes:** none predicted. The only existing tests holding these WMIs are 3 WDB VINs in
  `test_type_code_year.py`, which check the year only. Step 1 confirms it.

### Tests (`tests/unit/test_wmi_brands.py`, 19)

- `test_real_vin_decodes_true_make[WMI]` ×5, as in round 1.
- `test_engine_resolved_not_below_base[WMI]` ×5: decoded denominator == P3 and resolved ≥ P3 floor.
- `test_conflict_key_winner[R_vds]` ×9: each asserts `decoder._resolve_engine(<WMI+vds+9 zeros>, R, [])["engine_code"]`.

  | pair | vote gave the wrong row | vote gave the right row |
  |---|---|---|
  | Mercedes | `20102` → `102962` (28:7) | `24523` → `266.940` (213:42) |
  | Hyundai | `BT51H` → `G4EA` (753:1) | `VF21M` → `G4DGL` (1:1, **tie**) |
  | Suzuki | `FTA03` → `G16B` (172:2) | `EAK35` → `G13BA310796` (1:1, **tie**) |
  | Nissan | `BCAN1` → `GA14` (20:1) | `BAAN1` → `QG15` (61:56) |
  | Rover | `XWYLM` → `D16Z2` (7:1) | **lacks a side** (0 right picks) |

  Hyundai and Suzuki have no strict right-side vote: their 2 and 1 right picks are all 1:1 ties.
- Predicted: step 2 **`19 passed`**; step 1 **`248 passed, 8 skipped`**.
- **Red run (before the CSV edits):** 10 failed (make ×5; conflict wrong-side ×5, which still return the right row),
  9 passed (count ×5 on base; conflict right-side ×4, already the right row).
- **Mutants:**
  - M1-M5: revert one R1 row → `test_real_vin_decodes_true_make[<WMI>]`.
  - M6: delete the 252 copied rows → `test_engine_resolved_not_below_base[...]`, for the WMIs that lose rows.
  - M8: regenerate the map with every pick inverted → all 9 `test_conflict_key_winner` cases.
  - Each mutant file goes to `C:/4DApp/recheck/T-VINA-5/mut/`, is copied over the tracked file, the named test runs,
    then `git restore`.

### Runtime files

`C:/4DApp/recheck/T-VINA-5/mut/`: `keys.json`, `nio1.json`, `nio2.json`, `nio3.json`, `picks_impl.json`,
`map_dryrun.csv`, and the mutant copies. All are script output; no script file is written there. `impl_guard`
refused a `.py` there, so every script runs on stdin. `D:/` is read only.

## Build log (round 2)

1. **Red run** (`tests/unit/test_wmi_brands.py` on the base data): `10 failed, 9 passed`, as predicted.
   - Make ×5 fail on the old make (`assert 'Maybach' == 'MERCEDES-BENZ'`, …).
   - Conflict wrong-side ×5 fail on the right-brand row's code (`'102985' == '102962'`, `'GAEA' == 'G4EA'`,
     `'M16B' == 'G16B'`, `'G14DS' == 'GA14'`, `'K161.6' == 'D16Z2'`).
   - Count ×5 and conflict right-side ×4 pass.
2. **`wmi.csv`:** 5 exact line replacements by `sed` (`git diff --stat`: 5+/5−), LF kept.
3. **`vds_engine_map.csv`:** a stdin script made a line-level edit, so untouched lines are byte-identical.
   - Counts: same-code 95, copy 252, wrong-wins 109, right-wins 24. Right rows deleted 135, moved originals deleted
     198. Rows 12,928; folded duplicates 123 → 97; written keys 361.
   - All three correction 02 assertions passed: 0 exact duplicates, no new folded duplicate, every written key has
     one row. A parse check on every rewritten line also passed.
   - The output is byte-identical to the dry run. `git diff --stat`: 385+/357−.
4. **Spec change during the build.** `54ed256 spec(T-VINA-5): correction 02 (B7: …)` appeared on the branch
   (12:21:49Z) before my first commit. It rewrites R2's duplicate rule into the three assertions above, which is the
   interpretation in `T-VINA-5.blocker.json`. No change to the work was needed. My commits sit on top of it.

## VERIFICATION GATE

| step | command | result | expected |
|---|---|---|---|
| 1 | vinlab suite | `248 passed, 8 skipped` | plan: 248/8, no failed or error ✔ |
| 2 | `test_wmi_brands.py` | `19 passed` | plan: 19 ✔ |
| 3 | dnalab / wired / ui | `27 passed` / `41 passed` / `30 passed` | 27/41/30 ✔ |
| 4 | `measure.py` | `real decodes by (WMI, make): []`; `{'JN1': '9/10', 'JSA': '19/19', 'KMH': '40/40', 'SAX': '9/9', 'WDB': '26/26'}` | `[]`; ≥ P3 (8/19/40/9/25) ✔ |
| 5 | `.venv-loop` ruff; `git log 448c3ac..HEAD`; porcelain | `All checks passed!`; 5 spec commits + `cb31bd8`, `ed53d94`, `bbc1b6e`; `?? …/T-VINA-5.blocker.json`, `?? …/T-VINA-5.md` (and the RESULT once written) | ✔. The blocker JSON is the header-authorised sibling. |

Previous decisive failure absent:
- C6 `-k f2_`: `6 failed` → **`6 passed, 45 deselected`**.
- Whole C6 file: `22 failed, 29 passed` → `16 failed, 35 passed`. A set comparison against the base data (M0, with
  `git restore` after) shows the fixed cases are exactly the 6 `test_f2_make_matches_wmi_owner` cases, and nothing
  is newly failing. The 16 still failing are f1, f4, f5, f6 and f7, all out of scope.

Mutants (each copied over the tracked file from `C:/4DApp/recheck/T-VINA-5/mut/`, run, then `git restore`):

| mutant | change | failed (named) |
|---|---|---|
| M1 | WDB → `Maybach` | `test_real_vin_decodes_true_make[WDB]`, `test_engine_resolved_not_below_base[WDB]` |
| M2 | KMH → `Genesis` | `test_real_vin_decodes_true_make[KMH]` |
| M3 | JSA → `Kawasaki` | `test_real_vin_decodes_true_make[JSA]` |
| M4 | JN1 → `Datsun` | `test_real_vin_decodes_true_make[JN1]`, `…_not_below_base[JN1]` |
| M5 | SAX → `Sterling Motor Car` | `test_real_vin_decodes_true_make[SAX]`, `…_not_below_base[SAX]` |
| M6 | 252 copies removed (0+/252−) | `…_not_below_base[JSA]` 11/19, `[KMH]` 37/40, `[SAX]` 6/9 (as predicted) |
| M8 | every pick inverted (159+/140−) | all 9 `test_conflict_key_winner` cases |

Code gates on `test_wmi_brands.py`:
- `py_compile` ok; `py -m ruff check` and `.venv-loop` ruff `All checks passed!`; pyright 1.1.410 `0 errors, 0 warnings`.
- `ruff --select S`: 5 × S101 (pytest `assert`). This is the repo convention: the same check on `test_type_code_year.py`
  and `test_decoder.py` gives `Found 131 errors`.
- Import sanity (`from wired import diagnose`, deployed layout) ok; `audit/tools/isolation.py` `violations: 4` (the
  known 4).
- Repo-wide baseline (`baseline.sh`, the other five lab suites): **NOT RUN**. They are report-only, and Cowork runs
  them at review per the task.

**Verdict: CLEAN-WITH-FINDINGS.** Every in-scope gate passed. The finding is S101 in the security selection, the
repo's pytest convention.

## CODE REVIEW

1. **Scope:** the 3 commits touch only `wmi.csv`, `vds_engine_map.csv` and `test_wmi_brands.py`. No change to
   `decoder.py` or `build_wmi_map.py`; the year, vref, era, O₂ and petrol rows are untouched. ✔
2. **Contracts:** no new field or key. `majority_share` is an existing column the decoder reads (`decoder.py:778`). ✔
3. **Provenance:** the test's literals cite their origin: P3 for the floors and denominators, the Nio 1+2 votes in a
   comment on each conflict case, and the C6 probe for the real OPSI VINs. ✔
4. **Boundaries:** the test imports only `vinlab` and reads only `labs/vinlab/*`. No network. ✔
5. **Tests:** the private `_resolve_engine` is used the way the C6 probe and `measure.py` use it. The synthetic
   conflict VINs only feed `vin[3:8]`/`vin[7]`, which are the only positions the resolver reads. ✔
6. **Craft:** the map edit is line-level, so no requoting or line-ending churn. In the diff, 385+/357− = 252 copies +
   109 wrong-wins rows + 24 share rewrites; − 198 moved originals − 135 right rows on wrong-wins keys − 24 old share
   lines. ✔
- **Behaviour change to note:** 83 of the 133 winners now carry a share below 0.70, so `vds_engine_ambiguous` fires
  on those keys. On the 104 decoded real VINs, flags go from 42 to 45. Also on those VINs, `cylinder_count` changes
  for 27, all from `0` to a count. No existing test value changed (step 1).

## Time

| phase | start | end | minutes | context at end |
|---|---|---|---|---|
| precheck + plan | 2026-11-04T09:15:13Z | 2026-11-04T09:25:19Z | 10 | ABSENT (no context meter in this session) |
| round 2: parity + plan | 2026-11-04T12:11:34Z | 2026-11-04T12:21:43Z | 10 | ABSENT |
| round 2: build, verify, mutants, commit | 2026-11-04T12:21:43Z | 2026-11-04T12:27:28Z | 5 | ABSENT |

## Status

**completed** (round 2). Commits `cb31bd8`, `ed53d94`, `bbc1b6e` on `fix/T-VINA-5`, not pushed. Ledger row untouched (stays `pending`). RESULT: `tasks/results/RESULT_T-VINA-5.md`.
