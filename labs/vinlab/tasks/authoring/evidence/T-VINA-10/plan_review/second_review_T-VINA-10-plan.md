The proposed decoder change matches R1–R4, but the plan needs corrections to its known-euro coverage, production-caller check, and wiki claim.

1. **HIGH — The named tests do not protect known-euro horizon and RPM behavior.**

   The plan says: “test 4 (euro4 → ADAPTIVE with EURO_4, HIGH) and the 27 known VINs in `rehearse.py` cover that side.”

   For test 4’s `JF1GG9LK43G020691`, both model year 2003 and euro4 produce ADAPTIVE. Its 1.998-litre naturally aspirated euro4 profile also reaches the ADAPTIVE stress fallback of 3500. Consequently, all nine proposed tests permit these two mutants:

   - Resolve known-euro horizons from model year too.
   - Pass `euro=""` for known euros too.

   No explicitly named assertion distinguishes those mistakes. Merely counting 27 recognised euros does not establish their unchanged outputs.

   **Concrete checks and fix:** Add a known-euro horizon test using `VF7SA5FR8AW511081`: euro5 must retain MODERN despite model year 2010. Add a temporary-row case for `JF1GG9LK43G020691` with recognised euro4, naturally aspirated induction and `displacement_cc=2000`: ADAPTIVE with **4000 RPM**, rather than the 3500 horizon fallback. Name both mutants and their killers; revise test counts.

   This matters downstream: COMLab trusts `resolved_horizon`, so a known euro5 vehicle incorrectly changed to ADAPTIVE would receive different registry selection and threshold masks.

2. **MEDIUM — The wiki incorrectly rules out decoded MODERN vehicles.**

   Quote: “H2 caps decoded years at 2010, so MODERN is never reached by a decoded VIN.”

   `VF7SA5FR8AW511081` is the supplied counterexample: its recognised euro5 gives MODERN under R2, independently of the model-year fallback.

   **Fix:** Say: “Within the supported model-year range, the unknown-euro year fallback cannot produce MODERN. Recognised euro5 and later categories still resolve to MODERN.” Keep the existing known-euro behavior explicit.

3. **MEDIUM — The production-caller probe accepts an import without a call.**

   Quote: “The decisive check is both `f1_` probes passing.”

   The second probe counts textual references, including the proposed import. Consider replacing the unknown-euro branch with:

   ```python
   horizon = (
       Horizon.ADAPTIVE
       if model_year is not None and model_year >= 2001
       else Horizon.LEGACY
   )
   ```

   Leave `_year_to_horizon` imported. This mutant preserves all supported decoder outputs and passes the nine proposed tests; the textual caller probe also passes. Yet the documented helper still has no production call, contrary to R2 and the task’s goal.

   **Fix:** Add a test in the new test file that spies on the decoder’s imported `_year_to_horizon` and verifies a call with `2005` for `JHMAP11305S202318`. Name this mutant and its killer. This avoids expanding the authorised audit-probe edit beyond its population.

4. **LOW — The corpus verdict count is asserted without sufficient recorded evidence.**

   Quote: “no `verdict_differs` key, so 0 verdicts.”

   The embedded material does not establish that the script omits this key precisely when its count is zero. This is an evidence gap, not a demonstrated wrong count.

   **Fix:** Record the script’s relevant aggregation semantics or an explicit verdict comparison. Otherwise report the observed metric as `ABSENT`, with the cause, while separately attributing the expected zero to P3 and Cowork’s survey. Do not modify Cowork’s script.

The counts otherwise reconcile:

- Euro unknown: `541 + 563 = 1,104`; with 27 known, total `1,131`.
- Unknown partitions: `438 + 250 + 416 = 1,104`.
- Changed-year counts: `89 + 59 + 43 + 49 + 50 + 26 + 20 + 25 + 20 + 35 = 416`.
- Corpus: `259 + 19 + 1 = 279` unknown with a year; plus 27 without a year gives 306 decodable.
- Proposed tests: six red and three passing before implementation; `297 + 9 = 306` passing afterward, conditional on the stated fixture updates. Additional tests above require revised predictions.

The proposed **2001 and 2011 boundaries and regulatory dates are correct** against R5. The model-year versus registration-date distinction and one-year fuzz are also stated correctly. The dates support the heuristic bands; they do not establish an individual vehicle’s euro category.

The four assumptions assess as follows:

1. **Right.** Post-window `db_dict` represents the applied row; retaining a row when model year is absent matches the embedded code.
2. **Right within scope.** Vocabulary edits are unauthorised, and f9 already fails. Explicitly recording the additional undocumented flag is appropriate; unchanged failure colour does not mean unchanged diagnostic output.
3. **Right under R5.** The decoder adds the first production caller, restricted to unknown euro; retaining the conditional docstring follows the ruling.
4. **Right about ownership and timestamp noise.** Leave the rehearsal script unchanged and distinguish 303 timestamp differences from the single substantive changed run. The verdict-count inference needs the evidence correction above.

APPROVE WITH CORRECTIONS