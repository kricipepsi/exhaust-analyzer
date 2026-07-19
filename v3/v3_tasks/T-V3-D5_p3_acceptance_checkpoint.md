### Goal ###
Turn the T-V3-3 result into the pack's **disclosure keystone**: a tiered report that (a) proves
surfacing regressed nothing and banked the FREE set, and (b) lays out the **next-decision map** so
the owner picks the next pack from evidence. Measurement-only — no engine/oracle/CSV/schema edits.
Uses the instruments already built (T-V3-1 scorer + T-V3-D4 per-case `diff` = a text listing of
which case_ids changed pass/fail between two runs); does not extend them.

> **Bound to the T-V3-3 disclosure (2026-07-01).** The numbers below are the *measured* post-task
> result, not the pre-run estimate. Re-run `score`/`diff` to reproduce them, but the headline is
> already known and the surprises are already flagged — this task **writes them up in tiers and
> lays out the menu**, it does not re-discover them. Source: `progress_notes/T-V3-3.md` §Disclosure.

### Progressive-disclosure role — the keystone ###
This is where the pack "reveals, then lets the owner request the next layer." The report is written
in **three tiers**, essential-first, so the owner reads one line to know where v3 stands and drills
down only if a number surprises them.

- **Tier 1 — headline (<=3 lines).** State exactly:
  `top3_family 141/294 (47.96%) -> 176/294 (59.86%), +35`. Then the two reference ceilings:
  **trace ceiling 175/294 (59.52%) — EXCEEDED by +1**, and **reframing ceiling 181/294 (61.56%)
  — residual gap 5 cases**. One-word verdict: **on-track** (no regression, above trace ceiling).
- **Tier 2 — per-bucket residual table.** One row per open bucket with its count, what unlocks it,
  and its gate — the menu of next moves:

  | Bucket | Cases | Next move | Gate |
  |---|---|---|---|
  | SCORER_WINDOW (FREE, present but uncounted) | 2 | widen scorer sibling window top-2 -> top-3 | **owner decision** — changes the acceptance *definition* (what "top3 pass" counts); cheap + research-independent, but FT-8-adjacent honesty call |
  | TUNABLE | 20 | T-V3-4 bounded reweight | research-gated (cluster answers) + FT-8 risk |
  | ORACLE_SUSPECT | 10 | FL-V3-ORACLE-MW-MISFIRE re-pin | Cluster-1 disposition + owner sign-off |
  | abstain (honesty dial) | — | T-V3-3B emit abstain | this report's coverage numbers |
  | HARD | 49 | signal pack | research-dependent |
  | PRODUCER_GAP (signal) | 23 | signal pack | research-dependent |
  | DATA_GAP | 19 | acquisition | owner data |

- **Tier 3 — per-case detail (JSON only).** The full `diff` movement table + the per-FREE-case
  banked/not flag, deferred to the `.json` so Tier 1/2 stay scannable.

### The disclosed movement (bind these exactly — do not round or summarize past them) ###
`top3_family` rose `141 -> 176` (`+35`). The `+35` is **not** the clean "38 FREE flip" the plan
assumed. It decomposes as:
- **FREE (38 total):** 28 newly banked, 8 already family-pass before this task, **2 not banked**.
- **Non-FREE banked incidentally (7):** `era2_008`, `era2_015`, `CASE-023`, `CSV-120`, `EXP-N017`,
  `EXT-207`, `EXT-217` — surfaced siblings the frozen trace's rank snapshot did not count, which is
  **why 176 lands above the 175 trace ceiling**.
- **The 2 FREE not banked — the surprise:** `EXP-N010` (expected `rich_mixture` emitted as the 3rd
  sibling, after `lean_condition` and `misfire`) and `era3_008` (expected `lean_condition` emitted
  as the 3rd sibling, after duplicate `misfire` entries). Both families **are present** in the
  emitted differential; they fall outside the scorer's `{winner + top-2 siblings}` counting window.
  This is a scorer-window/dedupe artifact, not an engine miss — hence the SCORER_WINDOW row above.

### Success criteria ###
- Score the post-T-V3-3 run against the rebound `V3_YARDSTICK_2026-06-30` guard (no
  `--allow-new-yardstick`; `Hash lock: ok`).
- **No regression:** single-verdict family+state stays **133/294 (45.24%)**; no per-family primary
  count drops; `diff` `REGRESSIONS:` line is **empty**.
- **FREE reconciled (not "all 38 flip"):** `newly_pass` contains the **28** newly-banked FREE
  case_ids; the **8** already-passing and the **2** not-banked FREE cases are each accounted for.
  The 2 not-banked (`EXP-N010`, `era3_008`) are listed in Tier 2/3 with the one-line scorer-window
  reason above — a FREE case that did not move is a finding, reported, not hidden.
- **Ceiling framing correct:** Tier 1 shows 176 sits **above** the 175 trace ceiling and **5 short**
  of the 181 reframing ceiling. Do not present +35 as "the FREE set banked" — 2 FREE are still
  outside the counted window and 7 of the 35 are non-FREE.
- The report `v3/reports/V3_ACCEPTANCE_P3_2026-07-01.md` is written in the three tiers above; the
  companion `.json` carries Tier 3. `coverage` = 1.00 / `top3_on_covered` = 176/294 (59.86%) /
  `total_abstained` = 0 are recorded — state explicitly that coverage reads 1.00 **because abstain
  has not shipped yet (T-V3-3B)**, so the number isn't misread as calibrated honesty.
- Inner loop clean on any helper touched (`py_compile` = compiles; `ruff` = style check; `pyright`
  = type check); no new test required if no code changes (run+report task).

### Disclosure (what this task must surface, not hide) ###
The whole task is disclosure. Three specific guards:
1. Report the true decomposition of the +35 (28 FREE + 8 already + 7 non-FREE; 2 FREE missed). A
   reader must not come away thinking all 38 FREE banked.
2. 176 exceeding the 175 trace ceiling is real but small (+1) and is driven by incidental non-FREE
   banks — say so; do not frame it as beating the achievable ceiling (181 is still 5 away).
3. The Tier 2 gate column must name each next move's blocker honestly (research entanglement, FT-8
   risk, owner sign-off, or — for SCORER_WINDOW — that it moves the goalposts). No downstream task
   should look cheaper than it is.

### Context ###
Phase verification for `v3/V3_PLAN.md` §5-6, applied to the T-V3-3 landing. `diff` (T-V3-D4) already
emits per-case `newly_pass`/`newly_fail`/`unchanged` + REGRESSIONS on the v3 pass surface
(`single_verdict OR top3_family`); this task *uses* it. Baseline BEFORE = frozen run
`apps/wired/v7/runs/20260630_163900/results.json` (pre-T-V3-3, siblings `[]`); AFTER =
`apps/wired/v7/runs/POST_T_V3_3/results.json` (written by T-V3-3, verified present). FREE set +
buckets: `v3/reports/V3_OUTRANKED_MAP_2026-06-30.md` (FREE=38, TUNABLE=20, HARD=49). Ceilings:
`v3/reports/V3_TOPK_CEILING_2026-06-30.md` (trace top-3 = 175/294; measurable achievable = 181/294 =
61.56%).

### Consumer (signal/noise) ###
- **Consumer:** the owner's next-pack decision and the v3 acceptance gate. The SCORER_WINDOW row is
  a new consumer input the disclosure created — it puts a cheap, definition-changing option on the
  menu that did not exist before the run.
- **Code path:** `score_v3_yardstick.py score` and `... diff` only.

### Deliverables ###
1. `apps/wired/v7/runs/POST_T_V3_3/results.json` — the AFTER run (reuse the one T-V3-3 wrote).
2. `v3/reports/V3_ACCEPTANCE_P3_2026-07-01.{md,json}` — CREATE. Tiered report (md) + per-case (json).

### Files to touch ###
- `v3/reports/V3_ACCEPTANCE_P3_2026-07-01.md` (CREATE)
- `v3/reports/V3_ACCEPTANCE_P3_2026-07-01.json` (CREATE)

### Out of scope ###
No engine/oracle/CSV/scorer edits — **including the SCORER_WINDOW widen**: this task *lists* it as
an option, it does **not** implement it (that is the owner's call, forward-registered as
`T-V3-D6-SCORERWIN`). No new scoreboard subcommands (use `score` + `diff`). No re-hash or mutation
of any yardstick. No `Vault/` edits. GRAPH GUARDRAIL: no `graphify`/graph rebuild.

### Verification ###
```bash
cd /agent_workspace
/agent_workspace/.venv-wired/bin/python apps/wired/fl_tasks/score_v3_yardstick.py score \
  --results apps/wired/v7/runs/POST_T_V3_3/results.json | sed -n '1,16p'
/agent_workspace/.venv-wired/bin/python apps/wired/fl_tasks/score_v3_yardstick.py diff \
  --before apps/wired/v7/runs/20260630_163900/results.json \
  --after  apps/wired/v7/runs/POST_T_V3_3/results.json \
  --write-md v3/reports/V3_ACCEPTANCE_P3_2026-07-01.md \
  --write-json v3/reports/V3_ACCEPTANCE_P3_2026-07-01.json | grep -iE 'REGRESSIONS|newly_pass|unchanged'
```
Gate: `Hash lock: ok`; single_verdict 133/294 unchanged; top3_family 176/294; `REGRESSIONS: (empty)`;
`newly_pass` covers the 28 newly-banked FREE case_ids; `EXP-N010` and `era3_008` confirmed NOT in
`newly_pass` (they are the 2 documented scorer-window misses). (The `--write-md` output is the raw
movement table; hand-author the Tier 1/2 headline above it in the same file.)

### Progress hook ###
PROGRESS.md `T-V3-D5`: Status=done, Files changed=2, Verification="tiered disclosure: top3_family
141->176 (+35 = 28 FREE + 7 non-FREE; 8 already; 2 FREE missed=EXP-N010,era3_008), REGRESSIONS
empty, single_verdict 133/294; above 175 trace ceiling, 5 short of 181 reframing ceiling; Tier-2
menu = SCORER_WINDOW(2) + 20 TUNABLE + 10 ORACLE_SUSPECT + abstain(T-V3-3B) + signal packs".

### Depends on ###
T-V3-3 (surfacing) done — AFTER run `apps/wired/v7/runs/POST_T_V3_3/results.json` present (verified).
