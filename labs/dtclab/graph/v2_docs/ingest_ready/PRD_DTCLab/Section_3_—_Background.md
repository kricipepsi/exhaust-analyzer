
> **Context:** DTCLab PRD v2.0 (2026-06-11) · Module: DTCLab · Section: Section 3 — Background · Parent document: PRD_DTCLab.md
## Section 3 — Background

**Context.** OBD-II stores up to three DTC lists: confirmed (mode `$03`), pending (mode `$07`),
permanent (mode `$0A`). Each confirmed DTC carries a freeze-frame snapshot of PIDs captured when
the fault was set. Mode $06 continuous monitors provide a margin percentage showing how close each
system is to failing its test.

**Why now.** The 32-entry `routing_tag_map.yaml` (27 ungated + 5 DNA-gated) covers all major
petrol powertrain DTC families. The 33-MID `mode_06_hex_dictionary.json` covers universal CAN MIDs
for 2008+ vehicles. The Phase-2 scorer lets DTC evidence feed COMLab's Bayesian fusion as ranked
candidates rather than raw tags.

**What recently became possible.** Two cross-field signatures (`COOLANT_SYSTEM_MALFUNCTION`,
`CYLINDER_FLUID_MISFIRE`) read DTC + fuel-system status together to flag fluid-intrusion faults
that no single DTC names.

---


## Graph relations (explicit)

**Section 3 — Background** DESCRIBES **DTCLab PRD v2.0**
