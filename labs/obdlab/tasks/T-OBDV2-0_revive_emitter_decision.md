# T-OBDV2-0 — scope gate: REVIVE OBDLab as a perception-channel emitter

**Type:** scope-gate **decision** (no code) · **Lab:** OBDLab (Stage 2) · **Mode:** STRICT
**Decision:** **REVIVE — emitter role.** OBDLab is revived as a typed *perception-channel emitter* feeding COMLab fusion. It does **not** emit fault-family verdicts; standalone OBD fault-classification is conceded.
**Origin / evidence:** audit **Q10** (`docs/reference/audit_2026-06-03/4DLAB_CAPABILITY_AUDIT_AND_RESEARCH_QUESTIONS.md`, OBDLab §) · `OBDLAB_PURGE_AUDIT_2026-06-08.md` · `wiki/PID_LOGSET_RESEARCH_PROMPT.md` · `KGtopic.md` · `research/obd2-pid-table-service-01.csv`
**Owner ratification:** confirmed in-session 2026-06-08 (the commit of this file is the ratification).

### Goal ###

Resolve the gate that blocks all OBDLab work (`tasks/PROGRESS.md` north-star). Record the **revive vs
quarantine** decision, its evidence, the role revive commits OBDLab to, and the routing of consequences
(which rows unblock, what the first proof task is). This file is the gate's deliverable; there is no code in
T-OBDV2-0 itself.

### Decision and why ###

**REVIVE, in the emitter role.** Four evidence strands, all pointing the same way:

1. **The quarantine cause was data, not code.** `wiki/PID_LOGSET_RESEARCH_PROMPT.md` (lines 24-26): the module
   was quarantined because the test corpus *carried no live PID data*, so it returned `o2_mode=NO_FAULT` on
   >95% of cases, `ve_pct=0.0`, `ve_validity=UNKNOWN`. The live entry point
   `obdlab/core/sensor_signal_translator.py::translate()` already emits a fully typed `OBDLivePayload`; it was
   starved of input, not broken. Audit Culprit 2 confirms: OBDLab is "dead **on this corpus**," a measurement
   gap — "missing from the data, not from the code."
2. **The signatures to un-quarantine now exist.** Research is incorporated under `research/` — `chunks/fuel-trim`,
   `chunks/o2-logic`, `chunks/delta-relations`, `chunks/ecu-diagnosis`, and `formula-wiki/` — giving documented
   PID→signal signatures per fault family on 1990–2010 petrol. `research/obd2-pid-table-service-01.csv` is the
   SAE J1979 PID decode table (scale/offset/units); it also resolves audit **Q3** — real STFT range is −100…+99 %,
   so the corpus's ±127 values were a saturation **sentinel**, not a reading.
3. **The architecture wants OBDLab as an emitter, not a judge.** `KGtopic.md` (Division of Labor, lines 85-94):
   the parsing labs (GAS, OBD, DTC) translate raw metrics into standardized **"perceptions"** via their local
   knowledge graphs; **COMLab** cross-references those perceptions and outputs the **final verdict**. OBDLab's
   own KG (`graph/v2_current/graph.json`) is the interpretation ontology for that translation. The inherited
   cross-lab specs already assume this split (DEP-2 perception-half of `ecu_fault`; DEP-3 per-bank trim → COMLab
   fusion).
4. **Standalone OBD classification does not work and was already condemned.** Audit Culprit 2/4: OBD-II data
   alone cannot separate most fault families, and forced truth-vs-perception **override measured net-negative**
   (App 4 `resolve_conflicts` = −5) — the architecture pivoted to "prior, not override." The dead
   `OBDLabSimple` classifier (`ranking.py`/`family_map.py`) that collapsed everything to `no_fault` is removed
   by **T-OBDV2-PURGE-1**; this decision makes that removal permanent and correct.

### What "emitter role" commits OBDLab to ###

- **Emits** (typed channels on the frozen inter-lab contract, each with a named COMLab consumer): fuel trims
  (STFT/LTFT, per-bank), `normalized_obd_lambda`, `ve_pct`/`ve_validity`, `o2_failure_mode`,
  `trim_analytics_gate`, and the inherited `lambda_perception_delta` (DEP-2) + per-bank trim asymmetry (DEP-3).
- **Does NOT emit:** a fault-family verdict, a top-3 candidate list, or any `LabResult`/`LabCandidate`. Those are
  COMLab fusion products. OBDLab is a witness, not the judge.
- **Keeps:** its local KG/ontology for raw→perception translation (`KGtopic.md` §1, §3); the live §3–§12 pipeline.

### Consequences / routing (ledger re-point) ###

This decision = `revive`, so the north-star gate opens. Updated in `tasks/PROGRESS.md` atomically with this file:

- **T-OBDV2-PURGE-1**, **T-OBDV2-PURGE-2** — were blocked only by T-OBDV2-0 → now **runnable** (`pending`).
- **T-OBDV2-ECU-PERCEPT-1**, **T-OBDV2-BANK-ASYM-1** — no longer gated on T-OBDV2-0, but remain
  `pending (research-gated)` on their own audit Qs (Q1/Q4 and Q2/Q6) until the architect pins bounds.
- **T-OBDV2-1 … T-OBDV2-10** — the 10 audit questions become authorable specs.

### Immediate next task (recommended first runnable proof) ###

**T-OBDV2-1 — PID-logset wiring-gate proof** (author next session, not here). Build the test PID log set from
`wiki/PID_LOGSET_RESEARCH_PROMPT.md` using the incorporated `research/chunks` signatures + the J1979 CSV, and
prove the live `translate()` produces **discriminating, non-`NO_FAULT`** output across the coverage matrix. This
is the un-quarantine proof that turns "revive (decided)" into "revive (demonstrated)"; it de-risks every
downstream channel task. Until it passes, revive is ratified intent, not verified capability.

### Out of scope ###

This task does **not** author T-OBDV2-1 or the 10-Q specs (next sessions; one task per session), does **not**
write or modify any `obdlab/` code, and does **not** run the PURGE tasks. It only records the decision and
re-points the ledger.

### Consumer (signal/noise) ###

N/A — a decision adds no schema field. Note the standing rule this decision re-affirms: every channel OBDLab
emits under the emitter role must name an existing-or-proposed COMLab analytics / fault-atlas consumer and its
`file.py::function` code path, or it does not ship.

### Success criteria ###

- Decision recorded here and the `tasks/PROGRESS.md` north-star gate paragraph + T-OBDV2-0 row reflect
  `done — revive (emitter)`.
- Dependent rows re-pointed (PURGE-1/2 unblocked; inherited rows no longer cite T-OBDV2-0).
- The capability proof itself is delegated to **T-OBDV2-1** (PID-logset wiring gate) — it is that task's gate,
  not this one's.

### Progress hook ###

`tasks/progress_notes/T-OBDV2-0.md` records the decision rationale + owner ratification.
PROGRESS.md `T-OBDV2-0`: Status=done, Decision="revive (emitter)", Next="T-OBDV2-1 PID-logset wiring gate".
