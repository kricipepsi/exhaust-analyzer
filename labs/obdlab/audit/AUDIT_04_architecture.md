# OBDLab audit — Lens 4/5: `Improve Codebase Architecture`

**Date:** 2026-06-08 · **Auditor role:** architect (read + report; no code edits) ·
**Skill:** `_skills/codingskills/Improve Codebase Architecture` (deep vs shallow modules,
**deletion test**, seams/adapters, locality & leverage; "the interface is the test surface").
**Subject:** `4DLabV2/labs/obdlab/obdlab/` real source.

> The skill's process normally spawns an `Explore` subagent and runs a grilling loop. Per
> the workspace rule against unprompted subagents, the lens was applied by **direct
> reading**; candidates are presented for the owner to pick, not auto-refactored.

This lens overlaps the project's **signal/noise** rule directly: a deep module earns its
interface; an **orphan** (defined, read nowhere live) is the opposite — pure interface,
no leverage. Two orphan clusters are the headline architectural findings.

---

## Findings — deepening opportunities & seams

### 🟡 AR-1 `ranking.py` + `family_map.py`: a real seam with no live adapter on the other side
**Deletion test:** if `obdlab/ranking.py` (266 LOC) and `obdlab/family_map.py` (80 LOC)
were deleted, what live behaviour breaks? Grep across `4DLabV2` (excluding `ARCHIVE/`)
shows `classify_top3` / `rank_candidates` imported **only by OBDLab's own unit tests**
(`tests/unit/test_ranking.py`, `test_classify_top3.py`). No `comlab/`, no `wired/` app, no
fault-atlas path imports them. The module docstrings name the consumer explicitly:

> *"the internal runners-up needed by the later **OBDLabSimple** composition path"* and
> *"pass through to **COMLabSimple's** LabCandidate.fault_id"* (`family_map.py` L4-5,
> `ranking.py` L4-5).

Per the recorded decision (`project_simple_variants_dead`: *all `*Simple` labs → archive*),
**that named consumer is being removed.** So this is a one-sided seam: a well-built
adapter whose downstream port is scheduled for deletion. By the signal/noise rule, the
field/module ships only with a **named, existing** consumer.

This is **not** "delete it" advice — GASLab and DTCLab carry parallel, *wired*
`ranking.classify_top3` modules that feed their `LabResult` adapters (`dtclab` →
`T-DTW-1`). The OBDLab equivalent is very likely *meant* to feed the live COMLab fusion;
it just isn't wired yet.

- **Architect action (the decision this lens forces):** either
  1. **Name the live COMLab consumer** of `obdlab.ranking.classify_top3` and register the
     wiring as a task (forward progress — the preferred v2 disposition), or
  2. if COMLab consumes OBDLab via a different surface (the full `OBDLivePayload`, not the
     top-3), **register `ranking.py`/`family_map.py` as orphaned-on-Simple-removal** and
     schedule their excision with the `*Simple` cleanup.

  Until one is chosen, ~346 LOC sit behind a seam with no live adapter — the canonical
  "shallow because nothing downstream needs it yet" risk.

### 🟡 AR-2 Orphan vocabulary / schema members (signal/noise breaches)
Each below is **defined and (mostly) test-checked for existence, but read by no live code
path.** A field that is "defined but read nowhere is an orphan and a signal/noise breach,
regardless of a green test run" (CLAUDE.md anti-orphan rule).

| Member | Defined | Live consumer? | Note |
|--------|---------|----------------|------|
| `VERoutingMode` (enum) | `schemas/vocabulary.py` L21-29 | **None** | `VEEngine` routes on `AirMeteringStrategy`; `VERoutingMode` appears only in a `dna_view.py` docstring ("maps 1-to-1") + `test_vocabulary.py` existence check. A duplicate enum. |
| `dna_view.cylinder_count` | `schemas/dna_view.py` L66 | **None (live)** | Bank logic uses `number_of_banks`, which is **not** derived from `cylinder_count`. Set only in tests. The "bank-2 null contract" citation is aspirational — nothing reads it. |
| `O2FailureMode.SLUGGISH` / `WRONG_CENTERLINE` / `HEATER_FAULT` | `vocabulary.py` L110, L112-113 | **None** | Never produced by `o2_normalizer` and never consumed by `ranking`. Pure existence-tested enum members. |
| `O2FailureMode.DEAD` | `vocabulary.py` L111 | consumed by `ranking` (`_DEFINITIVE_O2_MODES` L68, `_freeze_frame_o2_rail_agrees` L243) | but **never produced** — `o2_normalizer` emits only `NO_FAULT/STUCK_LEAN/STUCK_RICH/WIDEBAND_OFFSET_CANDIDATE`. So `ranking` handles an unreachable case (and `ranking` itself is AR-1). |

- **Architect action:** for each, choose **proposal** (name a real producer+consumer and
  ship them together — e.g. an O2 SLUGGISH detector with a fault-atlas route) or **prune**.
  `cylinder_count` and `VERoutingMode` look like prune candidates; the missing
  `O2FailureMode` detectors (`SLUGGISH`, `DEAD`, `WRONG_CENTERLINE`, `HEATER_FAULT`) look
  like genuine **proposals** (the taxonomy is richer than the current detector) — register
  them in `comlab/config/proposals/` with consumer + code path, per the v2-forward rule.

### 🟡 AR/UB-1 The orchestrator is a shallow module made fragile by hidden state
(Cross-ref `AUDIT_02` UB-1.) `SensorSignalTranslator` is a deep, valuable module — a small
`translate()` interface over the whole §3–§12 chain (good leverage). But the two-point
linearity **instance state** undermines its *locality*: the knowledge "this result depends
on a previous call" lives nowhere at the interface. Threading the prior band explicitly
(UB-1) keeps the module deep **and** restores locality — the highest-value deepening here.

### 🟢 ARCH-3 Doc-vs-code drift weakens the interface contract
`VEValidity.FAULT_VE_SENSOR_SKEW` docstring (`vocabulary.py` L52) says *"VE > 85% at idle"*,
but the implementation thresholds are **90%** (`ve_engine.py` `_CUTOFF_VE_SKEW = 90.0` L49;
`semantic_consistency_checker.py` `_CUTOFF_VE_NA = 90` L25). For a numeric-literal-cited
codebase, the vocabulary's self-description disagreeing with the live cutoff is an interface
defect. Align the docstring to 90 (or the code to 85 if 85 is the wiki truth — confirm).

### 🎉 ARCH-4 Strong seam discipline at the lab boundary (praise)
The DNA seam is exemplary: `schemas/dna_view.py` is an OBDLab-owned mirror with an explicit
"never import from comlab/dnalab/vinlab" rule, `None`-at-boundary is a defined contract
(== `confidence == NONE`), and there are **zero** cross-lab Python imports. `OBDLivePayload`
is a clean typed JSON seam. The per-`§` module decomposition (validator / bucketing /
semantic / VE / O2 / trim / analytics) gives good locality — bugs in O2 logic live in one
file. This is the architecture working as intended; preserve it.

---

## Candidates for the owner to pick (skill step 2 — not auto-applied)

1. **AR-1** — name the live COMLab consumer of `classify_top3`, or schedule excision.
2. **AR-2** — proposal-vs-prune decision for each orphan member.
3. **AR/UB-1** — de-state the orchestrator (highest-value deepening).

## Draft task specs (architecture lens)

### T-OBDV2-AUDIT-ARCH-1 — Decide the fate of `ranking.py`/`family_map.py` (AR-1) **[architect/owner]**
- **Files (spec only):** `tasks/PROGRESS.md` + a new task file; touches `obdlab/ranking.py`,
  `obdlab/family_map.py`, and (if wired) the COMLab fusion import site.
- **Decision:** wire to a named live COMLab consumer **or** mark orphaned-on-Simple-removal
  and schedule with the `*Simple` excision (`T-RM-*`).
- **Success:** either a live module imports `classify_top3` with a passing integration
  assertion, **or** the modules + their tests are removed and `pytest -x -q` stays green.
- **Consumer (signal/noise):** this *is* the consumer decision — the task cannot be `done`
  until a live consumer is named or the code is removed.

### T-OBDV2-AUDIT-ARCH-2 — Proposal-or-prune the orphan members (AR-2)
- **Files:** `schemas/vocabulary.py`, `schemas/dna_view.py`, and (for proposals)
  `comlab/config/proposals/`
- **Change:** prune `VERoutingMode` + `cylinder_count` if no consumer can be named; register
  `O2FailureMode.{SLUGGISH,DEAD,WRONG_CENTERLINE,HEATER_FAULT}` as proposals **with** a named
  producer (detector) + consumer (fault-atlas route), per v2-forward-progress.
- **Success:** every remaining enum member / schema field has a live producer **and**
  consumer, or is in the proposals registry; anti-orphan grep is clean; `pytest -x -q` green.
- **Consumer (signal/noise):** named per member in the task file; "future use" is not allowed.

### T-OBDV2-AUDIT-ARCH-3 — Fix the VE-skew threshold doc drift (ARCH-3)
- **Files:** `schemas/vocabulary.py` L52 (or `ve_engine.py`/`semantic_consistency_checker.py`
  if 85 is the wiki truth — confirm against OBDLab_KG_Wiki §6.4/§4 first).
- **Success:** docstring and code agree on one cited cutoff; numeric-literal citation matches.
- **Consumer:** n/a (doc/contract correctness). No schema change.
