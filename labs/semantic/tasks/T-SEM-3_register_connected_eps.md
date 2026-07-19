# T-SEM-3 — register the connected EPs as the first registry entries

**Status:** `pending` · **Pack:** SEMANTIC · **Mode:** STRICT
**Origin:** `SEMANTIC_STANDARDIZATION_PROPOSAL.md` §9, §12 · **Blocked by:** `T-SEM-2`
**Consumer (signal/noise):** each entry carries its **own** named consumer (e.g. EP-COM-05 → `perception_contradiction.py`; EP-OBD-17 → `fault_atlas_router.py`; EP-COM-06 → `fault_atlas_router` discriminator table). The registry as a whole is consumed by `fault_atlas_router`.

### Goal ###

Populate the new `comlab/config/proposals/` registry with its **first entries**: the in-house EPs already
connected to semantic standardization (proposal §12). This makes the open mechanism real and captures the
forward-progress fault work so it is tracked, citable, and signal/noise-checked — **without implementing any
of it**. Each entry is a pointer: which EP, which EP-DTC-02 family it attaches under, its named consumer +
code path, its dual ISO/SAE citation, its `status`, and the **owning lab ledger** where implementation runs.
Done when every connected EP is a well-formed registry entry that T-SEM-4 accepts.

### Success criteria ###

- Registry entries created (status `proposed`, pointing to their `extracted/` source + owning ledger):
  - **EP-DTC-02** — already the backbone (graduated in T-SEM-2); cross-link only.
  - **EP-COM-05** semantic-coherence paradigm → consumer `comlab/core/perception_contradiction.py` (coherence flag) + `fault_atlas_router.py`; family: cross-cutting policy. Owning ledger: COMLab.
  - **EP-COM-04** ECU-hardware-fault checker → consumer `comlab/core/ecu_hardware_checker.py` (new) ; family: P06 Computer&Output. Owning ledger: COMLab. (Names the consumer for the EP-ECU-01..07 nodes.)
  - **EP-COM-06** traditional-fault signature matrix → consumer `fault_atlas_router.py` discriminator table; family: multiple (Air&Fuel/Ignition/Aux). Owning ledger: COMLab.
  - **EP-OBD-17** `WIDEBAND_OFFSET` O₂ failure-mode → producer `obdlab/core/o2_normalizer.py`, consumer `fault_atlas_router.py` (sensor-fault calibration node); family: Air&Fuel-metering / sensor. Owning ledger: OBDLab.
  - **EP-DTC-01** DTC causal hierarchy (root-vs-symptom) → consumer `fault_atlas_router.py`; family: cross-cutting. Owning ledger: DTCLab.
  - **EP-COM-15** truth-perception test corpus → consumer COMLab test harness + `perception_contradiction`; type: validation asset. Owning ledger: COMLab.
  - **EP-OBD-14** semantic-consistency gates → producer `obdlab/core/semantic_consistency_checker.py`, consumer EP-COM-04/05; family: P06 / sensor. Owning ledger: OBDLab.
- **Every entry has a non-empty `consumer` (file + symbol) and a dual ISO/SAE citation** (or, for cross-cutting policy entries, an explicit `family: cross-cutting` + the consumer code path). No entry is "future use".
- Entries map the proposal's high-risk fixes: HR-1 sensor_fault → {EP-COM-05, EP-COM-04, EP-OBD-14, EP-OBD-17}; HR-2 lean/rich → {EP-COM-05, EP-COM-03 (cross-link), EP-COM-15}; HR-3 cam_timing → {EP-COM-06, EP-DTC-02}. The mapping is recorded in the registry README's "high-risk index".
- No implementation, no `FaultFamily`/live-KG change. Inner loop green.

### Context ###

These EPs are **extracted specs, not live code** — consumers named, none verified as a live reader
(`INDEX.md` L5). Registering them here is the bridge: it moves them from a research folder into the auditable
`proposals/` store at status `proposed`, so the owning lab can later pin the consumer (`pinned`) and ship it
(`graduated`) through the T-SEM-2 graduation rule. This is exactly the "viable new fault gets added with a
named consumer" path the owner requires — applied first to the work we already have in hand.

Selection rule for *this* task: register **only** the EPs the proposal §12 names as connected to
standardization/discrimination. The other ~58 extracted EPs are registered by their owning labs as they
become relevant — the mechanism is open, but this task does not bulk-import the whole catalogue.

### Deliverables ###

1. `comlab/config/proposals/entries/EP-*.md` (or a single `entries.yaml`) — one well-formed entry per connected EP above.
2. `comlab/config/proposals/README.md` — append the "high-risk index" mapping HR-1/2/3 → entries.

### Files to touch ###

- `comlab/config/proposals/entries/` (NEW entries) or `comlab/config/proposals/entries.yaml` (NEW)
- `comlab/config/proposals/README.md` (append high-risk index)

### Out of scope ###

Do **not** implement any EP (no checker, no matrix, no o2 mode, no coherence flag — those run in the OBDLab /
COMLab / DTCLab ledgers). Do **not** bulk-import all 70 extracted EPs. Do **not** touch `FaultFamily`, the
live KG/registry, or any analytics module. Off-scope finds → `PROGRESS.md` follow-ups.

### Verification ###

```bash
cd <repo>/labs/comlab
ruff check comlab/ 2>/dev/null || true   # config-only task; ruff applies if any .py loader touched
# every entry has a consumer + citation (the signal/noise guard, also enforced by T-SEM-4)
python3.14 - <<'PY'
import pathlib, sys
root = pathlib.Path("comlab/config/proposals")
entries = list((root/"entries").glob("*")) if (root/"entries").exists() else [root/"entries.yaml"]
assert entries, "no registry entries created"
print(f"OK {len(entries)} entries present (content checked by T-SEM-4 gate)")
PY
pytest -x -q
```

All steps pass; changes confined to `comlab/config/proposals/`.

### Progress hook ###

`tasks/progress_notes/T-SEM-3.md` opens with `## Plan`, then `VERIFICATION GATE` + `CODE REVIEW`.
PROGRESS.md `T-SEM-3`: Status=done, Files changed=N, Verification="connected EPs registered as `proposed`
entries with consumer+citation; high-risk index recorded; no implementation, no live-KG/L3 change".
