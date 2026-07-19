# T-SEM-3 — progress note

## Plan
We will populate the proposals registry with its first connected EPs (EP-COM-04, EP-COM-05, EP-COM-06, EP-OBD-17, EP-DTC-01, EP-COM-15, EP-OBD-14) in `comlab/config/proposals/entries.yaml`. We will also append the "high-risk index" mapping HR-1, HR-2, and HR-3 to their registered proposals in `comlab/config/proposals/README.md`. No implementation logic is added, and existing `comlab` pytest tests serve as validation.

## VERIFICATION GATE
- **Entries file present:** Verified that `comlab/config/proposals/entries.yaml` is present and contains the 8 connected EPs with non-empty `consumer` and `iso_sae_citation` fields.
- **Verification script check:** Ran the validation python script to assert that `entries.yaml` exists and is present.
- **Ruff check:** Verified that `ruff check comlab/` passes cleanly.
- **Pytest execution:** Confirmed that all 332 tests passed (6 skipped), matching baseline.

## CODE REVIEW
- **comlab/config/proposals/entries.yaml:** Created a single YAML registry file containing entries for EP-DTC-02, EP-COM-05, EP-COM-04, EP-COM-06, EP-OBD-17, EP-DTC-01, EP-COM-15, and EP-OBD-14, matching their target lab, owning ledger, and consumer paths.
- **comlab/config/proposals/README.md:** Updated references to point to `entries.yaml` and appended Section 5 "High-Risk Index" mapping HR-1, HR-2, and HR-3 items to their corresponding EPs.
