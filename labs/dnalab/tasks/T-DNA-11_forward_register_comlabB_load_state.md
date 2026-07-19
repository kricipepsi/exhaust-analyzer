# T-DNA-11 — Forward-register COMLab-B (`load_state`) into the Stage-4 ledgers

**Authored:** 2026-06-12 (architect). **Source:** tri-module audit
`labs/dnalab/docs/audits/AUDIT_2026-06-12_trimodule_dna_vin_symptom.md` §2.
**Type:** ledger bookkeeping (architect/registry session) — **no code, no COMLab build.**

### Goal ###

`load_state` (emitted by T-DNA-2, live in `SymptomDNA`) names its consumer as proposal
**COMLab-B** in `comlab/config/proposals/entries.yaml` and in this pack's dependency table
(`PROGRESS.md` §"Cross-lab dependencies", COMLab-B row). But — unlike **every other**
emitted-and-waiting field (`ve_pct`, `per_bank_trim_delta`, `fuel_system_status`, …) —
COMLab-B has **no forward-registered row** in COMLab's Stage-4 ledger
(`comlab/tasks/PROGRESS.md`) nor in `CROSS_LAB_DEPENDENCIES.md` (the "source of record for
every DEP row"). Because the Stage-4-close anti-orphan grep runs against the **registered**
rows, an unregistered field is **off the checklist** and can be silently dropped when COMLab
is reworked. Close that hole by forward-registering COMLab-B exactly like its siblings.

This is **not** a live signal/noise breach — a forward-registered emitted field is compliant
until Stage 4. The defect is the *missing registration itself*.

### Named signal/noise consumer ###

The registration **is** the deliverable: it makes `symptom_dna.environmental_conditions.load_state`
a named, ledgered Stage-4 reader (COMLab-B context-modifier prior, 65% trust-ceiling cap).
After this task, the S4-close grep will include `load_state`.

### Success criteria ###

- `CROSS_LAB_DEPENDENCIES.md`: a new DEP row for COMLab-B, in the same shape as the existing
  DEP-2…DEP-12 rows — emitter = `T-DNA-2` (symptomlab, done); consumer = COMLab-B
  context-modifier; consumes = `symptom_dna.environmental_conditions.load_state`;
  promotions/demotions per DNAresearch §"Context-Modifier Shifts"; 65% cap.
- `comlab/tasks/PROGRESS.md`: a forward-registered `T-COMV2-CTXMOD-1` row
  (`pending (forward-registered · S4)`) mirroring the table at lines 20–31, Blocked-by
  `T-DNA-2 (done)`, Consumes `load_state`, Notes naming proposal **COMLab-B** + the 65% cap.
- `comlab/config/proposals/entries.yaml`: confirm the COMLab-B entry already names the
  consumer path + code-path stub; add the `dep_row` / `comlab_task` cross-reference field if
  the sibling entries carry one (consistency only — do not change the proposal's substance).
- No code in any lab changes. No COMLab implementation (that is a Stage-4 task, out of sequence now).

### Files to touch ###

- `v2-restructure/CROSS_LAB_DEPENDENCIES.md` (ADD — one DEP row)
- `labs/comlab/tasks/PROGRESS.md` (ADD — one forward-registered consumer row)
- `labs/comlab/comlab/config/proposals/entries.yaml` (MODIFY — cross-ref field only, if siblings have one)

### Out of scope ###

Building the COMLab-B context-modifier, the promotion/demotion weights, and the 65% cap
arithmetic — those are the Stage-4 COMLab rework (the row this task registers). Do **not**
implement them now.

### Verification ###

```bash
cd $HOME/mnt/4DLab/4DLabV2
grep -nI -i "load_state\|COMLab-B\|context.modifier" v2-restructure/CROSS_LAB_DEPENDENCIES.md
grep -nI -i "load_state\|CTXMOD\|COMLab-B" labs/comlab/tasks/PROGRESS.md
# both must now return the new rows
```

### On completion ###

Note in `progress_notes/T-DNA-11.md` that registration is present in both ledgers; flip the
row → `done`. STOP.
