# T-VLIVE-3b — Reconcile dtclab wired consumers in `vault-map.dtclab.yaml`
**Pack:** VAULT-LIVE · **Lane:** vault-tooling / architect-authoring (map asset) · **Mode:** STRICT
**Blocks:** T-VLIVE-3 (dtclab framing cannot pass the anti-orphan gate until this lands)
**Load skills:** `_skills/graph/4dlab-vault/SKILL.md`, `_skills/graph/4dlab-doc-prep/SKILL.md` (Step 4/5 orphan rule).

## Goal
Replace the three stale `wired:` consumer edges in `vault-map.dtclab.yaml` —
all pointing at the phantom `labs/wired/wired/adapters/dtw.py T-DTW-1 adapter` —
with edges that resolve to live reads (or a named live COMLab reader), so
T-VLIVE-3 frames dtclab with zero `MISSING` consumers.

## Context (why the edges are stale)
`T-DTW-1` and `labs/wired/wired/adapters/dtw.py` do **not exist** anywhere in the
live tree — no task spec, no file, no `adapters/` dir. The reference is doubly
wrong: wrong package root (`labs/wired/` — the wired package lives at `apps/wired/`
per `apps/wired/wired_tasks/T-WIRE-1_compose_labs_comlab.md`) **and** a phantom
file/task. Provenance: in the archived composition the "T-DTW-1 adapter" was the
DTC **top-3 `LabResult` adapter** (`from dtclab.ranking import classify_top3 …
# consumer: T-DTW-1 LabResult adapter`, `_build_dtc_lab_result`,
`ARCHIVE/4DLabWired/wired/composition.py:59,562`) — an in-`composition.py` helper,
never a standalone `dtw.py`. That top-3 adapter is **not** in the current wired
plan (T-WIRE-1..4 = compose / oil-case runner / OTel / FATAL-gate; no top-3
adapter task). So the edge cannot be repointed to a live or even authored path.

This mirrors the comlab map fix already applied (`vault-map.comlab.yaml`, the
`apps/4DLabWired` → `apps/wired/wired/composition.py (pending T-WIRE-1)` repoint).

## Decision (architect-pinned — do not redesign)
Three notes carry the phantom edge. Two already have live consumers; one does not.

1. **`LLD_DTCLab.md`** and **`DLD_DTCLab.md`** — already framed by four live
   `comlab:` consumers (`fault_atlas_router` DTCRoutingTag routing,
   `lab_pipeline_aggregator` DTCLabPayload integration, `perception_contradiction`,
   `power_loss_analytics`). **Drop** the phantom `dtw.py` edge. **Add** one
   pending forward edge to keep the wired→DTC dependency documented (same form as
   the comlab fix):
   `"wired (pending T-WIRE-1): apps/wired/wired/composition.py DTCLabPayload mapping"`
   — justified: `diagnose()` maps each lab output into a COMLab payload incl.
   `DTCLabPayload` (T-WIRE-1 Goal; cf. archived `dtc_lab_output=dtc_output`).

2. **`12_ranking_discriminator.md`** — its **only** consumer is the phantom edge,
   so dropping it alone would orphan the note. Its body self-declares as reference
   material that "inform[s] the existing COMLab rank/route step" (no schema field).
   The live home of that step is the `fault_atlas_router` discriminator table.
   **Replace** the phantom edge with the real live consumer:
   `"comlab: labs/comlab/comlab/core/fault_atlas_router.py routing-tag discriminator rank step"`
   (live read: `_load_discriminator_table`,
   `_DEFAULT_DISCRIMINATOR_PATH = config/tag_discriminator.yaml`, `routing_tag`).

The legacy DTC top-3 `LabResult` adapter is **out of scope** here — if it is to be
ported it needs its own authored wired task; it is not a vault-map consumer until
then. Do not invent a `T-DTW-1` row to satisfy the edge.

## Files to touch
- edit (consumer edges only): `_skills/graph/4dlab-vault/assets/vault-map.dtclab.yaml`
  — 3 edges at the `LLD_DTCLab.md`, `DLD_DTCLab.md`, `12_ranking_discriminator.md` entries.
- edit: `apps/vault/VAULT_LIVE_PROGRESS.md` (flip T-VLIVE-3 `blocked` → `pending`).

## Out of scope
- Any other map asset; dtclab note bodies/frontmatter (that is T-VLIVE-3); any
  Python; any graph; porting the top-3 adapter; `Vault/`.

## Verification
1. `grep -n 'dtw.py\|T-DTW-1' _skills/graph/4dlab-vault/assets/vault-map.dtclab.yaml`
   → no matches.
2. Every remaining dtclab consumer resolves to a live read:
   `fault_atlas_router.py` discriminator symbols present
   (`grep -n '_load_discriminator_table\|routing_tag' labs/comlab/comlab/core/fault_atlas_router.py`);
   the `(pending T-WIRE-1)` wired edges carry the pending marker (not a bare path).
3. Re-run the T-VLIVE-3 anti-orphan gate (dry-run the dtclab framing): every named
   consumer + `implements`/`drift_guards` path resolves; zero unresolved. No note
   bodies written by this task.
4. `git --no-pager diff --stat` shows only the two files above touched.

## Success criteria
`vault-map.dtclab.yaml` has zero phantom edges; all dtclab consumers resolve to a
live read or a `(pending T-WIRE-1)` forward edge; T-VLIVE-3 row is `pending`
(runnable) and its anti-orphan gate passes on re-run.

## Progress hook
`VAULT_LIVE_PROGRESS.md` T-VLIVE-3b: Status=done, Files changed=2,
Verification="phantom dtw.py/T-DTW-1 edges removed; note 12 → live fault_atlas_router discriminator; LLD/DLD → pending composition.py edge; T-VLIVE-3 unblocked".
