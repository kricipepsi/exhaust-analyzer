# T-VLIVE-5b — Reconcile vinlab DNALab/COMLab consumers in `vault-map.vinlab.yaml`
**Pack:** VAULT-LIVE · **Lane:** vault-tooling / architect-authoring (map asset) · **Mode:** STRICT
**Blocks:** T-VLIVE-5 (vinlab framing cannot pass the anti-orphan gate until this lands)
**Load skills:** `_skills/graph/4dlab-vault/SKILL.md`, `_skills/graph/4dlab-doc-prep/SKILL.md` (Step 4/5 orphan rule).

## Goal
Repoint the vinlab `dnalab:`/`comlab:` consumer edges that name **symbols on the
wrong file** to their real live readers, so T-VLIVE-5 frames vinlab with zero
`MISSING` consumers. Like dnalab (T-VLIVE-4b), this is a **naming** fix — the data
*is* consumed live, just under different symbols/files. The vinlab-internal
(`vinlab: …decoder.py …`) edges already resolve and are untouched.

## Context (why the edges are stale)
Three wrong attributions, each verified against the live tree:
- **`decode_vin_payload` is not in `dnalab/assembly.py`.** It is
  `labs/vinlab/vinlab/decoder.py:520 RobustVINDecoder.decode_vin_payload`. DNALab's
  integration symbol is `build_vehicle_dna` (`assembly.py:14`), which calls
  `vinlab.decode` (`from vinlab import decode as _decode_vin`, `assembly.py:9,40`)
  and assembles the result into `VehicleDNA.vin_dna`.
- **`lab_pipeline_aggregator.py` reads no `VinDNA`/`rated_rpm`** (grep: zero hits).
  The VehicleDNA envelope is read by `labs/comlab/comlab/projection.py` →
  `project()` (`rated_rpm=vin.get("rated_rpm")`, `projection.py:93`; the field is
  `lab_dna_views.py:56 LabDnaView.rated_rpm`).
- **`perception_contradiction.py` references no `FuelSystemStatus`** (grep: zero
  hits). The live `FuelSystemStatus` comparison is
  `labs/comlab/comlab/core/fault_atlas_router.py:294` (`fuel_system_status ==
  FuelSystemStatus.CL`, import at `:41`).

## Decision (architect-pinned — do not redesign)
Repoint as below; **grep-verify each target resolves AND matches the note's body
before writing**; route back any note whose body does not support the repointed
reader (do not force an edge).

| Note (map line) | Stale edge | Repoint to (live read) |
|---|---|---|
| `HLD_VINLab.md` (26), `LLD_VINLab.md` (45), `DLD_VINLab.md` (73) | `dnalab: …assembly.py decode_vin_payload() …` | `dnalab: labs/dnalab/dnalab/assembly.py build_vehicle_dna (vinlab.decode → VehicleDNA.vin_dna, Part A)` — the decode itself is already credited to `vinlab decoder.decode_vin_payload` on `10_decode_scope_rules.md` |
| `HLD_VINLab.md` (27), `LLD_VINLab.md` (46), `DLD_VINLab.md` (75) | `comlab: …lab_pipeline_aggregator.py (VinDNA integration)` | `comlab: labs/comlab/comlab/projection.py project() (VehicleDNA → LabDnaView, reads vin_dna)` |
| `LLD_VINLab.md` (47), `DLD_VINLab.md` (76) | `comlab: …perception_contradiction.py (FuelSystemStatus comparison)` | `comlab: labs/comlab/comlab/core/fault_atlas_router.py (FuelSystemStatus.CL comparison, :294)` |
| `11_engine_resolution.md` (114) | `comlab: …lab_pipeline_aggregator.py (VinDNA.rated_rpm)` | `comlab: labs/comlab/comlab/projection.py project() vin.get("rated_rpm") → LabDnaView.rated_rpm` |

**Leave untouched (already resolve):** `PRD_VINLab.md` (16) `build_vehicle_dna`;
`DLD_VINLab.md` (74) `dnalab/models.py VinDNA.from_json` (used at `models.py:106`);
all `vinlab: …decoder.py / overlay/*` edges (94–96, 110–113, 127 — symbols verified
present). **No note is demoted to `plain`**: every vinlab note keeps ≥1 live
consumer after the repoint.

## Files to touch
- edit (consumer edges only): `_skills/graph/4dlab-vault/assets/vault-map.vinlab.yaml`
  — the 9 edges across HLD/LLD/DLD + `11_engine_resolution.md` per the table.
- edit: `apps/vault/VAULT_LIVE_PROGRESS.md` (flip T-VLIVE-5 `blocked` → `pending`).

## Out of scope
- Any other map asset; vinlab note bodies/frontmatter (that is T-VLIVE-5); any
  Python; any graph; the vinlab→dnalab→comlab schema itself; `Vault/`.

## Verification
1. No stale attributions remain:
   `grep -nE 'assembly.py decode_vin_payload|lab_pipeline_aggregator.py \(VinDNA|perception_contradiction.py \(FuelSystemStatus' _skills/graph/4dlab-vault/assets/vault-map.vinlab.yaml`
   → no matches.
2. Every repointed target resolves to a live read:
   - `grep -n 'def build_vehicle_dna' labs/dnalab/dnalab/assembly.py`
   - `grep -n 'def decode_vin_payload' labs/vinlab/vinlab/decoder.py`
   - `grep -n 'rated_rpm=vin.get' labs/comlab/comlab/projection.py`
   - `grep -n 'FuelSystemStatus.CL' labs/comlab/comlab/core/fault_atlas_router.py`
3. Re-run the T-VLIVE-5 anti-orphan gate (dry-run vinlab framing): every named
   consumer + `implements`/`drift_guards` path resolves; zero unresolved. No note
   bodies written by this task.
4. `git --no-pager diff --stat` shows only the two files above touched.

## Success criteria
`vault-map.vinlab.yaml` names a live reader for every consumer edge; T-VLIVE-5 row
is `pending` (runnable) and its anti-orphan gate passes on re-run.

## Progress hook
`VAULT_LIVE_PROGRESS.md` T-VLIVE-5b: Status=done, Files changed=2,
Verification="decode_vin_payload → assembly.build_vehicle_dna; aggregator VinDNA/rated_rpm → projection.py; perception_contradiction FuelSystemStatus → fault_atlas_router; T-VLIVE-5 unblocked".
