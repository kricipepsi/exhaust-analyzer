> **Context:** OBDLab HLD v2.0 (2026-06-10) · Module: OBDLab · Section 9 Known Gaps / Accepted Behaviour · Parent document: HLD_OBDLab.md

## 9. Known Gaps / Accepted Behaviour

### Entity: Known gaps

- **`dna_view=None` VE** — Returns `VEValidity.UNKNOWN`, `ve_pct=0.0`; degraded-mode, no crash · Status: **Accepted**
- **`dna_view=None` O2** — Defaults to `NARROWBAND_0_TO_1V`; logged · Status: **Accepted**
- **FU-ECU-2** — PID 0x44 `commanded_equivalence_ratio` ingested with only a numeric check (no λ-range bound) · Status: **Follow-up** — bound to be pinned from wiki
- **Anti-orphan (S4)** — VE/O2/bank/perception fields read by no **live** COMLab path yet · Status: **Expected** — closes when S4 consumer tasks land
- **Doc-bug O2-FU-2** — `SUPPRESS_POST_CAT_TRIM` is not a `TrimAnalyticsGate` value (chunk o2-logic/06) · Status: **Logged, not an edge**

## Graph relations (explicit)

**FU-ECU-2** DESCRIBES **commanded_equivalence_ratio λ-range bound gap** (follow-up, pin from wiki)
**Anti-orphan (S4)** DESCRIBES **forward-registered fields without live COMLab reader** (expected divergence until Stage 4)
**Doc-bug O2-FU-2** DESCRIBES **SUPPRESS_POST_CAT_TRIM not in TrimAnalyticsGate** (logged, non-edge)
