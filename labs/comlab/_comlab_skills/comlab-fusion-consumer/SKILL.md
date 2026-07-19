---
name: comlab-fusion-consumer
description: >
  On-demand COMLab skill for the orphan-closer consumer tasks — the specs that
  mirror a single emitted OBD/Symptom field into COMLab's inbound schema and wire
  the named fusion consumer that reads it, closing the Stage-4 anti-orphan gate.
  Load when a task's Consumes line is a single upstream field with zero live
  COMLab reads today (per_bank_trim_delta, control_module_voltage_v, w_theo/
  sensor_error_delta, ltft_cell_vector, per_cylinder_misfire_counts, load_state,
  or any later field in the same shape). Captures the shared invariant so the six
  T-COMV2-*-{FUSE,GATE,LOC,CELL,LIN,CTXMOD} task files do not each re-derive it.
origin: "authored 2026-06-21 (architect, Cowork) — pack: COMLab orphan-closers"
updated: 2026-06-21 (initial build — gates the 6 orphan-closer consumer tasks)
---

# comlab-fusion-consumer — mirror an emitted field, wire its named reader, close the orphan

This skill is the read-only invariant shared by every **orphan-closer** task: a
task whose `Consumes` line is a single field that an emitter lab already ships but
**no live COMLab code reads yet** (grep returns 0 reader files). Each such task does
the same four moves — and the trap is doing only the first three and calling it
done. Loading this skill is named on the task's `Load skills:` line.

The single governing constraint of the lab applies here in its purest form:
**a field only ships when a named, existing consumer reads it in a live path.**
These tasks ARE that consumer. The deliverable is not "add a field"; it is
"add a field **and** the code that reads it, proven by grep."

---

## When to load

Load alongside the mandatory three (`comlab-python`, `comlab-verification-loop`,
`comlab-code-review`) when the assigned task is one of:

| Task | Field mirrored | Reader (the named consumer) |
|---|---|---|
| `T-COMV2-BANK-FUSE-1` | `per_bank_trim_delta` | `fault_atlas_router.py` |
| `T-COMV2-VPWR-GATE-1` | `control_module_voltage_v` | `perception_contradiction.py:detect` |
| `T-COMV2-MAF-LIN-1` | `w_theo` + `sensor_error_delta` | `fault_atlas_router.py` |
| `T-COMV2-LTFT-CELL-1` | `ltft_cell_vector` | `fault_atlas_router.py` |
| `T-COMV2-MISFIRE-LOC-1` | `per_cylinder_misfire_counts` | `fault_atlas_router.py` |
| `T-COMV2-CTXMOD-1` | `load_state` | `symptom_router.py` / `fault_atlas_router.py` |
| `T-COMV2-FUELSYS-GATE-1` | `fuel_system_status` (OBD-live) | `fault_atlas_router.py` |
| `T-COMV2-VE-GATE-1` | `ve_pct`/`ve_validity` + `air_metering_strategy` | `fault_atlas_router.py` |
| `T-COMV2-ECU-HW-1` | `intake_air_temp_c`/`throttle_pos_pct` | `ecu_hardware_checker.py:ECUHardwareChecker` |
| `T-COMV2-ECU-FUSE-1` | `lambda_perception_delta` + `total_trim_correction_delta_b2` | `fault_atlas_router.py` |

**Correction (2026-06-21):** an earlier note here said *not* to load the skill for
`ECU-FUSE-1`/`VE-GATE-1`/`FUELSYS-GATE-1`/`ECU-HW-1` because "those fields already
have a live reader." A code read disproved it — `ecu_hardware_checker.py` is an empty
stub, and `fuel_system_status` (OBD-live), `total_trim_correction_delta_b2`, and the
`ecu_fault` verdict have **no live COMLab reader**. The "reader" meant was OBD-**internal**,
not a COMLab one. So these four ARE orphan-closers of this exact shape — **load the skill.**
The one nuance: `ECU-FUSE-1` first **verifies** the already-live perception-axis read
(`perception_contradiction.detect`) before adding the `ecu_fault` discrimination on top — its
divergence input exists; the verdict and the `_b2` twin-trim mirror do not.

---

## Single-lab isolation (the framing constraint)

A diagnosis may run on **one lab's payload alone**. If no DTC is present, DTCLab is never
invoked; a legacy/no-OBD session carries no `obd_live_data`; a session with no symptom intake
carries an empty `symptom_dna`. Two consequences bind every consumer here:

1. **Absent payload/field is inert, never an error.** Default-`None` mirror, three falsy
   short-circuits, byte-identical when the field is missing. A consumer must degrade to "no
   verdict," not crash or fabricate, when its upstream lab did not run.
2. **Thresholds are COMLab-local.** A consumer reads its interpretation bands from the COMLab
   wiki (`§2a {#CONCEPT_OBD_CONSUMER_BANDS}` for OBD analytic fields), **never** from another
   lab's research tree at diagnostic time. A literal whose only home is `obdlab/research/...`
   is a latent cross-lab dependency — mirror it into the COMLab wiki first (architect patch),
   then cite the COMLab anchor.

## The four moves (do all four — the fourth is the real done)

### 1. Mirror the field — from the EMITTER, at the emitter's exact type

The source of record for the field's name, type, default, and bounds is the
**emitter's output schema**, never the COMLab wiki prose:

- OBD fields → `labs/obdlab/obdlab/schemas/payload.py` (the OBD output payload).
- Symptom fields → `labs/symptomlab/symptomlab/models.py`.

Add the mirror to the **existing** inbound sub-model — do not invent a new one:

- OBD fields → `comlab/schemas/ingestion.py::OBDLiveDataPayload`.
- Symptom fields → carried on `OrchestratorInboundRequest.symptom_dna` (dict);
  read the nested key (`environmental_conditions.load_state`), do not add a typed
  field unless the task says so.

**Type fidelity is load-bearing.** Mirror the emitter's exact annotation. The OBD
emitter emits `per_cylinder_misfire_counts: dict[int, int] | None` and
`ltft_cell_vector: dict[int, float] | None` — mirror them as `dict`, even though
wiki/02's type column abbreviates them as `list[...]`. The wiki column is
descriptive shorthand; the emitter schema is the contract. If you spot a genuine
contract drift, **flag it to the architect** (PROGRESS.md note) — do not "fix" the
emitter contract or silently change a type from a coding task.

The mirrored field is **default-`None`** (or the emitter's default) and additive:
an inbound request that omits it must validate byte-identically to today.

### 2. Cite every literal to the wiki

Every threshold, band edge, enum value, and confidence cap carries a
`# wiki: §…` provenance comment. The canonical bands live in:

- `wiki/02_lab_input_contract.md §2` — trim authority bands
  (±0–5 % within authority · ±5–15 % compensating · ±15–25 % rule threshold ·
  >±25 % saturated `ERR-EF-001` · `< −23 %` unmetered-fuel `ERR-RM-005`).
- `wiki/05_fault_taxonomy.md` — fault rows / `ERR-*` ids.
- `wiki/02_lab_input_contract.md §2a {#CONCEPT_OBD_CONSUMER_BANDS}` — the **COMLab-local**
  consumer bands for the OBD analytic fields (MAF ladder, VPWR rail, LTFT distribution,
  misfire localisation). **Cite this, not an `obdlab/research/chunk`.** The chunk is recorded
  there as provenance only; a consumer must not reach into another lab's tree (see "Single-lab
  isolation" below).

A literal with no wiki cite fails the verification gate's Phase 5. A literal cited to another
lab's research path (not the COMLab wiki) fails the code-review cross-lab check.

### 3. Ship behind a default-off flag; keep single-point byte-identical

New fusion capability is inert by default. Mirror the established pattern
(`enable_delta` / `use_v2_registry`): an `enable_<x>: bool = False` constructor
flag on the reader, optionally resolved from an env var. With the flag off — or
the mirrored field absent — the existing path must be **byte-identical**. The
regression test that proves this is mandatory; live activation is always a
separate follow-up, never folded into the orphan-closer.

Emit your finding **as evidence into the existing fusion path** (a `scored_rules`
re-rank term, or a qualifier on the perception result), never as a forced
override. Per `wiki/08 §graph-relations`, these consumers are
`CONCEPT_EVIDENCE_INPUTS` to conflict-aware fusion, not additive score bumps and
not overrides.

### 4. Prove the read with two greps (the anti-orphan gate)

Green pytest is **not** done. The task closes only when the mirrored field is
`grep`-confirmed read in a **live, reachable** path. Run two greps and paste both
into the `VERIFICATION GATE` block:

```bash
grep -nI "<field_name>" comlab/core/<reader>.py    # the read site
grep -nI "<flag_or_branch>" comlab/core/<reader>.py # the branch that reaches it
```

The second grep matters: a read inside a branch nothing reaches is still an
orphan. If you cannot show both, the task is not done — fix the wiring, do not
flip the ledger.

**Two reader shapes — know which one you have, or the field ends up dead:**

- **Router reader** (`fault_atlas_router.execute_triage_loop` / `route`): the field flows in
  via the **request object** (mirrored onto `OBDLiveDataPayload` or read off `request.symptom_dna`),
  and the flag is a **router constructor arg** (`enable_<x>: bool = False`, mirroring `enable_delta`).
  Self-contained: the read site is already a live method, and a test that constructs
  `FaultAtlasRouter(enable_<x>=True)` satisfies the gate. No aggregator change. (Pattern: BANK-FUSE.)
- **Free-function reader** (`perception_contradiction.detect`, `symptom_router.route_symptom`): the
  function takes **explicit scalar args**, so its **production caller — `lab_pipeline_aggregator.py` —
  is in scope.** You must add the field + flag to the aggregator (`__init__` flag mirroring
  `enable_delta`; pass the value at the call site) or the new param is dead and anti-orphan fails.
  (Lesson: VPWR-GATE — `detect()`'s only caller is `lab_pipeline_aggregator.py:317`.)

When a field could be wired either way (e.g. a symptom-prior modifier), **prefer the router reader** —
it is self-contained and avoids the free-function caller trap. The aggregator passing the flag to flip
the default on is always the separate live-activation follow-up, never part of the orphan-closer.

---

## Done checklist (in addition to the two mandatory gate blocks)

- [ ] Field mirrored at the **emitter's exact type**, default-absent, into the
      existing inbound sub-model. No new schema class. No cross-lab import.
- [ ] Every literal carries a `# wiki: §…` cite.
- [ ] Default-off flag added; single-point regression test proves byte-identity
      with the flag off / field absent.
- [ ] Finding enters fusion as evidence, not an override.
- [ ] Two greps prove the field is read in a reachable path; both pasted in the
      `VERIFICATION GATE`.
- [ ] DEP row Status updated in `CROSS_LAB_DEPENDENCIES.md` if wording needs it;
      PROGRESS.md row flipped to `done` only after both gate blocks are clean.

---

## Anti-patterns this skill exists to prevent

- **The field-only "done".** Mirroring the field and stopping — no reader, or a
  reader behind a branch nothing reaches. The orphan is still open; the grep gate
  catches it.
- **The wiki-type mirror.** Typing the mirror from wiki/02's `list[...]` shorthand
  instead of the emitter's `dict[...]`. Breaks the JSON contract silently.
- **The eager activation.** Flipping the default on, or surfacing the new signal
  into live output, inside the orphan-closer. That is the separate follow-up.
- **The override.** Emitting the finding as a forced verdict or a flat additive
  bump instead of conflict-aware evidence.
- **The new sub-model.** Inventing a fresh inbound class for one field instead of
  extending `OBDLiveDataPayload` / reading `symptom_dna`.
