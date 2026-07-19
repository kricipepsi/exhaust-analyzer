# T-OBDV2-10 — MAF linearity / theoretical-airflow cross-check (PROPOSAL, EP-OBD-11)

**Status:** `pending` — **coder-runnable** · **Lab:** OBDLab (Stage 2) · **Mode:** STRICT
**Origin:** `PROPOSAL_AUDIT_v2_boost.md` promotion **EP-OBD-11** · **Registry:** DEP-9
**Blocked by:** — (inputs already exist: `intake_air_temp_c` from `T-OBDV2-7` **done**; `manifold_vacuum_kpa`,
`mass_airflow_gps` present in `payload.py`)
**Consumer (signal/noise):** COMLab **`T-COMV2-MAF-LIN-1`** (Stage 4) — a MAF-contamination discriminator
that reads `w_theo` + `sensor_error_delta` to flag a **dirty/drifted MAF that is DTC-silent**, sharpening the
existing **`ERR-LC-002 maf_sensor_contaminated`** node (and separating it from an open-circuit MAF, which sets
P0102). Forward-register the row in COMLab's ledger; coder does not implement COMLab here. **Fields + consumer
ship together — signal/noise satisfied.**

> **Reference basis (NEW wiki):** `research/chunks/pids-protocol/05_maf-linearity-theoretical-airflow.md` (the
> enhanced wiki — `W_theo` form, two-point Δ, threshold ladder) and the profile it measures,
> `research/chunks/delta-relations/04_profile-maf-underreport.md`. **Do not** cite legacy
> `graph/v2_current/` or pre-enhancement sources. Every numeric literal added to `obdlab/`
> (the 3–4 % / 5–12 % / 12–15 % ladder, the `120`/`R` constants) carries a
> `# wiki: research/chunks/pids-protocol/05` comment per the obdlab/ numeric-literal rule.

> **Task shape — read first.** PROPOSAL (v2 forward progress): OBDLab **computes and emits** two new channels
> **plus** their named COMLab consumer, shipped together. Register in the proposals registry
> (`comlab/comlab/config/proposals/proposals.yaml`, id `EP-OBD-11`). OBDLab emits the **scalars only** — no
> MAF-fault verdict (that is the Stage-4 discriminator).

## Why this exists

A contaminated hot-wire MAF reads plausibly at idle but **under-reports as airflow rises** — an insulating
layer blocks the high-velocity cooling the sensor relies on. A single snapshot misses it and it sets **no
open-circuit DTC**. A **two-point** comparison of the measured MAF against speed-density **theoretical**
airflow exposes the non-linearity, giving the existing MAF-contamination node (`ERR-LC-002`) a DTC-silent
detector and separating it from an open-circuit MAF (`P0102`).

## Research gate — CLOSED (NEW wiki `pids-protocol/05`)

- **Theoretical airflow (speed-density):**
  `W_theo = (η_V · V_disp · P_manifold · RPM) / (120 · R · T_intake)` — uses `manifold_vacuum_kpa` (MAP) and
  `intake_air_temp_c` (IAT, K), already on the payload.
- **Non-linearity delta:**
  `ΔSensor_error = |Sensor_Stress − W_theo_Stress| − |Sensor_Idle − W_theo_Idle|` (two points: stabilised idle
  vs stress idle).
- **Threshold ladder (% deviation):** `< 3–4 %` healthy (LTFT absorbs uniform offset); `5–12 %`
  calibration-drift / dirty; `> 12–15 %` component fault (typically sets **P0101**).
- **Discriminator value:** separates a calibration-drifted (dirty, DTC-silent) MAF from an open-circuit MAF
  (`P0102`). It is the quantified detector behind the under-report ΔTrim profile in `delta-relations/04`.

## Scope (PINNED — owner may ratify field names / η_V source)

OBDLab computes and emits two scalars (proposal):

> **`w_theo: float | None`** (speed-density theoretical airflow, g/s) and
> **`sensor_error_delta: float | None`** (two-point non-linearity, %) on the `OBDLivePayload` boundary —
> computed in a new `obdlab/obdlab/core/` helper from MAF + MAP + IAT + RPM at the two idle bands. Emitted only
> when both bands are captured and the sensor type permits; `None` otherwise. `η_V` / `V_disp` come from
> DNALab topology (no OBDLab-invented constant). OBDLab **does not** assert a MAF-contamination verdict and
> **does not** read gas — that is the Stage-4 discriminator. Numeric literals carry the NEW-wiki cite.

## Success criteria

- New `w_theo` + `sensor_error_delta` computed and emitted under the two-point guard; `None` when a band is
  missing; round-trips through the payload.
- **Computability verified:** `ΔSensor_error ≈ 0` on a clean-MAF fixture (parallel error curve); elevated
  `ΔSensor_error` on a dirty-MAF fixture (stress error dwarfs idle error).
- **Registered as a proposal** in `comlab/comlab/config/proposals/proposals.yaml` (`id: EP-OBD-11`,
  `consumer: T-COMV2-MAF-LIN-1`, `status: proposed`, cite `research/chunks/pids-protocol/05`).
- **Emitter discipline:** OBDLab emits scalars only — grep-guard confirms no MAF-fault / `ERR-LC-002` verdict,
  no gas reference in the OBDLab path.
- **Forward-registered** COMLab row `T-COMV2-MAF-LIN-1` (Stage 4): reads the scalars, applies the 5–12 / >12 %
  ladder, routes to / sharpens `ERR-LC-002` vs open-circuit `P0102`.
- Inner loop (`ruff` → `pyright` → `pytest -x -q`) clean.

## Deliverables

1. `obdlab/obdlab/schemas/payload.py` — add `w_theo`, `sensor_error_delta` (optional).
2. `obdlab/obdlab/core/` — new helper computing `W_theo` + `ΔSensor_error` (literals carry NEW-wiki cites).
3. Tests — clean-MAF (`Δ≈0`) and dirty-MAF (elevated Δ) fixtures + `None`-when-band-missing + emitter discipline.
4. `comlab/comlab/config/proposals/proposals.yaml` — `EP-OBD-11` entry naming the consumer + NEW-wiki cite.
5. `wiki/OBDLab_KG_Wiki.md` — add the two fields to the §5 schema table + field count (schema-doc maintenance).
6. **Forward-register** `T-COMV2-MAF-LIN-1` in `comlab/tasks/PROGRESS.md` (Stage 4) — reads the scalars, sharpens `ERR-LC-002`.

## Files to touch

- `obdlab/obdlab/schemas/payload.py`
- `obdlab/obdlab/core/` (new MAF-linearity helper) + translator wiring
- `obdlab/tests/unit/…` (new test module)
- `comlab/comlab/config/proposals/proposals.yaml` — proposal row only
- `wiki/OBDLab_KG_Wiki.md` — schema-table rows + field count only
- `comlab/tasks/PROGRESS.md` — forward-registration row only (no COMLab code this task)

## Out of scope

No MAF-contamination verdict / `ERR-LC-002` routing in OBDLab (Stage-4 COMLab). No gas comparison. No new
input PID beyond the existing MAF/MAP/IAT/RPM. Do not reconcile the idle-band naming (SI/StI) — use the
existing `RpmStateBucket` bands. Off-scope finds → `PROGRESS.md` follow-ups.

## Verification

```bash
cd <repo>/labs/obdlab
ruff check obdlab/ tests/ && pyright obdlab/
# emitter discipline — scalars only, no verdict, no gas
grep -rn "ERR-LC-002\|maf_sensor_contaminated\|lambda_chem\|gas_\|FaultFamily" obdlab/obdlab/core/*maf*linearity* \
  && { echo "FAIL: OBDLab asserts a MAF verdict — emit scalars only"; exit 1; } || echo "OK scalar-only"
# numeric literals carry the NEW-wiki citation
grep -rn "wiki: research/chunks/pids-protocol/05" obdlab/obdlab/core/ || { echo "FAIL: missing wiki cite on literals"; exit 1; }
# proposal registered with named consumer
grep -n "EP-OBD-11\|w_theo\|sensor_error_delta\|T-COMV2-MAF-LIN-1\|pids-protocol/05" \
  ../comlab/comlab/config/proposals/proposals.yaml
pytest -x -q
```

## Anti-orphan note

`w_theo` / `sensor_error_delta` are **read by no live COMLab path** at Stage 2 (expected emit-S2/consume-S4).
Not orphans: `T-COMV2-MAF-LIN-1` (forward-registered) reads them at Stage 4 and sharpens the existing
`ERR-LC-002` node. The grep-confirm of the live read closes at that consumer task.

## Progress hook

`tasks/progress_notes/T-OBDV2-10.md`: `## Plan` (field names, `W_theo`/Δ form + the band guard, proposal id +
forward-registered consumer), then `VERIFICATION GATE` + `CODE REVIEW`. PROGRESS.md row → `done` with Files
changed + "w_theo + sensor_error_delta emitted under two-point guard; emitter-only; EP-OBD-11 +
T-COMV2-MAF-LIN-1 forward-registered; Stage-2 green."
