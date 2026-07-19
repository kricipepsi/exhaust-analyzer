# 4DLab v3 — Implementation Plan (top-3 differential to 95%)

**Date:** 2026-06-30 · **Author:** architect (Cowork) · **Owner:** Mutolovsky
**Working folder:** `/agent_workspace/v3/`
**Status:** plan + first task pack authored; build runs against this plan, judged by the v3 scoreboard.

> **Audience note.** This file is the canonical v3 spec. The prose is written for the owner
> (coding terms glossed on first use); the `v3_tasks/T-V3-*.md` files are written for coder
> sessions in normal coder register. Read this file top-to-bottom once; the task files pin
> the exact code targets.

---

## 0. The decision that defines v3

The owner set the goal and chose the direction (2026-06-30):

- **Goal:** at least **95% accuracy** measured as *the correct fault family appears in the
  engine's top-3 most-probable verdicts*, not as a single forced guess.
- **Verdict shape:** **ranked top-3 differential + abstain** (the engine shows up to three
  likely causes ranked by probability, and says "not sure" when the evidence can't separate them).
- **Scope:** **engine + answer-key fixes first, then new input signals** for the cases that a
  single idle gas snapshot physically cannot separate.

The owner's own read of the problem — *"the problem is in the ranker"* — is correct and is
confirmed at the row level (section 2). This plan is built around it.

---

## 1. Why this goal is reachable when "95% single-verdict on everything" was not

The June-30 root-cause audit proved, on real rows, that the ~50% single-verdict ceiling is a
**discrimination limit in the measurement** — one warm-idle 5-gas snapshot plus whatever DTC
exists does not physically separate the confusable families. No amount of rules, wikis, or
re-ranking moves a limit that lives in the input. That finding stands.

The top-3 reframe sidesteps most of that wall **without pretending the wall isn't there**.
Here is the whole 294-case graded set, sorted by *where* each case fails — and what the
top-3 reframe does to each bucket:

```
 bucket          n     what fails                       top-3 + abstain does...
 ---------------------------------------------------------------------------------
 SURFACE_DEFECT  133   routed RIGHT; only the answer-    already #1  -> COUNTS once
                       key format (code/confidence)      the answer key is re-pinned
 OUTRANKED       107   right answer scored, lost the     it's the runner-up -> COUNTS
                       tie to a louder family            (this is the ranker problem)
 ORACLE_SUSPECT   10   engine arguably right; answer     re-pin -> COUNTS
                       key questionable (mech-wear)
 PRODUCER_GAP     25   upstream lab never emitted the    still MISSES — needs new signal
                       state the right rule needs        (the discrimination wall)
 DATA_GAP         19   the deciding input is absent      still MISSES — needs new signal
                       from the case entirely            or honest abstain
 ---------------------------------------------------------------------------------
```

**Arithmetic of the reframe** (before any new-signal work):

```
 correct-in-top-3  ~  SURFACE_DEFECT + OUTRANKED + ORACLE_SUSPECT
                   =  133 + 107 + 10  =  250 / 294  ~  85%
 still missing     =  PRODUCER_GAP + DATA_GAP  =  44 / 294  ~  15%
```

So the **ranker reframe + answer-key re-pin alone lands ~85%** with *zero* discrimination
work and *zero* ranker re-tuning. Closing the last ~10 points to 95% is exactly the 44
PRODUCER_GAP/DATA_GAP cases — that is what "include new signals" buys, and nothing else can.

> **The 85% figure is an estimate from the frozen trace and must be measured first.**
> OUTRANKED means the correct rule *scored*, but the localization map does not yet confirm it
> scored in the **top 3** (vs 4th/5th). Task **T-V3-0** measures the real correct-in-top-3
> rate from the existing traced run before any code is written. That number sets the realistic
> target and tells us how many of the 107 need rank work after all.

---

## 2. What the engine already does (why this is cheaper than a rewrite)

The ranker is **not** missing the runner-ups — it computes them and throws them away at the
*display* surface. Verified in `labs/comlab/comlab/core/fault_atlas_router.py`:

- `execute_triage_loop()` returns a `TriageVerdict` with **`winner` + up to 3 `runner_ups`**
  (line 922; `runner_ups = scored[1:4]`, line 1654). ("triage loop" = the 5-step routine that
  prunes, scores, and ranks the candidate faults.)
- The output schema **already carries a differential list**:
  `DiagnosticVerdict.differential_siblings` — up to 5 entries, each with `fault_id`,
  `fault_name`, `confidence_score`, `source` (`labs/comlab/comlab/schemas/response.py:79-101`).
- `_merge_differential_siblings()` already merges the runtime runner-ups with editor-curated
  siblings from the knowledge graph ("knowledge graph" = the fault dictionary the engine reads).

```
 raw inputs -> GASLab / OBDLab -> rules score -> RANKER -> winner ----------> verdict (1 family)
   (gas,DTC)   (produce states)   (per-rule       |        runner_ups -----> differential_siblings
                                    score 0-1)     |                           +- COMPUTED but the
                                                   +- picks ONE winner            SCORER ignores it
```

**The gap is in the *scorer and answer key*, not the engine's math.** Today the grader checks
only `winner.fault_family`. The correct family is often sitting in `differential_siblings`
already. v3's core move is to **grade the differential**, not to rebuild the ranker.

One small engine change is still needed: `DifferentialSiblingOut` carries `fault_id` but **not**
a resolved `fault_family`, so the scorer (and the UI runner-up panel) must map each sibling's
id to its family. v3 adds that field with a named consumer (T-V3-3).

---

## 3. The v3 metric (what "95%" is measured against)

v3 keeps the old single-verdict number for honest comparison **and** adds the new top-3 number.
Both are reported every run.

| Metric | Definition | Role |
|---|---|---|
| `single_verdict` (family+state) | winner family == expected, state correct | the frozen BEFORE = **45.24%**; never deleted |
| **`top3_family`** | expected family in {winner} union {top-2 differential siblings by score} | **the v3 acceptance metric** |
| `coverage` | share of cases the engine did **not** abstain on | honesty dial — high accuracy on 60% coverage is not a win |
| `top3_on_covered` | `top3_family` restricted to non-abstained cases | the headline "95%" target |

**Abstain rule (proposed; T-V3-1 calibrates the numbers from data):** the engine abstains when
either no candidate clears a minimum score *floor*, or the top-1 and top-2 scores are within a
*margin* (a tie it cannot honestly break). An abstain is **not** scored as a wrong answer; it is
counted against `coverage`. This is what keeps the number honest where the audit proved the data
is ambiguous.

**Acceptance:** `top3_on_covered >= 95%` with `coverage` reported and not allowed to collapse
(a coverage floor is set once T-V3-0 shows the real distribution — likely >= 80%).

---

## 4. Phased build (keyed to the failure map)

Each phase targets a specific bucket from section 1. Phases 0-3 need **no new signal data** and
should land ~85%. Phase 4 is the discrimination work that closes to 95% and depends on
owner-supplied real-vehicle data.

```
 P0 measure -> P1 score top-3 -> P2 re-pin answer key -> P3 engine surfaces -> P4 new signals
 (no code)     (scorer)           (oracle, no engine)     differential+abstain  (GASLab/OBDLab)
   |             |                   |                       |                    |
 sets target   makes top-3        recovers 133 SURFACE     recovers the 107      cracks the 44
 + abstain     measurable         (zero engine risk)       OUTRANKED honestly    PRODUCER/DATA_GAP
 thresholds                                                                      (needs owner data)
   +------------- lands ~85% on the frozen corpus ----------+   +--- closes to 95% ---+
```

### Phase 0 — Measure the real top-3 ceiling (T-V3-0) · no engine change
Re-score the **existing frozen traced run** (`apps/wired/v7/runs/20260630_190651/` +
`...163900/results.json`, both already on disk) to compute, per case and per family:
*is the expected family in the engine's top-3 scored rules?* Output the realistic v3 target and
the exact list of OUTRANKED cases that fall **outside** top-3 (those, and only those, need Phase
rank work). **This is the no-regret first task** — it commits us to nothing and replaces the
~85% estimate with a measured number.

### Phase 1 — Top-3 + abstain scorer (T-V3-1) · scorer only
Extend the scoring harness (`apps/wired/fl_tasks/score_v3_yardstick.py` /
`apps/wired/v7/run_suite.py::score_case`) with the section-3 metrics: `top3_family`, `coverage`,
`top3_on_covered`, plus the fault_id->family map for siblings and the abstain floor/margin
(calibrated from T-V3-0). Mints **`V3_YARDSTICK`** (new oracle hash) while keeping
`FL_YARDSTICK_2026-06-30` as the immutable BEFORE.

### Phase 2 — Re-pin the answer key (T-V3-2) · oracle only, zero engine change
Apply the already-investigated **Option B** dispositions (memos `V7_CODE_NS_DECISION` and
`V7_CONF_DECISION`, both owner-pending sign-off):
- `expected_fault_code` -> short form (`MF-001`) for **named-fault rows only**; keep
  `ERR-ABORT-*` and `OPTIMAL_HEALTH`.
- `expected_confidence_*` -> the live scorer's **per-family** bands; keep abort / no_fault bands.
This converts the **133 SURFACE_DEFECT** cases from FAIL to PASS with no engine change and no
routing risk.

### Phase 3 — Engine surfaces a reliable ranked differential + abstain (T-V3-3) · engine
Ensure the v2 output path reliably populates `differential_siblings` with the runner-up
families, **add `fault_family` to `DifferentialSiblingOut`** (consumer: the top-3 scorer + the
UI runner-up panel, PRD section 5.3), and implement the section-3 abstain rule on the verdict. No
re-tuning of scores — this only *exposes* what the ranker already computed.

### Phase 4 — New discriminating signals (deferred; owner data-gated) · GASLab/OBDLab
The only lever for the 44 PRODUCER_GAP/DATA_GAP cases. Per the audit, add discriminating
**measurements**, not code heuristics:
- **snap-throttle / transient gas** — worn valve seals show a transient HC plume vs steady
  misfire (the engine's own `MW-004` note); separates `mechanical_wear`, parts of `rich_mixture`.
- **real STFT/LTFT fuel trims, dual-RPM deltas, Mode 06** — separate `ecu_fault`,
  `exhaust_leak`, `non_starter`, `sensor_fault` under-detection.
Each new signal follows the project's **signal/noise rule**: it ships only with a named producer
(GASLab/OBDLab state) *and* a named consumer (the rule that gates on it). Authored as its own
task pack once the owner supplies the real-vehicle or standards data; **do not synthesize sensor
values.** Families that remain unseparable after this honestly **abstain** rather than guess.

---

## 5. The hard rules v3 inherits (do not break)

- **`mechanical_wear -> misfire` (10 rows, `ORACLE_SUSPECT`/`FL-V3-ORACLE-MW-MISFIRE`)** — do
  **not** score these as engine routing errors. Re-pin to misfire for a single-snapshot
  yardstick, or require a mechanical discriminator (Phase 4) before scoring as mechanical_wear.
- **"Tuning ties regresses neighbours" (audit FT-8)** — any rank-weight change (Phase 4 / the
  residual OUTRANKED work) must run the full corpus and show **no regressed family** before it
  lands. The top-3 reframe is preferred precisely because it avoids this.
- **Frozen yardstick is immutable.** Any oracle/corpus edit mints a *new* yardstick file; the
  frozen `FL_YARDSTICK_2026-06-30` stays the historical BEFORE. The scoreboard refuses on hash
  mismatch by design.
- **Project canon:** never edit `Vault/` (edit live `labs/<lab>/`); never re-run `graphify` /
  rebuild a frozen graph; no secrets in files; the only git action is the **owner's** final
  commit by explicit path.

---

## 6. Acceptance (how we know v3 is done)

One command, bound to the v3 yardstick:

```bash
/agent_workspace/.venv-wired/bin/python apps/wired/fl_tasks/score_v3_yardstick.py score
```

v3 is accepted when that command reports, against the v3 yardstick:

1. `single_verdict` family+state — reported, **no family regressed** vs the frozen 45.24%.
2. **`top3_on_covered >= 95%`** with `coverage` >= the floor set in T-V3-0.
3. The per-mode buckets show SURFACE_DEFECT and OUTRANKED drained to ~0 remaining-miss; the
   residual misses are only PRODUCER_GAP/DATA_GAP that Phase 4 has not yet (or cannot) close,
   and those are **abstained**, not mis-answered.

---

## 7. Risks & owner dependencies

- **Phase 0 may show fewer than 107 OUTRANKED inside top-3.** Then the gap to 85% is real and a
  bounded rank-recovery task (with the FT-8 neighbour gate) is added before Phase 4. T-V3-0 tells
  us this up front — cheaply.
- **Phase 4 is data-gated.** 95% across *all* families is impossible without the new
  measurements; the owner must supply real-vehicle/standards data for snap-throttle gas and real
  trims. Until then v3 ships ~85% top-3 with honest abstention on the rest — already a large,
  defensible jump from 45% single-verdict.
- **Coverage vs accuracy trade.** Aggressive abstain raises `top3_on_covered` but lowers
  `coverage`. The floor in section 3 prevents gaming the headline.

---

## 8. First task pack (authored now)

| Task | Does | Runnable | Blocked by |
|---|---|---|---|
| **T-V3-0** | measure real correct-in-top-3 rate from the frozen trace; set target + abstain thresholds | **now** | — |
| **T-V3-1** | top-3 + abstain scorer; mint V3_YARDSTICK; keep frozen BEFORE | after T-V3-0 | T-V3-0 |
| **T-V3-2** | re-pin oracle (Option B) — recovers 133 SURFACE_DEFECT, zero engine change | **now** (parallel) | — |
| T-V3-3 | engine surfaces reliable ranked differential + `fault_family` on siblings + abstain | after T-V3-1 | T-V3-1 |
| T-V3-4+ | Phase 4 new-signal GASLab/OBDLab packs | deferred | owner signal data |

Build order, hard rule, and acceptance command live in `V3_START_HERE.md`. The ledger is
`V3_PROGRESS.md`. Coders never read this plan whole — the task files pin the exact targets.
