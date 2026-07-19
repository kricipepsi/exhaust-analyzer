# T-TH-13 — Per-lab projection rollout (OBD, DTC, COM, DNA/VIN)

> **Status: pending, gated.** One lab per session. Each lab is gated on its
> fork/descriptor existing (same gate as T-TH-8 / Unplanned H-2). Author the
> concrete task at the start of each lab's session.

### Goal ###

Generalise the T-TH-10 GASLab projection to the remaining four labs: reuse
`tools/extract_lab_cases.py --lab <name>` to derive a clean, lab-decidable
fixture from the master corpus for OBDLab, DTCLab, COMLab, and DNALab/VINLab.

For each lab, define (in that lab's session, cited):
  - **consumed columns** — the master columns that lab actually reads;
  - **decidability filter** — which master rows that lab can verdict alone
    (the COMLab fixture is the inverse case: it *is* the cross-lab integrator,
    so its filter keeps `expected_perception_gap` rows rather than dropping
    them);
  - **expected** — that lab's own output column(s) from the master truth.

### Per-lab order & gate ###

OBD → DTC → DNA/VIN → COM, each blocked on its fork existing
(`TESTSUITE_PROGRESS` phase-gates: OBD/DTC/DNA/COM forks still unscoped). A lab
without a fork does not run — same rule as T-TH-8.

### Named consumer ###

Each lab's per-module test gate (the retargeted parity gate for that fork),
mirroring T-TH-11 for GASLab. No fixture ships without its fork as consumer.

### Out of scope ###

No fixture for a lab whose fork does not exist. No master edits. Folds with
T-TH-8 descriptor rollout — do not duplicate generator work, only projection.
