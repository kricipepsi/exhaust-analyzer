**Findings**

- `MEDIUM` — The tests leave a one-sided normalization mutant alive. The changed rule is:
  `if db_maf is not None and db_map is not None and not db_maf and not db_map:`
  Change the assignment to `db_maf = None` only, leaving `db_map = 0`. All 9 tests still pass: `assert arch.has_maf_sensor or arch.has_map_sensor` only requires MAF, and the equivalence test uses `PORT_INJECTION`/`NATURALLY_ASPIRATED`/`Emissions()` where the unknown fallback also resolves `has_map=False`.
  Concrete input: `({"has_maf": 0, "has_map": 0}, FuelDeliveryType.GDI, InductionType.NATURALLY_ASPIRATED, Emissions())`. Correct output is `(True, True)` / `DUAL_MAF_MAP_CROSSCHECK`; the mutant gives `(True, False)` / `MAF_ONLY`, leaving the 27 GDI rows effectively unfixed.
  Fix: parameterize `test_zero_zero_equals_unknown` over `PORT_INJECTION` and `GDI`, and assert the exact `(has_maf_sensor, has_map_sensor, strategy)` tuple rather than only comparing against `{}`. Also strengthen the real-VIN test to assert `DUAL_MAF_MAP_CROSSCHECK`.

- `LOW` — The rule is not scoped to injected engines, although its comment justifies it using injection:
  `# with a MAF or a MAP sensor, so 0/0 is not a fact`
  The rule applies to `CARBURETOR` too, where `0/0` can be a true statement. Concrete input: `({"has_maf": 0, "has_map": 0}, FuelDeliveryType.CARBURETOR, InductionType.NATURALLY_ASPIRATED, Emissions())`. After normalization, the fallback `or fuel_delivery_type == FuelDeliveryType.CARBURETOR` makes `has_map_sensor=True`, so a carburettor with no stored sensors is reported as having a MAP sensor and `MAP_ONLY_SPEED_DENSITY`. No current row is affected, so this is latent rather than a present regression.
  Fix: add `and fuel_delivery_type != FuelDeliveryType.CARBURETOR` to the rule, or explicitly change the carburettor fallback/classification so it does not invent a MAP sensor. Add a carburettor regression case if future rows may store `0/0`.

**Check Results**

1. **R1 exactness: PASS.** The diff makes only the mandated `decoder.py` change and adds the new test file. `vref.db` and `build_vref_db.py` are untouched, so R4 is respected. The comment is three lines, but its “injected engine” justification is broader than the rule’s actual condition.
2. **M1–M3: PASS as reported.** The counts are consistent with the code: M1 and M2 remove the rule entirely and fail the two real-VIN cases plus the zero-zero equivalence case; M3 removes the `is not None` guards and fails the `0/None` case. These mutants are killed.
3. **Mutant survival: FAIL.** The one-sided assignment mutant above is not killed. The suite therefore does not prove that both stored flags are cleared.
4. **Population: no measured decode beyond the 13 C6 VINs.** The dnalab/wired/ui/probe suites are unchanged. However, the rule applies to all 68 `0/0` rows, so any VIN resolving to one of the other 55 rows would also change. “13” is a C6-corpus count, not the rule’s total reach.
5. **Consumers: none confirmed.** The reported dnalab 27, wired 41, ui 30, and probe 14 results show no tested consumer breaks. The residual risk is that those suites may not assert the 13 changed payloads’ exact strategy or `primary_load_calculation`.

I did not independently rerun the suites; this review uses the embedded diff and Cowork’s reported counts.

APPROVE WITH CORRECTIONS