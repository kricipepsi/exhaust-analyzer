---
proposal_id: EP-ECU-02
title: ECU fault node — low-side injector-driver failed open / shorted (bank-specific)
target_lab: fault-atlas (new node) → COMLab ECU checker
source: chunks/ecu-diagnosis/03; proposals/OBD_ImplProp.md FAULT 3 & 4 / §2.B
type: fault_node
status: PROPOSAL (consumer = EP-COM-04; refines ERR-EF-007)
date_extracted: 2026-06-07
---

## Signature
Single-bank railed trim with the opposite bank normal:
- **Failed open:** affected-bank Total Trim ≈ +50 %, dead cylinder acts as air pump,
  physical λ falsely lean (O₂ high, CO ≥ 1 %).
- **Shorted (MOSFET fused closed):** affected-bank Total Trim ≈ −50 %, injector stuck
  100 % duty, tailpipe heavily rich (CO ≥ 6 %, λ < 0.85).
The B1-vs-B2 asymmetry is the key tell.

## Proposed consumer + code path
[[EP-COM-04_ecu-hardware-fault-checker]] reading the bank-divergence audit
([[EP-OBD-13_bank-asymmetry-audit]]) + 5-gas λ. Register in `comlab/config/proposals/`.

## Related
[[EP-OBD-13_bank-asymmetry-audit]] · [[EP-GAS-01_5gas-brettschneider-schema]].
