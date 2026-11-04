The proposed decoder and merge changes follow R1–R3. I found two test-plan gaps requiring corrections, but no demonstrated wrong decode, coalesce implementation defect, or incorrectly narrowed guard in the embedded evidence.

1. **MEDIUM — R3 G2 has no explicit mutant run.**

   The plan says, “G2 (ii) removal is killed by the same stated-NA test as R2’s tool side,” but its mutant table names only decoder tests for R2:

   > “stated flag ignored” → “banks #4 (and #7 after the merge)”

   Those decoder tests cannot kill a mutation confined to the merge tool. Restoring G2 test (ii) would skip `ZZ5SKQ` again while leaving the decoder tests green.

   **Fix:** Add a separate mutant row restoring the tool’s `stated_na` calculation and induction rejection clause. Run `test_stated_na_heuristic_code_is_inserted` against that mutant and require failure because `ZZ5SKQ` is skipped. This makes the intended coverage explicit and satisfies R4’s named mutant/test requirement.

2. **MEDIUM — The coalesce tests leave important conflict rules unprotected.**

   The implementation rule is correct:

   > “returns `None` when a field holds more than one distinct non-blank value, except `displacement_cc` with exactly two values 1 cc apart”

   But the named rejection tests cover displacement conflicts only. The three-brand test covers a blank plus two compatible values, not three distinct values.

   For a concrete synthetic `ZZ9NEW` group, give BRANDA/BRANDB/BRANDC displacements **1597/1598/1599**. A mutant accepting a sequence whose adjacent differences are 1 would insert it. The named two-brand test, **1597/1599**, still rejects it, and the named first-stating-brand test still passes.

   Similarly, a mutant permitting conflicting non-displacement fields could accept `ZZ9NEW` with `is_v_engine="0"` versus `"1"`; no named coalesce test requires rejecting that conflict.

   **Fix:** Add:
   
   - A three-brand **1597/1598/1599** collision test.
   - A non-displacement conflict test, preferably parametrized over the remaining `COLLISION_FIELDS`.
   
   Name the corresponding mutants and killing tests. These are coverage corrections; the proposed algorithm itself already rejects these cases.

The other requested checks reconcile:

- **Decoder effects:** The seven listed R5 VINs have stated causes: four map BOXER bank changes, RFJ’s TecDoc euro value, and two RGX TecDoc induction changes. AZQ’s induction changes relative to the intermediate R1+R3 decoder, while remaining unchanged relative to the original base. That distinction correctly explains P4.
- **Coalesce and guards:** Alphabetical brand selection, first *stating* brand’s displacement, blank handling, and group-level `status`, `no_my_start`, and `span_gap` checks match R3. G1 retains the blank-flag V/W rejection; G2 retains count and bank checks. No supplied example demonstrates a newly inserted row contradicting TecDoc.
- **Counts:** `31 + 1 + 3 = 35` coalescible groups; two move to `no_my_start`, leaving `33 + 5 + 2 = 40` insertions. The final partition is `1186 + 9 + 37 + 34 + 40 = 1306`. Reach totals `568 + 479 + 68 + 16 = 1131`. Test totals also reconcile: `281 + 7 + 3 = 291`, and `23 + 7 = 30`, with the predicted red run `8 failed + 22 passed`.

APPROVE WITH CORRECTIONS