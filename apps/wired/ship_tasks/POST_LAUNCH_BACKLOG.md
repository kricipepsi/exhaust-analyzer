# Post-launch backlog — registered 2026-07-07 (T-SHIP-4)
Non-blocking items carried past publish. Each is a registered row, not a spec —
author the spec when a row is activated. None of these may be picked up as
score-chasing (owner stop ruling 2026-07-06).

| ID | One-liner | Source | Gate |
|---|---|---|---|
| BL-1 | Registry rule for `case_046` P0190 fuel-rail-pressure sensor (no matching KG node) | `registry/docs/REGISTRY_PROGRESS.md` follow-ups | none |
| BL-2 | Charging-system P0620–P0626 coverage — DTC wiki update first, then `REG-V2-AUTHOR-charging_system-v2` | same | wiki task first |
| BL-3 | `EXP-N023` VVT-solenoid drift uncoverable — needs richer OBD capture (protocol, not code) | same | real-data capture |
| BL-4 | `T-COM-CAMTIMING-MAF-1` — `_MAF`-variant cam-timing registry rules | comlab ledger (forward-registered 2026-06-28) | none |
| BL-5 | 4 deferred gas-delta columns (`gas_delta_{hc,co,co2,o2}`) — C3A/C9A showed non-load-bearing | C9B closing note | real two-point data |
| BL-6 | Abstain-cal (MARGIN retune/dedupe) — parked at 0.02; masked tally 19 (12 C3 + 5 C6 + CASE-022 + EXT-216) | owner ruling 2026-07-06 | owner |
| BL-7 | CASE-022 covered-wrong (systematic under C4/C5 precedence) — needs C6 sensor-dynamics data for the case | C4B review addendum | real data |
| BL-8 | MF-001 HC/O2 SUGGESTIVE-row overlap with head-gasket chemistry — 0.001 knife-edge demotes MW-003 single verdict (abstains, family shown rank 2). Candidate: chemistry-state guard on MF-001's gas rows, decided on real data | T-SHIP-1 F-2 | real data; NOT weight-chasing |
| BL-9 | Empty-chemistry + charging-DTC payload winners: MF-005 outranks CS-001 — review misfire rule firing on evidence-free payloads | T-SHIP-1 F-3 | with BL-2 |
| BL-10 | Rings/PCV reconciles (`T-XLAB-RINGS-RECONCILE-1`, `T-XLAB-PCV-VERIFY-1`, gaslab ledger) | T-PREP-WIRE-1 | **D-SHIP-1 owner ruling** |
| BL-11 | Q-C5-EGR wiki-vs-cluster5 trim-signature conflict — authenticated firecrawl verification, then edit the losing doc | DECISIONS 2026-07-06 | **D-SHIP-2 owner** |
| BL-12 | Graph-lane trust items (GRAPH-TRUST, T-VLIVE-3c) — dev tooling, off runtime path | vault-live ledger | none |
| BL-13 | CS-002 follow-up row in registry ledger can be closed — hard-absence semantics verified 2026-07-07 (T-SHIP-1 §5) | this pack | close on next registry-ledger touch |
