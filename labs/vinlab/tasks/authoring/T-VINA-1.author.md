# T-VINA-1 — authoring sidecar (Windows Cowork, 2026-11-03)

### Verified context ###
1. **Findings still reproduce** on `fix/T-AUD-7a` (`9fe682d`): `audit/scratch/C6/test_c6_probes.py` → `33 failed,
   18 passed`; every one of F-C6-1…14 has at least one red probe (observed, 2026-11-03).
2. **The rule (read in `decoder.py`):** `_resolve_year` takes the `ERA_3` row of `L` (2020) for every WMI whose
   `era_hint` is not `legacy` (13,239 of 13,383 rows). `years.csv` gives `A`-`K` only as 2010-2019. The H2 gate is
   `model_year < 1990 or model_year > 2020`.
3. **Scope source:** `labs/comlab/wiki/04_horizon_eras.md:54` (petrol 1990-2010, Euro 1-5); `audit/FIX_PLAN.md`
   T-AUD-9 names "scope cap 2010/Euro 5".
4. **Census (P3, `recheck/T-AUD-9/year_census.py`):** real VINs base: 1,360 ok (273 after 2010), 4 checksum refusals;
   rehearsal: 229 refused as out of scope. Corpus: base 314 ok (267 after 2010); rehearsal 306 ok, 8 refused.
5. **Suites, base vs rehearsal (`recheck/T-AUD-9/suites.sh`):** comlab, dnalab, dtclab, gaslab, obdlab, symptomlab,
   wired identical (`526+4s+2e`, 27, 590, 208, 388, 63, 41); ui `30 passed` both; vinlab `203 passed, 8 skipped` →
   `194 passed, 9 failed` with the rule alone → `215 passed, 8 skipped` with R3-R4. The 9 failures are the R3 list.
6. **Import shadowing works:** with `PYTHONPATH=<copy>`, `vinlab.decoder.__file__` is the copy's, also from
   `apps/wired` (checked); the vinlab suite itself ran from the copy's own folder.

### Rulings and the tradeoff that lost ###
- Scope 1990-2010 at the producer (H2), refusal not flag. Lost: a flag on an out-of-scope decode (F-C6-8 allows
  either): the H2 refusal already exists and every consumer handles `VINDecodeError`; a flag needs a new field and a
  reader (signal/noise rule).
- `L` = 1990 for every WMI; `era_hint` no longer read for the year. Lost: keep `era_hint` as a tie-break: within the
  scope there is no tie left to break, and the hint is wrong for 13,239 WMIs (finding 2).
- Docs in the same row. Lost: a docs-only follow-up row: a code change that leaves 30 lines saying 2020 is new doc drift.
- Base `fix/T-AUD-7a`, not `main` (ledger header). Plan NONE, difficulty 3: every edit is rehearsed by `make_rh.py`.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | SIMULATED | `make_rh.py` copy, run from its folder: `215 passed, 8 skipped` |
| step 2 | SIMULATED | copy: `16 passed`; M1 `10 failed, 6 passed`; M2 `2 failed, 14 passed` |
| step 3 | SIMULATED | `PYTHONPATH` on the copy: dnalab `27`, wired `41`, ui `30 passed` |
| step 4 | SIMULATED | copy: `3 failed, 5 passed`; base `8 failed` |
| step 5 | DEFERRED | the prose edits are the implementer's; base counts `36`, `10`, `0` (measured 2026-11-03) |
| step 6 | SIMULATED | ruff on the copy's 3 files: `All checks passed!` |

### Exclusivity ###
No other implementer runs. T-LOOP-8 closed. The repo is on `fix/T-VINA-1` with the spec commit.

### Progress hook ###
T-VINA-1: model year inside 1990-2010 (`L` = 1990, `B`-`K` refused), docs say 2010, UI placeholder a 2010 Golf.

### Cold read ###
own pass 2026-11-03: anchors 5 (each `grep -cF` = 1 in `decoder.py` or `app.py`; `make_rh.py` asserts each `rep()`
literal once) · counts: 215 = 203 - 4 + 16; 16 = 1 + 2 + 4 + 9 · rule rehearsal: real VINs and corpus (P3), the 9
codes B-K and 4 edges through the real decoder · traceability: criteria 1-5 → steps 1-6; every R3 file has a Files
line (DELETE is a write tag in impl_guard) · JUDGEMENT criteria: 0.
cold read 2026-11-03 FOCUSED reader; trigger grep hit (R6 "every"); 0 findings, 0 patched, 0 not-a-conflict — 22 k tok,
5 calls (`recheck/scratch/coldread_T-VINA-1.md`).

### Correction history ###
- **01 (2026-11-03, Cowork review of round 1; not accepted).** Re-run by Cowork: steps 1-6 as P2 (`215 passed, 8
  skipped`; `16 passed`; 27/41/30; `3 failed, 5 passed`; `0`, `0`, `1`; ruff clean); the 8 suites equal the base
  except vinlab; M1 `10 failed`, M2 `2 failed`, decoder restored byte-identical; code, tests and fixture equal the
  `make_rh.py` copy (CR stripped); docs diff read: every bound says 2010, the comlab source is cited. Codex second
  review (`recheck/codex/T-VINA-1_review.md`, gpt-6.1-sol medium, embedded prompt 44.9 KB): APPROVE WITH
  CORRECTIONS. Rulings: F1 (no test protects the in-scope pick; `row = candidates[0]` survives) UPHELD, re-derived:
  the whole vinlab suite passes on that mutant (`215 passed`), because `years.csv` lists `L,1990` first → R7;
  rehearsed on the copy: `216 passed`, M3 `1 failed`, M2 still `2 failed`. F2 (heading edit vs "keep heading
  text") NOT UPHELD as a defect: the §10.5 heading states the bound, R6.1 required the change, the anchor is kept;
  R6.3 now says so.
- **01, gate:** authoring-checks below; DELTA cold read skipped: the patch adds one rehearsed test and updates counts.
