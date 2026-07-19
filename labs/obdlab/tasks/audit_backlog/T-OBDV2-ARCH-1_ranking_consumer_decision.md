# T-OBDV2-ARCH-1 — Name the live consumer of `ranking.py`/`family_map.py`, or excise (🟡 signal/noise)

**Status:** `done` — **RULING RECORDED: (B) EXCISE** (owner-ratified 2026-06-09) → coder-runnable removal ·
**Lab:** OBDLab (Stage 2) · **Mode:** STRICT

## Owner ruling (2026-06-09)

**Disposition (B) — excise.** Repeatedly stated by the owner; consistent with
`project_simple_variants_dead` (the named consumer `OBDLabSimple → COMLabSimple` is archived,
not a live port). No live (non-test, non-archive) module imports `classify_top3` /
`rank_candidates` — verified by grep across `4DLabV2`: the only importers are OBDLab's own unit
tests (`test_ranking.py`, `test_classify_top3.py`, `test_family_map.py`). DTCLab/GASLab carry
their *own* parallel `ranking` modules — separate codebases, no cross-lab import, untouched.
Disposition (A) is **not** taken: COMLab fusion consumes OBDLab via the full `OBDLivePayload`,
not a pre-ranked top-3.

**Coupling → T-OBDV2-ARCH-2 (DEAD).** `O2FailureMode.DEAD`'s only reader is inside
`ranking.py` (`_DEFINITIVE_O2_MODES`, `_freeze_frame_o2_rail_agrees`). Excising `ranking.py`
removes that reader, so after this task `DEAD` is consumer-less — it joins `SLUGGISH` /
`WRONG_CENTERLINE` / `HEATER_FAULT` as a uniformly orphaned `O2FailureMode` member. ARCH-2 must
be (re)specced **after** this lands: all four O2 modes become proposals (new producer+consumer)
or prune — no surviving "DEAD already has a consumer" branch.
**Origin:** OBDLab skills-audit 2026-06-08 — finding **AR-1** (`audit/AUDIT_04_architecture.md`).
**Blocked by:** — (decision-bearing)
**Consumer (signal/noise):** **this task *is* the consumer decision.** Cannot reach `done`
until a live consumer is named **or** the code + its tests are removed.

## Why this exists

Deletion test: removing `obdlab/ranking.py` (266 LOC) and `obdlab/family_map.py` (80 LOC)
breaks **no live behaviour**. Grep across `4DLabV2` (excluding `ARCHIVE/`) shows
`classify_top3` / `rank_candidates` imported **only by OBDLab's own unit tests**. The module
docstrings name the consumer as the **OBDLabSimple → COMLabSimple** composition path —
which is being archived (`project_simple_variants_dead`). So this is a one-sided seam: a
built adapter whose downstream port is scheduled for deletion. Per the signal/noise rule, a
module ships only with a **named, existing** consumer.

Context that argues *against* deletion: GASLab and DTCLab carry parallel, **wired**
`ranking.classify_top3` modules feeding their `LabResult` adapters (e.g. DTCLab → T-DTW-1).
The OBDLab equivalent is plausibly *meant* to feed the live COMLab fusion — just not wired yet.

## Disposition (owner picks — do not guess)

- **(A) Wire it (preferred, v2 forward-progress).** Name the live COMLab fusion consumer of
  `obdlab.ranking.classify_top3` and register the wiring as a Stage-4 task (mirroring
  GASLab/DTCLab). OBDLab then has a real top-3 emit path.
- **(B) Excise on Simple-removal.** If COMLab consumes OBDLab via the full `OBDLivePayload`
  (not the top-3), mark `ranking.py`/`family_map.py` orphaned and schedule removal with the
  `*Simple` cleanup (`T-RM-*`), deleting their tests too.

The audit cannot choose for you — it depends on the COMLab fusion contract (does COMLab want
OBDLab's pre-ranked top-3, or does it rank from the payload itself?).

## Success criteria (ruling = B)

- `obdlab/ranking.py`, `obdlab/family_map.py`, and their three unit tests are removed.
- `ruff` / `pyright` / `pytest -x -q` stay green; **no dangling imports** of `ranking` /
  `family_map` / `classify_top3` / `rank_candidates` anywhere under `labs/obdlab/` (grep clean).
- Anti-orphan note: `O2FailureMode.DEAD` is now read by no live path — record it in the
  T-OBDV2-ARCH-2 progress note (do **not** silently leave it dangling).

## Files to touch (ruling = B — exact, verified 2026-06-09)

- `obdlab/obdlab/ranking.py` — delete
- `obdlab/obdlab/family_map.py` — delete
- `obdlab/tests/unit/test_ranking.py` — delete
- `obdlab/tests/unit/test_classify_top3.py` — delete
- `obdlab/tests/unit/test_family_map.py` — delete

## Out of scope

Do not half-wire (no live consumer + keep the code = the current orphan state persists).
Test-infra build deferred.

## Progress hook

`tasks/progress_notes/T-OBDV2-ARCH-1.md`: `## Plan` (ratified A or B + the named consumer) →
gates. PROGRESS.md row → `done` only when the consumer is live **or** the code is gone.
