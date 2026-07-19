# T-DNA-6 — `fuel_type` proposal (+ `altitude_band` context note)

### Goal ###

The reworked GASLab DNA-ingestion wiki (§1.4) lists two **proposed v2** context-only
fields it would consume: `fuel_type` (E5/E10/winter-blend λ-correction context) and
`altitude_band` (informational; λ math is altitude-invariant). Register these
correctly per the v2-rework proposal model instead of letting them sit as "future
use" or leak silently into the live schema.

### Named signal/noise consumer ###

- `fuel_type` → GASLab `lab_dna_views` context for E5/E10 blend correction
  (gaslab wiki §1.4 `[v2: q9]`). Consumer is **proposed**, not yet live → this ships
  as a **proposal**, not a live `VinDNA` field.
- `altitude_band` → context-only, and the gaslab wiki states it relaxes **no** gate
  (λ is altitude-invariant). It is **session/context**, not a `VinDNA` attribute →
  document as non-schema; do **not** add it to `VinDNA`.

### Success criteria ###

- A proposal entry in `labs/comlab/comlab/config/proposals/entries.yaml` for
  `fuel_type`: the field, its `gaslab/lab_dna_views` consumer + code path, the
  E5/E10 rationale, and a draft contract §4.1 line. Status: **proposal** (ships when
  the gaslab consumer lands; not added to live `VinDNA` here).
- A one-paragraph note (progress note or the proposal entry) recording `altitude_band`
  as deliberately **not** a schema field, with the altitude-invariance reason.
- No live `VinDNA` schema change in this task (proposal-only) — unless the owner
  elects to land `fuel_type` together with the gaslab consumer in a paired session.
- Inner loop: n/a for code (config + docs); `ruff`/`pyright` only if any `.py` touched.

### Files to touch ###

- `labs/comlab/comlab/config/proposals/entries.yaml` (ADD `fuel_type` proposal)
- `labs/dnalab/docs/research/` or the progress note (altitude_band rationale)

### Out of scope ###

Adding `fuel_type` to the live `VinDNA`/contract (deferred to the paired gaslab-consumer
session). Any λ-correction math (GASLab owns it). `altitude_band` as a schema field.

### On completion ###

Proposal registered and altitude_band documented; flip T-DNA-6 → `done`. STOP.

### Verification ###

```bash
cd $HOME/mnt/4DLab/4DLabV2
grep -n "fuel_type" labs/comlab/comlab/config/proposals/entries.yaml   # proposal present
grep -rn "fuel_type\|altitude_band" labs/gaslab/wiki/01_role_boundaries_dna_ingestion.md  # consumer provenance
```
