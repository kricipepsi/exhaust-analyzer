# T-OBDV2-ARCH-2 — Proposal-or-prune the orphan vocab/schema members (🟡 signal/noise)

**Status:** `done` — **owner/architect decision per member** (then coder-runnable) ·
**Lab:** OBDLab (Stage 2) · **Mode:** STRICT
**Origin:** OBDLab skills-audit 2026-06-08 — finding **AR-2** (`audit/AUDIT_04_architecture.md`).
**Blocked by:** —
**Consumer (signal/noise):** named **per member** in the plan; "future use" is not a consumer.

## Why this exists

Each member below is defined (and mostly existence-tested) but **read by no live code path** —
an orphan and a signal/noise breach regardless of green tests (CLAUDE.md anti-orphan rule).
Verified by grep across `4DLabV2` (excluding `ARCHIVE/`):

| Member | Defined | Live reader? | Disposition (recommended) |
|--------|---------|--------------|---------------------------|
| `VERoutingMode` (enum) | `schemas/vocabulary.py` L21-29 | none — `VEEngine` routes on `AirMeteringStrategy`; only a `dna_view` docstring + `test_vocabulary` reference it | **prune** (duplicate of `AirMeteringStrategy`) |
| `dna_view.cylinder_count` | `schemas/dna_view.py` L66 | none — bank logic uses `number_of_banks`, not derived from this; set only in tests | **prune** (or wire `number_of_banks ← cylinder_count` if that is the intent — name it) |
| `O2FailureMode.SLUGGISH` / `WRONG_CENTERLINE` / `HEATER_FAULT` | `vocabulary.py` L110, L112-113 | none — never produced by `o2_normalizer`, never consumed | **proposal** — register detectors + consumers (the taxonomy is richer than today's detector) |
| `O2FailureMode.DEAD` | `vocabulary.py` L111 | consumed by `ranking` (`_DEFINITIVE_O2_MODES`, `_freeze_frame_o2_rail_agrees`) but **never produced** | **proposal** — add the DEAD detector (no-activity O2), or prune the consumer branch if not pursued |

## Disposition rule (v2 forward-progress)

For each member: **proposal** (name a real producer **and** consumer, register in
`comlab/comlab/config/proposals/proposals.yaml`, ship them together) **or** **prune**
(remove the member + its existence test). Pruning `VERoutingMode`/`cylinder_count` looks
clear; the missing `O2FailureMode` detectors look like genuine proposals — but the owner
ratifies each.

## Success criteria

- Every remaining `O2FailureMode` / `VERoutingMode` member and `dna_view` field has a live
  producer **and** consumer, **or** is in the proposals registry, **or** is removed.
- Anti-orphan grep clean for the surviving members; `pytest -x -q` green; inner loop clean.

## Files to touch

- `schemas/vocabulary.py` · `schemas/dna_view.py` · `tests/unit/test_vocabulary.py`,
  `test_dna_view.py` · (for any proposal) `comlab/comlab/config/proposals/proposals.yaml` +
  a forward-registered COMLab consumer row.

## Out of scope

`ranking.py`'s own consumer question is **T-OBDV2-ARCH-1** (the `DEAD` consumer branch lives
there — coordinate if pruning). Test-infra build deferred.

## Progress hook

`tasks/progress_notes/T-OBDV2-ARCH-2.md`: `## Plan` (per-member proposal/prune ruling + named
consumers) → gates. PROGRESS.md row → `done` only when every member is consumer-backed,
registered, or removed.
