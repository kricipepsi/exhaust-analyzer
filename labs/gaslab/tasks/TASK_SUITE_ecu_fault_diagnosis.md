# Task suite — ECU-internal fault diagnosis (GASLab + OBDLab → COMLab fusion)

**Author role:** architect (specs only). **Origin:** `STUDY_ecu_fault_gas_signatures_merge.md`.
**Answers:** `ROADMAP.md` Research-Question **#3** ("Is `ecu_fault` separable from real
mixture faults at all — OBDLab + GASLab"). **Date:** 2026-06-05.

## Governing finding (sets the architecture for all five tasks)

Internal-ECU faults emit **no gas signature of their own**; each presents as an existing
GASLab `chemical_state`. The *internal-ECU* verdict is a **fusion product** of GASLab gas
truth + OBDLab ECU-perception, assembled at the **COMLab** layer (reworked last, per
roadmap Stage 4, to suit upstream labs' settled output). Therefore:

- **GASLab adds nothing.** `ecu_fault` stays unmapped in `gaslab/family_map.py` (verified).
- New schema fields live **OBD-side + COMLab-side**, and ship **only** with the COMLab
  fusion rule as their named consumer (signal/noise).
- Cross-lab e2e for ECU faults goes green at **Stage 4**, intentionally divergent until
  then — matches the roadmap's "revised first, divergent until consumers catch up."

## Staging & dependency graph

```
T-GV2-6d (reframe/close, GASLab) ── now (this study)
T-DOC-ECU-1 (wiki) ── owner sign-off
   └─ T-DOC-ECU-2 (wiki)
T-OBDV2-ECU-PERCEPT-1 (OBDLab, Stage 2) ── references DOC-ECU-2; consumer = FUSE-1
   └─ T-COMV2-ECU-FUSE-1 (COMLab, Stage 4) ── the named consumer; closes the loop
```

Scope for the five faults is **locked**: capacitor leakage, injector driver (open +
shorted), ignition coil driver, sensor ground trace, 5 V rail collapse. All numbers come
from the source's intact master matrix; **none enters code until adopted into the v2 wiki
with a real citation** (source `[n]` markers are non-authoritative).

---

## T-GV2-6d — GASLab-side disposition (reframe + close) · Stage 1 · runnable now

**Pack:** GASLabV2 · **Status:** ready (architect close) · **Blocked-by:** —
**Deliverable:** ledger reframe only — no code.
**Scope:** Record that no gas-only ECU `ChemicalSignature` exists; the six failure modes
already route to existing states (`RICH_MIXTURE`, `LEAN_MIXTURE`+`HIGH_COMBUSTION_TEMP`,
`IGNITION_MISFIRE`, `LEAN_MISFIRE`, `RICH_MISFIRE`). Re-home the ECU verdict to OBD+COMLab
fusion. Supersedes the ABSTAIN-1 question (GASLab does not abstain — it emits true state).
**Consumer:** n/a (no field added).
**Success:** 6d row reflects disposition; ABSTAIN-1 marked resolved; suite linked. Done
in the ledger edit accompanying this suite.

---

## T-DOC-ECU-1 — Fault-atlas map: internal-ECU → existing chemical_state · wiki/doc-sync

**Pack:** wiki (`docs/GASLab/wikiNEW/05_fault_atlas_part_a.md`) · **Blocked-by:** owner sign-off
**Deliverable:** a sub-section "Internal-ECU faults present as existing chemical states"
holding the §3 mapping table from the study (fault → `chemical_state` → idle→2500
differential → wiki anchor). Pure cross-reference; **mints no new state, no schema field.**
**Consumer:** n/a (documentation; no signal/noise gate).
**Success criteria:**
- Each of the six modes cross-referenced to an existing `FAULT_*` atlas entry.
- Masking-rule note included for F4/F5 (1 dead cyl) **and** the F3 global-lean false-
  positive caveat (O₂ 6.5 reads as 1 dead cyl; CO≈0 + NOₓ-spike + OBD break the tie).
- No new `chemical_state` introduced.

---

## T-DOC-ECU-2 — Extend §4.12 divergence catalogue with ECU perception patterns · wiki/doc-sync

**Pack:** wiki (`docs/GASLab/wikiNEW/04_inter_gas_grammar_validity_gates.md` §4.12) ·
**Blocked-by:** T-DOC-ECU-1
**Deliverable:** extend the ECU-vs-tailpipe divergence-magnitude table with the five
structural perception patterns from the study §4: (1) impossible-input (warm engine reads
−40 °C / WOT), (2) lockstep 5 V-rail sensor drop, (3) trim pegged with no effect,
(4) oscillation (cap leak), (5) ADC flat-line "lean" vs rich gas. This is the reusable
internal-vs-external discriminator.
**Consumer:** read by the COMLab fusion rule (T-COMV2-ECU-FUSE-1).
**Success criteria:** each pattern names the OBD observation + the gas truth it contradicts;
directional, not a single magic threshold; references the source master-matrix rows.

---

## T-OBDV2-ECU-PERCEPT-1 — ECU-perception contract · OBDLab · Stage 2

**Pack:** OBDLabV2 (stood up at Stage 2 start; do not pre-scaffold) · **Blocked-by:**
OBDLab v2 scope decision (revive vs quarantine) + T-DOC-ECU-2
**Deliverable:** OBD-side typed JSON fields needed to test divergence — at minimum:
ECU-reported λ / upstream-O₂ state, STFT, LTFT, and the implicated raw sensor reads
(ECT, IAT, TPS, MAP). Coder pins realistic per-family bounds from the OBD wiki.
Also owns **F1 capacitor leakage** end-to-end as an **OBD-only** detection (trim
oscillation / 5 V-ref AC ripple) — a standalone OBD signal, not a fusion input (owner
decision 2026-06-05); its consumer is OBD/DTC routing, not FUSE-1.
**Consumer (named, signal/noise):** the divergence fields' consumer is **T-COMV2-ECU-FUSE-1**;
the F1 oscillation field's consumer is OBD/DTC routing. Divergence fields are
**intentionally orphaned until Stage 4** per roadmap divergence policy; do not flip to
`done` claiming a live consumer before FUSE-1 reads them, OR land both in the same Stage-4
window. State the choice in scope confirmation.
**Success criteria:** fields typed + bounded with OBD-wiki citations; no field added that
its named consumer will not read; e2e divergence demoable against the **five** fusion
fixtures (F1 validated separately on the OBD-only path).

---

## T-COMV2-ECU-FUSE-1 — Divergence fusion rule → `ecu_internal_*` verdict · COMLab · Stage 4 (last)

**Pack:** COMLab (`COMLab/COMLAB_START_HERE.md`) + registry alongside · **Blocked-by:**
T-OBDV2-ECU-PERCEPT-1 (and DTCLab DTC-presence channel if used as corroboration)
**Deliverable:** the fusion rule that consumes GASLab `chemical_state` + chemistry-λ and
OBD perception, computes the gas-vs-perception divergence, and emits an `ecu_internal_*`
routing/verdict when one of the catalogued patterns (T-DOC-ECU-2) fires; otherwise keeps
GASLab's external `chemical_state`. This rule is the **named consumer** that makes
T-OBDV2-ECU-PERCEPT-1's fields shippable.
**Consumer:** fault-atlas routing / COMLab analytics (terminal consumer — emits the verdict).
**Success criteria:**
- Agreement (gas≈perception) → external fault, GASLab state unchanged.
- Catalogued disagreement → `ecu_internal_*` verdict; the **five** in-scope fixtures classify
  correctly (F1 capacitor leakage is OBD-only, not handled here — owner decision 2026-06-05).
- F3-vs-misfire tie broken by CO + NOₓ + lockstep-rail signal, not masking O₂ alone.
- Registry vocab reconciled alongside (Stage-4 consolidation); no orphan field remains.

---

## Owner decisions (resolved 2026-06-05)

1. **Capacitor leakage (F1) → OBD-only.** Gas is **inconclusive** for this mode (its only
   tell is temporal oscillation, which the two-snapshot low/high-idle gas contract does not
   capture). F1 is therefore **removed from the gas+fusion discrimination set**; OBDLab owns
   it end-to-end as an **OBD-trim-oscillation / 5 V-ref AC-ripple** detection, surfaced as an
   OBD signal — not a GASLab `chemical_state` and not a gas↔OBD divergence verdict. This
   drops the FUSE-1 gas-discrimination set from 6 modes to **5** (injector open, injector
   shorted, coil driver, sensor ground, 5 V rail collapse).
2. **OBD-I / early-OBD-II PID-availability edge cases → out of scope.** Modes that depend on
   pre-CAN architecture specifics (EPROM bit-flip, internal BARO) or PIDs that may not be on
   the bus for older ECUs are **conceded as marginal**; T-OBDV2-ECU-PERCEPT-1 pins the
   perception contract against commonly available PIDs only and does not chase older-bus
   coverage.
