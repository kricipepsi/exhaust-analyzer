# T-VAULT-PRD-V2-1 — progress note

## Plan

Refresh `labs/obdlab/docs/PRD_OBDLab.md` from v1.0 (2026-05-22) to v2, grounded in the shipped `obdlab/` source
exactly as the sibling v2 docs (HLD/DLD/LLD/ADR/BDD) are. Reconcile every field/bound/enum/exception to the AST
ground-truth from the 2026-06-10 handoff: `OBDLivePayload`=31 fields, `ObdLabDnaView`=7, 8 StrEnums with
`O2FailureMode`={NO_FAULT,STUCK_LEAN,STUCK_RICH,WIDEBAND_OFFSET_CANDIDATE}, `FuelSystemStatus` added (CL/OL/OL_DRIVE/
OL_FAULT), 12 bounds, no live Physics Gate 3, exceptions under `ObdLabError`. Drop every pruned v1 value
(SLUGGISH/DEAD/WRONG_CENTERLINE/HEATER_FAULT, ±100 trim, 8-PID schema). Keep numeric literals' wiki-citation
comments; keep the Truth-vs-Perception framing. Architect-authoring lane — no lab inner-loop/gate; the gate is an
accurate, internally consistent v2 PRD. No code/test edit; no `graph.json` re-extraction. Blocks T-VAULT-DOCPREP-1.

## VERIFICATION GATE

- [x] **Version bumped to 2.0** — header line 3 reads `Version: 2.0`, dated 2026-06-10.
- [x] **No pruned v1 enum value as live** — SLUGGISH/DEAD/WRONG_CENTERLINE/HEATER_FAULT appear only in
  negation/pruning contexts ("pruned … per ARCH-2", "no pruned v1 member … survives", "scan finds zero
  occurrences"). They are not presented as current O2FailureMode values. The live taxonomy is
  NO_FAULT/STUCK_LEAN/STUCK_RICH/WIDEBAND_OFFSET_CANDIDATE (4 values).
- [x] **No stale ±100 trim bound** — the only ±100 reference is the T-W-6 rationale sentence explaining
  the widening *from* OBD-nominal [−100, 99.22] *to* OBD-rail ±127. All bound tables carry ±127.
- [x] **No 8-PID schema** — zero occurrences in the v2 PRD.
- [x] **Physics Gate 3** — referenced only as "removed per FIX-1" and in the v2 scope summary; not
  presented as a live gate. Live gates are Physics 1/2/4.
- [x] **HIGH_IDLE_LOAD** — referenced only as "permanently retired"; not presented as a live enum value.
- [x] **Readability gate** — zero `![][` image placeholders. Document is plain markdown with text tables
  and LaTeX-free formulas (ASCII bounds notation). Full read confirmed (no truncation).
- [x] **No code/test/graph touched** — only `docs/PRD_OBDLab.md` was written. No `.py`, `.json`, or
  `graph.json` file modified.
- [x] **Numeric literals carry wiki citations** — all bounds and constants tables include `wiki:` source
  comments (§3.1, §6.4, §10.1, T-W-6, research/chunks/*).
- [x] **Cross-references resolve to v2 docs** — HLD §3 (pipeline), HLD §4 (VE), HLD §5 (O2), HLD §6
  (trim gate), HLD §7 (COMLab integration), LLD §1 (constants), LLD §2 (bounds), DLD §2 (vocabulary),
  DLD §4 (payload). Spot-checked; all section numbers match the shipped v2 docs.

**Result: ALL CHECKS PASS.** The PRD is a clean v2 document with no stale v1 value presented as live.

## CODE REVIEW

### What changed vs v1.0, section-by-section

**Header:** Version 1.0 → 2.0. Date 2026-05-22 → 2026-06-10. Scope updated from "v1" to
"v2 — OBD live-PID analytics module (revive-as-emitter rework)".

**§1 Summary:** Complete rewrite. Updated field counts (21→31 payload, 10→12 bounds). Added
7-step pipeline description. Added O2FailureMode (4-value), FuelSystemStatus, MAF linearity.
Replaced "4 Physics Gates" with "Physics Gates 1/2/4 (Gate 3 removed)." Added revive-as-emitter
context (T-OBDV2-0). Updated exception handling reference. Truth-vs-Perception framing preserved.

**§2 Contacts:** Updated COMLab Team responsibilities to reflect v2 consumer surface (perception
delta, bank asymmetry, VE evidence, O2 failure mode). Added MAF linearity to OBDLab Owner row.

**§3 Background:** Rewritten. Added v2 rework summary (10 new fields, trim widening, O2 taxonomy
replacement, Physics Gate 3 removal). Added MAF linearity monitoring description. Added
guarded-emitters pattern rationale with forward-registered COMLab consumers.

**§4 Objective:** KR4 updated (10→12 fields). Added KR5 (O2FailureMode taxonomy = 4 values,
no pruned v1 member). Added KR6 (every payload field has named consumer per signal/noise).

**§5 Market Segment:** Unchanged.

**§6 Value Proposition:** Expanded. Added O2 failure mode classification, MAF linearity
monitoring, per-cylinder misfire counting, per-bank trim delta, lambda perception delta. Added
OBD-rail trim bounds rationale (sensor-fault signal preservation). Added emitter-only stance.

**§7 Solution — Key Features:** All P0 items updated. "10 fields" → "12 fields" for bounds.
"4 Physics Gates" → "3 Physics Gates (1/2/4; Gate 3 removed)." Added P0 items: O2 failure mode
classification (4-value), FuelSystemStatus tracking, guarded emitters, MAF linearity. "21 fields"
→ "31 fields" for OBDLivePayload. Technology section: added LinearityAccumulator parameter,
ObdLabError exception hierarchy.

**§7 — New tables (no v1 equivalent):** Payload fields (31 rows with types/bounds/citations),
DNA view fields (7 rows), vocabulary enums (8 rows), physical sensor bounds (12 rows with
T-W-6 rationale), physical constants (5 rows). These replace v1's inline prose descriptions
with exact, citation-backed tables matching the shipped code.

**§7 — Assumptions:** Updated from 4 to 7 items. Added O2FailureMode 4-value taxonomy check,
OBD-rail trim bounds rationale, WIDEBAND_OFFSET_CANDIDATE proposal-vs-verdict stance. Removed
stale v1 assumptions. All validation columns reference live test files or consumer tasks.

**§8 Release:** Complete rewrite. v2 Scope summarizes the T-OBDV2-0…11 rework. Deferred items
updated (added FU-ECU-2 PID 0x44 bound). Success criteria expanded from 3 to 7 items, covering
O2FailureMode scan, import isolation, bounds drift guard, and signal/noise consumer check.
