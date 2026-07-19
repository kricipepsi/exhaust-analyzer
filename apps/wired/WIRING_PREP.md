# Wiring pre-prep gate — `apps/wired`

**Date authored:** 2026-06-28 (architect, Cowork)
**Purpose:** the labs are *structurally* fit to wire (all import clean, all
public surfaces match the composition contract, COMLab's `LabPipelineAggregator`
constructs and is callable). This gate covers the **one hard prerequisite** and
the **triage items** that must clear before the wiring pack (`WIRED_START_HERE.md`)
can run a clean end-to-end case.

> Read this before `WIRED_START_HERE.md`. The wiring pack's first runnable task
> (`T-WIRE-1`) is **blocked by Section A** below.

---

## Fitness verdict (2026-06-28)

Live check against `.venv-wired` (Python 3.14.6):

| Lab | Import | Entry point (signature verified) | Output type | Verdict |
|---|---|---|---|---|
| GASLab | `from gaslab import process, GasLabContext, GasReading` | `process(reading, context) -> GasLabPayload` | `GasLabPayload` | OK fit |
| OBDLab | `from obdlab import SensorSignalTranslator` | `.translate(raw_user_inputs, dna_view, accumulator) -> OBDLivePayload` | `OBDLivePayload` | OK fit |
| DTCLab | `from dtclab import DataFusionSanitizer` | `.sanitize(raw_dtcs, raw_freeze_frame, raw_mode06, *, ...) -> DTCLabPayload` | `DTCLabPayload` | OK fit |
| DNALab | `from dnalab import build_vehicle_dna` | `build_vehicle_dna(vin, triage) -> VehicleDNA` | `VehicleDNA` | OK fit |
| VINLab | `from vinlab import decode, VINDecodeError` | `decode(vin) -> VinDNA` / exception for no-VIN fallback | `VinDNA` | OK fit |
| COMLab | `from comlab.core.lab_pipeline_aggregator import LabPipelineAggregator` | `.process(OrchestratorInboundRequest, fault_code=None) -> OrchestratorFinalUIOutput` | `OrchestratorFinalUIOutput` | OK fit |

COMLab inbound contract `OrchestratorInboundRequest` is at
`labs/comlab/comlab/schemas/ingestion.py:488`; the payload mirrors
(`SessionMetadata` 151, `GasLabPayload` 165, `DTCLabPayload` 289,
`OBDLiveDataPayload` 324) and the output `OrchestratorFinalUIOutput`
(`labs/comlab/comlab/schemas/response.py:132`) are all present. The risky
**FATAL gates are behind a default-off flag** (`enable_fatal_gates=False`), so a
baseline `diagnose()` run does not trip them.

**Conclusion:** wiring may *start* once Section A clears. Sections B and C are
carried into the wiring pack as documented work, not blockers to authoring it.

---

## Section A — Hard prerequisite (gate; blocks `T-WIRE-1`)

One emitter->consumer drift would make COMLab reject a valid GAS payload at the
boundary. The GASLab emitter now produces a **34-value** `ChemicalSignature`
enum (a fixed list of allowed chemistry labels). COMLab's local **mirror** of
that enum (the copy COMLab re-declares so it never imports a lab) is still at
the old count — its docstring literally reads "28-value canonical fault label"
at `labs/comlab/comlab/schemas/ingestion.py:168`. If `apps/wired` forwards a GAS
payload carrying one of the 3 new `CAM_TIMING_*` values, COMLab's Pydantic
validation (the schema-shape check) rejects or mis-routes it.

The fix is a **pair-land** (a cross-package consistency guard checks both lists
land together). **The registry half is already done**; only the COMLab-mirror
half remains.

| Prereq | Spec (existing, on a lab ledger) | Status | Must reach |
|---|---|---|---|
| Registry `ChemistryState` -> 34 | `labs/comlab/registry/docs/registry_tasks/REG-V2-CHEMSIG-34_chemistry_state_reconcile.md` | done (`fba3b96`, 2026-06-21) | — |
| COMLab mirror enum 28/32 -> 34 | `labs/gaslab/tasks/T-GV2-2_chemsig_consumer_mirror_reconcile.md` | **done (2026-06-28, Cowork)** | — (cleared) |

> **Action:** assign `T-GV2-2` to a coder on the **gaslab** ledger
> (`labs/gaslab/tasks/PROGRESS.md`) via `.agent/assignments.md`, exactly as any
> other lab task — `apps/wired` does **not** edit lab code (lab isolation). When
> `T-GV2-2` is `done`, clear `T-WIRE-1`'s `Blocked by` in `WIRED_PROGRESS.md`.

---

## Section B — Triage task (authored here; output is a ruling, not lab code)

Two GASLab->registry chemistry contradictions blocked specific oil-burning cases
in the prior wiring (archived as `U-WV2-1` rings / `U-WV2-2` PCV). They are
**case-routing** issues, not surface-fitness issues, so they surface *during*
the oil-case run (`T-WIRE-2`). One architect triage decides, up front, whether
each is fixed at the emitter/registry or accepted as a known-blocked case so the
wiring pack doesn't stall mid-session.

| Task | File | Status |
|---|---|---|
| `T-PREP-WIRE-1` | `wiring_prep_tasks/T-PREP-WIRE-1_rings_pcv_chemistry_triage.md` | **done (2026-06-28)** → `RINGS_PCV_TRIAGE_RULING.md` |

---

## Section C — Known wiring-time gotchas (carry into the wiring pack)

Not blockers to authoring; the wiring task files name them so a coder isn't
surprised.

- **Registry guard rule-count drift.** A pending registry follow-up
  (`wired-registry-guard-rule-count-drift`, in
  `labs/comlab/registry/docs/REGISTRY_PROGRESS.md`) records that
  `apps/wired/wired/registry_guard.py` must expect **73** rules, not 68, or the
  side-by-side harness raises `RegistryActivationError`. `T-WIRE-1` creates that
  guard with the correct count.
- **High-idle gas block must be forwarded.** The prior composition dropped the
  high-idle (`*_high`) GAS reading; the oil case depends on it. `T-WIRE-1`
  forwards it onto the COMLab `GasLabPayload` (composition-contract skill section 6).
- **`air_metering_strategy` token.** `SessionMetadata.air_metering_strategy` is
  an optional DNA token the VE gate reads — forward it from DNALab.
- **The deferred fusion path is gone.** Do not import or reference it; the live
  verdict comes only from `LabPipelineAggregator.process()` (REG-V2 shim at
  `labs/comlab/registry/integration_shim.py`).

---

## Exit criteria for this gate

1. ~~`T-GV2-2` is `done` on the gaslab ledger (Section A).~~ **DONE 2026-06-28** — COMLab mirror at 34, registry CT-001/003 re-pointed, 510 tests green.
2. ~~`T-PREP-WIRE-1` is `done`~~ **DONE 2026-06-28** — `RINGS_PCV_TRIAGE_RULING.md`: both rings & PCV ruled ACCEPT-KNOWN-BLOCKED; cross-lab reconciles `T-XLAB-RINGS-RECONCILE-1` / `T-XLAB-PCV-VERIFY-1` forward-registered on the gaslab ledger.

When both hold, start the wiring pack: paste `WIRED_START_HERE.md` as message 1
of a fresh coder session.
