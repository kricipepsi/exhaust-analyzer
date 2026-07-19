# Architecture Decision Records — OBDLab (v2)

**Scope:** OBDLab (Stage 2, electronic-perception channel).
**Format:** Nygard template (one decision per record, immutable once Accepted).
**Date compiled:** 2026-06-10 — back-filled from the shipped revive-as-emitter
rework (T-OBDV2-0 … T-OBDV2-11, FIX-1…7, ARCH-1/2, PURGE-1…3).

> These ADRs record decisions already implemented in `obdlab/`. They are written
> as historical records: each captures *why* a choice was made, with the task ID
> that carried it. Future changes supersede an ADR with a new one rather than
> editing it in place.

| ADR | Title | Status |
|-----|-------|--------|
| ADR-0001 | Revive OBDLab as a perception-channel emitter, not a fault classifier | Accepted |
| ADR-0002 | Emit at Stage 2, consume at Stage 4 — forward-registered consumers & proposals | Accepted |
| ADR-0003 | No cross-lab Python imports — OBDLab mirrors the types it needs | Accepted |
| ADR-0004 | Remove Physics Gate 3; fold its intent into `FAULT_VE_SENSOR_SKEW` | Accepted |
| ADR-0005 | Unify the exception hierarchy under `ObdLabError` | Accepted |
| ADR-0006 | Widen fuel-trim bounds to the OBD rail `±127` and treat rails as signal | Accepted |
| ADR-0007 | Prune the dead standalone classifier and orphan enums/fields | Accepted |
| ADR-0008 | VE is evidence only under the dual-sensor gate; single-sensor → `UNKNOWN` | Accepted |
| ADR-0009 | Bank-2 trims are `null`, never `0.0`, on single-bank engines | Accepted |

---

## ADR-0001: Revive OBDLab as a perception-channel emitter, not a fault classifier

**Status:** Accepted (2026-06-08, owner-ratified — T-OBDV2-0)

### Context

On the available corpus, standalone OBDLab returned `NO_FAULT` for >95% of
cases, which triggered a revive-vs-quarantine review. Investigation showed the
result was a **PID-less-corpus artefact** (the corpus lacked live PID rows), not
a defect in the translation logic. Separately, the 4D architecture assigns
root-cause verdicts to COMLab's system-level causality graph; the parsing labs
(GAS/OBD/DTC) are meant to translate raw metrics into typed perceptions, not to
judge faults (`KGtopic.md`).

### Decision

OBDLab is revived as a **typed perception-channel emitter** feeding COMLab
fusion. It emits its own channels — trims, normalized lambda, VE, sensor
provenance, perception-deltas — and **does not emit fault-family verdicts**.
Standalone OBD fault classification is conceded.

### Consequences

- **Positive:** clear separation of concerns; OBDLab is testable as a pure
  transform; the NO_FAULT non-issue is closed; COMLab owns one verdict surface.
- **Positive:** validates the dead-classifier purge (see ADR-0007).
- **Negative:** OBDLab alone produces no human-facing diagnosis; usefulness
  depends on COMLab consuming its channels (much of which lands at Stage 4).
- **Neutral:** the payload becomes wider (more emitted channels) rather than
  narrower.

### Alternatives Considered

1. **Quarantine OBDLab** — shelve the lab until a PID-rich corpus exists.
   Rejected: the >95% NO_FAULT was a corpus artefact, so quarantine would shelve
   working code for a non-defect.
2. **Keep OBDLab as a standalone classifier** — let it emit fault verdicts.
   Rejected: duplicates COMLab's job, splits the verdict surface across labs, and
   couples OBDLab to cross-lab fault taxonomy.

---

## ADR-0002: Emit at Stage 2, consume at Stage 4 — forward-registered consumers & proposals

**Status:** Accepted (2026-06-08 — T-OBDV2-ECU-PERCEPT-1 and the T-OBDV2-2…11 pack)

### Context

The signal/noise rule is non-negotiable: every schema field must have a named,
existing consumer in COMLab analytics or fault-atlas routing — "future use" is
not a consumer. But OBDLab (Stage 2) is built **before** the COMLab fusion tasks
(Stage 4) that will read several of its channels. A strict reading would block
useful channels until COMLab is rebuilt.

### Decision

Allow a field to ship at Stage 2 when its consumer is **named and specced as a
forward-registered COMLab task** (e.g. `T-COMV2-VE-GATE-1`,
`T-COMV2-ECU-FUSE-1`), recorded in the proposals registry with the consumer and
code path. New diagnostic content defaults to a **proposal** (e.g. `EP-OBD-11`,
`EP-OBD-12`, `EP-OBD-17`) rather than to "defer/PENDING". The proposal and its
consumer are tracked together; the Stage-4 anti-orphan grep closes the loop when
the COMLab reader lands.

### Consequences

- **Positive:** OBDLab makes forward progress without waiting on COMLab; the
  signal/noise discipline is preserved (every field has a *named* consumer).
- **Positive:** the emit-S2/consume-S4 fields are an explicit frozen contract,
  so COMLab reconciles **up to** OBDLab, not the reverse.
- **Negative:** between Stage 2 and Stage 4 these fields are read by no *live*
  COMLab path — an accepted, tracked divergence (HLD §9), not an orphan.
- **Negative:** requires discipline — a forward-registered task that never lands
  would turn its field into a real orphan.

### Alternatives Considered

1. **Defer every cross-stage field to PENDING** until COMLab exists. Rejected:
   this is the "v1-stuck" failure mode; it defers nameable consumers.
2. **Ship fields with no consumer ("future use")** and wire them later.
   Rejected: a direct signal/noise breach.

---

## ADR-0003: No cross-lab Python imports — OBDLab mirrors the types it needs

**Status:** Accepted (architecture constraint; exercised by T-OBDV2-6)

### Context

The 4D architecture keeps each lab a fully isolated codebase connected only
through typed JSON boundaries. OBDLab nonetheless needs types that originate
elsewhere — e.g. fuel-system loop status, which DTCLab defines
(`DTC_VOCABULARY §8`).

### Decision

OBDLab **never imports** from `gaslab`, `dtclab`, `comlab`, `dnalab`, or
`vinlab`. When it needs a cross-lab type it **mirrors a local copy** — e.g.
`FuelSystemStatus` in `schemas/vocabulary.py`, sourced verbatim from
`DTC_VOCABULARY §8`, with a `from_wire()` coercion for legacy strings. The DNA
view is likewise an OBDLab-owned mirror (`ObdLabDnaView`) of the COMLab DNA
projection. An import-isolation audit in the test suite enforces this.

### Consequences

- **Positive:** labs build, test, and version independently; no import cycles.
- **Positive:** the wire contract is explicit and drift-guarded by tests.
- **Negative:** mirrored types can drift from their source of truth; sync is a
  manual, documented responsibility (e.g. COMLab keeps the DTC frozensets in
  sync).

### Alternatives Considered

1. **Shared `common` package** of cross-lab enums. Rejected: reintroduces the
   coupling the isolation rule exists to remove.
2. **Direct import from DTCLab** for `FuelSystemStatus`. Rejected: violates the
   no-cross-lab-import constraint.

---

## ADR-0004: Remove Physics Gate 3; fold its intent into `FAULT_VE_SENSOR_SKEW`

**Status:** Accepted (2026-06-08 — T-OBDV2-FIX-1, Option B)

### Context

Physics Gate 3 raised on "VE > 90% on a naturally-aspirated engine at stabilized
idle". The same physical condition is also expressible as a VE-validity
classification, creating two code paths for one fact — and the gate raised
(hard-stopping the pipeline) for what is really an evidence signal.

### Decision

Remove Physics Gate 3 from `SemanticConsistencyChecker`. Carry its intent as
`VEValidity.FAULT_VE_SENSOR_SKEW` in the VE engine (VE > 90 AND
`STABILIZED_IDLE` AND `NATURALLY_ASPIRATED`). The semantic checker now runs gates
**1, 2, 4** only; `gates_passed` collects three.

### Consequences

- **Positive:** one code path for the NA-VE-ceiling condition; it becomes
  emitted evidence (`ve_validity`) rather than a pipeline-aborting raise.
- **Positive:** removes a `dead_read` of `calculated_ve` flagged in the audit.
- **Negative:** downstream readers must treat `FAULT_VE_SENSOR_SKEW` as a
  validity value, not an exception — a contract change COMLab must honour.
- **Neutral:** `semantic_gates_passed` is now `len(gates_passed) == 3`.

### Alternatives Considered

1. **Keep Gate 3 as a raise** (Option A). Rejected: hard-stops on an evidence
   signal and duplicates the VE classifier.
2. **Keep both** the gate and the validity value. Rejected: two sources of truth
   for one condition.

---

## ADR-0005: Unify the exception hierarchy under `ObdLabError`

**Status:** Accepted (2026-06-08 — T-OBDV2-FIX-5)

### Context

OBDLab exceptions inherited from stdlib bases: `PIDValidationError(ValueError)`
and `SemanticConsistencyError(AssertionError)`. COMLab's fusion error-handling
path could not catch "any OBDLab error" without catching unrelated `ValueError`s,
and `AssertionError` is semantically wrong for a validation failure.

### Decision

Introduce a single root `ObdLabError(Exception)` and reparent both subclasses
under it. Physics Gate 4 now raises `SemanticConsistencyError` (consistent with
the other gates) rather than a bare `ValueError`.

### Consequences

- **Positive:** COMLab catches the whole family with one `except ObdLabError`.
- **Positive:** exception semantics match intent (no `AssertionError` for
  validation).
- **Negative:** any caller that previously caught `ValueError`/`AssertionError`
  from OBDLab must update to `ObdLabError` — a breaking change for downstream
  error handling (in-repo callers updated in the same task).

### Alternatives Considered

1. **Leave stdlib bases in place.** Rejected: forces broad, imprecise `except`
   clauses in COMLab.
2. **Multiple unrelated roots** (one per module). Rejected: defeats the
   single-`except` goal.

---

## ADR-0006: Widen fuel-trim bounds to the OBD rail `±127` and treat rails as signal

**Status:** Accepted (T-W-6)

### Context

The OBD-nominal trim range is roughly `[-100, 99.22]%`. Real ECUs report
**railed** values (`±127`) when a trim saturates — and a railed trim is itself a
diagnostic signal (the fuel system has run out of correction authority).
Rejecting `±127` as out-of-bounds would discard that signal.

### Decision

Widen the `shrtft*`/`longft*` bounds (in `physical_sensor_bounds.json` and the
Physics Gate 4 rails) to `[-127, 127]`. Document the rail value as a
sensor-fault signal consumed by COMLab trim-evidence scoring.

### Consequences

- **Positive:** railed trims survive validation and reach COMLab as evidence.
- **Negative:** the validator no longer rejects physically implausible mid-range
  values that happen to fall inside `±127`; semantic plausibility moves
  downstream.
- **Neutral:** bounds, Physics Gate 4 rails, and the JSON note are kept in sync.

### Alternatives Considered

1. **Keep nominal bounds and reject `±127`.** Rejected: loses the saturation
   signal.
2. **Clamp `±127` to nominal.** Rejected: fabricates a value and still loses the
   "railed" fact.

---

## ADR-0007: Prune the dead standalone classifier and orphan enums/fields

**Status:** Accepted (2026-06-08 — T-OBDV2-PURGE-1/2/3, ARCH-1/2)

### Context

Post-revive (ADR-0001), several constructs had no consumer: the standalone
ranking/classification path (`ranking.py`, `family_map.py`), the
`VERoutingMode` enum (a duplicate of `AirMeteringStrategy`), several
`O2FailureMode` members (`SLUGGISH`, `DEAD`, `WRONG_CENTERLINE`, `HEATER_FAULT`),
the `ObdLabDnaView` fields `cylinder_count`/`emissions`/`resolved_horizon`, and
the `EuroEmissionCategory`/`ResolvedHorizon` enums. The signal/noise rule says a
field read nowhere is an orphan.

### Decision

Excise all of the above. Keep `O2FailureMode` at four members
(`NO_FAULT`, `STUCK_LEAN`, `STUCK_RICH`, `WIDEBAND_OFFSET_CANDIDATE`) and
`ObdLabDnaView` at seven fields. COMLab fusion consumes the full payload, not a
top-3 ranking, so the classifier is genuinely dead.

### Consequences

- **Positive:** the surface matches what is actually consumed; no orphan fields;
  smaller, clearer schemas.
- **Negative:** removing required DNA fields forced edits across the tests that
  build `ObdLabDnaView` (8 files in PURGE-2) — a one-time cost.
- **Neutral:** any future need for a pruned member returns via the proposal path
  (ADR-0002), not by un-deleting.

### Alternatives Considered

1. **Keep orphans "for future use".** Rejected: direct signal/noise breach.
2. **Mark them deprecated but retained.** Rejected: dead surface still has to be
   maintained and drift-guarded.

---

## ADR-0008: VE is evidence only under the dual-sensor gate; single-sensor → `UNKNOWN`

**Status:** Accepted (2026-06-08 — T-OBDV2-2, Q5)

### Context

VE can be computed three ways depending on the air-metering hardware. But in the
`MAP_ONLY` and `MAF_ONLY` branches the missing sensor is emulated/back-calculated
from the very quantity VE would cross-check, so the value algebraically cancels —
there is no independent corroboration.

### Decision

Only `DUAL_MAF_MAP_CROSSCHECK` yields a classified `ve_validity` (VALID or one of
the three fault modes). `MAP_ONLY` and `MAF_ONLY` always return
`VEValidity.UNKNOWN`. COMLab treats VE as evidence **only** when validity is not
`UNKNOWN`; single-sensor rationality is left to P0068-style checks.

### Consequences

- **Positive:** OBDLab never overstates VE confidence it cannot justify.
- **Positive:** the `0.0` sentinel + `UNKNOWN` pair cleanly suppresses VE-based
  router decisions.
- **Negative:** single-sensor vehicles get no VE-fault evidence from OBDLab;
  that diagnosis must come from elsewhere.

### Alternatives Considered

1. **Classify validity in all three branches.** Rejected: would assert
   cross-checks that do not exist.
2. **Emit no VE for single-sensor configs.** Rejected: `ve_pct` is still useful
   context; only its *validity* is unknown.

---

## ADR-0009: Bank-2 trims are `null`, never `0.0`, on single-bank engines

**Status:** Accepted (`OBDLab_KG_Wiki.md §3.1` contract; enforced in validator & aggregator)

### Context

Inline-engine (single-bank) vehicles have no bank-2 trims. Emitting `0.0` for an
absent bank is indistinguishable from a real zero trim and would corrupt
bank-asymmetry analytics (`per_bank_trim_delta`).

### Decision

When `number_of_banks == 1`, `shrtft2`/`longft2` (and the derived
`total_trim_correction_delta_b2`, `per_bank_trim_delta`) must be `null`.
Supplying a non-null bank-2 value on a single-bank engine raises
`PIDValidationError` (`SEMANTIC_CONTRACT §4.4` violation). The aggregator raises
if `number_of_banks == 2` but a bank-2 field is `None`.

### Consequences

- **Positive:** "absent bank" and "zero trim" are unambiguous; bank-asymmetry
  analytics stay sound.
- **Negative:** callers must pass `None` (not `0.0`) for absent banks — a
  contract they must observe.
- **Neutral:** bank-2 validation in bounds-checking is conditional on
  `number_of_banks == 2`.

### Alternatives Considered

1. **Default absent banks to `0.0`.** Rejected: conflates absence with a real
   zero and breaks `per_bank_trim_delta`.
2. **Omit bank-2 fields entirely from single-bank payloads.** Rejected: a
   variable field set complicates the fixed JSON contract; `null` is cleaner.

---

## References

- `KGtopic.md` — division of labor (parsing labs perceive, COMLab judges).
- `tasks/PROGRESS.md` — the OBDLab v2 task ledger (consumers, proposals, FU table).
- `tasks/T-OBDV2-0_revive_emitter_decision.md` — the scope-gate decision.
- `HLD_OBDLab.md` / `DLD_OBDLab.md` / `LLD_OBDLab.md` — current design surface.
- Proposals registry: `EP-OBD-11/12/17`, `EP-OBD-IN-05/07/08`, `EP-DTC-NOSTART-1`.
