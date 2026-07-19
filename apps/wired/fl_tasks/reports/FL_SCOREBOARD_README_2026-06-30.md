# FL_SCOREBOARD_README_2026-06-30 — v3 before/after scoreboard

**Task:** [[T-FL-4_v3_scoreboard]]  
**Harness:** `apps/wired/fl_tasks/score_v3_yardstick.py`  
**Bound yardstick:** [[FL_YARDSTICK_2026-06-30]]  
**Failure-mode source:** [[FL_LOCALIZATION_2026-06-30]]  
**Mode:** measurement only; no engine/oracle/lab/wiki/CSV edits.

## What this command answers

The scoreboard scores an installed `wired` engine, or an existing result JSON, against the frozen T-FL-1 yardstick. It reports:

- overall primary family+state routing (`fault_family=PASS` and `state=PASS`),
- per-family primary routing,
- per-mode movement using the frozen T-FL-3 mode buckets,
- surface dimensions separately (`fault_code`, `confidence`, `perception_gap`, `demotion_note_contains`), and
- build identity (`git_sha` plus `USE_V2_REGISTRY` / `WIRED_OTEL`).

Primary routing deliberately excludes the two known surface defects from [[V7_ACCURACY_2026-06-30]]: `fault_code` namespace and confidence saturation. It is the yardstick T-FL-1 froze for judging whether v3 changed the real diagnostic routing signal.

## Score the current installed engine

Run from `/agent_workspace`:

```bash
/agent_workspace/.venv-wired/bin/python apps/wired/fl_tasks/score_v3_yardstick.py score
```

Expected baseline reproduction on the current v2-default build:

```text
OVERALL PRIMARY ROUTING
  family+state: 133/294 = 45.24 %
  family only : 141/294 = 47.96 %
  state only  : 275/294 = 93.54 %
  adjudicated : 143/294 = 48.64 % (ORACLE_SUSPECT +10)
```

Per-mode baseline buckets should read:

```text
SURFACE_DEFECT  bucket=133 primary_pass=133 remaining_miss=0
ORACLE_SUSPECT  bucket=10  primary_pass=0   remaining_miss=10
PRODUCER_GAP    bucket=25  primary_pass=0   remaining_miss=25
PRUNED_OTHER    bucket=0   primary_pass=0   remaining_miss=0
OUTRANKED       bucket=107 primary_pass=0   remaining_miss=107
DATA_GAP        bucket=19  primary_pass=0   remaining_miss=19
```

By default the harness suppresses noisy engine stdout/stderr during live scoring so the scoreboard is legible. Add `--show-engine-log` only when diagnosing engine logging.

## Score an existing run result

Use this when v3 has already produced a `results.json` via `apps/wired/v7/run_suite.py` or this scoreboard harness:

```bash
/agent_workspace/.venv-wired/bin/python apps/wired/fl_tasks/score_v3_yardstick.py score \
  --results apps/wired/v7/runs/20260630_163900/results.json
```

The harness accepts both legacy v7 `run_suite.py` JSON and its own comparison-ready JSON.

## Write a comparison-ready v3 result set

Store generated JSON under an ignored run directory, not in tracked reports:

```bash
/agent_workspace/.venv-wired/bin/python apps/wired/fl_tasks/score_v3_yardstick.py score \
  --label v3-candidate \
  --write-results apps/wired/v7/runs/<timestamp>/scoreboard_results.json
```

`apps/wired/v7/runs/` is git-ignored by the repository root `.gitignore`; the raw JSON should stay untracked. The JSON embeds the same scored rows plus the yardstick hash lock and build identity.

## Compare before and after

Self-comparison sanity check:

```bash
/agent_workspace/.venv-wired/bin/python apps/wired/fl_tasks/score_v3_yardstick.py compare \
  --before apps/wired/v7/runs/20260630_163900/results.json \
  --after apps/wired/v7/runs/20260630_163900/results.json
```

Expected result: every per-family delta is `+0`, every per-mode remaining-miss delta is `0`, and overall primary routing is `133/294 -> 133/294` with `+0.00 pp`.

Future v3 acceptance comparison:

```bash
/agent_workspace/.venv-wired/bin/python apps/wired/fl_tasks/score_v3_yardstick.py compare \
  --before apps/wired/v7/runs/20260630_163900/results.json \
  --after apps/wired/v7/runs/<v3-run>/scoreboard_results.json
```

Read the per-mode table as **remaining primary misses in the frozen T-FL-3 buckets**. Lower is better. Example interpretation:

- `PRODUCER_GAP 25 -> 12` means v3 made 13 originally producer-gap rows primary-correct.
- `OUTRANKED 107 -> 107` means v3 did not move the rank/scoring-term failures.
- `SURFACE_DEFECT 0 -> 0` means primary routing stayed correct for cases that were already routing-correct and only failed non-routing surfaces.

## Hash lock and override path

The historical `FL_YARDSTICK_2026-06-30` hashes below remain the immutable BEFORE record. Active
v3 scoring is pinned to `V3_YARDSTICK_2026-06-30`, after the T-V3-2 Option-B oracle re-pin:

| Active v3 artifact | Active V3 SHA-256 |
|---|---|
| `apps/wired/v7/data/cases_petrol_v7.csv` | `47182b3d9c4d4cb9e08645746a07fbae0d09b5db3d913fe00e1567965dd86dc9` |
| Oracle subset (`case_id`, `tag`, all `expected_*`, `accuracy_excluded`) | `192d7be1a339ce45afa7682d710ccfca7b1a0102bff447d037a63a64a73879f5` |
| `apps/wired/v7/run_suite.py` | `dc47eb4fc7701ae6e5b942c369411af51dca54c5aea4890f2bd401935cc75966` |

Historical FL BEFORE hashes:

| Artifact | Frozen FL SHA-256 |
|---|---|
| `apps/wired/v7/data/cases_petrol_v7.csv` | `a94a7731bcc55a1ab826bdc46d5c9658d47dd86984902e3c93d7bab3be02a2ae` |
| Oracle subset (`case_id`, `tag`, all `expected_*`, `accuracy_excluded`) | `a4de411098eb3c08d23d4881f4863fa1bd0a204cbb4041acb595474a1cecad7d` |
| `apps/wired/v7/run_suite.py` | `dc47eb4fc7701ae6e5b942c369411af51dca54c5aea4890f2bd401935cc75966` |

If the active V3 tuple differs, the command refuses to score. This prevents accidental moving-goalpost comparisons.

Override path: first create a new explicitly named yardstick report that freezes the changed corpus/oracle/scorer. Then rerun with the new yardstick name recorded:

```bash
/agent_workspace/.venv-wired/bin/python apps/wired/fl_tasks/score_v3_yardstick.py score \
  --allow-new-yardstick V3_YARDSTICK_<new-date-or-name>
```

That override is not a silent bypass: stdout prints `Hash lock: OVERRIDDEN`, and comparison-ready JSON records the override name. Do not use it to compare v2 and v3 against different corpora.

## How to read a null result honestly

A null v3 result is not just "same accuracy." The per-mode table tells which layer failed to move:

- `PRODUCER_GAP` unchanged: v3 did not add/produce the discriminating upstream states the expected rules need.
- `OUTRANKED` unchanged: v3 did not change the rank/scoring-term collisions where the expected family scored but lost.
- `DATA_GAP` unchanged: v3 still lacks the input channel or DTC evidence needed to distinguish those rows.
- `ORACLE_SUSPECT` unchanged: the known mechanical-wear/misfire product-definition issue remains unresolved; either repin those rows for a single-snapshot yardstick or add a mechanical discriminator before scoring them as mechanical wear.
- `SURFACE_DEFECT` unchanged at zero remaining misses: expected; those rows were already family+state-correct and only failed non-primary dimensions.

The scoreboard is therefore a layer-specific diff, not a headline-percent generator. v3 should be built against [[FL_LOCALIZATION_2026-06-30]] and accepted against [[V3_YARDSTICK_2026-06-30]] with this command.
