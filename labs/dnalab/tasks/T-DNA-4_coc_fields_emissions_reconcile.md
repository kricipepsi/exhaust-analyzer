# T-DNA-4 — Formalize CoC fields + reconcile emissions block

### Goal ###

Resolve two latent data-flow bugs surfaced by the 2026-06-11 audit, both rooted in
`VinDNA`'s shape disagreeing with what COMLab's projector reads:

1. **CoC empirical fields are unconsumed orphans.** `target_lambda_v112`,
   `co_low_idle`, `co_high_idle` (and the other CoC/type-approval/noise fields) are
   **top-level** on `VinDNA` but `projection.py:79-81` reads them from `emissions{}` →
   always `None`. They are also absent from `SEMANTIC_CONTRACT.md §4.1`.
2. **Emissions flags read at the wrong nesting.** `projection.py` reads
   `has_catalyst` / `egr_equipped` at **top level**, but `VinDNA` nests them under
   `emissions{}` → always `None`. Contract §4.1 lists `downstream_o2_present` +
   `secondary_air_equipped` and **no `has_catalyst`**, while `VinDNA.Emissions` carries
   `has_catalyst` + `downstream_trim_role` and drops `secondary_air_equipped` —
   a three-way drift to reconcile.

The DNA-side deliverable is the **canonical schema decision + contract amendment**;
the matching `projection.py` path fix is paired **COMLab-C** (separate codebase).

### Named signal/noise consumer ###

GASLab CoC threshold tables — `co_high_idle` is a proven live consumer
(`gaslab/resolution.py`, task CHI-1) and the gaslab DNA-ingestion wiki §1.4 lists
`target_lambda_v112` / `co_low_idle` / `co_high_idle` as `vin_dna.*` top-level reads.
Emissions flags gate EGR_STUCK (GAS) and CATALYST/EGR_HISTORY routing (DTC).
**Anti-orphan rule:** every CoC field kept in the contract must name such a consumer;
any with none moves to a proposal or is pruned — do not formalize an unconsumed field.

### Success criteria ###

- A short canonical-shape decision recorded in the progress note: CoC fields are
  **top-level** `vin_dna.*` (matches gaslab wiki); emissions membership reconciled
  (keep `has_catalyst` vs `secondary_air_equipped` — decide with the gaslab/dtc
  consumers, cite each).
- `SEMANTIC_CONTRACT.md §4.1` amendment drafted (CoC fields + reconciled `emissions`
  block) — flagged for COMLab/semantic sign-off.
- `VinDNA.to_json()` output verified against the decided paths by a test (assert
  `target_lambda_v112` is top-level, `has_catalyst` under `emissions`).
- **COMLab-C dependency registered** in `proposals/entries.yaml`: `projection.py` must
  read CoC top-level and emissions flags at `emissions.*`. (DNA task does not edit
  `projection.py`.)
- Per-field consumer audit table in the progress note: field → gaslab/dtc consumer →
  keep / proposal / prune.
- Inner loop clean on every edited file.

### Files to touch ###

- `labs/vinlab/vinlab/models.py` (MODIFY — comments/alignment only if the decision
  keeps the current shape; otherwise minimal field move with consumer justification)
- `labs/vinlab/tests/test_models.py` (MODIFY — serialized-path assertions)
- `labs/comlab/comlab/config/proposals/entries.yaml` (ADD COMLab-C dependency note)

### Out of scope ###

Editing `projection.py` (COMLab-C). Adding new CoC fields beyond those already on
`VinDNA`. The `rated_rpm` field (→ T-DNA-3). Changing CoC numeric values.

### On completion ###

Both gates clean in `progress_notes/T-DNA-4.md`; flip T-DNA-4 → `done`. STOP.

### Verification ###

```bash
cd $HOME/mnt/4DLab/labs/vinlab
ruff check vinlab/ && pyright vinlab/
python3.14 -c "from vinlab.models import VinDNA; import json; d=VinDNA().to_json(); print('top-level CoC:', 'target_lambda_v112' in d); print('emissions nested:', 'has_catalyst' in d.get('emissions',{}))"
grep -rn "co_high_idle\|target_lambda_v112" ../gaslab/code/ 2>/dev/null   # consumer proof
pytest tests/ -x -q --tb=short
```
