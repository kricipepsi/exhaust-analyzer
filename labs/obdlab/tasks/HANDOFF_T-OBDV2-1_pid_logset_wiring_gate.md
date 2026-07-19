# Handoff — T-OBDV2-1: PID-logset wiring gate (the un-quarantine proof)

**For:** next session (architect authors the task spec; coder then runs it). **Date:** 2026-06-08.
**Status going in:** gate `T-OBDV2-0` = **revive (emitter)** is done. `T-OBDV2-1` is **not yet authored** — this
handoff is what you need to author it without re-deriving context.

---

## 1. What this task is, in one line

Prove OBDLab is no longer "dead": build a set of **PID-bearing test fixtures** and a test that drives the live
`translate()` pipeline to **discriminating, non-`NO_FAULT` output** across the coverage matrix. This converts
the revive decision from ratified *intent* into demonstrated *capability*.

## 2. Why it exists (don't re-litigate)

The >95% NO_FAULT that quarantined OBDLab was a **PID-less-corpus artefact, not a code defect**
(`wiki/PID_LOGSET_RESEARCH_PROMPT.md` L24-26; audit Culprit 2). The pipeline already emits a typed
`OBDLivePayload`; it was starved of input. T-OBDV2-0 decided revive **as an emitter** — OBDLab emits typed
*perceptions* (trims, λ, VE, `o2_failure_mode`, gates), and COMLab judges (`KGtopic.md` division-of-labor). So
this task proves the **emitter** produces non-trivial channels — it does **not** ask OBDLab to name fault
families. Assert on channels, never on a fault-family verdict.

## 3. Inputs already in place (read these, narrow)

- **The logset spec itself:** `wiki/PID_LOGSET_RESEARCH_PROMPT.md` — carries the exact input contract (Part A
  raw PIDs, Part B `ObdLabDnaView`), the 8-cell coverage matrix, the fault families in scope, and the output
  JSON shape. This is the authoring spec for the fixtures.
- **Signatures (the research, now incorporated):** `research/chunks/fuel-trim/*`, `research/chunks/o2-logic/*`,
  `research/chunks/delta-relations/*`, `research/chunks/ecu-diagnosis/*`, and `research/formula-wiki/*` — the
  documented PID→signal values per fault family on 1990–2010 petrol.
- **PID decode reference:** `research/obd2-pid-table-service-01.csv` — SAE J1979 table (scale/offset/min/max/
  unit). Use it to keep raw PID values in real ranges. It also fixes the ±127 question: **real STFT range is
  −100…+99 %**, so ±127 is a saturation sentinel, not a reading — fixtures should use realistic trims.
- **Working model:** the 6 existing fixtures in `tests/regression/fixtures/case_0*.json` show the JSON shape
  `translate()` already consumes (`raw_pids` + `dna_view_json`) — mirror their structure.
- **The contract being exercised:** `obdlab/core/sensor_signal_translator.py::translate()` → `OBDLivePayload`
  (`obdlab/schemas/payload.py`); DNA view `obdlab/schemas/dna_view.py::ObdLabDnaView`.

## 4. Deliverable shape (what "done" looks like)

1. A PID logset — ~25–40 JSON fixtures covering the matrix in `PID_LOGSET_RESEARCH_PROMPT.md` §"Coverage
   matrix" (3 VE branches, 3 O2 types, lambda outcomes, trim outcomes, VE-validity faults, RPM/thermal states,
   trim-analytics gates, and the boundary/rejection cases).
2. A signal-map table: `case_id → the single OBDLab channel it is designed to move` (the prompt asks for this).
3. A wiring-gate **test** that loads the logset, runs `translate()` on each, and asserts the designed channel
   actually moved (and that rejection cases raise the typed error, not crash).

## 5. Decisions to PIN before/while authoring (architect work — do not leave to the coder)

These are open. Resolve them in the task spec or with the owner:

1. **Pass threshold.** What makes the gate green? e.g. "≥ N cases emit a non-`NO_FAULT`/non-default channel,
   and every matrix cell has ≥ 1 passing case." Pin a number, not "looks discriminating."
2. **Where the logset lives.** New `tests/pid_logset/` dir vs extending `tests/regression/fixtures/`. Recommend
   a dedicated dir so the un-quarantine set is distinct from the 6 legacy regression cases.
3. **Split into two tasks?** ~25–40 cases × per-row (source signature → encode PIDs → cite) is likely **>1
   half-session** (breakdown checklist: ≥20 units of per-row work = split). Recommended split:
   **T-OBDV2-1a** author the logset + signal-map (data), **T-OBDV2-1b** wire the gate test + prove (code).
4. **CSV usage.** Reference-only (architect reads it to set ranges) vs a small decode helper. Default:
   reference-only — do **not** build a J1979 decoder this task didn't ask for (signal/noise).
5. **Sourcing rigor.** The prompt requires citing every non-obvious numeric and flagging estimates. Decide
   whether unsourced/estimated cases are allowed in the gate or quarantined to a separate file.

## 6. Sequencing — important interaction with PURGE-2

`PID_LOGSET_RESEARCH_PROMPT.md` Part B lists `emissions.egr_equipped` as a DNA field. **T-OBDV2-PURGE-2
removes `ObdEmissionsView` / `emissions` from `ObdLabDnaView`.** So author the logset against the
**post-PURGE-2 schema**: fixtures must **not** carry `emissions` or `resolved_horizon`. Cleanest order:

> run **PURGE-1 → PURGE-2 → T-OBDV2-1** so fixtures pin the final DNA contract and don't need rework.

If T-OBDV2-1 is authored before PURGE-2 lands, explicitly note "DNA view = post-purge: no `emissions`,
no `resolved_horizon`" in the task's Context so the coder doesn't copy the stale Part B field list.

## 7. Scope guardrails (carry into the task file)

- **Petrol, 1990–2010, NA + turbo only.** No diesel, no out-of-window GDI/forced-induction families.
- **Emitter assertions only** — assert on `OBDLivePayload` channels (`o2_failure_mode`, `normalized_obd_lambda`,
  `ve_pct`/`ve_validity`, `trim_analytics_gate`, trims), never on a fault-family verdict or a top-3 list.
- **Signal/noise still applies** — this task adds no schema field; if it's tempted to, name the COMLab consumer
  or cut it.
- **No cross-lab imports**; **no graphify / KG rebuild** — `graph/v2_current/graph.json` is canonical
  (`CLAUDE.md`: never re-run extraction unless instructed). This task touches fixtures + a test, not the graph.
- **One task per session.** If you adopt the 1a/1b split, author 1a, stop, run it, then 1b next session.

## 8. First action next session

Author `tasks/T-OBDV2-1_pid_logset_proof.md` (or the 1a/1b pair) from §3–§7 above, add the row(s) to
`tasks/PROGRESS.md` (the T-OBDV2-1 placeholder row is already there), create the progress-note stub(s), then
hand to the coder. Do **not** run the inner loop yourself (architect role).
