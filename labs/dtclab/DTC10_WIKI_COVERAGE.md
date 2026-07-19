# DTC10 vs new DTCLab wiki — coverage check

**Date:** 2026-06-11
**Wiki checked:** `labs/dtclab/wiki/` (v2.0, chunks `00`–`12`)
**Questions:** `labs/dtclab/DTC10.md`

## Bottom line

**All 10 questions are now covered (updated 2026-06-11).** The original check
found 4 answered / 4 partial / 2 not — the gaps were the *empirical* questions
(corpus prevalence and code→family fan-out) that a reasoning-grammar wiki can't
answer by itself. Those were closed by a web-research synthesis
(`DTCanswers.md` / `DTCansw2.md`) integrated as new chunk `12` (prevalence Q1,
fan-out Q2, P1xxx Q3, priority Q10) and `01 §1.4` (maturation skew Q9); Q7 was
closed earlier by the 1990–2010 scope decision.

Score: **10 answered.** (originally 4 answered, 4 partial, 2 not answered.)

## Per-question verdict

| # | Question (short) | Verdict | Where / why |
|---|---|---|---|
| 1 | Fraction of 1990–2010 cases with a stored DTC at diagnosis *(core)* | **Answered (2026-06-11)** | New chunk `12.1`: industry ~60–65% confirmed; corpus n=90 → 21 confirmed (23.3%), 5 pending (5.6%), **64 no-DTC (71.1%)** — matches DTC10's 64/90. Plus downstream-artifact table (`12.2`). Consumer: rank step treats a DTC as a bonus, not a precondition. |
| 2 | Empirical P-code→family mapping strength (does P0171 mean lean, or fire across many causes?) *(OUTRANKED)* | **Answered (2026-06-11)** | New chunk `12.3` fan-out matrix with real distributions: P0171 = 45/30/15/10 (vacuum/MAF/fuel/exhaust) — weak; P0420 = 65/25/8/2 — outcome code; P0401 = 60/25/15 — discriminating ~1:1; P0300, P0101 included. Corpus shares alongside. |
| 3 | Which P1xxx codes add discriminating power; usable without per-OEM DBs? *(coverage)* | **Answered (2026-06-11)** | New chunk `12.4`: stable cross-OEM cohort = **P1000** (readiness), **P1260** (PATS theft), **P1101** (MAF self-test); all else unstable (e.g. P1404 differs by make). Verdict: generic use unfeasible **except** the Ford-Mazda-Jaguar PATS/readiness + P1101 subset. |
| 4 | Which freeze-frame params most improve discrimination; OEM-consistent? *(OUTRANKED)* | **Answered** | Strong: chunk `02` (SAE-mandated FF set, CLV bands, ECT gate), `03` (trim grammar), `10.4` (curb vs stress idle). Load+RPM+ECT+trim-at-freeze each given a discriminator role; mandated set is SAE-standard, so OEM-consistent. |
| 5 | How should `$07`/`$03`/`$0A` state weight the family prior? *(ranking)* | **Answered** | Chunk `01`: full lifecycle, pinned cycle counts (3 confirm / 3 heal / ≥40 warm-up erase), `PERMANENT` > stale `CONFIRMED`, age-in-warm-up-cycles as a down-weight. Consumer = `DTC_VOCABULARY.md §16` confidence weights. |
| 6 | Multi-DTC patterns as a combined signature (P0300+P030x, P0171+P0174) *(OUTRANKED)* | **Answered** | Covered: `02.4.2` (P030x + lean ⇒ misfire-masked), `05.1` (P0171+P0174 bank pattern), `09` (P0171+P0300 routing), `08.3` (P0172+P0087 pair). The two named pairs are both handled. |
| 7 | Are GPF / Euro-6d hex-tailed codes (P244A) in scope for 1990–2010, or dead weight? Ties to T-FX-13 regex gap *(scope)* | **Resolved (2026-06-11)** | Scope fixed to **1990–2010 (Euro 1–5)**. Post-2010 / Euro 6+ tech (GPF P2452, LSPI P0324, hex-tailed P244A) removed from chunk `08` and recorded out-of-scope in `11.4`: they are dead weight from a wider-scope era, so the `T-FX-13` regex need not match them. GDI + turbo kept (both predate 2010). SAI/P0411 also dropped. |
| 8 | Can P0301–P0308 + pattern/count discriminate mechanical/ignition/lean/fuel misfire from the DTC set alone? *(OUTRANKED)* | **Answered (with caveat)** | Discrimination logic is covered: `06.1` (single-cyl coil arcing), `02.4.4` (neutral-trim ⇒ ignition/mechanical), `06.3` (ghost misfire = ripple/crank-jitter), `05.2` (random distribution ⇒ global lean), `06.4` Type A/B. **Caveat:** the wiki shows it is *not* doable from codes alone — it needs Mode `$06` per-cyl counts + freeze-frame trims (and ripple from OBDLab). So the honest answer to "from the DTC set alone" is *no — but yes with FF + `$06`*. |
| 9 | One-trip vs two-trip maturation & clearing bias on which codes are present; corpus skew? *(corpus realism)* | **Answered (2026-06-11)** | New chunk `01 §1.4`: one-trip (Type A) vs two-trip (Type B) monitor table + enable criteria, and the skew finding — continuous one-trip families (misfire/fuel/circuit) over-represented; non-continuous two-trip (catalyst/EVAP/EGR) under-represented **~1.5–2.0×**. Consumer: family prior corrects for the under-count. |
| 10 | Domain heuristic techs use to pick the "primary" code among several; standard severity ordering? *(ranking)* | **Answered (2026-06-11)** | New chunk `12.5`: ECM freeze-frame priority (Priority 1 fuel+misfire > Priority 2 others) **plus** a five-tier professional hierarchy (safety/catalyst-damage → power/comms → circuit hard faults → air/fuel rationality → downstream outcomes) and three tie-breaks (freeze-frame anchor; confirmed > pending; upstream sensor > downstream outcome), with the worked P0300→P0171→P0420 chain. |

## How the gaps were closed

The originally-answered questions (4, 5, 6, 8) were "what rule applies" — the
wiki's native job. The gaps (Q1, Q2, Q9 empirical; Q10 convention; Q3, Q7
contract/scope) all needed something a reasoning-grammar wiki can't generate by
itself. They are now closed:

- **Q1, Q2 (empirical):** web-research synthesis supplied the prevalence split
  (64/90 no-DTC) and the fan-out matrix → chunk `12.1–12.3`. The corpus figures
  match DTC10's own 64/90, so they cross-check.
- **Q9 (maturation skew):** one-trip/two-trip table + the ~1.5–2.0× over/under-
  representation correction → chunk `01 §1.4`.
- **Q10 (ordering convention):** ECM freeze-frame priority + five-tier hierarchy
  + three tie-breaks → chunk `12.5` (consumer = the rank step).
- **Q3 (P1xxx):** stable cohort (P1000/P1260/P1101) vs unstable; feasibility
  verdict → chunk `12.4`.
- **Q7 (scope):** closed by the 1990–2010 / Euro 1–5 decision; GPF/P244A out.

> Signal/noise: chunk `12` and `01 §1.4` are **reference material** (statistics
> and conventions, no new schema field), so they ship freely per `00_INDEX §2`.
> Each names the existing rank/route consumer it informs. The standing
> `[PROPOSAL]` tokens (`P-DTC-1/2/3` in chunk `11`) still carry their own named
> consumers.

## Remaining (verification, not coverage)

| Item | Note |
|---|---|
| ~~Scope line mismatch~~ | **Resolved** — scope set to 1990–2010 (Euro 1–5); Era C / Euro 6+ / GPF / LSPI / SAI removed. |
| ~~Corpus-statistics gap (Q1/Q2/Q9)~~ | **Closed** by chunk `12` + `01 §1.4` from the research synthesis. |
| ~~Primary-code ordering (Q10)~~ | **Closed** by chunk `12.5`. |
| Verify corpus counts | The 64/90, 21/5/64 split and per-code corpus shares come from the research doc; a direct count over `DTCLab/cases/` would confirm them before they're treated as canonical. |
