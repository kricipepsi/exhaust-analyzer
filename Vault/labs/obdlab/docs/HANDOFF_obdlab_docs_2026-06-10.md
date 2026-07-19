# Handoff — OBDLab docs follow-ups (2026-06-10)

Context: this session refreshed `HLD/DLD/LLD_OBDLab.md` (v1.0→v2.0) and authored
`ADR_OBDLab.md` + `BDD_OBDLab.md` from the live `obdlab/` source. Graphify
ingestion of the docs was **deferred** (wiki-prep skill is wrong for design docs).
Below is the remaining work, one task per session.

## Disposition of the two files asked about

| File | Verdict | Action |
|------|---------|--------|
| `docs/OBDlab.md` | **Superseded historical blueprint** — describes non-existent `obd_live_lab/` tree, `mkdir/touch` build steps, old 8-PID schema, ±100 trim bounds, pre-rework math. | **Do NOT ingest.** Archive or mark `SUPERSEDED` at top. No rework. Its useful content (KG node inventory, VE math narrative) is already captured in HLD §3–6 / LLD §1–8. |
| `docs/OBD_VOCABULARY.md` | **Duplicate** (byte-identical to `labs/semantic/vocabul/OBD_VOCABULARY.md`) **and stale**. | De-duplicate (see TODO-1) + reconcile to code (see TODO-2). |

## Remaining tasks (next sessions)

**TODO-1 — De-duplicate OBD_VOCABULARY.**
Canonical home is `labs/semantic/vocabul/OBD_VOCABULARY.md` (semantic pack is the
cross-lab vocab authority, T-SEM-1…4 done). Replace `labs/obdlab/docs/OBD_VOCABULARY.md`
with a one-line pointer to the canonical file, or delete it. Confirm no doc/code
references the obdlab/docs path before removing.

**TODO-2 — Reconcile vocab to shipped code** (edit the **canonical** semantic copy):
- §12.4 `O2FailureMode`: drop `SLUGGISH`, `DEAD`, `WRONG_CENTERLINE`, `HEATER_FAULT`
  (pruned by ARCH-2); keep `NO_FAULT/STUCK_LEAN/STUCK_RICH`; add
  `WIDEBAND_OFFSET_CANDIDATE` (T-OBDV2-4 / EP-OBD-17).
- §5.2 OBDLab enums: add `FuelSystemStatus` (`CL/OL/OL_DRIVE/OL_FAULT`, T-OBDV2-6,
  mirrored from DTC_VOCABULARY §8).
- Note: semantic pack did "zero value churn" by design, so these were never its
  scope — this is OBDLab-vocab reconciliation, route via the proposals/graduation
  mechanism if a value needs a consumer check.

**TODO-3 — Archive `OBDlab.md`.**
Move to an `archive/` subfolder or prepend a `> SUPERSEDED by HLD/DLD/LLD/ADR/BDD
v2 (2026-06-10)` banner. Exclude from any graphify doc-ingestion set.

**TODO-4 — Graphify doc-prep (deferred this session).**
Craft a **doc-specialized** prep skill (architectural predicates: `consumes`,
`mirrors_contract_in`, `supersedes`, `verifies`; entities: modules, schemas,
task-IDs) — `4dlab-wiki-prep` is built for the domain chunk corpus, not design
docs. Then prep + ingest HLD/DLD/LLD/ADR/BDD. Do **not** include `OBDlab.md` or
the duplicate vocab.

**TODO-5 — Optional: refresh `PRD_OBDLab.md` / `drift_inventory_*.md`** to v2 if
still used as task inputs (low priority; not on the critical path).

## Open code follow-up (coder lane, not architect)
- **FU-OBD-DOC-3**: `obdlab/schemas/vocabulary.py` docstring says "7 StrEnums" —
  now 8 (`FuelSystemStatus` added). One-line docstring fix when next touching it.

## Verified this session (AST ground-truth)
`OBDLivePayload` = 31 fields · `ObdLabDnaView` = 7 · vocabulary = 8 StrEnums
(O2FailureMode=4) · bounds = 12 · no live Physics Gate 3 · exceptions under
`ObdLabError`. Docs match.
