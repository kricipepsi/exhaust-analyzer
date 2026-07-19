## Plan

I am beginning task `T-VLIVE-5b` to reconcile the vinlab DNALab/COMLab consumer edges in `vault-map.vinlab.yaml`. I will repoint the 9 incorrect consumer attributions to their correct live targets (in `assembly.py`, `projection.py`, and `fault_atlas_router.py`), confirm every target resolves, and then update `VAULT_LIVE_PROGRESS.md` to flip `T-VLIVE-5` from `blocked` to `pending`.

## Verification results

- Stale edges check: `grep` for `decode_vin_payload`, `lab_pipeline_aggregator.py (VinDNA`, and `perception_contradiction.py (FuelSystemStatus` in `vault-map.vinlab.yaml` returned 0 results.
- Target resolution check:
  - `labs/dnalab/dnalab/assembly.py:14 def build_vehicle_dna` exists.
  - `labs/vinlab/vinlab/decoder.py:520 RobustVINDecoder.decode_vin_payload` exists.
  - `labs/comlab/comlab/projection.py:93 rated_rpm=vin.get("rated_rpm")` exists.
  - `labs/comlab/comlab/core/fault_atlas_router.py:294 FuelSystemStatus.CL` exists.
- Diff check: `git status` shows only `vault-map.vinlab.yaml` under skills and progress tracking files touched.

## VERIFICATION GATE

- [x] Eligibility: `T-VLIVE-5b` is a pending task with status `pending` and blocked by `—`.
- [x] No stale edges remain in map file: verified.
- [x] Every repointed target resolves to a live read: verified.
- [x] Ledger updated: `T-VLIVE-5` status flipped from `blocked` to `pending`.

## CODE REVIEW

- [x] Schema conformance: no new fields introduced.
- [x] Live path representation: targets use correct package names (e.g. `dnalab` / `comlab` core).
- [x] Signal/noise: no notes demoted to `plain`; every note still has at least one live consumer.
