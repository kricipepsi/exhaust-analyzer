# v3 Phase-4 Handoff — signal packs (start here in the fresh session)
**Date:** 2026-07-01 · **Author:** architect (Cowork) · **Owner:** Mutolovsky
**Read order for a fresh session:** `v3/V3_START_HERE.md` → `v3/CLAUDE.md` → **this file** → the
cluster/report pointers below. Phases 0–3 + rank-recovery + oracle re-pin + abstain-cal are **done**;
Phase 4 is the remaining work and it is **owner-data-gated**.

---
## 1. Where v3 stands now (measured, post-everything)
Active yardstick: **`V3_YARDSTICK_2026-07-01`** (minted by the oracle re-pin).
Latest run: `apps/wired/v7/runs/POST_T_V3_3D/results.json`. Re-score command:
`/agent_workspace/.venv-wired/bin/python apps/wired/fl_tasks/score_v3_yardstick.py score`

| Metric | Value | Note |
|---|---|---|
| `top3_family` | **193/294 = 65.65%** | up from 141 at project start; past the 175 trace + 181 reframing ceilings |
| `coverage` | **0.73** (216/294) | abstain dial at MARGIN=0.02 |
| `top3_on_covered` | **155/216 = 71.76%** | acceptance target is ≥95% on covered |
| `total_abstained` | **78** | split 38 hidden wins / 40 correct silences (net-honest, narrowly) |
| single-verdict family+state (covered) | **85/294** | raw dims higher; abstain masks some |
| Hash lock | **ok** | on `V3_YARDSTICK_2026-07-01`; `run_suite.py` untouched/frozen |

**This is the research-independent ceiling (~193/294 ≈ 66%).** No further reweight, re-pin, or
abstain tuning moves it. The gap to 95% is the discrimination wall: families that a single warm-idle
5-gas snapshot physically cannot separate. Closing it needs **new measurements** = Phase 4.

---
## 2. What Phase 4 is (and the one rule that governs it)
Phase 4 adds **discriminating signals**, not code heuristics. **Signal/noise rule (canon):** a new
field/state ships **only** with a named **producer** (GASLab/OBDLab state that emits it) **and** a
named **consumer** (the rule that gates on it). **Provisional-synthetic policy (updated 2026-07-01,
owner):** until the app has real users, a pack **may seed** its columns with **research-grounded,
tolerance-wide synthetic values** derived from each case's oracle fault — flagged `synthetic=true`,
kept in a synthetic-vs-real scoreboard split, calibrated when real data lands. Values are grounded in
the research band **and web-corroborated against real-world reported values before commit (cite
sources)**, **never back-solved to force a pass**; cases the research cannot ground stay **abstained**.
Full policy: `4DLab_CLAUDE.md` §Provisional synthetic signals.

So each Phase-4 "signal pack" is: (seed the new corpus column with grounded, tolerance-wide synthetic values — or a real measurement once available) → (add a
producer that emits the state) → (add/adjust one consumer rule) → re-score, no regression, mint a new
yardstick if the corpus changes. **Until the owner supplies data, Phase-4 coding cannot begin** — the
first Phase-4 deliverable is the acquisition spec (section 4), not engine code.

---
## 3. The residual, by bucket → cluster (the Phase-4 target list)
Exact case lists live in the reports cited. Counts:

| Bucket | Count | Report (exact cases) | Nature |
|---|---|---|---|
| PRODUCER_GAP · SIGNAL_REQUIRED | 23 | `v3/reports/V3_PRODUCER_GAP_SPLIT_2026-06-30.md` | upstream lab never emitted the state the right rule needs |
| DATA_GAP · ACQUISITION_GAP | 19 | `v3/reports/V3_DATA_GAP_SPLIT_2026-06-30.md` | deciding input absent from the case entirely |
| HARD (OUTRANKED, rank>3) | 49 | `v3/reports/V3_OUTRANKED_MAP_2026-06-30.md` (bucket=HARD) | correct rule scored but far down; needs discrimination |
| TUNABLE held (not reweighted) | 12 | `v3/reports/V3_TUNABLE_REWEIGHT_MAP_2026-07-01.md` (S/K/H) | 1 signal-gated + 6 neighbour-risky + 5 ceiling |
| PRODUCER_GAP · CLASSIFIER_FIXABLE | 2 | same producer-gap report (`era2_008`, `CASE-039`) | **NOT data-gated** — possible cheap engine/classifier fix; check first |

**Signal demand by research cluster** (which measurement unlocks how many cases):

| Cluster | Discriminating measurement (from research) | Cases waiting |
|---|---|---|
| C2 rich vs catalyst | pre- vs post-cat 5-gas / upstream-downstream O2; STFT/LTFT; Mode $06 cat monitor | 11 (producer_gap) |
| C9 confirm no-fault | OBD no-fault evidence bundle (obd:hc, obd_lambda, readiness) | 10 (data_gap) |
| C5 lean root cause | STFT/LTFT across idle vs ~2500 rpm vs load | 5 (data_gap) |
| C8 non-starter | crank/compression + start-sequence evidence | 4 (producer) + 1 (data) |
| C1 mech vs misfire | snap-throttle transient HC; relative compression; per-cyl Mode $06 | 3 (producer) |
| C3 ECU/control fault | live PID plausibility; STFT/LTFT adaptation; module voltages | 3 (producer) |
| C6 sensor under-detection | O2 switch rate / forced rich-lean slew; MAF actual vs calc | 3 (data_gap) |
| C7 cam timing / VVT | cam-to-crank correlation / VVT angle; idle→2500 VE signature | 2 (producer) |
| C4 exhaust leak vs lean vs biased O2 | (already the T-V3-4 reweight zone) O2 vs load; up/down probe | (rank work done; residual needs signal) |

The **full, copy-pasteable data ask** is `v3/reports/RESEARCH_PROMPT_blocking_measurements.md` — it
already states, per cluster, why idle-5-gas fails and the candidate signals to acquire.

---
## 4. Recommended first Phase-4 task (author before any owner data lands)
**Author the acquisition spec** (a `V3_SIGNAL_ACQUISITION_SPEC`): turn each cluster's discriminating
measurement into a concrete corpus-column + producer-state contract the owner can fill — column name,
units, source (GASLab/OBDLab/shop test), the exact families it separates, and the case_ids it unlocks.
Order by yield: **C2 (11) → C9 (10) → C5 (5) → C8 (5) → C1/C3 (3 each) → C6 (3) → C7 (2)**.
This is research-independent (research has landed) and produces the precise data request; the owner
then supplies one cluster's data, and *that* unblocks the first real signal pack.

Also cheap and non-data-gated — **do first as a warm-up:** re-check the **2 CLASSIFIER_FIXABLE**
producer-gap cases (`era2_008`, `CASE-039`) — their required state is reachable from existing row
inputs, so they may be a small classifier fix, not a signal pack. (`era2_008` may already bank via
T-V3-3 surfacing; confirm against the current run.)

---
## 5. Open (non-Phase-4) items, decided/parked
- **Abstain dial** is at MARGIN=0.02 (owner-picked, net-honest). It still hides 38 top3-correct cases
  — accepted for now; revisit only if coverage matters more than honesty. Floor=0.80 is inert (0/297
  fire) and kept as a safety net. No further action unless owner asks.
- **12 held TUNABLE** are routed here (signal packs), not to more reweighting (would regress
  neighbours / need absent signals). See the reweight map.
- **T-V3-D6-SCORERWIN** (widen scorer sibling window top-2→top-3 to bank `EXP-N010`, `era3_008`)
  remains forward-registered — a cheap acceptance-*definition* change, owner's call, not Phase 4.

---
## 6. Guardrails the fresh session must not break (canon)
- **Hash lock:** the scorer refuses if corpus/oracle/`run_suite.py` hashes drift. `run_suite.py` is
  the hash-locked "scorer" — **never edit it.** Any oracle/corpus change **mints a new yardstick**
  (see `T-V3-2R` + the oracle re-pin for the mint+rebind pattern); never overwrite a frozen one.
  `score_v3_yardstick.py` is NOT hash-locked (safe to edit read-sites/constants).
- **Never edit `Vault/`** (archived mirror) — edit live `labs/comlab/`.
- **No `graphify` / frozen-graph rebuild.** (Weights load live from the registry, so reweights don't
  need it; querying/building a *new* index offline is fine.)
- **No secrets in files.** **Synthetic sensor values are allowed provisionally** — grounded in the case's oracle fault + research band, tolerance-wide, `synthetic=true`-flagged, calibrated on real data (`4DLab_CLAUDE.md` §Provisional synthetic signals). Signal/noise structural rule (named producer + consumer) still holds.
- **Git:** the only git action is the **owner's** final commit, by explicit path. Never branch/stash.
- Progressive disclosure: split any task that both *discloses* a number and *commits* a policy; author
  only the next runnable task in full, forward-register the rest in `V3_PROGRESS.md`.

---
## 7. Key pointers
- Ledger (task log + forward-registered): `v3/V3_PROGRESS.md`
- Plan / acceptance definition: `v3/V3_PLAN.md` (§4 phases, §5 FT-8, §6 acceptance)
- Per-task detail: `v3/v3_tasks/progress_notes/<id>.md`
- Scoreboard: `apps/wired/fl_tasks/score_v3_yardstick.py` (`score` / `diff`); denominator = 294
- Engine: `labs/comlab/comlab/core/fault_atlas_router.py`; rules: `labs/comlab/registry/rules/*.json`
- Research answers: `v3/research/research_answers/cluster{1-9}.md`
- The data ask: `v3/reports/RESEARCH_PROMPT_blocking_measurements.md`

**Bottom line for Phase 4:** v3 is at 193/294 (66%) honestly. Everything left needs a real
measurement the idle snapshot lacks. Start by authoring the acquisition spec (§4) so the owner knows
exactly what data to bring; the first signal pack begins the moment one cluster's data lands.
