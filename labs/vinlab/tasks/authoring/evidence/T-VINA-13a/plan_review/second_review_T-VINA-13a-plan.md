Reviewed the plan against R1–R7, the pinned values, and the success criteria. Findings grouped by the requested categories, with severity, quotes, a concrete engine/pair, and a fix.

**1. Ruling not implemented / contradicted**

- **MEDIUM — T1 is extended beyond R3 without a tier.** Assumption 2: *"The whole-`X` key adds 7 pairs (274 against 267). P3's 274 counts it, and R3's own example `M52 B20` is two tokens, so I take it as intended."* R3 defines T1 only as *"a parenthesised alias or the head token"*; the whole normalised description (`M52B20`) is neither the head token (`M52`) nor the paren alias (`206S4`). Example: map `BMW M52B20` ↔ `M52 B20 (206S4)` matches only via this extra key. Fix: drop the whole-`X` key (count those 7 as no-code/other-manufacturer) or promote it to a named tier with its count and three sampled rows, per R3's tier rule. This also changes the pinned `274` T1 composition.

**2. Matching rule that joins the wrong engine**

- **MEDIUM — Numeric/short head tokens join model codes to engine variants.** `_code_keys` emits *"the first whitespace token of `X`"* with no guard. Cowork's own measurement shows 7 all-digit T1 codes, e.g. `PEUGEOT 106 → '106 (XN1)'`, `SKODA 136 → '136 L'`, `ZASTAVA 100 → '100 GL. 0.64'`. `106` is a Peugeot model, not an engine code; the row would present `XN1`'s fields under engine code `106`. Fix: in `_code_keys`, do not emit a head-token key that is all digits or shorter than ~4 alphanumeric chars; count those pairs as no-code and list them in the report.

- **MEDIUM — `GENESIS`→`HYUNDAI` is not a same-company alias.** Alias table: *"`GENESIS` | `HYUNDAI` | 37 | Genesis is a brand of Hyundai Motor Company."* R3's test is a same-company alias (`VOLKSWAGEN` = `VW`); Genesis is a separate marque (Genesis Motor) that TecDoc files as its own manufacturer, not an alternative spelling of Hyundai. Example: the plan's own T0A sample `GENESIS G4DJ` → HYUNDAI `G4DJ` (id 9400). Fix: drop it and count those rows under another-manufacturer, or get explicit same-legal-entity sign-off from Cowork before pinning it.

- **LOW — Family head-token pools are emitted `OK`.** The strict ambiguity rule keeps a field when all ids agree, so `RENAULT F2N` → `F2N 700/704/708/710` (all 1721 cc, 4-cyl, NA, port) yields `status=OK` with a single concrete `displacement_cc`, despite pooling four distinct engines (planned `T1 OK 228`). Fix: when a T1 head-token (non-paren) match resolves to more than one distinct `Description`, set `status=AMBIGUOUS` (or a dedicated `FAMILY` status) even if scalar fields agree, so T-VINA-13b can rule on the merge.

- **Checked, not a defect — petrol filter order.** Option (a) (filter after the tier is chosen) is the correct call: option (b) would let a diesel exact hit fall through to a petrol engine that only shares a head token. The plan's measured difference is 0; just pin the order with a dedicated test/mutant since the `non_petrol=27` count assumes (a).

**3. Field mapping writing a wrong vref value**

- **LOW/MEDIUM — twincharger collapsed to `TURBOCHARGED`.** Derivation table: *"`Turbocharger/Compressor` (twincharger, as the old builder's `турбо/нагнетатель`) → `TURBOCHARGED`."* A twincharger is turbocharged **and** supercharged; writing `TURBOCHARGED` + `has_turbo=1` silently drops the compressor, and the vref vocabulary has no `TWINCHARGED`. Example: VW 1.4 TSI Twincharger engines (`BLG`/`BMY`/`CAVD`). Fix: leave `induction_type` blank for this value and report its count, or keep `TURBOCHARGED` only with an explicit recorded caveat for T-VINA-13b.

- **Checked, not a defect — years/open ends.** `my_start`/`my_end` as calendar years of `From`/`To` matches R4; open `To` → blank matches R4. One unstated choice to record: the plan ignores `0000-00-00` `From` (20 rows) for `my_start`, which R4 doesn't spell out but is the only sane reading. Also note `Turbocharger/Compressor` has no measured count in the table — add it.

**4. Planned test or mutant that cannot fail**

- **MEDIUM — determinism mutant survives as specified.** Row 9: *"test_deterministic (two runs equal bytes, and a run on reversed input rows equals them) | sort | write rows unsorted."* With the mutant, output order comes from the population iteration; reversing `engines.csv` (or any TecDoc table read into an id-keyed dict) does not change that order, so the reversed-run check passes and the mutant is not killed. Fix: reverse/shuffle the fixture **map** CSV (the population source), or assert an explicit expected first/last row, and state which input is reversed.

- **MEDIUM — open-end mutant may not fail.** Row 7: *"test_years_from_cars_with_open_end (one open `To` → `my_end` blank; closed → max) | years | max over non-open `To` only."* The mutant differs from correct behaviour only when a pair mixes an open-`To` car with a closed-`To` car; two disjoint cases ("all open", "all closed") let a defensively-written mutant return blank and pass. Fix: add a fixture with one engine linked to one open-`To` and one closed-`To` car, asserting `my_end` is blank.

**5. Predicted count that does not follow**

- **HIGH — alias-tier counts contradict P4, and the 1,503/643 totals rest on them.** The alias table adds *"`VOLKSWAGEN` | `VW` | 75 (77 before petrol)"* and *"`GENESIS` | `HYUNDAI` | 37"* (T0A = 118), while R3 says the alias count is P4's and P4 pins *"`VOLKSWAGEN`/`VW` 36 ... `GENESIS`/`HYUNDAI` 14"* (alias-relevant sum 54; only `FORD`/`BMWI` match P4 at 2/2). Readiness (c) claims the re-run *"reproduces P3/P4/P5 exactly"*, so the plan's own numbers disagree. Either the T0A measurement is broader than the stated *"T0 code rule"* or it double-counts pairs already captured at T0/T1. Fix: re-measure T0A as "no T0/T1 row, matched at the T0 code rule under the alias" and show it equals P4 per brand; then recompute the total (`1,503`), the no-row split, and the `643` VIN prediction.

**Verdict**
APPROVE WITH CORRECTIONS