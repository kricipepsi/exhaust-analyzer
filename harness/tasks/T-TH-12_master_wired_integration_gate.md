# T-TH-12 — Master CSV as the wired end-to-end integration gate

> **Status: blocked** on the 4DLabWired integration seam existing. Author the
> full task at the start of its own session once the wired pipeline is runnable.
> This file fixes scope and the one tradeoff so the row is not lost.

### Goal ###

The per-lab fixtures (T-TH-10/13) gate each lab in isolation. This task makes
the **master corpus** `TestSuite/cases_petrol_master_v6.csv` the gate for the
**whole wired pipeline**: feed each master row through the full L1→L5 chain
(GASLab → OBDLab → DTCLab → freeze-frame → live-PID → COMLab decision) and
assert the end-to-end columns: `expected_top_fault`, `expected_top_fault_family`,
`expected_state`, `expected_perception_gap` (and confidence band).

This is the "when the whole lab is wired, the master CSV must also pass"
requirement. It runs at the integration seam, not on any single lab.

### The tradeoff to settle here (do not pre-decide) ###

The master "stays the same" structurally — same rows, same columns. But T-TH-10
adjudication will have found master cells whose label is provably stale (e.g.
`WRONG_VALVE_TIMING`, an enum GASLab can no longer emit, H-5). A frozen master
with stale labels **cannot** pass end-to-end. Two options, owner's call:
  - **Reconcile labels:** fix only the provably-stale expected cells (enum
    removed / routing intentionally changed), keeping rows and inputs intact.
    Treat as label maintenance, not a rebuild.
  - **Quarantine rows:** move provably-stale rows to a `known_drift` partition
    excluded from the pass gate until the owner re-labels them.
Surface the count and the list; do not silently edit master.

### Blocked by ###

T-TH-11 (clean per-lab GASLab gate) **and** a runnable 4DLabWired pipeline
(see `project_jaeger_deferred` — activates at the integration seam).

### Out of scope until unblocked ###

No wired-harness code while the seam is absent. No master edits without owner
sign-off on the tradeoff above.
