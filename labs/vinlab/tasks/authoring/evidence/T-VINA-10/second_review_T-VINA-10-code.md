The decoder change follows R1–R4 and the C2–C4 corrections. I found no demonstrated unreported production change, but the embedded evidence leaves two test gaps, one inaccurate wiki statement, and one unsupported RESULT inference.

1. **MEDIUM — Normalisation and blank euro values lack regression tests.**

   The implementation correctly uses:

   ```python
   euro_known = (db_dict.get("euro_norm") or "").strip().lower() in _EURO_MAP
   ```

   However, recognised test values are lowercase, and the unrecognised `"Euro IV"` remains unrecognised even without `.lower()`. Removing `.strip()` or `.lower()` therefore survives these 12 tests. No test supplies a blank string.

   **Concrete input:** `JF1GG9LK43G020691`, with EJ20 `displacement_cc=2000` and `euro_norm=" EuRo 4 "`. Expected: EURO_4, ADAPTIVE, stress 4000, no `euro_unknown`. A normalisation mutant instead produces EURO_1, fallback 3500 and PARTIAL confidence.

   **Fix:** parameterise recognised mixed-case/whitespace values and unknown `""`/whitespace values. Assert category, horizon, stress and flag, and demonstrate that normalisation mutants fail.

2. **MEDIUM — No test separates a recognised euro from the no-model-year fallback.**

   The correct branch order is:

   ```python
   if euro_known:
       horizon = euro_to_horizon(_euro_emission_category)
   else:
       ...
       horizon = _year_to_horizon(model_year) if model_year is not None else Horizon.LEGACY
   ```

   But the only no-year test explicitly has **no row**:

   ```python
   dna, flags = _decode(vref_copy(), NO_YEAR_VIN, monkeypatch)
   ```

   A mutant that gives every yearless decode LEGACY passes this file: every recognised-euro fixture has a year.

   **Concrete input:** `model_year=None`, applied row with `euro_norm="euro5"`. The existing window check retains that row when the year is absent. Expected: EURO_5, MODERN, no `euro_unknown`.

   **Fix:** add a yearless decode with a recognised applied row, assert those values, and kill the “no year always means LEGACY” mutant. This is a coverage gap; the submitted implementation handles it correctly.

3. **MEDIUM — The wiki overstates the registration deadlines.**

   It says:

   > “Euro 3 is compulsory for every new petrol car registered from 2001-01-01”

   and:

   > “Euro 5 is compulsory for every new car registered from 2011-01-01”

   These statements reproduce R5, so this is an inherited specification error rather than an implementation deviation. The legislation includes later deadlines: the Euro 3 registration provision distinguishes passenger vehicles above 2,500 kg, while the Euro 5 provision includes a 2012 exception for vehicles fulfilling specific social needs. [Directive 98/69/EC](https://eur-lex.europa.eu/legal-content/en/TXT/?uri=CELEX%3A31998L0069), [Regulation 715/2007, Article 10(3)](https://eur-lex.europa.eu/legal-content/EN/ALL/?uri=celex%3A32007R0715).

   **Concrete input:** a petrol passenger vehicle above 2,500 kg registered during 2001 is outside the wiki’s universal Euro 3 claim.

   **Fix:** qualify these as the general EU deadlines, identify the exceptions, and retain 2001/2011 as the decoder’s chosen heuristic boundaries.

4. **LOW — The RESULT extrapolates the real-VIN rehearsal to the corpus.**

   It states:

   > “NOT RUN on the build: the step-4 rehearsal (`total 0`) already shows that the patch is a no-op there.”

   The displayed build rehearsal covers 1,131 real VINs. It does not establish the result for the separate corpus population of 306 decodable cases.

   **Concrete input:** P3’s single changed 2010 corpus case; its built-decoder outcome is not demonstrated by the displayed real-VIN output.

   **Fix:** remove the inference and retain `NOT RUN`, or run the built corpus comparison and report field-level changes with timestamp noise excluded. The RESULT already acknowledges this limitation elsewhere.

I re-derived the supplied counts: the ten yearly counts sum to **416**; `563 + 541 = 1,104` euro-unknown decodes; and the 12 tests yield the claimed base split of **7 failing, 5 passing**. I found no count discrepancy or inherently non-failing test. The embedded production code handles windowing, NULL, blank, case, unrecognised strings and absent years consistently with the rulings. The original plan and test execution were unavailable for independent verification.

APPROVE WITH CORRECTIONS