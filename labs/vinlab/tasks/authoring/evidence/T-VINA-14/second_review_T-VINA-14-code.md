The implementation matches R1–R3 for valid extract rows. I found two test gaps, but no demonstrated decoder or coalescing defect in the supplied code.

1. **MEDIUM — No regression test proves the guards receive the coalesced values.**

   The implementation correctly uses:

   ```python
   if _g1_map_banks(row, map_rows):
   ...
   if _g2_cylinder_heuristic(row, map_rows):
   ```

   However, changing either argument back to `group[0]` would escape the added tests. The blank-coalescing test supplies no map that exercises either guard.

   **Concrete inputs and fixes:**

   - G1: BRANDA has blank `is_v_engine`; BRANDB states `"0"`; the map states `V6` with six cylinders. The coalesced `"0"` must allow insertion. Running G1 on BRANDA incorrectly skips it.
   - G2: BRANDA has blank displacement; BRANDB states `"1198"`; both state cylinder count `"4"` and `is_v_engine="0"`. Supply a SKODA map with blank displacement and cylinder count. The coalesced displacement produces the documented three-cylinder hint, so G2 must skip it. Running G2 on BRANDA incorrectly inserts it.

   Add both tests and mutations restoring `group[0]` independently.

2. **LOW — R2’s empty-string case lacks a discriminating test.**

   Production code correctly checks:

   ```python
   induction_stated=bool((db_dict.get("induction_type") or "").strip())
   ```

   The new tests exercise stated NA and SQL NULL, but not a blank string. This plausible mutant survives those cases:

   ```python
   induction_stated=db_dict.get("induction_type") is not None
   ```

   **Concrete input:** use `AZQ_ROW` with `induction_type=""`. R2 requires the turbo hint to apply; the mutant incorrectly preserves NATURALLY_ASPIRATED.

   **Fix:** parameterize the fallback test over `None`, `""`, and whitespace, and require TURBOCHARGED for each.

The other requested checks do not establish additional defects:

- **Ruling mismatch:** none demonstrated. R1 preserves BOXER while letting stated zero override map V/W; R2 reads the applied row after the window check; R3 removes precisely the specified clauses.
- **Values without a stated source:** a newly inserted SKODA 1198 cc row with NULL induction and unknown map cylinder count can acquire TURBOCHARGED from the heuristic. That follows R2’s explicit NULL exception. The fallback’s possible second-bank override is explicitly out of scope.
- **Coalescing:** sorting occurs before `_coalesce`; `"0"` remains a stated value; three distinct displacement values are rejected; the guards receive the coalesced row. The `RuntimeError` branch is unreachable because `_skip_reason` returns `"collision"` whenever `row is None`.
- **Counts:** they reconcile: `35 − 2 + 5 + 2 = 40`; `1,186 + 9 + 37 + 34 + 40 = 1,306`; `1,234 + 40 = 1,274`; and `568 + 479 + 68 + 16 = 1,131`. Tests reconcile as `20 + 5 + 7 = 32` and `281 + 12 = 293`.
- **RESULT:** no supplied claim is contradicted. The omitted binary database and mutant execution records prevent independent confirmation of existing-row preservation and all nine mutant kills; that is an evidence limit, not proof those claims are false.

APPROVE WITH CORRECTIONS