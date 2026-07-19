# T-DTCV2-NOSTART-1 — Mode $06 monitor-aborted + freeze-frame cut no-start emitter (PRODUCER, CAN-era)

**Status:** `pending` (spec authored 2026-06-16 — coder-runnable) · **Lab:** DTCLab · **Stage:** 3 (producer) → reader COMLab Stage 4 · **Mode:** STRICT
**Origin:** OBDLab audit **Q8**, dispositioned cross-lab by `T-OBDV2-5` · **Registry:** DEP-8 · **Proposal:** `EP-DTC-NOSTART-1` (ADR-0009)
**Blocked by:** — (research gate CLOSED: Q8 answered in `obdlab/research/AUDIT_ANSWERS_OBDLab.md`; producer substrate already exists)
**Consumer (signal/noise):** COMLab **`T-COMV2-NOSTART-1`** (Stage 4) — `fault_atlas` no-start branch in `comlab/comlab/core/fault_atlas_router.py`, keyed on **(monitor-aborted state + freeze-frame fuel/spark-cut)**, routing **security-lockout** vs **mechanical-no-start**. Reader pre-registered by `T-OBDV2-5` (DEP-8).

> **Task shape — read first.** DTCLab is **emitter-only**. This task emits two raw discriminator signals; it does **not** decide security-lockout vs mechanical-no-start — that verdict is COMLab's at Stage 4. The emit-at-S3 / consume-at-S4 split is the same pattern as the OBDLab perception channels; anti-orphan closes at the COMLab reader. One task per session; both gates clean before `done`.

## Why this exists

A non-starting engine leaves no running PIDs and often no DTC, so the audit's no-start cases are largely invisible to COMLab today. The decisive, non-OEM signal is the **"Incomplete / monitor-aborted" Mode $06 state itself** — a Misfire Monitor (MID `$A1` / TID `$53`) that reads all-zero/Incomplete because *no ignition was authorised* (immobiliser lock-out) versus one that *could not run* (CKP/CMP loss / mechanical). Paired with a freeze-frame fuel/spark-cut tell, this lets COMLab split security-lockout from mechanical-no-start. The current `mode06_evaluator.classify_margin` only resolves the three **margin** tri-states (`PASSED` / `PENDING_FAIL_MARGINAL` / `CRITICAL_FAIL`); an aborted monitor has **no margin**, so the no-start signal cannot currently be represented. Source: wiki `10_nonstart_diagnostics.md` §10.3; ADR-0009.

## Research gate — CLOSED (Q8)

`obdlab/research/AUDIT_ANSWERS_OBDLab.md` Q8 + `pids-protocol/01_mode06-freezeframe-nostart-method.md`:
- The Incomplete/aborted state is itself diagnostic (security lock-out vs mechanical no-start).
- Primary monitor: Misfire **MID `$A1` / TID `$53`** — Incomplete/all-zero CIDs = aborted.
- **CAN-era gate:** Mode $06 MID/TID are only standardised/portable on **CAN (≈ 2008+)**; pre-CAN → per-OEM, **do not assert** (flag unreliable). Wiki §10.1 era table.

## Contract (PINNED)

Three additive changes; all ship with the named COMLab consumer (signal/noise satisfied):

1. **New monitor state** — add `Mode06MonitorState.MONITOR_ABORTED = "MONITOR_ABORTED"` to `dtclab/schemas/vocabulary.py` (today: `PASSED` / `PENDING_FAIL_MARGINAL` / `CRITICAL_FAIL`). Cite wiki §10.3. This is a *distinct* state, **not** a margin value — it must never be conflated with `CRITICAL_FAIL` (margin ≤ 0 = a real fail; aborted = the test never ran).

2. **Evaluator detects aborted** — extend `mode06_evaluator.evaluate_monitor` to accept an explicit completeness signal (pinned: add parameter `monitor_incomplete: bool = False`). When `monitor_incomplete is True` → classify `MONITOR_ABORTED` and bypass `classify_margin` (margin is meaningless for an aborted monitor). `classify_margin` itself is **unchanged** — the three existing margin branches stay byte-identical (regression-guarded). Default `False` preserves every current call site.

3. **Freeze-frame cut flag** — add one derived symptom flag `ff_fuel_spark_cut_at_crank: bool = False` to `FreezeFrameRecord` §12.3 in `dtclab/schemas/freeze_frame.py` (the existing six §12.3 flags do not cover fuel/spark cut), computed in `freeze_frame_extractor.extract_freeze_frame`. **Note — deviation from ADR wording:** ADR-0009 says "Mode-06 schemas"; the FF-cut indicator correctly belongs with the other §12.3 derived flags on `FreezeFrameRecord`, not on `Mode06MonitorResult`. Flagged for owner ratification.

4. **CAN-era gate** — the `MONITOR_ABORTED` no-start assertion is emitted **only** when the vehicle is CAN-era, read from `DnaView.euro_emission_category` (`EuroEmissionCategory`, `dna_view.py`). Pre-CAN / `UNKNOWN` → classify normally (margin tri-state) and do **not** assert the aborted no-start signal. Every numeric/boundary literal carries a wiki cite.

## Scope-confirm before coding (two genuinely under-determined predicates)

Per OBDLab/DTCLab START_HERE step 5, post a one-paragraph scope confirm resolving **both** of these (each needs a wiki citation per the numeric-literal rule) before writing code:

- **(a) `ff_fuel_spark_cut_at_crank` predicate.** The exact computable condition over the §12.1 PIDs at a cranking/key-on snapshot is not pinned by a single threshold in wiki §10.3 (which gives *signatures*, e.g. RPM 0 while cranking, OL-Fault, low system voltage). Pin the predicate from wiki §10.3 + `DTC_VOCABULARY.md` §12.3 and cite it.
- **(b) CAN-era boundary.** wiki §10.1 places CAN at 2000–2010; OBDLab Q8 says Mode-06 is portable "≈ 2008+". Pin which `EuroEmissionCategory` members are the CAN-portable set (default: `EURO_4`/`EURO_5`/`EURO_6`/`EURO_7`; `EURO_1`–`EURO_3` and `UNKNOWN` → do not assert) and cite §10.1 + Q8.

If either cannot be pinned to a cited rule, raise one question — do **not** invent a threshold.

## Success criteria

- `MONITOR_ABORTED` member added with wiki cite; `classify_margin` unchanged (diff touches only the new branch).
- `evaluate_monitor` returns `state == MONITOR_ABORTED` for `monitor_incomplete=True` on a CAN-era vehicle for MID `$A1`/TID `$53`; returns the normal margin tri-state when `monitor_incomplete=False`.
- Pre-CAN / `UNKNOWN` → aborted no-start signal **not** asserted (margin tri-state path taken).
- `ff_fuel_spark_cut_at_crank` present on `FreezeFrameRecord`, computed in `freeze_frame_extractor`, default `False`, cited predicate.
- **Emitter-only:** no security-lockout/mechanical-no-start verdict string produced in `dtclab/**` (grep-guarded — that routing is COMLab's).
- New unit tests cover: aborted classification, margin path unchanged (regression), CAN-era gate (pre-CAN not asserted), FF-cut flag true/false.
- Inner loop green: `ruff check .` → `pyright dtclab/` → `pytest -x -q`.

## Deliverables

1. `dtclab/dtclab/schemas/vocabulary.py` — `Mode06MonitorState.MONITOR_ABORTED`.
2. `dtclab/dtclab/core/mode06_evaluator.py` — `monitor_incomplete` handling + CAN-era gate wiring.
3. `dtclab/dtclab/schemas/freeze_frame.py` — `ff_fuel_spark_cut_at_crank` §12.3 flag.
4. `dtclab/dtclab/core/freeze_frame_extractor.py` — compute the new flag (cited predicate).
5. `dtclab/tests/unit/` — new cases (aborted, regression, CAN-era gate, FF-cut).
6. `tasks/progress_notes/T-DTCV2-NOSTART-1.md` — `## Plan` scope-confirm, then `VERIFICATION GATE` + `CODE REVIEW`.

## Files to touch

- `dtclab/dtclab/schemas/vocabulary.py`
- `dtclab/dtclab/core/mode06_evaluator.py`
- `dtclab/dtclab/schemas/freeze_frame.py`
- `dtclab/dtclab/core/freeze_frame_extractor.py`
- `dtclab/tests/unit/**`
- **No graph/wiki/docs rebuild; no cross-lab imports; no COMLab/OBDLab source change.**

## Out of scope

- The COMLab no-start **verdict** (security vs mechanical) — that is `T-COMV2-NOSTART-1` (Stage 4).
- Pre-CAN per-OEM MID/TID tables — excluded/flagged, not asserted.
- Any margin-threshold change to `classify_margin`.
- Re-running graphify or touching `graph/**` (forbidden per `OBDLAB`/`DTCLAB` START_HERE).
- Off-scope finds → follow-ups in the progress note, not the diff.

## Verification

```bash
cd <repo>/labs/dtclab
# 1. new state exists, margin tri-state intact
grep -n "MONITOR_ABORTED" dtclab/schemas/vocabulary.py
grep -n "PASSED\|PENDING_FAIL_MARGINAL\|CRITICAL_FAIL" dtclab/core/mode06_evaluator.py   # classify_margin unchanged
# 2. evaluator gate + FF flag present
grep -n "monitor_incomplete\|euro_emission_category" dtclab/core/mode06_evaluator.py
grep -n "ff_fuel_spark_cut_at_crank" dtclab/schemas/freeze_frame.py dtclab/core/freeze_frame_extractor.py
# 3. emitter-only — no COMLab verdict leaked into DTCLab
! grep -rniE "security[_-]?lockout|mechanical[_-]?no[_-]?start" dtclab/ && echo "OK emitter-only"
# 4. no cross-lab imports
! grep -rnE "from (gaslab|obdlab|comlab|dnalab)" dtclab/ && echo "OK no cross-lab imports"
# 5. inner loop
ruff check . && pyright dtclab/ && pytest -x -q
```

All steps pass; the no-start signals are emitted and CAN-era gated; `classify_margin` and all prior call sites are unchanged; DTCLab asserts no no-start verdict.

## Anti-orphan note

The two signals are produced here (DTCLab S3) and read by COMLab `T-COMV2-NOSTART-1` (S4) under the same proposal `EP-DTC-NOSTART-1` — not an orphan. Until S4 lands, the new state/flag are pre-frozen contract surface (expected divergence, like the OBDLab emit-S2/consume-S4 channels). CAN-era gating bounds applicability; pre-CAN is flagged, not asserted. Anti-orphan grep-confirm closes at the COMLab reader.

## Progress hook

`tasks/progress_notes/T-DTCV2-NOSTART-1.md` opens with the confirmed `## Plan` (resolve scope-confirm (a) and (b) with wiki cites; name the consumer code path; the CAN-era gate), then `VERIFICATION GATE` + `CODE REVIEW`. On completion, flip the PROGRESS.md row to `done` with: "MONITOR_ABORTED + ff_fuel_spark_cut_at_crank emitted, CAN-era gated; classify_margin unchanged; emitter-only; T-COMV2-NOSTART-1 (S4) reads; inner loop green."
