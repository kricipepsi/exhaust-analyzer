# ORACLE_TRIAGE_2026-06-30 — Oracle Rederivation Triage Report

This report documents disagreements, ambiguities, and potential engine divergences identified during the rederivation of the wired-v7 test suite oracle. In accordance with strict guidelines, all conflicts have been resolved in favor of the lab wikis (the source of domain truth), and are logged here for future architecture review.

---

## 1. Disagreements (Library vs. Wiki)

### A. EVAP Purge Valve Stuck Open (`ERR-RM-004`)
- **Conflict:** The case library categorizes the purge valve stuck open cases (e.g., `era2_002`, `CASE-025`, `EXT-206`, `EXT-240`) under `lean_condition` because unmetered air/vapor enters the intake at idle. However, the COMWIKI-05 taxonomy table and `rich_mixture.json` classify `ERR-RM-004` (`evap_purge_valve_stuck_open`) strictly within the `rich_mixture` family due to the high-load fuel vapor saturation driving trims negative.
- **Resolution:** Set `expected_fault_family` to `rich_mixture`, overriding the library's `lean_condition` categorization.
- **Follow-up:** Review whether the diagnostic engine should route this as a rich mixture or lean condition depending on engine operating state (load vs. idle).

### B. PCV Valve Failure (`ERR-RM-004` / `P_NEW_11`)
- **Conflict:** The case library places PCV valve failure (`era2_019`) in the `lean_condition` category. However, the physical mechanism draws raw oil and fuel vapors into the intake manifold, causing a rich mixture. In the current taxonomy, it maps to `ERR-RM-004` (`evap_purge_valve_stuck_open`) or `P_NEW_11` (`oil_consumption_pcv_stuck_open` in `mechanical_wear`).
- **Resolution:** Set `expected_fault_family` to `rich_mixture`.
- **Follow-up:** Clarify whether PCV stuck-open failures should be moved to the `mechanical_wear` family (as part of the oil consumption sub-domain) or remain under the `rich_mixture` family.

---

## 2. Ambiguities in current Wiki/Atlas

### A. Ignition Fault vs. Misfire (`ERR-IF-*` vs. `ERR-MF-*`)
- **Ambiguity:** Several cases categorized under `ignition_fault` (e.g., `era3_003`, `CASE-035`, `EXP-N026`) describe misfire symptoms (such as low-speed pre-ignition or spark coil breakdown). The wiki lists `ignition_fault` and `misfire` as separate families. Spark generation failures are mapped to `ignition_fault`, while combustion dropout is mapped to `misfire`.
- **Resolution:** Mapped to the specific active family based on the primary physical cause (e.g., `ignition_fault` for primary/secondary coil drivers, `misfire` for spark plug gap/carbon fouling).
- **Follow-up:** Evaluate if the diagnostic engine should consolidate ignition faults and misfires into a single family, or maintain the current separation.

### B. ECU Logic Inversion (`ERR-EF-006` / `ERR-EF-007`)
- **Ambiguity:** The case library lists logic inversions (`ECU_Logic_Inversion_False_Lean`, `ECU_Logic_Inversion_False_Rich`) as `ecu_fault`. In the wiki and taxonomy table, `ERR-EF-006` (`ecu_fault_lean_bias`) and `ERR-EF-007` (`ecu_fault_rich_bias`) are indeed in `ecu_fault`. However, some cases describe sensor-bias anomalies that map conceptually to `sensor_fault`.
- **Resolution:** Mapped to `ecu_fault` (with code `ERR-EF-006`/`ERR-EF-007`) in accordance with the taxonomy table.
- **Follow-up:** Confirm whether logic inversion represents an ECU software bias or an underlying sensor fault.

---

## 3. Suspected Engine Divergences

### A. Low-Support Families (`ignition_fault`, `non_starter`)
- **Risk:** COMWIKI-12 notes that families with fewer than 10 cases have low support. `ignition_fault` (3 viable cases) and `non_starter` (5 viable cases) fall below this threshold.
- **Resolution:** Retained these cases with family-level expectations.
- **Follow-up:** Monitor driver accuracy in these categories.

### B. Misfire Hallucinations (`ERR-MF-008`)
- **Risk:** Ghost misfires due to AC compressor vibration or DMF play (e.g., `CASE-028`, `EXT-225`, `EXT-226`) expect a `no_fault` or `misfire` (intermittent) verdict. The engine might misroute these to `misfire` due to high CKP jitter.
- **Resolution:** Set expectations to `misfire` (code `ERR-MF-008` for intermittent normal test) or `no_fault` depending on the wiki description.
- **Follow-up:** Audit engine robustness against false misfire DTC triggers.
