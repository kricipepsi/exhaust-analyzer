# T-VLIVE-3b — Reconcile dtclab wired consumers in `vault-map.dtclab.yaml`

## Plan

Scope: `T-VLIVE-3b` reconciles the three stale `wired:` consumer edges in `vault-map.dtclab.yaml` pointing to the phantom `dtw.py` file/task. I will drop the phantom edge from `LLD_DTCLab.md` and `DLD_DTCLab.md` and add a pending composition edge, and replace it on `12_ranking_discriminator.md` with the live COMLab fault-atlas router discriminator rank step consumer. I will verify that every other consumer in `vault-map.dtclab.yaml` resolves to a live file and symbol on disk before proceeding, and flip `T-VLIVE-3` from `blocked` to `pending` in the progress ledger.

## Verification results

- Eligibility: `T-VLIVE-3b` is the first runnable `pending` row (no blockers).
- Consumer edges updated in `_skills/graph/4dlab-vault/assets/vault-map.dtclab.yaml`:
  - `LLD_DTCLab.md` and `DLD_DTCLab.md` phantom `dtw.py` edges dropped; replaced with `"wired (pending T-WIRE-1): apps/wired/wired/composition.py DTCLabPayload mapping"`.
  - `12_ranking_discriminator.md` phantom `dtw.py` edge replaced with `"comlab: labs/comlab/comlab/core/fault_atlas_router.py routing-tag discriminator rank step"`.
- Anti-orphan check: Checked all other consumer paths in `vault-map.dtclab.yaml`. All resolve perfectly to live files and symbols. Symbol verification confirms `_load_discriminator_table` and `routing_tag` exist in `labs/comlab/comlab/core/fault_atlas_router.py`.
- Test suites:
  - `labs/dtclab/tests` -> 590 passed.
  - `labs/comlab/tests` -> 510 passed.
- Graph untouched: `labs/dtclab/graph/` remains completely clean/untouched.
- Progress Ledger: Flipped `T-VLIVE-3b` status to `done` and updated details; flipped `T-VLIVE-3` status to `pending`.

## VERIFICATION GATE

- [x] Eligibility: `T-VLIVE-3b` had no blockers and was runnable.
- [x] Framed notes: N/A (this task is map-only, no notes framed/edited).
- [x] No empty consumers: All updated mapped notes have valid, non-empty consumers.
- [x] Bases render: N/A (dry-run/mechanical check of the map passes).
- [x] Tests green: both dtclab (590 passed) and comlab (510 passed) are green.
- [x] Graph untouched: git status shows no changes to `labs/dtclab/graph/` or other graph dirs.
- [x] Anti-orphan confirmed: every remaining consumer path in `vault-map.dtclab.yaml` resolves to a live file on disk.

## CODE REVIEW

- [x] Schema conformance: N/A (map change conforms to the schema).
- [x] Live path remap: Live remapped paths in the updated consumers are correctly documented (e.g. `labs/comlab/comlab/...`).
- [x] Signal/noise: Every mapped note has at least one live named consumer.
- [x] No duplicate frontmatter: N/A (no notes written/edited).
- [x] Scope guard: Checked that no other files/notes were modified.

