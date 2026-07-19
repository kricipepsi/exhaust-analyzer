# T-V3-D2 — progress note (PRODUCER_GAP split)

**Task:** `T-V3-D2_producer_gap_split.md` · **Status:** done · **Author:** Codex · **Date:** 2026-07-01
**Report:** `v3/reports/V3_PRODUCER_GAP_SPLIT_2026-06-30.md`
**JSON:** `v3/reports/V3_PRODUCER_GAP_SPLIT_2026-06-30.json`

## Plan

Build a read-only split for every `PRODUCER_GAP` case from frozen on-disk artefacts only:
1. Parse `FL_LOCALIZATION_2026-06-30.md` for the 25 per-case `PRODUCER_GAP` labels.
2. Join `FL_UPSTREAM_2026-06-30.json` for expected code, required GASLab gating state, emitted GASLab state, and predicted family.
3. Replay each case's raw v7 row through GASLab and OBDLab in query mode using `v7.load_corpus.row_to_raw_inputs` and the same `wired.composition` lab helpers used by the upstream evidence harness.
4. Compare the required GASLab state against the row's actual chemistry thresholds and GASLab bound/resolution candidate lists.
5. Emit per case: expected code/family, required state, emitted state, `CLASSIFIER_FIXABLE` vs `SIGNAL_REQUIRED`, threshold evidence, missing physical quantity, and research-cluster mapping.

Result: 25 total = 2 `CLASSIFIER_FIXABLE` + 23 `SIGNAL_REQUIRED`. Signal-required clusters: Cluster 1 = 3, Cluster 2 = 11, Cluster 3 = 3, Cluster 7 = 2, Cluster 8 = 4.

## VERIFICATION GATE

```
Phase 1 Syntax/compile : PASS (`/agent_workspace/.venv-wired/bin/python -m py_compile v3/producer_gap_split.py`)
Phase 2 Lint           : PASS (`/agent_workspace/.venv-wired/bin/python -m ruff check v3/producer_gap_split.py` -> OK)
Phase 3 Types          : PASS (`PYTHONPATH=apps/wired:apps/wired/fl_tasks:labs/comlab:labs/dnalab:labs/dtclab:labs/gaslab:labs/obdlab:labs/symptomlab:labs/vinlab /agent_workspace/.venv-wired/bin/python -m pyright v3/producer_gap_split.py` -> 0 errors)
Phase 4 Tests          : PASS (`/agent_workspace/.venv-wired/bin/python v3/producer_gap_split.py` -> 25 total; CLASSIFIER_FIXABLE=2; SIGNAL_REQUIRED=23; report+json written)
Phase 5 Contract       : PASS (`grep` equivalent via tool found 25/25 total, both labels, all per-case rows; every SIGNAL_REQUIRED row names a research cluster and missing quantity)
Phase 6 Anti-orphan    : N-A (read-only analysis; no new field/enum/fault and no producer/consumer mapping)
Result: CLEAN
```

## CODE REVIEW

```
Scope         : PASS (new split script plus the two contracted report artefacts; no engine/lab/oracle/CSV/scorer edits)
Composition   : PASS (query-only replay through existing wired helpers; no labs/ edits, no graphify, no Vault edits, no legacy imports)
Consumers     : PASS (N/A for new mapped fields; output consumer is Phase-4 scoping and classifier-fix follow-up work list)
Literals      : PASS (25 expected producer gaps is from T-V3-D2/FL_LOCALIZATION; thresholds come from GASLab ontology/rule helpers, not duplicated runtime constants except cluster labels)
Docstrings    : PASS (module, dataclass, and helpers documented)
Craft (WARN)  : depth: one read-only script with parse/replay/split/render seams; deletion: no unused options or scaffolding; seam: no routing logic added to wired/labs; interface: public command `python v3/producer_gap_split.py` regenerates both artefacts
Result: CLEAN
```
