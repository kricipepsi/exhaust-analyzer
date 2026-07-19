# T-SEM-2 — proposals registry + EP-DTC-02 taxonomy backbone (the open mechanism)

**Status:** `pending` · **Pack:** SEMANTIC · **Mode:** STRICT
**Origin:** `SEMANTIC_STANDARDIZATION_PROPOSAL.md` §4.2, §12 · **Blocked by:** `T-SEM-1`
**Consumer (signal/noise):** `comlab/comlab/core/fault_atlas_router.py` — routes against the family taxonomy/registry; the registry is the named, code-read home under which every present and future fault node attaches.

### Goal ###

Build the **open extension mechanism** that lets the semantic standard stay closed while new faults keep
arriving. Three artefacts: (1) the `comlab/config/proposals/` registry (the separate proposals store CLAUDE.md
mandates — never silently in the live KG/registry); (2) the **EP-DTC-02 eight-family P-code taxonomy** as the
fault-atlas routing/registry backbone (L2), graduated from `extracted/` into config; (3) a written
**graduation rule + dual ISO/SAE citation convention** every entry must follow. Done when a new fault can be
added by dropping one well-formed registry entry under a taxonomy family, with no code change beyond that
entry and its named consumer.

### Success criteria ###

- `comlab/config/proposals/` exists with a `README.md` defining: entry schema (`id`, `family` (EP-DTC-02 P-code family), `consumer` (file + symbol), `iso_sae_citation`, `status` ∈ {proposed, pinned, graduated}, `owning_ledger`), the **graduation rule** (extracted EP → `proposed` when consumer named → `pinned` when consumer is a live reader → `graduated` to the live KG/registry when shipped+gated), and the **dual ISO/SAE citation convention** from T-SEM-1.
- The **EP-DTC-02** 8-family taxonomy (Air&Fuel P01/P02, Ignition&Misfire P03, Aux-Emissions P04, Speed&Idle P05, Computer&Output P06, plus the P00 air/fuel-metering and transmission blocks per `SAE.md`) is materialised as `comlab/config/proposals/taxonomy_backbone.{md,yaml}` with each family carrying its ISO 15031-6/SAE J2012 P-code range and a one-line "what attaches here".
- `fault_atlas_router` is shown to be able to read the taxonomy backbone (a thin loader or documented read path) — the consumer is real, not "future use".
- **Extensibility demonstrated:** the README includes a worked example of adding one new fault entry end-to-end (entry → family → consumer → citation) that the T-SEM-4 gate will accept.
- No `FaultFamily`/L3 change; no live-KG mutation (entries land in `proposals/`, not the live registry).
- Inner loop green.

### Context ###

`labs/obdlab/research/proposals/extracted/INDEX.md` L9: "When a consumer is pinned, a proposal graduates to
`comlab/config/proposals/`." That graduation target does **not exist yet** (verified: no `comlab/config/`
dir). This task creates it. **EP-DTC-02** (`extracted/EP-DTC-02_j2012-fault-taxonomy.md`) already specifies
the 8-family backbone with consumer `comlab/config/kg/* family registry + fault_atlas_router.py` — graduate it
here as the spine; it is the correctly-scoped (L2, not L3) SAE/ISO standardization the proposal endorses.

The "Progress the app forward" rule (CLAUDE.md) is the reason this is a *registry + rule*, not a frozen list:
a new fault/field and its consumer **ship together as a proposal**; this task builds the path that makes that
routine and auditable. Signal/noise is enforced structurally by the entry schema (no entry without a
`consumer`) and mechanically by T-SEM-4.

### Deliverables ###

1. `comlab/config/proposals/README.md` — entry schema + graduation rule + dual ISO/SAE citation convention + worked add-a-fault example.
2. `comlab/config/proposals/taxonomy_backbone.md` (+ optional `.yaml`) — graduated EP-DTC-02 8-family backbone with P-code ranges and ISO/SAE citations.
3. A documented/loaded read path proving `fault_atlas_router` consumes the backbone (thin loader or explicit reference in the router's family-resolution path).

### Files to touch ###

- `comlab/config/proposals/README.md` (NEW)
- `comlab/config/proposals/taxonomy_backbone.md` (NEW; optional `taxonomy_backbone.yaml`)
- `comlab/comlab/core/fault_atlas_router.py` (minimal read path only — no routing-behaviour change)
- (test for the loader is authored in T-SEM-4, not here)

### Out of scope ###

Do **not** register the individual EPs yet — that is T-SEM-3. Do **not** mutate the live KG/registry or
`FaultFamily`. Do **not** implement any discrimination logic (sensor_fault split, lean/rich, signature
matrix). Do **not** change routing *behaviour* — only add the ability to read the backbone. Off-scope finds →
`PROGRESS.md` follow-ups.

### Verification ###

```bash
cd <repo>/labs/comlab
ruff check comlab/
pyright comlab/
test -f comlab/config/proposals/README.md && test -f comlab/config/proposals/taxonomy_backbone.md \
  && echo "OK registry scaffold present" || { echo "FAIL scaffold missing"; exit 1; }
# backbone is loadable by the router's read path
python3.14 -c "from comlab.core import fault_atlas_router as r; print('router import OK')"
pytest -x -q
```

All steps pass; live KG/registry untouched (`git status` shows changes only under `comlab/config/proposals/`
+ the router read-path line).

### Progress hook ###

`tasks/progress_notes/T-SEM-2.md` opens with `## Plan`, then `VERIFICATION GATE` + `CODE REVIEW`.
PROGRESS.md `T-SEM-2`: Status=done, Files changed=N, Verification="proposals registry + EP-DTC-02 backbone
live; router read path verified; graduation rule + citation convention documented; no L3/live-KG change".
