# T-OBDV2-11 — LTFT load-cell vector input (PROPOSAL, EP-OBD-12)

**Status:** `pending` — **coder-runnable** · **Lab:** OBDLab (Stage 2) · **Mode:** STRICT
**Origin:** `PROPOSAL_AUDIT_v2_boost.md` promotion **EP-OBD-12** (held out of the 9/10 batch — bigger shape) · **Registry:** DEP-9
**Blocked by:** — (scalar `shrtft1/longft1` (+b2), `calculated_engine_load_pct`, `rpm_state_bucket` already on the payload; this adds the *cross-cell* vector)
**Consumer (signal/noise):** COMLab **`T-COMV2-LTFT-CELL-1`** (Stage 4) — a **load-cell trim analyzer** that
reads `ltft_cell_vector` and flags **which operating region deviates** (idle-only / part-throttle-only /
global), feeding `fault_atlas_router` family selection. Forward-register the row in COMLab's ledger; coder
does not implement COMLab here. **Field + consumer ship together — signal/noise satisfied.**

> **Reference basis (NEW wiki):** `research/chunks/fuel-trim/13_ltft-load-cell-matrix.md` (the enhanced wiki —
> per-cell LTFT, the idle-only/part-throttle-only/global localisation rule, GMH VT V8 cell examples). The
> scalar idle-vs-RPM approximation it supersedes lives in `research/chunks/fuel-trim/04`. **Do not** cite
> legacy `graph/v2_current/` or pre-enhancement sources. Any numeric literal added to `obdlab/` carries a
> `# wiki: research/chunks/fuel-trim/13` comment per the obdlab/ numeric-literal rule.

> **Task shape — read first.** PROPOSAL (v2 forward progress): a new OBDLab **input field** **plus** its named
> COMLab consumer ship together. Register the field in the proposals registry
> (`comlab/comlab/config/proposals/proposals.yaml`, id `EP-OBD-12`), never silently in the live schema. OBDLab
> **ferries the cell vector only** — no region-localisation verdict (that is the Stage-4 analyzer). This is
> the larger of the three audit promotions: the OBDLab side is one optional field, but it unlocks a **new
> COMLab analyzer** (forward-registered here, built at Stage 4).

## Why this exists

The PCM does not learn one LTFT — it learns a **matrix of LTFT cells indexed by MAF (load) × RPM**. *Which*
cells deviate localises the fault: idle/low-load cells only → idle-specific (vacuum leak, IAC, PCV);
part-throttle cells only → mid-range (fuel delivery, EGR); **all** cells → global (MAF, fuel pressure, O₂
bias). v2 today carries only **scalar** trims + the *current* load bucket — enough to know where the engine
is, but **not** to compare LTFT *across* cells. The cross-cell view is a forward-progress diagnostic
dimension that localises a fault to the operating region where trim deviates.

## Research gate — CLOSED (NEW wiki `fuel-trim/13`)

- **Field:** `ltft_cell_vector` — per-cell LTFT (%), indexed by load × RPM cell. **Optional, platform-gated**:
  emitted only on platforms that expose the cell PIDs (e.g. GMH VT V8 idle cells 0/17 auto, 16/33 manual);
  the cell index itself encodes operating context (e.g. whether canister purge is flowing). **Manual-entry**
  input (4DApp ingests user-entered scan data — no live comms; mirrors the `fuel_system_status` dropdown
  pattern of `T-OBDV2-6`).
- **Localisation rule (consumer logic, not OBDLab's job):** idle/low-load cells only → idle-specific cause;
  part-throttle cells only → mid-range cause; all cells → global cause.
- **Today's gap:** scalar `shrtft1/longft1` (+b2) + `calculated_engine_load_pct` + `rpm_state_bucket` give the
  current bucket but no cross-cell comparison; no live code reads a per-cell LTFT vector. Until this lands,
  scalar idle-vs-RPM (`fuel-trim/04`) is the **active approximation**.

## Scope (PINNED — owner may ratify field name / cell-index encoding)

OBDLab adds one optional manual-entry input field (proposal):

> **`ltft_cell_vector: dict[int, float] | None`** on the OBDLab input + `OBDLivePayload` boundary —
> cell-index → LTFT % for the cells the platform exposes. Default `None` (cell PIDs unavailable / not
> supplied). OBDLab **ferries it only** — no region classification, no fault-family verdict. The
> cell-indexing convention is supplied per-platform (DNALab topology), not invented by OBDLab.

## Success criteria

- New optional `ltft_cell_vector` field added to the OBDLab input + payload; round-trips; default `None` when
  cell PIDs are absent (graceful degradation to the scalar `fuel-trim/04` path).
- **Registered as a proposal** in `comlab/comlab/config/proposals/proposals.yaml` (`id: EP-OBD-12`,
  `consumer: T-COMV2-LTFT-CELL-1`, `status: proposed`, cite `research/chunks/fuel-trim/13`).
- **Emitter discipline:** OBDLab ferries the vector only — grep-guard confirms no region-localisation /
  fault-family verdict, no gas reference in the OBDLab path.
- **Forward-registered** COMLab row `T-COMV2-LTFT-CELL-1` (Stage 4): reads the vector, classifies
  idle-only / part-throttle-only / global, feeds `fault_atlas_router` family selection.
- Inner loop (`ruff` → `pyright` → `pytest -x -q`) clean.

## Deliverables

1. `obdlab/obdlab/schemas/payload.py` — add `ltft_cell_vector` (optional) to `OBDLivePayload`.
2. OBDLab input model + `obdlab/obdlab/core/sensor_signal_translator.py` — accept + ferry the field; `None` fallback.
3. Tests — round-trip, `None`-default (no cell PIDs), and emitter-discipline (no verdict) assertions.
4. `comlab/comlab/config/proposals/proposals.yaml` — `EP-OBD-12` entry naming the consumer + NEW-wiki cite.
5. `wiki/OBDLab_KG_Wiki.md` — add the field row to the §5 `OBDLivePayload` schema table + field count (schema-doc maintenance, same as `T-OBDV2-8`).
6. **Forward-register** `T-COMV2-LTFT-CELL-1` in `comlab/tasks/PROGRESS.md` (Stage 4) — the new load-cell trim analyzer.

## Files to touch

- `obdlab/obdlab/schemas/payload.py`
- `obdlab/obdlab/schemas/` input model + `obdlab/obdlab/core/sensor_signal_translator.py`
- `obdlab/tests/unit/…` (new/updated cases)
- `comlab/comlab/config/proposals/proposals.yaml` — proposal row only
- `wiki/OBDLab_KG_Wiki.md` — schema-table row + field count only
- `comlab/tasks/PROGRESS.md` — forward-registration row only (no COMLab code this task)

## Out of scope

No region localisation / fault-family verdict in OBDLab (Stage-4 COMLab analyzer). No DNALab/cell-index
authoring (topology supplies it). No change to the scalar trim fields or the `fuel-trim/04` active path. Do
**not** build the COMLab load-cell analyzer here — only forward-register it. Off-scope finds →
`PROGRESS.md` follow-ups.

## Verification

```bash
cd <repo>/labs/obdlab
ruff check obdlab/ tests/ && pyright obdlab/
# emitter discipline — vector ferried only, no verdict
grep -rn "idle_only\|part_throttle\|FaultFamily\|lambda_chem\|gas_\|localis" obdlab/obdlab/core/sensor_signal_translator.py \
  && { echo "FAIL: OBDLab asserts a region/localisation verdict — ferry only"; exit 1; } || echo "OK ferry-only"
# proposal registered with named consumer + NEW-wiki cite
grep -n "EP-OBD-12\|ltft_cell_vector\|T-COMV2-LTFT-CELL-1\|fuel-trim/13" \
  ../comlab/comlab/config/proposals/proposals.yaml
pytest -x -q
```

## Anti-orphan note

`ltft_cell_vector` is **read by no live COMLab path** at Stage 2 (expected emit-S2/consume-S4). Not an orphan:
`T-COMV2-LTFT-CELL-1` (forward-registered) reads it at Stage 4. The grep-confirm of the live read closes at
that consumer task.

## Progress hook

`tasks/progress_notes/T-OBDV2-11.md`: `## Plan` (field name/shape, optional `None` no-cell-PID path, proposal
id + forward-registered consumer), then `VERIFICATION GATE` + `CODE REVIEW`. PROGRESS.md row → `done` with
Files changed + "ltft_cell_vector ferried (optional, platform-gated); emitter-only; EP-OBD-12 +
T-COMV2-LTFT-CELL-1 forward-registered; Stage-2 green."
