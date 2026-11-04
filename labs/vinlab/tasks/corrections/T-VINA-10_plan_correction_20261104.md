# T-VINA-10 — plan correction 01 (Windows Cowork, 2026-11-04)

Plan: `repo/labs/vinlab/tasks/progress_notes/T-VINA-10.md` § `## Plan`. Verdict: **APPROVED with corrections C1-C4**,
written into `repo/labs/vinlab/tasks/T-VINA-10_era_from_year_when_euro_unknown(4).md` (§ Routing, R4, R5, R7, Files to
touch). The task file is the spec; this file is the approval record. No hand-back.

## Accepted from the plan
The single edit in `decode_vin_payload` reading the raw euro from the post-window `db_dict`; `""` as the unknown euro
for `stress_idle_rpm`; explicit `Horizon.LEGACY` with no year; the §10.8 content and its citations; the probe edit;
the three named snapshot changes (horizon, stress RPM); assumptions 1, 3, 4; the 9 tests and mutants M1-M5.

## Re-derived by Cowork
- `VIN_VOCABULARY.md` § 4 is the flag table (`engine_not_in_vref`, `coc_null_<field>` rows); the f9 probe is
  `1 failed` on the base.
- Fixture rows: F16D3 2003-2020, 14K4F 1991-2006, RFK 2003-2020 with NULL euro; EJ20 1998-2010 euro4; F20C2, G15SF,
  Z5 absent from `vref.db`.

## Cowork's own finding
- **C1** (assumption 2): an undocumented new flag is a known drift. `labs/vinlab/docs/VIN_VOCABULARY.md` § 4 gains the
  row the plan drafted (`euro_unknown` … PARTIAL). The f9 probe stays red for its two older missing flags.

## Second review (`C:/4DApp/recheck/codex/T-VINA-10_plan_review.md`, codex, embedded): APPROVE WITH CORRECTIONS
- **F1** (HIGH, no test separates the known-euro path): **upheld.** Test 4 gives ADAPTIVE and 3500 by the year and by
  the fallback too. → **C2**: two `PIN` tests: `VF7SA5FR8AW511081` (2010, euro5) stays `HORIZON_MODERN`; EJ20 on a copy
  with `displacement_cc` 2000 (euro4, NATURALLY_ASPIRATED) gives stress 4000, not the fallback 3500. Mutants "year for
  every VIN" and "`euro=""` for every VIN".
- **F2** (MEDIUM, wiki says MODERN is never reached): **upheld.** → **C3**: §10.8 says the unknown-euro year fallback
  cannot give MODERN inside the supported years; a recognised euro5 or later still gives MODERN.
- **F3** (MEDIUM, a hard-coded `>= 2001` passes every test and the textual probe): **upheld.** → **C4**: one `NEW` test
  monkeypatches `vinlab.decoder._year_to_horizon` to return `Horizon.MODERN` and asserts that `JHMAP11305S202318`
  (2005) decodes MODERN, so the decoder calls the cited helper. Mutant "hard-coded threshold".
- **F4** (LOW, "no `verdict_differs` key, so 0"): **not upheld.** `rehearse.py` (Cowork's) increments
  `cs['verdict_differs']` only when the fault codes differ; an absent key is 0.

## Counts after C1-C4
New test file 9 → **12** tests; red run **7 failed, 5 passed** (the two C2 tests are green on the base); step 2
`12 passed`; step 1 `309 passed, 8 skipped`. Other suites as planned.
