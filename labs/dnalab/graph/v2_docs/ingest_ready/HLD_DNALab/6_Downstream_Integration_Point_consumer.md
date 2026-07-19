> **Context:** DNALab HLD_DNALab v2.1 (2026-06-12) · Module: DNALab · Section: 6. · Parent document: HLD_DNALab.md · Boundary contract: SEMANTIC_CONTRACT.md §4.3

## 6. Downstream Integration Point (consumer)

| `VehicleDNA` | Consumer | Status |
|--------------|----------|--------|
| whole payload | COMLab `OrchestratorInboundRequest.vehicle_dna` ingestion | live mirror |
| `schema_version` | COMLab distinguishes the current `1.2` payload (new fields + renamed `engine_state` value) from legacy `1.0`/`1.1` | landed (T-DNA-7 → 1.1, T-DNA-10 → 1.2) |

> **Cross-lab note:** COMLab mirrors `VehicleDNA` and reconciles up to the §4.3 contract.
> DNALab is never blocked on COMLab; the version field is the signal COMLab keys off.

---

## Graph relations (explicit)

**VehicleDNA** CONSUMED_BY **COMLab OrchestratorInboundRequest.vehicle_dna** (live mirror)
**schema_version "1.2"** CONSUMED_BY **COMLab generation detection** (live, distinguishes 1.2 from legacy 1.0/1.1)
**DNALab** DESCRIBES **one-way delivery to COMLab** (DNALab never imports COMLab)
