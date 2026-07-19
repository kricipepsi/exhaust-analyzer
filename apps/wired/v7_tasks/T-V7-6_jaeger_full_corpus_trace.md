# T-V7-6 — Run the full v7 corpus under Jaeger `--trace` (the pass that didn't run)
**Authored by:** architect (Cowork), 2026-06-30 · **Status:** `pending` (runnable now) · **Blocked by:** —
**Mode:** STRICT — runs the suite under trace + writes one report; **no engine/oracle edits**. · **Scope owner:** wired-v7.
**Load skills:** wired-python, wired-verification-loop, wired-code-review.

## Why this task exists
T-V7-5 reported the optional Jaeger `--trace` pass as **NOT run** (V7_ACCURACY §6) — it is
gated on a live Jaeger/OTLP collector at `localhost:4317`, which was not up in that session.
The owner has asked for the full corpus traced. This task brings the collector up and runs it.

## Signal/noise
Adds no domain field or fault. The **named consumer** is the routing-defect investigation
that comes next: F-V7-ECU-ROUTE, F-V7-DEAD-ROUTE, F-V7-SENSOR-MISS (V7_PROGRESS follow-ups).
The trace report localises *where* in the prune/rank pipeline each misroute diverges, so those
P1 fix tasks can be authored against a phase, not a symptom. No span field is added that this
report does not read.

## Pinned facts (verified at authoring, 2026-06-30)
- `apps/wired/v7/run_suite.py` already has `--trace` plumbing: OTLP gRPC exporter +
  `TracerProvider` wired (`run_suite.py:40-66`), `trace_enabled` param (`:201`).
- Trace tooling lives at `apps/wired/trace/`: `setup_env_wired.sh` (env profile),
  `run_traced_case.py`, `extract_traces.py`, `sanity_emit_span.py`, `README.md`. These
  reuse the **native-Linux Jaeger v2 binary** stood up by T-WTEST-3 (Jaeger v2.19.0,
  UI 200, OTLP gRPC 4317) — **not** docker, **not** the Windows `.ps1`.
- `apps/wired/trace/` and `apps/wired/_jaeger/` symlinks into `ARCHIVE/` are reference-only:
  **clone/read, never import** (AGENTS: no `ARCHIVE/` imports).
- Two tracing gates (carried-in known issue, TEST_PROGRESS): spans reach Jaeger only when a
  provider with the OTLP exporter is registered **and** `WIRED_OTEL=1`. Set both.
- Router phase spans observed in T-WTEST-5: `phase.prune` / `phase.rank` carry
  `router.candidates_in/out`, `router.winner_id`, `router.threshold_miss`.
- Corpus: `apps/wired/v7/data/cases_petrol_v7.csv` (314 rows). Last untraced run:
  `v7/runs/20260630_163900/` (0 crashes, 141/294 family routing).

## Success criteria (verify against these; loop until all hold)
1. Collector ONLINE: Jaeger UI returns 200 and OTLP gRPC 4317 is open **before** the run
   (re-verify the T-WTEST-3 profile; do not assume a prior session left it up).
2. All **314** cases execute under `--trace` with the same verdicts as the untraced
   `20260630_163900` run (tracing must not change outcomes) — **0 new crashes**.
3. Every case has a retrievable Jaeger trace id; spot-check ≥1 trace per fault family via the
   Jaeger REST API carries `phase.prune`/`phase.rank` with the four router fields above.
4. For the **§5 misroute clusters** and the three **dead-routing families** (`exhaust_leak`
   0/10, `mechanical_wear` 0/14, `non_starter` 0/5), the report records *where* routing
   diverged: `candidates_in/out`, `winner_id`, `threshold_miss` per cluster.

## Scope
**IN:**
- Bring up the collector via `apps/wired/trace/setup_env_wired.sh` + the T-WTEST-3 profile;
  verify criterion 1.
- Run `run_suite.py --trace` over the full 314-case corpus; capture trace id per case
  (extend `extract_traces.py` only if needed to map case_id → trace_id).
- Write `apps/wired/v7_tasks/reports/V7_TRACE_<date>.md`: collector proof; case→trace_id
  index; per-§5-cluster and per-dead-routing-family phase-of-divergence
  (`phase.prune`/`phase.rank` field values); a one-line "diverges at prune | rank | lab
  boundary" verdict per cluster.
- Update `F-V7-TRACE` → `done` in `V7_PROGRESS.md` and link the report from V7_ACCURACY §6.

**OUT:** any engine, router, oracle, wiki, or CSV edit (this is measure-only); fixing any
misroute; committing run/trace JSON or the Jaeger binary (keep raw JSON under
`apps/wired/trace/runs/` and `.gitignore` it, per T-WTEST-5); `graphify`; `Vault/`.

## Steps
1. Verify collector (criterion 1). If down, follow `apps/wired/trace/README.md` to start it.
2. `WIRED_OTEL=1` + provider registered; run `run_suite.py --trace` over the full corpus.
3. Diff verdicts vs `20260630_163900` (criterion 2); confirm 0 new crashes.
4. Pull spans per §5 cluster + dead-routing family; record phase-of-divergence.
5. Write `V7_TRACE_<date>.md`; flip `F-V7-TRACE` → done; cross-link V7_ACCURACY §6.

## Gate (STRICT dual-gate → `progress_notes/T-V7-6.md`)
- **VERIFICATION GATE:** paste the collector 200/4317 proof, the 314/314 run line, the
  verdict-diff result, and one REST span dump showing the four router fields.
- **CODE REVIEW:** confirm no engine/oracle edit; any `extract_traces.py` change is additive
  and ARCHIVE-import-free; raw JSON is git-excluded.
