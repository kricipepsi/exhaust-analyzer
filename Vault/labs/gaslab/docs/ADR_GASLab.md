# Architecture Decision Records — GASLab
**Status:** Living index (individual records are immutable once Accepted)
**Version:** 1.0
**Date:** 2026-06-10
**Format:** Nygard template, per `_skills/doc/ADR.md`
**Code baseline:** GASLab v2.1 (34-value surface, dual-RPM input)

This file records the standing architectural decisions that shape GASLab. Records are numbered sequentially and, once **Accepted**, are not edited — a later decision supersedes an earlier one with a new record. Each captures *why*, not *how*; the *how* lives in HLD / LLD / DLD.

| # | Decision | Status |
|---|----------|--------|
| ADR-0001 | Brettschneider chemistry is ground truth over ECU perception | Accepted |
| ADR-0002 | Signal/noise — every schema field needs a named, existing consumer | Accepted |
| ADR-0003 | No cross-lab Python imports — mirror types locally | Accepted |
| ADR-0004 | A declarative YAML ontology is the single source of fault signatures | Accepted |
| ADR-0005 | DNA gates are strict and unconditional, not confidence-weighted | Accepted |
| ADR-0006 | Deterministic specificity ranking with catch-alls last | Accepted |
| ADR-0007 | Retire `WRONG_VALVE_TIMING`; adopt three `CAM_TIMING_*` states (32→34) | Accepted |
| ADR-0008 | Cam-timing states are not DNA-gated; the MAF/MAP split rides a gas discriminator | Accepted |
| ADR-0009 | Optional high-idle (2500 RPM) reading drives RPM-differential separation | Accepted |
| ADR-0010 | Collapse the `target_lambda` low/high pair into a single `target_lambda_v112` window | Accepted |
| ADR-0011 | `confidence` is carried but gates only the `co_high_idle` override | Accepted |

---

## ADR-0001: Brettschneider chemistry is ground truth over ECU perception

**Status:** Accepted

**Context.** A diagnosis must resolve the "DTC says lean, gas says rich" dead end. The ECU reports a *perceived* air-fuel state derived from O₂-sensor feedback and fuel trims, which can be wrong (biased sensor, vacuum leak, mechanical fault). A 5-gas analyser measures the actual products of combustion. We need one of the two to be authoritative when they conflict.

**Decision.** The Brettschneider lambda computed from tailpipe chemistry (`lambda_chem`) is the **ground truth**. The ECU's lambda is *perception*. GASLab emits `lambda_chem` and (optionally) a directly-measured `lambda_measured`; COMLab compares these against the ECU's `normalized_obd_lambda` to detect perception contradictions. GASLab never adjusts its chemistry verdict to agree with the ECU.

**Consequences.**
- Positive: a physically grounded answer that survives a lying sensor; clean separation of "truth" (GASLab) from "perception" (OBDLab).
- Positive: the lambda formula is a pure function — deterministic, testable in isolation.
- Negative: chemistry quality depends on a clean sample, so the validity gates (ADR-referenced in HLD §3) must run first and can halt a diagnosis.
- Neutral: GASLab cannot, alone, prove *intent* faults (e.g. cam phase) — those need OBD/CKP correlation downstream.

**Alternatives considered.**
1. *Trust the ECU and use gas only to corroborate.* Rejected — it reproduces the dead end the product exists to solve; a biased sensor would poison the verdict.
2. *Fuse ECU and gas with a learned weight.* Rejected for v1/v2 — introduces a tuning surface with no first-principles anchor and is hard to make deterministic.

**References.** `PRD_GASLab` §3–4; `GAS_VOCABULARY §6`; the Truth-vs-Perception override principle in the project context.

---

## ADR-0002: Signal/noise — every schema field needs a named, existing consumer

**Status:** Accepted

**Context.** Schemas accrete "might be useful later" fields. Each unused field is a maintenance and correctness liability: it must be populated, validated, kept in sync across the JSON boundary, and reasoned about, while delivering nothing.

**Decision.** Every field added to any GASLab schema (`GasLabPayload`, `GasLabDnaView`, `GasLabContext`) must have a **named consumer** in COMLab analytics or fault-atlas routing, plus the code path that reads it. "Future use" is not a consumer. The consumer may be added in the *same* change (a new field and the new reader ship together), but it must be named and real. If the consumer cannot be named, the field does not ship.

**Consequences.**
- Positive: the contract surface stays minimal and every field is traceable to a reader.
- Positive: review has an objective gate — grep for the consumer, or reject.
- Negative: genuinely forward-looking schema work must be staged as a proposal with a specced consumer, not merged speculatively.
- Neutral: drives an "anti-orphan" check before a task closes (a field read nowhere is a breach even with green tests).

**Alternatives considered.**
1. *Allow reserved fields for forward compatibility.* Rejected — this is exactly the accretion failure mode; reserved fields are never cleaned up.
2. *Gate only on the payload, not the inputs.* Rejected — DNA-view and context fields carry the same sync cost across the boundary.

**References.** Project `CLAUDE.md` "Signal/noise principle"; `GAS_VOCABULARY §12.2` (fields deliberately excluded).

---

## ADR-0003: No cross-lab Python imports — mirror types locally

**Status:** Accepted

**Context.** GASLab, OBDLab, DTCLab, and COMLab must evolve independently. A direct `import` from one lab into another couples their release cycles and lets a change in one silently break another.

**Decision.** GASLab performs **zero** cross-lab Python imports. Types it shares with COMLab are **mirrored locally**: `GasLabDnaView` (the 13-field slice COMLab projects), the `ChemicalSignature` enum, the `GasLabPayload` shape, and `family_map.SIGNATURE_TO_FAMILY`. The cross-lab contract is the **JSON values**, not the Python classes. Two independent declarations of the same enum are intentional and accepted.

**Consequences.**
- Positive: each lab is a fully isolated codebase; the boundary is a typed JSON document.
- Positive: enforceable mechanically (the import-isolation audit fails CI on a cross-lab import).
- Negative: shared enums/shapes are declared twice and can drift — which is why a coordinated cross-lab change is required when the contract changes (see ADR-0007).
- Neutral: COMLab owns its own mirror and validates incoming payloads against it.

**Alternatives considered.**
1. *A shared `common` package of contract types.* Rejected — reintroduces the coupling and a shared release cadence we are avoiding.
2. *Generate mirrors from a single schema file at build time.* Deferred — adds a build step; the hand-maintained mirror plus the drift guard is sufficient at current scale.

**References.** `README.md` boundary note; `GAS_VOCABULARY §13` invariant 6; `SEMANTIC_CONTRACT.md §1`.

---

## ADR-0004: A declarative YAML ontology is the single source of fault signatures

**Status:** Accepted

**Context.** Fault signatures (per-gas bounds, operating state, gates, differentiators) are knowledge, not control flow. Encoding them in Python scatters thresholds through branches and makes them hard to audit against the wiki.

**Decision.** All fault signatures live in `gas_lab_ontology.yaml`, loaded once by `ontology_loader.load_ontology()` with schema validation. The rule engine reads bounds and grammar from the ontology; it does not hard-code signatures. A wiki-drift guard (`audits.parse_vocabulary_thresholds`) compares the ontology's numeric thresholds against `GAS_VOCABULARY.md §10` on every CI run, so the YAML and the wiki cannot silently diverge.

**Consequences.**
- Positive: signatures are auditable in one declarative file; thresholds carry citations.
- Positive: adding/adjusting a fault is a data change plus a test, not a control-flow rewrite.
- Negative: the YAML and the wiki must be changed together or CI fails (by design).
- Neutral: a few genuinely procedural rules (priority overrides, RPM-differential gates) still live in code; the ontology supplies their thresholds.

**Alternatives considered.**
1. *Hard-code signatures as Python constants.* Rejected — not auditable, no drift guard possible.
2. *A database of signatures.* Rejected — adds I/O and infra for a small, static, version-controlled dataset.

**References.** `DLD_GASLab §8, §9, §11`; `ontology_loader.py`; `audits.py`.

---

## ADR-0005: DNA gates are strict and unconditional, not confidence-weighted

**Status:** Accepted

**Context.** A fault that is physically impossible for a vehicle (a catalyst fault on a catless car) must never be emitted. The DNA view carries a `confidence` field; one design option is to weaken gates when DNA confidence is low.

**Decision.** DNA gates are applied **strictly and unconditionally** in `resolution.apply_differentiators`: if a candidate's gate field does not match the DNA view, the candidate is removed, regardless of `confidence`. Equipment we are unsure about does not earn a fault a second chance through a softened gate.

**Consequences.**
- Positive: no false positives from impossible faults; the gate is simple equality, trivially testable.
- Positive: deterministic — the verdict does not depend on a confidence heuristic.
- Negative: a wrong/missing DNA field can suppress a real fault; correctness of the verdict leans on DNA-projection quality upstream.
- Neutral: `confidence` is still carried for COMLab and used in one narrow, explicit place (ADR-0011).

**Alternatives considered.**
1. *Confidence-weighted gates (relax when DNA is PARTIAL/NONE).* Rejected for the canonical pipeline — it trades a clear, testable rule for a tunable heuristic and risks emitting impossible faults.
2. *Top-N ranked output that keeps gated candidates as low-confidence options.* Exists only in the out-of-scope `ranking.py` (GASLabSimple), not on the `process()` path.

**References.** `LLD_GASLab §7`; `HLD_GASLab §5`; `resolution.py`.

---

## ADR-0006: Deterministic specificity ranking with catch-alls last

**Status:** Accepted

**Context.** Multiple fault signatures can match one reading. The engine must pick exactly one verdict, and the same input must always yield the same output (frozen models, CI grids, reproducible diagnoses).

**Decision.** Surviving candidates are ordered by `_candidate_rank = (is_catch_all, signature_width)`: catch-all faults (`VVT_FAILURE`, `EVAP_CANISTER_SATURATED`, `POA_SIGNATURE`) sort last, then the **narrowest** total signature width wins (more specific = preferred). On an exact tie the winner is the first in ontology declaration order. `min()` over this key is deterministic across process restarts.

**Consequences.**
- Positive: a single, reproducible verdict; specific faults beat broad ones.
- Positive: ties resolve by a stable, declared order — no hidden nondeterminism.
- Negative: declaration order becomes semantically meaningful for tied faults, so the ontology order is part of the contract.
- Neutral: catch-alls remain reachable when nothing more specific matches.

**Alternatives considered.**
1. *Emit all matches and let COMLab choose.* Rejected — pushes the disambiguation cost across the boundary and breaks the "single chemical state" invariant.
2. *Score by a weighted prior.* Rejected — reintroduces a tuning surface; the project flags weight-nudging as a smell.

**References.** `LLD_GASLab §5`; `GAS_VOCABULARY §13` invariant 3; `rule_engine.py`.

---

## ADR-0007: Retire `WRONG_VALVE_TIMING`; adopt three `CAM_TIMING_*` states (32 → 34)

**Status:** Accepted (2026-06-03)

**Context.** The single `WRONG_VALVE_TIMING` value conflated distinct, separately diagnosable cam-timing states. Source research (the 1990–2010 petrol-timings document) describes five first-class timing states: two ignition (retained) and three cam-system-specific.

**Decision.** Retire `WRONG_VALVE_TIMING` and add `CAM_TIMING_RETARDED_MAP`, `CAM_TIMING_RETARDED_MAF`, and `CAM_TIMING_ADVANCED`, bringing the contract surface to **34** values. These states are marked `SPECIFIC`, not `DEFINITIVE`: the tailpipe cannot prove cam phase alone. The GASLab enum and ontology are revised first; the canonical `OBD_VOCABULARY.md §17` mirror, `SEMANTIC_CONTRACT.md`, and the COMLab schema are updated in a **coordinated cross-lab change**. Until that lands, the GASLab side is intentionally divergent.

**Consequences.**
- Positive: three separately routable cam-timing diagnoses instead of one ambiguous label.
- Positive: aligns the enum with the five-state timing taxonomy applied across labs later.
- Negative: a temporary, deliberate enum divergence between GASLab (34) and the COMLab-side mirror (32) until the breaking change is coordinated — tracked, not silent.
- Negative: a breaking change per the change protocol; consumers must update together.

**Alternatives considered.**
1. *Keep `WRONG_VALVE_TIMING` and sub-type it with a side field.* Rejected — adds a field with no clean consumer and hides three diagnoses behind one label.
2. *Add the three states but keep `WRONG_VALVE_TIMING` as an alias.* Rejected — leaves a dead enum value and stale routing.

**References.** `wiki/CHANGE_v2.1_timing_taxonomy.md`; `GAS_VOCABULARY §3, §21`; ADR-0008.

---

## ADR-0008: Cam-timing states are not DNA-gated; the MAF/MAP split rides a gas discriminator

**Status:** Accepted

**Context.** `CAM_TIMING_RETARDED_MAP` vs `CAM_TIMING_RETARDED_MAF` differ by the engine's air-metering system (Speed-Density/MAP vs MAF). The obvious implementation is a DNA field for the metering system used as a gate.

**Decision.** The cam-timing states carry **no DNA gate**. There is no DNA field for MAF-vs-MAP metering, and adding one purely to gate these faults would introduce a field with no other consumer — a signal/noise violation (ADR-0002). Instead the MAP/MAF distinction rides the **gas-direction discriminator** (Speed-Density tends rich; MAF tends lean), corroborated by OBD trims downstream and confirmed by the idle→2500 RPM behaviour (ADR-0009).

**Consequences.**
- Positive: no orphan DNA field; the split is carried by chemistry the engine already has.
- Positive: keeps the DNA view at 13 fields, all with consumers.
- Negative: the MAP/MAF call rests on gas direction plus the high-idle vector, so it needs `reading_high` to be confident; without it the call is weaker.
- Neutral: full phase confirmation still belongs downstream (CKP/CMP in OBDLab/DTCLab).

**Alternatives considered.**
1. *Add an `air_metering_type` DNA field and gate on it.* Rejected — a field whose only reader is this gate; violates signal/noise.
2. *Emit a generic `CAM_TIMING_RETARDED` and let COMLab split it.* Rejected — pushes the discriminable distinction across the boundary and loses the gas-direction signal GASLab uniquely holds.

**References.** `wiki/CHANGE_v2.1_timing_taxonomy.md`; `GAS_VOCABULARY §3.1`; `resolution.py` cam-timing gates.

---

## ADR-0009: Optional high-idle (2500 RPM) reading drives RPM-differential separation

**Status:** Accepted

**Context.** Several faults are indistinguishable from a single idle reading — cam timing vs vacuum lean, weak vs dead catalyst, and the mechanical-wear leaves all overlap at idle. The discriminating information is *how the chemistry changes between idle and ~2500 RPM*.

**Decision.** `GasLabContext` accepts an **optional** second reading at 2500 RPM (`reading_high`). When present it unlocks the RPM-differential discriminators in `resolution.apply_differentiators` (normalise / persist / NOx-rise patterns, catalyst dual-idle, mechanical-wear leaf routing). All fault bound-matching stays scoped to `operating_state: STABILIZED_IDLE`; the high-idle reading is a *discriminator input*, not a new operating-state bucket. When `reading_high` is absent the engine still classifies on the idle reading alone.

**Consequences.**
- Positive: resolves overlapping idle signatures using behaviour over RPM, the physically correct discriminator.
- Positive: backwards-compatible — single-reading callers keep working; the new branches are additive.
- Negative: the strongest separations require the technician to take a second reading; without it some pairs stay ambiguous.
- Neutral: the engine carries both single- and dual-reading code paths.

**Alternatives considered.**
1. *Promote `REGULATORY_HIGH_IDLE`/`STRESS_IDLE` to first-class operating states with their own fault tables.* Deferred to v2 — larger ontology change; the discriminator approach delivers the separation now without duplicating fault tables.
2. *Require two readings always.* Rejected — breaks single-reading callers and the common quick-check workflow.

**References.** `HLD_GASLab §6`; `LLD_GASLab §6`; `process.py` (`GasLabContext.reading_high`).

---

## ADR-0010: Collapse the `target_lambda` low/high pair into a single `target_lambda_v112` window

**Status:** Accepted (supersedes the v1 `target_lambda_low` / `target_lambda_high` pair)

**Context.** v1 carried two CoC fields, `target_lambda_low` and `target_lambda_high`, to express a certified lambda band for NORMAL_OPERATION. In practice the certified value is a single centre point, and a two-field band invites inconsistent or inverted inputs.

**Decision.** Replace the pair with a single `target_lambda_v112` (the certified CoC λ centre). `_coc_adjust_normal_bounds` centres the NORMAL λ window on `[v112 − 0.005, v112 + 0.005]`, clamped to `[0.85, 1.15]`. Absent → the generic ±0.005 window centred on 1.000.

**Consequences.**
- Positive: one unambiguous input; no inverted-band failure mode; window half-width is a single owned constant.
- Positive: smaller DNA view (contributes to the 13-field surface).
- Negative: a fixed ±0.005 half-width cannot express an asymmetric certified band — acceptable given the data available.
- Neutral: a breaking change to the DNA-view shape, handled with the cross-lab projection.

**Alternatives considered.**
1. *Keep the low/high pair.* Rejected — two fields for one certified value, with an inversion hazard.
2. *Make the half-width configurable per vehicle.* Rejected — a second field with no current consumer (signal/noise); revisit only when real CoC data demands asymmetry.

**References.** `LLD_GASLab §8`; `DLD_GASLab §5`; `GAS_VOCABULARY §11`; `rule_engine._coc_adjust_normal_bounds`.

---

## ADR-0011: `confidence` is carried but gates only the `co_high_idle` override

**Status:** Accepted

**Context.** `GasLabDnaView.confidence` (`HIGH` / `PARTIAL` / `NONE`) describes how trustworthy the DNA projection is. ADR-0005 rules out using it to weaken fault gates. The question remains whether it should be consumed anywhere in GASLab at all.

**Decision.** `confidence` is **carried and forwarded to COMLab** but has exactly one functional use inside GASLab: `_rich_co_ceiling` uses the per-vehicle `co_high_idle` as the rich-CO ceiling for the `CAM_TIMING_RETARDED_MAP` branch **only when `confidence == "HIGH"`**; otherwise the Euro-scaled default applies. There is no other branching on `confidence` in the canonical pipeline.

**Consequences.**
- Positive: a per-vehicle CoC limit is trusted only when the lookup is high-confidence; otherwise a safe class default is used.
- Positive: the field earns its place (it has a named reader) without becoming a broad heuristic.
- Negative: a subtle, easily overlooked coupling — documented here precisely so it is not mistaken for general confidence weighting.
- Neutral: COMLab may use `confidence` for its own purposes independently.

**Alternatives considered.**
1. *Ignore `confidence` entirely in GASLab.* Rejected — then `co_high_idle` would be trusted blindly even on a low-confidence lookup.
2. *Use `confidence` to weight all per-vehicle overrides.* Rejected — broadens into the heuristic ADR-0005 declines; one explicit gate is enough.

**References.** `LLD_GASLab §7, §9`; `DLD_GASLab §5`; `resolution._rich_co_ceiling`.

---

## Maintenance

New decisions append as **ADR-0012+** with status **Proposed**, then **Accepted** after review. To change an accepted decision, write a new record that **supersedes** the old one (set the old record's status to *Superseded by ADR-####*) — never edit an accepted record in place.
