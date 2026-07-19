# OBDLab PID Log Set

This directory contains the un-quarantine proof test data for OBDLab.
The main test corpus of 38 cases is defined in `logset.json`, which contains realistic, sourced vehicle parameters designed to exercise and move specific channels (lambda, trims, VE, sensor validity, and gates) across the 8-cell coverage matrix, without returning the default `NO_FAULT`/unknown outputs. 
Rejection cases are included to verify input validation boundaries (under `PIDValidationError` and `SemanticConsistencyError`).
Any estimated values are quarantined in `estimated/logset_estimated.json` to keep the primary gate test deterministic and sourced.
All cases pin the post-PURGE `ObdLabDnaView` contract (no `emissions` or `number_of_banks` or `resolved_horizon` fields are carried inside `dna_view`).
The behavioural validation of these cases is performed by the wiring-gate test in task **T-OBDV2-1b**.
