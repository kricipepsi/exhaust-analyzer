# SEMANTIC pack — START HERE

**Pack:** Semantic-vocabulary standardization (cross-lab) · **Mode:** STRICT · **Created:** 2026-06-08
**Why this pack exists:** `labs/semantic/SEMANTIC_STANDARDIZATION_PROPOSAL.md` (read it first — it is the *why*).
**This file is a procedure, not documentation. Execute it step by step.**

---

## What "closing semantic standardization" means here

This pack **settles two things and then closes**:

1. **What our standard is.** A three-layer vocabulary, standards-anchored where standards belong:
   - **L1 — wire identifiers:** PID names ← **SAE J1979 / ISO 15031-5**; DTC strings + structure ← **SAE J2012 / ISO 15031-6**.
   - **L2 — routing groupings:** `DTCRoutingTag` + the **EP-DTC-02 eight-family P-code taxonomy** as the fault-atlas routing/registry backbone.
   - **L3 — diagnostic verdict:** `FaultFamily` — proprietary, **stays**. Not SAE-shaped (it is the answer, not the evidence). See proposal §1, §3.
2. **How a new fault gets added.** The `comlab/config/proposals/` registry + a graduation rule + a growth-safe conformance test. This is the **open mechanism** — the pack does **not** freeze the vocabulary.

> **HARD REQUIREMENT — the standard must stay open.** There are many proposed new faults
> (`labs/obdlab/research/proposals/extracted/`, 70 of them). Per the "Progress the app forward" rule, any
> that is viable to push a lab forward **will be added** — with a named consumer + code path. So every
> artefact this pack builds (taxonomy backbone, citation convention, conformance test) MUST be
> **growth-safe**: a future fault that arrives with a proper dual ISO/SAE citation **and** a named consumer
> passes automatically; one that arrives **without** a citation or a consumer **fails** the gate. The gate
> enforces signal/noise; it never hardcodes a fixed count of families/values.

The decision is **closed** when L1/L2 carry dual ISO-primary citations, the proposals registry + graduation
rule exist, the connected EPs are registered as the first entries, and the conformance+extensibility gate is
green. Implementing each registered fault's *discrimination* (sensor_fault, lean/rich, signature matrix, …)
is **not** this pack — those live in the OBDLab / COMLab / DTCLab ledgers and flow through the mechanism
this pack establishes.

---

## Mandatory reads (in order, before authoring/coding anything)

1. `labs/semantic/SEMANTIC_STANDARDIZATION_PROPOSAL.md` — the audit + decision (§1 layers, §3 verdict, §9 high-risk fixes, §10 ISO, §12 connected EPs).
2. This file.
3. `labs/semantic/tasks/PROGRESS.md` — the ledger; pick the first `pending` row whose Blocked-by IDs are all `done`.
4. The task spec for that row in `labs/semantic/tasks/`.
5. The standards inputs the task names: `labs/semantic/SAE.md`, `labs/semantic/obd2-pid-table-service-01.csv`, `labs/semantic/vocabul/{SEMANTIC_CONTRACT,OBD_VOCABULARY,DTC_VOCABULARY}.md`.

## Sandbox Python (coder, every session)

Run the canonical cache-first Python 3.14 restore block from the **root `CLAUDE.md` → "Sandbox Python"**
section before any inner-loop command. Do not re-derive it here.

## Inner loop (coder, after EVERY meaningful edit)

```
ruff check <touched dirs>
pyright <touched pkg>
pytest -x -q
```

Then fill the task's `progress_notes/<task-id>.md` `VERIFICATION GATE` + `CODE REVIEW` blocks. A row flips to
`done` only when **both** blocks are clean (CLAUDE.md HARD RULE).

## Roles (HARD RULE, from CLAUDE.md)

- **Architect** authors the task spec (Goal / Success / Context / Deliverables / Files / Out-of-scope /
  Verification / Progress-hook) and the ledger row — **no implementation code, no inner loop, no gate.**
- **Coder** implements one spec per session, runs the inner loop + the 6-phase gate, fills the note.
- **One task per session — HARD STOP.** Finish one row, update its ledger row atomically, then stop and
  tell the owner to clear context.

## Signal/noise — the one rule

Every field/enum/registry entry added must have a **named, existing or same-change** consumer in COMLab
analytics or fault-atlas routing, plus the code path that reads it. "Future use" is not a consumer. The
T-SEM-4 gate makes this mechanical.

## Git

Per CLAUDE.md: the only git action is the final commit, run by the **owner** in a terminal (bash), staging the
task's deliverables by **explicit path**. Never branch/stash; never raise git as a blocker.
