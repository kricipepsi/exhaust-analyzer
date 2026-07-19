# T-OBDV2-9 — Per-cylinder misfire counts input (PROPOSAL, EP-OBD-IN-07)

**Status:** `pending` — **coder-runnable** · **Lab:** OBDLab (Stage 2) · **Mode:** STRICT
**Origin:** `PROPOSAL_AUDIT_v2_boost.md` promotion **EP-OBD-IN-07** · **Registry:** DEP-9 (OBDLab-owned input)
**Blocked by:** — (mirrors the manual-entry dropdown pattern already shipped in `T-OBDV2-6`/`-7`, both `done`)
**Consumer (signal/noise):** COMLab **`T-COMV2-MISFIRE-LOC-1`** (Stage 4) — a misfire **localiser** that reads
`per_cylinder_misfire_counts` to separate a single-cylinder fault from global fuel starvation and to feed the
`misfire_vs_fuelling` pre-route gate (**EP-COM-07**). Forward-register the row in COMLab's ledger; coder does
not implement COMLab here. **Field + consumer ship together — signal/noise satisfied.**

> **Reference basis (NEW wiki):** `research/chunks/fuel-trim/17_per-cylinder-misfire-counts.md` (the enhanced
> wiki — field, discriminators, catalyst boundary, RQ-D ownership) and its discriminator partner
> `research/chunks/fuel-trim/11_ignition-misfire-cases-and-trim-discriminator.md`. **Do not** cite the legacy
> `graph/v2_current/` or any pre-enhancement source. Numeric literals added to `obdlab/` carry a
> `# wiki: research/chunks/fuel-trim/17` comment per the obdlab/ numeric-literal rule.

> **Task shape — read first.** This is a **PROPOSAL** (v2 forward progress): a new OBDLab **input field**
> **plus** its named COMLab consumer ship together. Register the field in the **proposals registry**
> (`comlab/comlab/config/proposals/proposals.yaml`, id `EP-OBD-IN-07`), never silently in the live schema
> without its consumer. OBDLab **emits the counts only** — no misfire verdict (that is COMLab fusion).

## Why this exists

A misfiring cylinder pumps unburned O₂ past the upstream sensor, so the ECU reads **false-lean** and adds
fuel — a non-fuel fault masquerading as a lean fuel fault (`fuel-trim/11`). Per-cylinder misfire counts
(Mode 06, 200- and 1000-rev windows) are what let the engine tell a **localised** single-cylinder fault
(coil/plug/injector) from a **global** weak-pump starvation, and guard the trim path against a
misfire-driven false-lean mis-route. The counts must be read **alongside** trims, not after.

## Research gate — CLOSED (NEW wiki `fuel-trim/17`)

- **Field:** `per_cylinder_misfire_counts` — Mode-06 per-cylinder counts over **200** and **1000** engine
  revolutions. **Manual-entry** input (4DApp ingests user-entered scan data — no live comms; mirrors the
  `fuel_system_status` dropdown of `T-OBDV2-6`). **OBDLab-owned** per audit **RQ-D** — the discriminator must
  run even when no DTC is stored and DTCLab is not in the session, so the counts cannot be a DTCLab-only
  artefact.
- **Availability:** portable on **CAN (~2008+)**; pre-CAN MID/TID are per-OEM → the field is **optional** and
  the localiser **degrades gracefully** to the scalar misfire-vs-trim logic in `fuel-trim/11`.
- **Discriminators (consumer logic, not OBDLab's job):** single cylinder escalating + positive trim `>15 %`
  → localised; counts spread across all cylinders → global starvation; counts **clear** at stress idle →
  vacuum-leak/dirty-injector; counts **spike** at stress idle → ignition/fuel-volume.
- **Catalyst boundary:** sustained misfire **> 1 % of events** is the catalyst-meltdown escalation flag.

## Scope (PINNED — owner may ratify the field name)

OBDLab adds one optional manual-entry input field (proposal):

> **`per_cylinder_misfire_counts: dict[int, int] | None`** on the OBDLab input + `OBDLivePayload` boundary —
> per-cylinder index → count, with the rev-window (200 / 1000) carried as context. Default `None` (pre-CAN /
> not supplied). OBDLab **ferries it only** — no localisation, no misfire verdict, no catalyst-meltdown
> verdict. The `> 1 %` catalyst boundary and the `>15 %` trim cross-reference are **consumer-side** constants;
> if any literal lands in `obdlab/` it carries `# wiki: research/chunks/fuel-trim/17`.

## Success criteria

- New optional `per_cylinder_misfire_counts` field added to the OBDLab input + payload, round-trips through
  the translator, default `None` when absent (pre-CAN graceful path).
- **Registered as a proposal** in `comlab/comlab/config/proposals/proposals.yaml` (`id: EP-OBD-IN-07`,
  `consumer: T-COMV2-MISFIRE-LOC-1`, `status: proposed`, cite `research/chunks/fuel-trim/17`).
- **Emitter discipline:** OBDLab emits the counts only — grep-guard confirms no misfire/localisation verdict,
  no catalyst-meltdown verdict, no gas/`FaultFamily` reference in the OBDLab path.
- **Forward-registered** COMLab row `T-COMV2-MISFIRE-LOC-1` (Stage 4): reads the counts, localises single-cyl
  vs global, feeds the `misfire_vs_fuelling` pre-route (EP-COM-07).
- Inner loop (`ruff` → `pyright` → `pytest -x -q`) clean.

## Deliverables

1. `obdlab/obdlab/schemas/payload.py` — add `per_cylinder_misfire_counts` (optional) to `OBDLivePayload`.
2. OBDLab input model + `obdlab/obdlab/core/sensor_signal_translator.py` — accept + ferry the field; `None` fallback.
3. Tests — round-trip, `None`-default (pre-CAN), and emitter-discipline (no verdict) assertions.
4. `comlab/comlab/config/proposals/proposals.yaml` — `EP-OBD-IN-07` entry naming the consumer + NEW-wiki cite.
5. `wiki/OBDLab_KG_Wiki.md` — add the field row to the §5 `OBDLivePayload` schema table + field count (schema-doc maintenance, same as `T-OBDV2-8`).
6. **Forward-register** `T-COMV2-MISFIRE-LOC-1` in `comlab/tasks/PROGRESS.md` (Stage 4).

## Files to touch

- `obdlab/obdlab/schemas/payload.py`
- `obdlab/obdlab/schemas/` input model + `obdlab/obdlab/core/sensor_signal_translator.py`
- `obdlab/tests/unit/…` (new/updated cases)
- `comlab/comlab/config/proposals/proposals.yaml` — proposal row only
- `wiki/OBDLab_KG_Wiki.md` — schema-table row + field count only
- `comlab/tasks/PROGRESS.md` — forward-registration row only (no COMLab code this task)

## Out of scope

No misfire localisation / catalyst-meltdown verdict in OBDLab (Stage-4 COMLab). No DTCLab dependency. No
change to existing fields. Do not implement the `misfire_vs_fuelling` gate (EP-COM-07) here. Off-scope finds →
`PROGRESS.md` follow-ups.

## Verification

```bash
cd <repo>/labs/obdlab
ruff check obdlab/ tests/ && pyright obdlab/
# emitter discipline — counts only, no verdict
grep -rn "meltdown\|localis\|FaultFamily\|lambda_chem\|gas_" obdlab/obdlab/core/sensor_signal_translator.py \
  && { echo "FAIL: OBDLab asserts a misfire/localisation verdict — ferry only"; exit 1; } || echo "OK ferry-only"
# proposal registered with named consumer + NEW-wiki cite
grep -n "EP-OBD-IN-07\|per_cylinder_misfire_counts\|T-COMV2-MISFIRE-LOC-1\|fuel-trim/17" \
  ../comlab/comlab/config/proposals/proposals.yaml
pytest -x -q
```

## Anti-orphan note

`per_cylinder_misfire_counts` is **read by no live COMLab path** at Stage 2 (expected — same emit-S2/consume-S4
pattern as the inherited channels). It is **not** an orphan: `T-COMV2-MISFIRE-LOC-1` (forward-registered)
reads it at Stage 4. The grep-confirm of the live read closes at that consumer task.

## Progress hook

`tasks/progress_notes/T-OBDV2-9.md`: `## Plan` (field name/shape, optional `None` pre-CAN path, proposal id +
forward-registered consumer), then `VERIFICATION GATE` + `CODE REVIEW`. PROGRESS.md row → `done` with Files
changed + "per_cylinder_misfire_counts ferried (optional, CAN-era); emitter-only; EP-OBD-IN-07 +
T-COMV2-MISFIRE-LOC-1 forward-registered; Stage-2 green."
