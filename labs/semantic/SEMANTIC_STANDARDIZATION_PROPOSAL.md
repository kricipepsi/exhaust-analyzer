# Semantic-Vocabulary Standardization — Audit & Proposal

**Author:** architect (4DLab)
**Date:** 2026-06-08
**Status:** proposal for owner review — no task rows registered yet
**Inputs audited:** `StandardProp.md`, `SAE.md` (J2012 DEC2007 full text), `obd2-pid-table-service-01.csv` (J1979 Service 01), `vocabul/{SEMANTIC_CONTRACT,OBD_VOCABULARY,GAS_VOCABULARY,DTC_VOCABULARY}.md`, and the live code: `comlab/comlab/schemas/{vocabulary,response,kg}.py`, `comlab/comlab/core/{fault_atlas_router,fault_atlas_kg,lab_pipeline_aggregator}.py`, `dtclab/dtclab/family_map.py`, `dtclab/dtclab/schemas/vocabulary.py`, `obdlab/obdlab/schemas/vocabulary.py`.
**Readability gate:** all `.md` inputs passed (no `![][` placeholders; math/tables are plain text; SAE.md read by line-addressed P-code lookup).

---

## 0. Verdict (TL;DR)

`StandardProp.md` is a competent *generic* SAE write-up, but its central recommendation — rework `FaultFamily` into SAE J2012 P-code families (`SaeFaultFamily`) behind a `LegacyFaultFamily` + `LEGACY_TO_SAE_MAP` adapter — **does not fit 4DLab and should be rejected.** It misreads where standardization lives in this engine and would manufacture an orphan enum with no consumer, in direct breach of the signal/noise rule.

The audit's correction is structural: **4DLab is already SAE/ISO-anchored where it matters** — at the PID layer (J1979) and the DTC layer (J2012). `FaultFamily` is not a P-code router; it is the diagnostic *output* bucket anchored to the cases corpus. The viable standardization is therefore **not** an enum migration. It is (1) hardening the SAE/J1979 *traceability* that already exists into a verifiable conformance test, and (2) giving "our proprietary faults" (the timing set, and others) a disciplined **proposals** home with a named consumer and an SAE-mapping citation. Both fit the existing architecture and the signal/noise rule without touching a single wire value.

> **Addendum (2026-06-08, owner feedback) — forward progress, not v1-stuck.** Rejecting `SaeFaultFamily` is *not* a vote to freeze v1. v1 "did not give results" because of poor **discrimination** (OBD-alone → >95% `NO_FAULT`), not because of naming. So the high-risk items StandardProp flagged are now reworked into **solutions that add a consumer and buy discrimination** (§9), per the "Progress the app forward" rule — a new field/consumer ships together when it improves the engine. And the owner's ISO point is correct and valuable: **SAE and ISO are already harmonized**, so unifying on ISO is essentially free and strictly better provenance for an EU-petrol engine (§10). See §§9–11.

---

## 1. What "standardization" actually means in 4DLab — three layers, not one

`StandardProp.md` collapses three distinct vocabulary layers into one and then "standardizes" the wrong one. The audit separates them:

| Layer | Artefact | What it is | Standard that governs it | Already standardized? |
|---|---|---|---|---|
| **L1 — Wire identifiers** | PID names (`OBD_VOCABULARY §2`), DTC code strings (`P0171`…), `DTC_REGEX` | The raw telemetry vocabulary entering the engine | **SAE J1979** (PIDs), **SAE J2012 / ISO 15031-6** (DTC structure) | **Yes** — explicitly anchored |
| **L2 — Routing groupings** | `DTCRoutingTag` (19 values), `dtclab/family_map.py` | Groups raw P-codes into actionable buckets, then maps buckets → family | **SAE J2012** P-code blocks | **Yes** — each tag cites its P-code range |
| **L3 — Diagnostic output** | `FaultFamily` StrEnum (12) / `FaultFamilyLit` (16), `FaultNode` IDs | COMLab's *verdict* label, anchored to `cases_petrol_master_v5.csv` `expected_top_fault_family` | **None** — this is 4DLab's diagnostic taxonomy, by design | n/a (correctly proprietary; but L3 has an internal count drift — see §7) |

`StandardProp.md` proposes to standardize **L3** to SAE families. But SAE J2012 is a *fault-code* taxonomy (L1/L2), not a *diagnostic-conclusion* taxonomy. L3 is intentionally proprietary because it is the engine's answer, not its input. Standardizing L3 to P-code families would mean renaming the conclusion to look like the evidence.

---

## 2. Where SAE / ISO already anchors today (evidence)

Standardization is not a greenfield task here. The codebase and wikis already bind to the standards:

- **`OBD_VOCABULARY.md §1`** declares the anchor set: SAE J1979/J1979DA (PIDs, Mode 01/02), SAE J2012/J2012DA (DTC structure), ISO 15031-5/6 (EU equivalents), ISO 14229/UDS (Mode 06).
- **`OBD_VOCABULARY.md §2`** maps every canonical PID name to its J1979 PID id, unit, and range (e.g. `engine_rpm`→`010C`, `coolant_temp_c`→`0105`). The provided `obd2-pid-table-service-01.csv` is that same J1979 Service 01 table.
- **`DTC_VOCABULARY.md §2`** ("DTC code structure (per SAE J2012)"), **§2.3** canonical regex, **§5** `DTCSeverityClass`, **§19** standards references. In code: `DTC_REGEX = r"^[BCPU][0-3][0-9]{3}$"` (vocabulary.py L34) and `DTCSeverityClass` docstring "per SAE J2012 §6"; `DTCState` docstring "per SAE J1979 Mode 03 / 07 / 0A".
- **`DTCRoutingTag`** (vocabulary.py L429–464): every value carries its J2012 P-code range as a citation comment — `LEAN_HISTORY` = P0171/P0174, `MISFIRE_HISTORY` = P0300–P0312, `VVT_HISTORY` = P0010–P0016, etc.

So the honest finding is: **the SAE/ISO alignment StandardProp asks us to "introduce" is largely already present** — as wire identifiers and routing-tag citations. What is missing is not structure; it is *verification* (nothing asserts the citations are correct against SAE.md / the J1979 CSV) and a *disciplined channel* for proprietary additions.

---

## 3. Assessment of `StandardProp.md` — item by item

Each row is scored against the one rule that governs every change: **does the proposed field/enum have a named, existing (or same-change proposed) consumer in COMLab analytics or fault-atlas routing?**

| # | StandardProp recommendation | Disposition | Reason (signal/noise + architecture) |
|---|---|---|---|
| P-1 | Add `SaeFaultFamily` StrEnum (P00XX…P08XX families) | **REJECT** | No consumer. Nothing in `fault_atlas_router`/`fault_atlas_kg`/`lab_pipeline_aggregator`/`response.py` reads SAE family strings. It would be an orphan enum — the exact anti-pattern the anti-orphan check forbids. |
| P-2 | Add `LegacyFaultFamily` + `LEGACY_TO_SAE_MAP` + `normalize_inbound_family()` adapter | **REJECT** | Speculative abstraction with no consumer. It exists only to feed P-1, which is itself unconsumed. "Non-breaking adapter" is solving a migration that has no destination. |
| P-3 | Merge `lean_condition` + `rich_mixture` → one `FUEL_AIR_METERING_P01` family | **REJECT (hard)** | Destroys the engine's ground truth. Brettschneider λ from GASLab distinguishes lean vs rich as *chemistry truth* (`ChemicalSignature.LEAN_MIXTURE` vs `RICH_MIXTURE`; `DTCRoutingTag.LEAN_HISTORY` vs `RICH_HISTORY`; distinct cases-corpus labels). Collapsing them is precisely the "tightening that erases the discriminator" failure mode flagged in prior feedback. |
| P-4 | Premise: incoming DTCs route *through* `FaultFamily`, so make it SAE-shaped | **REJECT (false premise)** | In 4DLab, P-codes route via `DTCRoutingTag` → `family_map.ROUTING_TAG_TO_FAMILY` (L2). `FaultFamily` is the *output* (L3). The cross-mapping layer StandardProp wants to eliminate already exists and is the correct place for it. |
| P-5 | Rename `FaultFamily` values to SAE strings via "minor" v1.1 bump | **REJECT** | Values are the wire format (SEMANTIC_CONTRACT §8 — "renames of values are breaking changes"). This is a §10 **major** (2.0) change touching `response.py`/`kg.py` `FaultFamilyLit`, the cases-corpus column, `dtclab/family_map.py`, and every fixture — for zero diagnostic gain. The framing as "minor v1.1" is also wrong per §10. |
| P-6 | Cam timing belongs in the P00XX air/fuel block; SAE doesn't split it by MAF vs speed-density | **ADOPT — already satisfied** | Correct, and SAE.md confirms (P0011/P0014 over-advanced, P0012/P0015 over-retarded; no MAF/SD split). 4DLab already keeps the calc-strategy out of the fault label: `AirMeteringStrategy`/`VERoutingMode` carry MAF-vs-MAP as a *separate field* consumed by OBDLab VE routing. No change needed beyond §5 below. |
| P-7 | Store MAF-vs-speed-density as live-data metadata, not a fault code | **ADOPT — already satisfied** | This is exactly `AirMeteringStrategy` (VIN-driven) + OBDLab `VERoutingMode`. The principle is right; 4DLab implements it. Do **not** add StandardProp's `timing_resolver.py` / `AppEngineStrategy` — duplicate of existing field. |
| P-8 | "Your 5 timing faults aren't all covered by SAE baseline codes" | **ADOPT — the real kernel** | True and useful. This is the legitimate "proprietary fault" case. Handle via the proposals path in §4.2 — **not** by inventing SAE-shaped families. |
| P-9 | Leverage existing test harness to enforce the standard | **ADOPT — repurposed** | Right instinct, wrong target. Use it for *traceability conformance* (§4.1), not to police a `SaeFaultFamily` that shouldn't exist. |

Net: of nine moves, four are rejected (the entire enum-migration spine), three are already satisfied by existing fields, and two — proprietary-fault discipline and a conformance test — are the genuinely useful kernel, salvaged and re-pointed below.

---

## 4. The viable standardization (adapted plan)

Three workstreams. None adds a wire-schema field. Each names its consumer.

### 4.1 Workstream A — Traceability hardening (citation + conformance test)

**Goal:** turn the *implicit* SAE/J1979 alignment (§2) into a *verified* one, so drift is caught mechanically rather than by reading.

- **A1 — Complete and normalize the citations** already present as comments: every `DTCRoutingTag` value's P-code range, every `DTCSeverityClass`/`DTCState` standard reference, and every `OBD_VOCABULARY §2` PID row gets a precise, uniform SAE clause/PID reference. This is comment/wiki work — **adds no field, no enum value.**
- **A2 — Add a conformance drift-guard test**, mirroring the existing `comlab/tests/unit/test_vocabulary.py` pattern: assert that (a) every PID name in `OBD_VOCABULARY §2` matches the J1979 CSV on id/scale/offset/range, and (b) every `DTCRoutingTag` cited P-code (e.g. `P0171`) resolves to a real definition line in `SAE.md`.
- **Named consumer / code path:** the test itself (`comlab/tests/unit/test_vocabulary_sae_conformance.py`) is the consumer; it reads the citations + the CSV + SAE.md. Because A1/A2 add **no schema field**, the signal/noise rule is satisfied trivially (nothing new crosses a lab boundary). This is pure conformance, the same class of work as the existing vocabulary drift-guard.

### 4.2 Workstream B — Proprietary faults: the proposals path

**Goal:** a disciplined home for faults SAE does not encode (timing set first; the user notes "there are more"), per the "Progress the app forward" rule — new content ships as a **proposal** with a named consumer, not deferred because "not in v1."

- **B1 — Each proprietary fault is registered as a proposal** in `comlab/config/proposals/` (the separate proposals registry, never silently in the live KG/registry), naming its consumer + code path, exactly as the rule requires.
- **B2 — SAE mapping is a citation, not a field.** Each proprietary fault/signature carries an `# SAE: <P-code family or "no SAE equivalent">` *comment* next to its enum value (identical to how `DTCRoutingTag` already cites P-codes). This gives full standards traceability with **zero** new wire field — sidestepping signal/noise entirely. (If a machine-readable mapping is ever wanted, it lives in the proposals-registry config and its consumer is the A2 conformance test — but the comment form is preferred and sufficient.)
- **Existing home to reuse, not reinvent:** the timing faults are already in flight as the **GASLab v2 `ChemicalSignature` 32→34** change (retire `WRONG_VALVE_TIMING`; add three `CAM_TIMING_*` signatures), which has a registered task slate and whose consumer is the fault-atlas router via the `cam_timing` `FaultFamily` (already present, L3). This proposal does **not** re-open that; it asks that the 32→34 work carry the B2 SAE citation so the timing set is standards-traceable when it lands.

### 4.3 What NOT to do (guardrails for the coder session)

- Do **not** add `SaeFaultFamily`, `LegacyFaultFamily`, `LEGACY_TO_SAE_MAP`, `normalize_inbound_family()`, `timing_resolver.py`, or `AppEngineStrategy`.
- Do **not** rename any `FaultFamily` / `ChemicalSignature` / `DTCRoutingTag` **value** — those are wire format (§8 lock). Citations are comments; comments are free to change.
- Do **not** merge `lean_condition` and `rich_mixture`.
- Do **not** re-run graphify / KG extraction. This is citation + test + proposal-registry work only.

---

## 5. The five timing faults — worked example (end to end)

StandardProp's strongest section; here is how it resolves under the adapted plan, using SAE.md as ground truth.

| 4DLab proprietary fault | SAE.md reality | 4DLab home (existing) | SAE citation (B2) |
|---|---|---|---|
| Over-advanced ignition timing | No unique DTC for *calculated* spark error; captured as P035x coil circuits / P0324 knock (SAE.md L≈1040+, knock block) | `FaultFamily.ignition_fault`; `ChemicalSignature.TIMING_OVER_ADVANCED` | `# SAE: no direct DTC — P035x/P0324 adjacency` |
| Retarded ignition timing | Same — no unique DTC | `FaultFamily.ignition_fault`; `ChemicalSignature.TIMING_RETARDED` | `# SAE: no direct DTC — P035x/P0324 adjacency` |
| Advanced cam timing (A & B) | **Covered:** P0011/P0014 "Camshaft Position – Timing Over-Advanced" (SAE.md L1047/L1052) | `FaultFamily.cam_timing`; `DTCRoutingTag.VVT_HISTORY` (P0010–P0016); `CAM_TIMING_*` (proposal) | `# SAE: P0011/P0014` |
| Retarded cam timing (Speed Density) | Covered by P0012/P0015; SAE **forbids** splitting by calc strategy (SAE.md L1050/L1055) | `FaultFamily.cam_timing`; calc strategy = `AirMeteringStrategy.MAP_ONLY_SPEED_DENSITY` (separate field, OBDLab-consumed) | `# SAE: P0012/P0015 (calc strategy not encoded)` |
| Retarded cam timing (MAF) | Same P0012/P0015; calc strategy not encoded | `FaultFamily.cam_timing`; calc strategy = `AirMeteringStrategy.MAF_ONLY` | `# SAE: P0012/P0015 (calc strategy not encoded)` |

The MAF-vs-speed-density distinction StandardProp wanted as metadata is *already* a first-class VIN-driven field with a real consumer (OBDLab VE routing). No new structure is required — only the SAE citations and, for the cam variants, the in-flight `CAM_TIMING_*` signatures.

---

## 6. Recommended work sequence (proposed slate — not yet registered)

If the owner accepts this direction, the work decomposes into small, single-consumer tasks (each ≤ ½ context). Registration deferred per the chosen "standalone proposal" option.

1. **T-SEM-1 — SAE/J1979 citation normalization (Workstream A1).** Comment + wiki pass across `vocabulary.py` DTC/PID enums and `OBD_VOCABULARY §2`. No code-path change. Consumer: A2.
2. **T-SEM-2 — Conformance drift-guard test (A2).** New `test_vocabulary_sae_conformance.py`. Consumer: CI / inner loop. Blocked-by T-SEM-1.
3. **T-SEM-3 — Proprietary-fault proposals registry scaffold (B1/B2).** `comlab/config/proposals/` layout + SAE-citation convention; seed it with the timing set as the first entries, cross-linked to the GASLab `ChemicalSignature` 32→34 slate. Consumer: fault-atlas router (via existing `cam_timing`/`ignition_fault` families) + T-SEM-2.

These are architect-authored specs; a coder session runs the inner loop and gate.

---

## 7. Unplanned follow-ups (out of scope — surfaced, not fixed)

- **L3 family-count drift (enum vs Literal vs contract).** Three "fault family" surfaces disagree on count: `comlab/schemas/vocabulary.py FaultFamily` StrEnum = **12** values (= `SEMANTIC_CONTRACT §8` lock + `OBD_VOCABULARY §6`), but `response.FaultFamilyLit` / `kg.FaultFamilyLit` = **16** values — the extra four (`invalid_input`, `vacuum_leak`, `overheating`, `charging_system`, tagged "T-P6-5b-2 REG-V2 family") are the *actually-emitted* verdict labels. `dtclab/family_map.py`'s 16-family `CANONICAL_FAMILIES` set matches the **Literal**, not the enum. So the locked 12-value enum and the contract are **stale** relative to the runtime verdict type. This is real internal drift and a latent signal/noise question (are all four REG-V2 families consumed?). Flagged only; reconciling it — and deciding whether `FaultFamily`/`§8`/`§6` should grow to 16 — is its own task, and it should be settled **before** any L3 standardization is attempted.
- **ChemicalSignature count.** `GAS_VOCABULARY §3` already advertises the **34-value** enum, while `comlab/schemas/vocabulary.py ChemicalSignature` still carries `WRONG_VALVE_TIMING` and ~32 values. That reconciliation is the existing GASLab v2 slate, not this proposal.

---

## 8. Open questions for the owner

1. Confirm the rejection of the `SaeFaultFamily` migration spine (§3 P-1…P-5). The rest of the plan assumes `FaultFamily` values stay frozen.
2. Should `SEMANTIC_CONTRACT.md §1` "Standards anchored" be promoted to name **ISO 15031-6** explicitly alongside J2012 (it currently lives in the wikis, not the contract), or is wiki-level anchoring sufficient?
3. For the proprietary-fault proposals: comment-only SAE citation (preferred here), or also a machine-readable `sae_mapping` in the proposals config consumed by the conformance test?

---

## 9. Solving the high-risk items — forward progress, with consumers

StandardProp flagged three "high-risk / structural-conflict" items. The right response is neither "rename to SAE" (cosmetic, no discrimination gain) nor "leave as v1" (the bucket stays low-signal). It is to **mine each distinction for signal by adding a consumer** — using the perception channels OBDLab now emits (post-revive) and COMLab's fusion role. Each fix below names a real, verified consumer; each may ship its consumer in the same change (allowed by the "Progress forward" rule).

### HR-1 — `sensor_fault` (component-vs-system "structural conflict")

StandardProp's instinct (a sensor fault belongs to its target *system*) is half-right, but its fix (fold `sensor_fault` into a fuel/air family) **deletes** the component signal — the opposite of progress. 4DLab can do better: `sensor_fault` is *already* routed through perception-contradiction (`lab_pipeline_aggregator.py` L361, "sensor_fault routing" ← `perception_result`), and OBDLab now emits component-level discriminators — `o2_failure_mode` (7 states: `STUCK_LEAN`/`SLUGGISH`/`DEAD`/…), `maf_status`, `ve_validity = FAULT_MAF_CONTAMINATION`.

- **Forward-progress fix (proposal):** add a `sensor_fault_target` qualifier on the sensor-fault verdict, derived from those emitter channels, that records *which* subsystem the sensor fault attacks (O2 / MAF / knock). This honours SAE's "faults belong to systems" insight **and** keeps the component detail.
- **Named consumer (same-change):** the `sensor_fault` branch in `fault_atlas_router` reads `sensor_fault_target` to split today's flat `sensor_fault` verdict into discriminated outcomes (O2-bias vs MAF-contamination vs knock-drift). That is a discrimination gain — the exact v1 deficit.

### HR-2 — `lean_condition` / `rich_mixture` "semantic-drift risk"

Merging them is rejected (Brettschneider λ makes lean-vs-rich the single most discriminating axis — see §3 P-3). But there *is* a real drift risk, and it is **cross-layer**, not within the family: chemistry truth (`ChemicalSignature.LEAN_MIXTURE`/`RICH_MIXTURE`) vs verdict (`lean_condition`/`rich_mixture`) vs ECU perception (`DTCRoutingTag.LEAN_HISTORY`/`RICH_HISTORY`).

- **Forward-progress fix:** formalize the lean↔lean / rich↔rich correspondence across the three layers as an explicit, tested mapping, and feed it into `perception_contradiction.detect()` — which already compares λ-truth vs λ-perception and already reads the rich DTCs `P0172/P0175`. When chemistry says lean but the ECU history says rich (or trims rail the opposite way), that contradiction is a **discriminating finding** (sensor bias / compensated-rich), not noise.
- **Named consumer (exists):** `perception_contradiction.detect()` (consumed at `lab_pipeline_aggregator.py` L313/L361). Mining the lean/rich split across layers turns StandardProp's "drift risk" into signal — the inverse of merging.

### HR-3 — VVT / `cam_timing` separation

Already solved correctly and just needs the dual citation. `cam_timing` is one family; the MAF-vs-speed-density calc strategy lives in `AirMeteringStrategy` (OBDLab-consumed), and SAE/ISO confirm they do **not** split cam codes by calc strategy. Forward progress here is the **in-flight GASLab `ChemicalSignature` 32→34** (retire `WRONG_VALVE_TIMING`; add three `CAM_TIMING_*`), each a proposal whose consumer is the router's `cam_timing` branch, carrying the standards citation `P0011/P0014` (over-advanced) and `P0012/P0015` (over-retarded) — identical in SAE J2012 and ISO 15031-6.

---

## 10. ISO 15031-6 / 15031-5 — yes, unify on ISO (it's already harmonized, so it's nearly free)

The owner's question — *is ISO unified with SAE?* — checks out, and unifying on ISO is a strict improvement for an EU-petrol engine. Web research (sources below) confirms the two are harmonized pairs, not alternatives:

| Concern | SAE | ISO | Relationship |
|---|---|---|---|
| **DTC definitions** | J2012 (`J2012_201612` = 2016) | **ISO 15031-6:2015** | Technically equivalent (J2012_201612 ≡ ISO 15031-6:2010, exceptions in §1.2). ISO 15031-6 *references* **SAE J2012-DA** (Digital Annex) as the canonical DTC + Failure-Type-Byte list — ISO points **at** the SAE code list. |
| **PIDs** | J1979 | **ISO 15031-5** | "Almost technically equivalent"; same bit-encoded PID structure; scaling/format defined in both (ISO 15031 part 5). |
| **Transport / connector** | J1978 / J1962 | ISO 15031-4 / ISO 15765-4 (CAN) | EU OBD lineage. |

4DLab's `SAE.md` is `J2012 DEC2007` (≡ the ISO 15031-6:2005-era text).

**Why "unify on ISO" is the right call and costs almost nothing:** because the *code and PID values are identical*, this is a **citation/labeling** decision, not a code-set change — zero wire-value churn. For 4DLab (petrol, Euro 1–7, EU-market 1990–2010 vehicles), ISO is the more apt primary anchor than a US SAE recommended practice.

- **Recommendation:** make `vocabul/` and the enum citation comments **dual-anchor, ISO-primary** — cite `ISO 15031-6` (DTC) and `ISO 15031-5` (PID) as the lead standard with the equivalent `SAE J2012` / `J1979` clause alongside. `OBD_VOCABULARY §1` already lists ISO as a cross-reference; promote it to co-primary.
- **No structural change:** this is a Workstream-A (§4.1) citation edit. The A2 conformance test simply becomes dual-keyed (assert names/ranges against the J1979 CSV *and* note the ISO 15031-5 equivalence; assert DTC citations against `SAE.md` / J2012-DA *and* ISO 15031-6).
- **Caveat to log, not solve here:** the live, authoritative DTC list is the **SAE J2012-DA Digital Annex** (and the matching ISO 15031-6:2015), both newer than the 2007 `SAE.md` in-repo. The conformance test should cite the in-repo `SAE.md` as the working copy and flag that a refresh to the current J2012-DA / ISO 15031-6:2015 is a separate, optional procurement step (the petrol-1990–2010 P-code set is stable across these revisions, so it is low-urgency).

---

## 11. Updated work sequence (supersedes §6 where they differ)

1. **T-SEM-1 — Dual-anchor ISO-primary citation pass (A1 + §10).** Comment + `vocabul/` edit: ISO 15031-6 / 15031-5 lead, SAE J2012 / J1979 equivalent. No field/enum change. Consumer: T-SEM-2.
2. **T-SEM-2 — Dual-keyed conformance drift-guard test (A2).** Consumer: CI / inner loop. Blocked-by T-SEM-1.
3. **T-SEM-3 — Proprietary-fault proposals scaffold (B1/B2)**, seeded with the timing set + dual citation; cross-linked to the GASLab `ChemicalSignature` 32→34 slate. Consumer: router `cam_timing`/`ignition_fault` branches.
4. **T-SEM-4 — `sensor_fault_target` qualifier (HR-1, proposal + same-change consumer).** Adds discrimination to the `sensor_fault` verdict from OBDLab emitter channels. Consumer: `fault_atlas_router` sensor-fault branch. Depends on the OBDLab emitter channels being live (ties to T-OBDV2-1 PID-logset proof).
5. **T-SEM-5 — Lean/rich cross-layer correspondence (HR-2).** Formalize + test the 3-layer lean/rich mapping; wire as input to `perception_contradiction`. Consumer: `perception_contradiction.detect()` (exists).

T-SEM-4/5 are the "forward progress" tasks — each adds a consumer that improves discrimination, the actual v1 failure. T-SEM-1/2/3 remain pure traceability/proposal hygiene. **Settle the §7 L3 family-count drift (12 vs 16) before T-SEM-4/5**, since both touch verdict-family routing.

---

## 12. Connected in-house proposals that strengthen this plan

`obdlab/research/proposals/extracted/` (70 architect-drafted proposals, `INDEX.md`) already contains the right-shaped version of most of this work — consumers *named but not yet wired* ("graduates to `comlab/config/proposals/` when a consumer is pinned", `INDEX.md` L9). This is the same proposals path §4.2 recommends, already populated. The directly-connected ones:

| This proposal | Connected EP | How it strengthens / supersedes |
|---|---|---|
| §10 SAE/ISO unification; §4.2 proprietary-fault home | **EP-DTC-02** — *"SAE J2012 / ISO 15031-6 eight-family fault taxonomy backbone"* | **The concrete, in-house home for SAE/ISO standardization, scoped correctly.** It adopts the 8 standard P-code families as a **fault-atlas routing/registry backbone** (my L2), explicitly **not** as the L3 verdict — exactly the layer split in §1, and it already names ISO 15031-6. Adopt **this** as "standardize on SAE/ISO," not StandardProp's verdict rename. Consumer: `comlab/config/kg/*` family registry + `fault_atlas_router.py`; `EP-FA-*`/`EP-ECU-*` nodes register under its families. |
| §9 HR-1 `sensor_fault` discrimination | **EP-COM-05** (semantic-coherence paradigm) + **EP-COM-04** (ECU-hardware checker) + **EP-OBD-14** (semantic-consistency gates) + **EP-OBD-17** (`WIDEBAND_OFFSET` O₂ mode) | These already design the discrimination my HR-1 qualifier was reaching for — **adopt them instead of inventing a parallel mechanism.** EP-COM-05 sets a `coherence` flag (in `perception_contradiction.py`) that gates *traditional family* vs *ECU-hardware checker* before family routing; EP-OBD-17 adds a concrete wideband-calibration `SENSOR_FAULT` node (field+consumer ship together — the forward-progress rule, stated verbatim). |
| §9 HR-2 lean/rich cross-layer | **EP-COM-05** + **EP-COM-03** (lambda cross-delta engine) + **EP-COM-15** (30-case truth-perception corpus) | EP-COM-05 *is* the truth-vs-perception organizing principle my HR-2 formalizes; EP-COM-03 is the λ_chem-vs-λ_obd delta engine that consumes it; EP-COM-15 is a ready-made labelled corpus to validate it. |
| §9 HR-3 cam_timing | **EP-COM-06** (signature matrix — has "retarded cam"/"retarded spark" rows) + **EP-DTC-02** (P00xx/P03xx homes) | Confirms the calc-strategy-as-metadata treatment and gives cam timing explicit two-state PID discriminators. |
| The actual v1 deficit (discrimination, not naming) | **EP-COM-06** (10-family × PID two-state signature matrix) + **EP-DTC-01** (DTC causal hierarchy, root-vs-symptom) | EP-COM-06 is the deterministic discriminator table for `fault_atlas_router` (replaces scattered if/else) — the single highest-leverage forward-progress asset. EP-DTC-01 hands COMLab the root cause instead of a flat code list. |
| §4.1/§11 conformance + validation | **EP-COM-15** | Labelled truth-vs-perception fixtures the conformance/validation work can reuse. |

**Net effect on this proposal:** the standardization direction is *confirmed by in-house work* — EP-DTC-02 standardizes at L2 (routing backbone), not L3 (verdict), and is ISO-inclusive. My §11 sequence should therefore **adopt/pin existing EPs rather than author from scratch**:

- **T-SEM-3** (proprietary-fault scaffold) ⇒ graduate **EP-DTC-02** first as the registry backbone, then attach `EP-FA-*`/`EP-ECU-*`/`EP-OBD-17` nodes under its families with dual ISO/SAE citation.
- **T-SEM-4** (`sensor_fault` discrimination) ⇒ pin the consumers in **EP-COM-05 + EP-COM-04 + EP-OBD-17** instead of a new `sensor_fault_target` field.
- **T-SEM-5** (lean/rich) ⇒ realize via **EP-COM-05 + EP-COM-03**, validated by **EP-COM-15**.

One caveat: these EPs are *extracted specs*, not live code — consumers are proposed, none verified as a live reader (`INDEX.md` L5). They are the right inputs to the T-SEM tasks, but each still needs the inner loop + verification gate before it ships.

---

## 13. Decision — how this is incorporated, and the task pack that closes it

The study above resolves to one decision: **standardize at L1/L2, keep L3 proprietary, and make the
vocabulary openly extensible through a registry + a growth-safe gate.** That is now authored as a runnable
self-contained pack at `labs/semantic/` (START_HERE + ledger + four specs), so the question can close and
work can move on. The pack deliberately separates *closing the standard* from *implementing each fault*:

| # | Task | What it incorporates | Closes |
|---|---|---|---|
| **T-SEM-1** | ISO-primary dual-anchor citations | §2, §10 — ISO 15031-6/-5 lead, SAE J2012/J1979 equivalent; L1 PIDs + L2 routing tags. Comments/prose only, zero value churn. | "what standard, cited how" |
| **T-SEM-2** | Proposals registry + **EP-DTC-02** taxonomy backbone | §4.2, §12 — the **open mechanism**: `comlab/config/proposals/` + graduation rule + citation convention; EP-DTC-02 8-family P-code spine as the fault-atlas routing backbone (L2). | "how any new fault is added" |
| **T-SEM-3** | Register the connected EPs | §9, §12 — EP-COM-05/04/06, EP-OBD-17/14, EP-DTC-01, EP-COM-15 become the first registry entries (consumer + ISO/SAE citation), implemented later in their lab ledgers. | "the work in hand is captured, not lost" |
| **T-SEM-4** | Growth-safe conformance + extensibility gate | §4.1 — dynamic drift-guard: PID↔J1979, P-code↔SAE.md, and **every registry entry must have a consumer + citation**. No hardcoded counts. | "closed, self-policing, still open" |

**This directly answers the extensibility mandate.** The standard is "closed" (T-SEM-1/2 settle it) yet
**open to further additions** by construction: a new viable fault is added by dropping one well-formed
registry entry (family + consumer + dual ISO/SAE citation) under the EP-DTC-02 backbone; the T-SEM-4 gate
*welcomes* it (no count is hardcoded) but *rejects* any addition lacking a consumer or citation — signal/noise
enforced mechanically. The high-risk fixes (§9) and the broader `extracted/` fault catalogue flow through this
same path, implemented in their owning labs.

**Out of this pack, by design:** the L3 family-count drift (§7), the GASLab `ChemicalSignature` 32→34, and
every fault's *discrimination implementation*. Those are tracked in the pack ledger's follow-ups and run in
the COMLab/OBDLab/GASLab ledgers.

> Architect deliverable complete: specs + ledger authored, not run. A coder session starts at
> `labs/semantic/SEMANTIC_START_HERE.md`, takes T-SEM-1 first, one task per session.

---

## Sources

- `labs/semantic/StandardProp.md` — third-party generic proposal (assessed in §3)
- `labs/semantic/SEMANTIC_START_HERE.md` + `tasks/PROGRESS.md` + `tasks/T-SEM-1..4_*.md` — the task pack (§13)
- `labs/obdlab/research/proposals/extracted/INDEX.md` + `EP-DTC-02`, `EP-DTC-01`, `EP-COM-03/04/05/06/15`, `EP-OBD-14/17` — connected in-house proposals (§12)
- `labs/semantic/SAE.md` — SAE J2012 DEC2007 full text (P-code definitions; cam-timing block ≈ L1040–1075, fuel-trim block ≈ L1424–1431)
- `labs/semantic/obd2-pid-table-service-01.csv` — SAE J1979 Service 01 PID table
- `labs/semantic/vocabul/SEMANTIC_CONTRACT.md` — §3 source-of-truth table, §8 locked enums, §10 change protocol
- `labs/semantic/vocabul/OBD_VOCABULARY.md` — §1 standards anchored, §2 canonical PIDs, §6 fault families
- `labs/semantic/vocabul/DTC_VOCABULARY.md` — §2 DTC structure (J2012), §4 DTCRoutingTag, §5/§6/§19
- `labs/semantic/vocabul/GAS_VOCABULARY.md` — §3 ChemicalSignature 34-value enum
- `labs/comlab/comlab/schemas/vocabulary.py` — `FaultFamily` L217, `ChemicalSignature` L241, `DTCRoutingTag` L429, `DTC_REGEX` L34
- `labs/comlab/comlab/schemas/response.py` / `kg.py` — `FaultFamilyLit` (16 values: the 12 contract families + 4 REG-V2 families)
- `labs/comlab/comlab/core/{fault_atlas_router,fault_atlas_kg,lab_pipeline_aggregator}.py` — `FaultFamily` consumers
- `labs/dtclab/dtclab/family_map.py` — `ROUTING_TAG_TO_FAMILY`, 16-family `CANONICAL_FAMILIES`
- `labs/obdlab/obdlab/schemas/vocabulary.py` — `VERoutingMode`, `O2NormalizationMode`
- `labs/obdlab/tasks/T-OBDV2-0_revive_emitter_decision.md` + `tasks/PROGRESS.md` — emitter-vs-judge decision; >95% NO_FAULT = data artefact; discrimination is the v1 deficit

### Web sources (SAE ↔ ISO harmonization, §10)

- [ISO 15031-6:2015 — DTC definitions (iso.org)](https://www.iso.org/standard/66369.html)
- [SAE J2012_201612 — Diagnostic Trouble Code Definitions (saemobilus)](https://saemobilus.sae.org/standards/j2012_201612-diagnostic-trouble-code-definitions)
- [SAE J2012 (2013) — equivalent to ISO 15031-6 (ANSI webstore)](https://webstore.ansi.org/standards/sae/sae20122013j2012)
- [J2012B (work in progress) — SAE](https://www.sae.org/standards/content/j2012/)
- [OBD-II PIDs / J1979 ↔ ISO 15031-5 (Wikipedia)](https://en.wikipedia.org/wiki/OBD-II_PIDs)
- [Automotive diagnostic standards overview — x-engineer.org](https://x-engineer.org/automotive-diagnostic-standards/)
