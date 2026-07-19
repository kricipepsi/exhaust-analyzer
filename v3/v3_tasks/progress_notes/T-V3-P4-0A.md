# Progress Note — T-V3-P4-0A: Classifier-fixable recheck

Read-only disclosure for [[T-V3-P4-0A_classifier_fixable_recheck]] against `POST_T_V3_3D`.

## Disclosure Summary
- **Headline**: 2 CLASSIFIER_FIXABLE cases rechecked; **1 already-bank / 0 classifier-fix / 1 re-bucket**.
- **`era2_008`**: `ALREADY_BANKS`. Expected `cam_timing` appears at top-3 rank 2 (`sensor_fault`, `cam_timing`, `catalyst_failure`); it remains abstained by margin, so no classifier commit is needed.
- **`CASE-039`**: `RE-BUCKET_TO_SIGNAL`. `POA_SIGNATURE` is reachable only as a co-surviving catch-all, but live GASLab emission stays `EGR_STUCK_OPEN`; no safe one-case threshold/enum fix exists without broad EGR/POA neighbour risk. Route to the ECU/control evidence signal path.
- **Self-check**: replayed 294 accuracy cases; drift=0.
- **Artifacts**: `v3/reports/V3_P4_CLASSIFIER_FIXABLE_RECHECK_2026-07-01.md`, `v3/reports/V3_P4_CLASSIFIER_FIXABLE_RECHECK_2026-07-01.json`, `v3/p4_classifier_recheck.py`.

## VERIFICATION GATE — T-V3-P4-0A
1. Compile : PASS  (`.venv-wired/bin/python -m py_compile v3/p4_classifier_recheck.py`)
2. Lint    : PASS  (`.venv-wired/bin/python -m ruff check v3/p4_classifier_recheck.py` -> OK)
3. Types   : PASS  (`PYTHONPATH=apps/wired:apps/wired/fl_tasks:apps/wired/v7:labs/comlab:labs/dnalab:labs/dtclab:labs/gaslab:labs/obdlab:labs/symptomlab:labs/vinlab:v3 .venv-wired/bin/python -m pyright v3/p4_classifier_recheck.py` -> 0 errors)
4. Tests   : PASS  (`.venv-wired/bin/python v3/p4_classifier_recheck.py` -> 1 already-bank / 0 classifier-fix / 1 re-bucket; self-check drift=0; report+json written. `score_v3_yardstick.py score --results apps/wired/v7/runs/POST_T_V3_3D/results.json` -> Hash lock ok, top3_family 193/294, coverage 216/294.)
5. Contract: PASS  (both target case_ids present with verdicts; `era2_008` rank answered; `CASE-039` neighbour risk surfaced; no engine/lab/registry/oracle/corpus/scorer edits)
6. Orphan  : N-A  (no field/consumer mapping added)
Result: CLEAN

## CODE REVIEW — T-V3-P4-0A
Scope         : PASS  (only the read-only helper and contracted report artifacts under `v3/` were created)
Composition   : PASS  (no lab edits, no registry/engine edits, no legacy/deferred path imports; lab calls are read-only query/replay only)
Consumers     : PASS  (no new mapped fields; consumer is owner go/no-go for `T-V3-P4-0B`)
Literals      : PASS  (no threshold literals changed; reported numeric bounds are read from live GASLab ontology/replay)
Docstrings    : PASS  (module docstring plus `ReplayCase` and helper function docstrings where public-ish)
Craft (WARN)  : Depth: helper is a thin disclosure driver around existing replay paths. Deletion: no speculative commit code; reports are generated artifacts. Seam: classifier decisions remain in GASLab/COMLab, not copied into the helper. Interface: task surface is CLI + MD/JSON reports, not private test hooks.
Result: CLEAN
